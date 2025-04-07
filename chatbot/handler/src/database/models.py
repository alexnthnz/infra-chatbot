import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from .database import Base


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
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Account status and security
    is_verified = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
