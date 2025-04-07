from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None
