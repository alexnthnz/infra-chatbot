from typing import Optional, List
from uuid import UUID
from datetime import datetime
from schemas.bases.chat import ChatBase, MessageBase, FileBase, TagBase


class FileInDB(FileBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class MessageInDB(MessageBase):
    id: UUID
    chat_id: UUID
    file_id: Optional[UUID] = None
    message_metadata: Optional[dict] = None
    created_at: datetime
    file: Optional[FileInDB] = None

    class Config:
        from_attributes = True


class ChatInDB(ChatBase):
    id: UUID
    is_pinned: bool
    last_read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatDetailInDB(ChatInDB):
    messages: List[MessageInDB] = []


class TagInDB(TagBase):
    id: UUID

    class Config:
        from_attributes = True
