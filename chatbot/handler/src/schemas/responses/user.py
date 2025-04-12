from pydantic import BaseModel
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

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    refresh_token_expires_at: Optional[datetime] = None
