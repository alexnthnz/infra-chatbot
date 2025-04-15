import jwt
import uuid
from datetime import datetime, timedelta
from fastapi import status
from fastapi.responses import JSONResponse

from config.redis_client import redis_client
from config.config import config
from schemas.responses.common import CommonResponse


def create_access_token(user_id: str) -> str:
    """
    Create a JWT access token with standard claims (iss, iat, aud) and unique jti.

    Args:
        user_id (str): Unique user identifier (used as sub).

    Returns:
        str: Encoded JWT access token.
    """
    jti = str(uuid.uuid4())
    to_encode = {
        "sub": str(user_id),
        "type": "access",
        "jti": jti,
        "iss": config.JWT_ISSUER,
        "iat": int(datetime.utcnow().timestamp()),
        "aud": config.JWT_AUDIENCE,
    }
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, config.JWT_ACCESS_SECRET, algorithm=config.JWT_ALGORITHM)
    # Store jti in Redis
    redis_client.store_access_token_jti(user_id=user_id, jti=jti)
    return encoded_jwt


def create_refresh_token(user_id: str) -> tuple[str, datetime]:
    """
    Create a JWT refresh token with standard claims (iss, iat, aud) and unique jti.

    Args:
        user_id (str): Unique user identifier (used as sub).

    Returns:
        tuple[str, datetime]: Refresh token and its expiration datetime.
    """
    jti = str(uuid.uuid4())
    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": jti,
        "iss": config.JWT_ISSUER,
        "iat": int(datetime.utcnow().timestamp()),
        "aud": config.JWT_AUDIENCE,
    }
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, config.JWT_REFRESH_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt, expire


def create_tokens(user_id: str) -> tuple[str, str, datetime]:
    """
    Create both access and refresh tokens.

    Args:
        user_id (str): Unique user identifier.

    Returns:
        tuple[str, str, datetime]: Access token, refresh token, and refresh token expiration.
    """
    access_token = create_access_token(user_id)
    refresh_token, refresh_expires_at = create_refresh_token(user_id)
    return access_token, refresh_token, refresh_expires_at


def verify_access_token(token: str):
    """
    Verify an access token, checking jti against Redis, iss, and aud.

    Args:
        token (str): JWT access token to verify.

    Returns:
        dict or JSONResponse: Decoded payload if valid, error response if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            config.JWT_ACCESS_SECRET,
            algorithms=[config.JWT_ALGORITHM],
            audience=config.JWT_AUDIENCE,
            issuer=config.JWT_ISSUER,
        )
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
        user_id = payload.get("sub")
        jti = payload.get("jti")
        if not user_id or not jti:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="Invalid token",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="Token missing user_id or jti",
                ).dict(),
            )
        # Check jti in Redis
        stored_jti = redis_client.get_access_token_jti(user_id)
        if stored_jti is None or stored_jti != jti:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=CommonResponse(
                    message="Unauthorized",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    data=None,
                    error="Invalid or revoked token",
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
                error="Invalid access token format, signature, issuer, or audience",
            ).dict(),
        )


def verify_refresh_token(token: str):
    """
    Verify a refresh token, checking for blacklisting, iss, and aud.

    Args:
        token (str): JWT refresh token to verify.

    Returns:
        dict or JSONResponse: Decoded payload if valid, error response if invalid.
    """
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

        payload = jwt.decode(
            token,
            config.JWT_REFRESH_SECRET,
            algorithms=[config.JWT_ALGORITHM],
            audience=config.JWT_AUDIENCE,
            issuer=config.JWT_ISSUER,
        )
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
                error="Invalid refresh token format, signature, issuer, or audience",
            ).dict(),
        )
