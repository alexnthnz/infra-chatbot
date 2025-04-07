from fastapi import Depends, status, Header
from fastapi.responses import JSONResponse

from auth.jwt_handler import verify_access_token
from repository.user import UserRepository, get_user_repository
from schemas.responses.common import CommonResponse


def get_current_user(token: str = Header(..., alias="Authorization"),
                     user_repo: UserRepository = Depends(get_user_repository)):
    if not token.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid token format",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Token must start with 'Bearer '"
            ).dict()
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
                    error="Token missing required fields"
                ).dict()
            )
        user = user_repo.get_user_by_email(email)
        if user is None or str(user.id) != user_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="User not found or invalid ID",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="User does not exist or token ID mismatch"
                ).dict()
            )
        return user
    else:
        return payload
