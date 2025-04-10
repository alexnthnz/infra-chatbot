import uuid
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Message, Chat, SenderType


def get_message_repository(db: Session = Depends(get_db)):
    return MessageRepository(db)


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, chat: Chat, sender: SenderType, content: str = None,
                       file_id: uuid.UUID = None, metadata: dict = None) -> Message:
        """Create a new message in a chat."""
        message = Message(
            id=uuid.uuid4(),
            chat_id=chat.id,
            sender=sender,
            content=content,
            file_id=file_id,
            message_metadata=metadata
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_by_chat(self, chat: Chat) -> List[Message]:
        """Retrieve all messages for a chat."""
        return self.db.query(Message).filter(Message.chat_id == chat.id).order_by(Message.created_at.asc()).all()
