from fastapi import status, Header
from fastapi.responses import JSONResponse

from auth.jwt_handler import verify_access_token
from config.redis_client import redis_client
from schemas.responses.common import CommonResponse
from schemas.responses.user import UserInDB


def get_current_user(
    token: str = Header(..., alias="Authorization"),
):
    """
    Authenticate a user by validating the JWT token and checking user info in Redis.

    Args:
        token (str): Authorization header with Bearer token.

    Returns:
        UserInDB: Authenticated user data as a Pydantic model.
        JSONResponse: 401 error if token is invalid or user info not found in Redis.
    """
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
    if isinstance(payload, JSONResponse):
        return payload

    user_id = payload.get("sub")
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid token",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Token missing user_id",
            ).dict(),
        )

    # Check Redis for user info
    user_info = redis_client.get_user_info(user_id)
    if user_info is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Unauthorized",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="User info not found in Redis",
            ).dict(),
        )

        # Map user_info dict to UserInDB
    try:
        return UserInDB(**user_info)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CommonResponse(
                message="Failed to parse user data",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None,
                error=str(e),
            ).dict(),
        )
