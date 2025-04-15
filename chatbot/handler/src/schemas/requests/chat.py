from pydantic import Field, field_validator
from typing import Optional
from schemas.bases.chat import ChatBase, MessageBase, TagBase


class ChatCreate(ChatBase):
    title: str

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


class MessageCreate(MessageBase):
    # sender not included in request (set to "user" by Handler)
    content: Optional[str] = Field(None, max_length=1000)
    # File upload handled via FastAPI UploadFile, not in this model


class TagCreate(TagBase):
    pass  # Inherits name: str
