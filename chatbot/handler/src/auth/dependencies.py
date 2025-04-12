from fastapi import Depends, status, Header
from fastapi.responses import JSONResponse

from auth.jwt_handler import verify_access_token
from config.redis_client import redis_client
from database.models import User
from repository.user import UserRepository, get_user_repository
from schemas.responses.common import CommonResponse
from sqlalchemy.orm import Session
from database.database import get_db


def get_current_user(
    token: str = Header(..., alias="Authorization"),
    user_repo: UserRepository = Depends(get_user_repository),
    db: Session = Depends(get_db),
):
    if not token.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid token format",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Token must start with 'Bearer '",
            ).dict(),
        )
    token = token.split(" ")[1]
    payload = verify_access_token(token)
    if isinstance(payload, dict):  # Successful token verification
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None or user_id is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="Invalid token",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="Token missing required fields",
                ).dict(),
            )

        # First try to get user from Redis
        cached_user = redis_client.get_user_data(user_id)
        if cached_user:
            # Recreate the User object from cached data
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user and str(db_user.id) == user_id:
                return db_user

        # If not in Redis or not valid, fallback to database
        user = user_repo.get_user_by_email(email)
        if user is None or str(user.id) != user_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="User not found or invalid ID",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="User does not exist or token ID mismatch",
                ).dict(),
            )

        # Store in Redis for future requests
        from schemas.responses.user import UserInDB

        user_data = UserInDB.from_orm(user).dict()
        redis_client.store_user_data(user_id, user_data, ttl_seconds=3600)

        return user
    else:
        return payload
