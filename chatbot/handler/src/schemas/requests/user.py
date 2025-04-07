from pydantic import BaseModel, EmailStr

from schemas.bases.user import UserBase


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
