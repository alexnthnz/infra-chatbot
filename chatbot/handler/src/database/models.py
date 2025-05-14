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
    CORE = "core"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for social login users
    is_active = Column(Boolean, default=True)
    google_id = Column(String, unique=True, nullable=True)  # For Google login users

    # Profile information
    username = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)

    # Authentication metadata
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Account status and security
    is_verified = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    # Relationships
    chats = relationship("Chat", back_populates="user")


class Chat(Base):
    __tablename__ = "chats"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    title = Column(String, nullable=True)  # Optional title for the chat
    is_pinned = Column(Boolean, default=False)  # For pinning important chats
    last_read_at = Column(DateTime, nullable=True)  # For read/unread status
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="chats")
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
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    name = Column(String, nullable=False)  # Tag name (e.g., "work", "personal")

    # Relationships
    chats = relationship("Chat", secondary="chat_tags", back_populates="tags")
    user = relationship("User")


class ChatTag(Base):
    __tablename__ = "chat_tags"
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True)
