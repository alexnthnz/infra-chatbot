import jwt
from datetime import datetime, timedelta
from fastapi import status
from fastapi.responses import JSONResponse

from config.redis_client import redis_client
from config.config import config
from schemas.responses.common import CommonResponse


def create_access_token(user_id: str, email: str) -> str:
    to_encode = {"sub": email, "id": str(user_id), "type": "access"}
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_ACCESS_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: str, email: str) -> tuple[str, datetime]:
    to_encode = {"sub": email, "id": str(user_id), "type": "refresh"}
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_REFRESH_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt, expire


def create_tokens(user_id: str, email: str) -> tuple[str, str, datetime]:
    access_token = create_access_token(user_id, email)
    refresh_token, refresh_expires_at = create_refresh_token(user_id, email)
    return access_token, refresh_token, refresh_expires_at


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, config.JWT_ACCESS_SECRET, algorithms=[config.JWT_ALGORITHM])
        if payload.get("type") != "access":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="Invalid token type",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="Token is not an access token",
                ).dict(),
            )
        return payload
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Access token has expired",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Expired access token",
            ).dict(),
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid access token",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Invalid access token format or signature",
            ).dict(),
        )


def verify_refresh_token(token: str):
    try:
        if redis_client.is_token_blacklisted(token):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="Refresh token has been revoked",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="Revoked refresh token",
                ).dict(),
            )

        payload = jwt.decode(token, config.JWT_REFRESH_SECRET, algorithms=[config.JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="Invalid token type",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="Token is not a refresh token",
                ).dict(),
            )
        return payload
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Refresh token has expired",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Expired refresh token",
            ).dict(),
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid refresh token",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Invalid refresh token format or signature",
            ).dict(),
        )
