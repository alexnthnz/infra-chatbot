from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import field_serializer

from schemas.bases.chat import ChatBase, MessageBase, FileBase, TagBase


class FileInDB(FileBase):
    id: UUID
    created_at: datetime

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.timestamp()

    class Config:
        from_attributes = True


class MessageInDB(MessageBase):
    id: UUID
    chat_id: UUID
    file_id: Optional[UUID] = None
    message_metadata: Optional[dict] = None
    created_at: datetime
    file: Optional[FileInDB] = None

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("chat_id")
    def serialize_chat_id(self, chat_id: UUID, _info):
        return str(chat_id)

    @field_serializer("file_id")
    def serialize_file_id(self, file_id: Optional[UUID], _info):
        return str(file_id) if file_id else None

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.timestamp()

    class Config:
        from_attributes = True


class ChatInDB(ChatBase):
    id: UUID
    is_pinned: bool
    last_read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.timestamp()

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info):
        return updated_at.timestamp()

    @field_serializer("last_read_at")
    def serialize_last_read_at(self, last_read_at: Optional[datetime], _info):
        return last_read_at.timestamp() if last_read_at else None

    class Config:
        from_attributes = True


class ChatDetailInDB(ChatInDB):
    messages: List[MessageInDB] = []


class TagInDB(TagBase):
    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    class Config:
        from_attributes = True
