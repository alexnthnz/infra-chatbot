import uuid
from sqlalchemy.orm import Session
from .models import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_google_id(db: Session, google_id: str):
    return db.query(User).filter(User.google_id == google_id).first()


def create_user(db: Session, email: str, hashed_password: str = None, google_id: str = None):
    user = User(
        id=uuid.uuid4(),  # Explicitly generate UUID (optional, since default is set in the model)
        email=email,
        hashed_password=hashed_password,
        google_id=google_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
