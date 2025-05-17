import enum
import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Integer,
    ForeignKey,
    Enum,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


# Enum for message sender types
class SenderType(enum.Enum):
    USER = "user"
    AGENT = "agent"


class Chat(Base):
    __tablename__ = "chats"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=True)  # Optional title for the chat
    is_pinned = Column(Boolean, default=False)  # For pinning important chats
    last_read_at = Column(DateTime, nullable=True)  # For read/unread status
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    messages = relationship("Message", back_populates="chat")
    tags = relationship("Tag", secondary="chat_tags", back_populates="chats")


class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chat_id = Column(
        UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False, index=True
    )
    sender = Column(Enum(SenderType), nullable=False)  # Enum for user, agent, or core
    content = Column(String, nullable=True)  # Text content, nullable if only a file
    file_id = Column(
        UUID(as_uuid=True), ForeignKey("files.id"), nullable=True, index=True
    )
    message_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    chat = relationship("Chat", back_populates="messages")
    file = relationship("File", foreign_keys=[file_id])


class File(Base):
    __tablename__ = "files"  # Renamed from "attachments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_url = Column(String, nullable=False)  # URL to the file in external storage
    file_type = Column(String, nullable=True)  # e.g., "image/jpeg", "application/pdf"
    file_size = Column(Integer, nullable=True)  # Size in bytes
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Tag(Base):
    __tablename__ = "tags"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)  # Tag name (e.g., "work", "personal")

    # Relationships
    chats = relationship("Chat", secondary="chat_tags", back_populates="tags")


class ChatTag(Base):
    __tablename__ = "chat_tags"
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
