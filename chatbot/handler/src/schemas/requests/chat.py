from pydantic import Field
from typing import Optional
from schemas.bases.chat import ChatBase, MessageBase, TagBase


class ChatCreate(ChatBase):
    pass  # Inherits title: Optional[str]


class MessageCreate(MessageBase):
    # sender not included in request (set to "user" by Handler)
    content: Optional[str] = Field(None, max_length=1000)
    # File upload handled via FastAPI UploadFile, not in this model


class TagCreate(TagBase):
    pass  # Inherits name: str
