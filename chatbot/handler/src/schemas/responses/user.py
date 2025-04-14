from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime
from typing import Optional

from schemas.bases.user import UserBase


class UserInDB(UserBase):
    id: UUID
    google_id: Optional[str] = None
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    failed_login_attempts: int
    locked_until: Optional[datetime] = None

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer("created_at")
    def serialize_create_at(self, create_at: datetime, _info):
        return create_at.timestamp()

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info):
        return updated_at.timestamp()

    @field_serializer("last_login_at")
    def serialize_last_login_at(self, last_login_at: datetime, _info):
        return last_login_at.timestamp()

    @field_serializer("locked_until")
    def serialize_locked_until(self, locked_until: datetime, _info):
        if not locked_until:
            return None
        return locked_until.timestamp()

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    refresh_token_expires_at: Optional[datetime] = None
