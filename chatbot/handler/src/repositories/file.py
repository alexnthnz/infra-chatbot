import uuid
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import File, User


def get_file_repository(db: Session = Depends(get_db)):
    return FileRepository(db)


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_file(
        self, user: User, file_url: str, file_type: str = None, file_size: int = None
    ) -> File:
        """Store metadata for a file uploaded by the user."""
        file = File(
            id=uuid.uuid4(),
            file_url=file_url,
            file_type=file_type,
            file_size=file_size,
            user_id=user.id,
        )
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def get_file_by_id(self, file_id: uuid.UUID, user: User) -> File | None:
        """Retrieve a file by ID, ensuring it belongs to the user."""
        return (
            self.db.query(File)
            .filter(File.id == file_id, File.user_id == user.id)
            .first()
        )
