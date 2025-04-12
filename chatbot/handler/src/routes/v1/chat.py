from fastapi import Depends, status, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import uuid

from agent_service.client import enhance_prompt
from auth.dependencies import get_current_user
from config.config import config
from config.s3 import upload_to_s3, generate_presigned_url
from core_service.client import generate_response
from repository.chat import get_chat_repository, ChatRepository
from repository.message import get_message_repository, MessageRepository
from repository.file import get_file_repository, FileRepository
from repository.tag import get_tag_repository, TagRepository
from routes.v1 import api_v1
from schemas.requests.chat import ChatCreate, TagCreate
from schemas.responses.chat import ChatInDB, ChatDetailInDB, MessageInDB, TagInDB
from schemas.responses.common import CommonResponse
from database.models import SenderType


@api_v1.post("/chats", response_model=CommonResponse, status_code=status.HTTP_201_CREATED)
def create_chat(
    chat: ChatCreate,
    user=Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repository),
):
    db_chat = chat_repo.create_chat(user, title=chat.title)
    return CommonResponse(
        message="Chat created successfully",
        status_code=status.HTTP_201_CREATED,
        data=ChatInDB.from_orm(db_chat).dict(),
        error=None,
    )


@api_v1.get("/chats", response_model=CommonResponse)
def list_chats(
    user=Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repository),
    limit: int = 50,
    offset: int = 0,
):
    chats = chat_repo.get_chats_by_user(user)[offset : offset + limit]
    return CommonResponse(
        message="Chats retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=[ChatInDB.from_orm(chat).dict() for chat in chats],
        error=None,
    )


@api_v1.get("/chats/{chat_id}", response_model=CommonResponse)
def get_chat(
    chat_id: uuid.UUID,
    user=Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repository),
    message_repo: MessageRepository = Depends(get_message_repository),
    limit: int = 50,
    offset: int = 0,
):
    db_chat = chat_repo.get_chat_by_id(chat_id, user)
    if not db_chat:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CommonResponse(
                message="Chat not found",
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                error="Chat does not exist or belongs to another user",
            ).dict(),
        )

    messages = message_repo.get_messages_by_chat(db_chat)[offset : offset + limit]
    chat_response = ChatDetailInDB.from_orm(db_chat)
    chat_response.messages = []

    for msg in messages:
        message_response = MessageInDB.from_orm(msg)
        if msg.file_id:
            db_file = file_repo.get_file_by_id(msg.file_id, user)
            if db_file:
                # Regenerate presigned URL for the file
                file_key = db_file.file_url.split(
                    f"{config.S3_BUCKET}.s3.{config.AWS_REGION}.amazonaws.com/"
                )[-1]
                message_response.file.file_url = generate_presigned_url(file_key, expires_in=3600)
        chat_response.messages.append(message_response)

    return CommonResponse(
        message="Chat details retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=chat_response.dict(),
        error=None,
    )


@api_v1.post(
    "/chats/{chat_id}/messages", response_model=CommonResponse, status_code=status.HTTP_201_CREATED
)
async def send_message(
    chat_id: uuid.UUID,
    content: Optional[str] = Form(None, max_length=1000),
    file: Optional[UploadFile] = File(None),
    user=Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repository),
    message_repo: MessageRepository = Depends(get_message_repository),
    file_repo: FileRepository = Depends(get_file_repository),
):
    db_chat = chat_repo.get_chat_by_id(chat_id, user)
    if not db_chat:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CommonResponse(
                message="Chat not found",
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                error="Chat does not exist or belongs to another user",
            ).dict(),
        )

    # Handle file upload (simplified, replace with actual S3 logic)
    file_id = None
    file_url = None
    if file:
        try:
            file_url = upload_to_s3(file, folder=f"chat_{chat_id}", expires_in=3600)
            db_file = file_repo.create_file(
                user=user, file_url=file_url, file_type=file.content_type, file_size=file.size
            )
            file_id = db_file.id
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=CommonResponse(
                    message="File upload failed",
                    status_code=e.status_code,
                    data=None,
                    error=e.detail,
                ).dict(),
            )

    # Create user message
    db_message = message_repo.create_message(
        chat=db_chat, sender=SenderType.USER, content=content, file_id=file_id
    )

    # Call Agent and Core Services asynchronously
    if content or file_id:
        try:
            enhanced_prompt = await enhance_prompt(content, file_url if file_id else None)
            message_repo.create_message(
                chat=db_chat,
                sender=SenderType.AGENT,
                content=enhanced_prompt,
                metadata={"original_content": content},
            )
            core_response = await generate_response(enhanced_prompt)
            message_repo.create_message(chat=db_chat, sender=SenderType.CORE, content=core_response)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=CommonResponse(
                    message="Service call failed",
                    status_code=e.status_code,
                    data=None,
                    error=e.detail,
                ).dict(),
            )

    return CommonResponse(
        message="Message sent successfully",
        status_code=status.HTTP_201_CREATED,
        data=MessageInDB.from_orm(db_message).dict(),
        error=None,
    )


@api_v1.post(
    "/chats/{chat_id}/tags", response_model=CommonResponse, status_code=status.HTTP_201_CREATED
)
def add_tag(
    chat_id: uuid.UUID,
    tag: TagCreate,
    user=Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repository),
    tag_repo: TagRepository = Depends(get_tag_repository),
):
    db_chat = chat_repo.get_chat_by_id(chat_id, user)
    if not db_chat:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CommonResponse(
                message="Chat not found",
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                error="Chat does not exist or belongs to another user",
            ).dict(),
        )

    db_tag = tag_repo.create_tag(user, tag.name)
    tag_repo.add_tag_to_chat(chat_id, db_tag.id)
    return CommonResponse(
        message="Tag added to chat successfully",
        status_code=status.HTTP_201_CREATED,
        data=TagInDB.from_orm(db_tag).dict(),
        error=None,
    )


@api_v1.delete(
    "/chats/{chat_id}/tags/{tag_id}",
    response_model=CommonResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_tag(
    chat_id: uuid.UUID,
    tag_id: uuid.UUID,
    user=Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_chat_repository),
    tag_repo: TagRepository = Depends(get_tag_repository),
):
    db_chat = chat_repo.get_chat_by_id(chat_id, user)
    if not db_chat:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CommonResponse(
                message="Chat not found",
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                error="Chat does not exist or belongs to another user",
            ).dict(),
        )

    db_tag = tag_repo.get_tag_by_id(tag_id, user)
    if not db_tag:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CommonResponse(
                message="Tag not found",
                status_code=status.HTTP_404_NOT_FOUND,
                data=None,
                error="Tag does not exist or belongs to another user",
            ).dict(),
        )

    tag_repo.remove_tag_from_chat(chat_id, tag_id)
    return CommonResponse(
        message="Tag removed from chat successfully",
        status_code=status.HTTP_204_NO_CONTENT,
        data=None,
        error=None,
    )
