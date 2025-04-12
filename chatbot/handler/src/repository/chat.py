import uuid
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Chat, User


def get_chat_repository(db: Session = Depends(get_db)):
    return ChatRepository(db)


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, user: User, title: str = None) -> Chat:
        """Create a new chat for the user."""
        chat = Chat(id=uuid.uuid4(), user_id=user.id, title=title)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_chats_by_user(self, user: User) -> List[Chat]:
        """List all chats for a user."""
        return self.db.query(Chat).filter(Chat.user_id == user.id).all()

    def get_chat_by_id(self, chat_id: uuid.UUID, user: User) -> Chat | None:
        """Retrieve a specific chat by ID, ensuring it belongs to the user."""
        return self.db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
