from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SenderType(str, Enum):
    USER = "user"
    AGENT = "agent"


class ChatBase(BaseModel):
    title: Optional[str] = Field(None, max_length=100)


class MessageBase(BaseModel):
    content: Optional[str] = Field(None, max_length=1000)
    sender: SenderType


class FileBase(BaseModel):
    file_url: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class TagBase(BaseModel):
    name: str = Field(..., max_length=50)
