import uuid
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Tag, ChatTag, User


def get_tag_repository(db: Session = Depends(get_db)):
    return TagRepository(db)


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_tag(self, user: User, name: str) -> Tag:
        """Create a new tag for the user, or return existing one if it exists."""
        tag = (
            self.db.query(Tag).filter(Tag.user_id == user.id, Tag.name == name).first()
        )
        if not tag:
            tag = Tag(id=uuid.uuid4(), user_id=user.id, name=name)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def add_tag_to_chat(self, chat_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        """Associate a tag with a chat."""
        chat_tag = ChatTag(chat_id=chat_id, tag_id=tag_id)
        self.db.add(chat_tag)
        self.db.commit()

    def remove_tag_from_chat(self, chat_id: uuid.UUID, tag_id: uuid.UUID) -> None:
        """Remove a tag association from a chat."""
        chat_tag = (
            self.db.query(ChatTag)
            .filter(ChatTag.chat_id == chat_id, ChatTag.tag_id == tag_id)
            .first()
        )
        if chat_tag:
            self.db.delete(chat_tag)
            self.db.commit()

    def get_tag_by_id(self, tag_id: uuid.UUID, user: User) -> Tag | None:
        """Retrieve a tag by ID, ensuring it belongs to the user."""
        return (
            self.db.query(Tag).filter(Tag.id == tag_id, Tag.user_id == user.id).first()
        )
