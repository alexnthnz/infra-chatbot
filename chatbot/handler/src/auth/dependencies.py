from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from database.database import get_db
from database.crud import get_user_by_email

from .jwt_handler import verify_jwt_token


def get_current_user(token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)):
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    token = token.split(" ")[1]
    payload = verify_jwt_token(token)
    email = payload.get("sub")
    user_id = payload.get("id")

    if email is None or user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = get_user_by_email(db, email)
    
    if user is None or str(user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or invalid ID")
    
    return user
