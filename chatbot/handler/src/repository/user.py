import uuid

from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.database import get_db
from database.models import User


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_google_id(self, google_id: str) -> User | None:
        return self.db.query(User).filter(User.google_id == google_id).first()

    def create_user(
        self,
        email: str,
        username: str,
        hashed_password: str = None,
        google_id: str = None,
        phone_number: str = None,
        profile_picture_url: str = None,
    ) -> User:
        user = User(
            id=uuid.uuid4(),
            email=email,
            username=username,
            hashed_password=hashed_password,
            google_id=google_id,
            phone_number=phone_number,
            profile_picture_url=profile_picture_url,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_last_login(self, user: User) -> None:
        user.last_login_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)

    def increment_failed_login_attempts(
        self, user: User, max_attempts: int = 5, lockout_minutes: int = 15
    ) -> None:
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= max_attempts:
            user.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
            user.failed_login_attempts = 0  # Reset attempts after lockout
        self.db.commit()
        self.db.refresh(user)

    def reset_failed_login_attempts(self, user: User) -> None:
        user.failed_login_attempts = 0
        user.locked_until = None
        self.db.commit()
        self.db.refresh(user)
