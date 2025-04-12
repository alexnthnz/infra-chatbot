from fastapi import Depends, status, Header, FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import bcrypt

from auth import jwt_handler, social_login, dependencies
from config.redis_client import redis_client
from repository.user import get_user_repository, UserRepository
from routes.v1 import api_v1
from schemas.requests.user import UserCreate, UserLogin
from schemas.responses.common import CommonResponse
from schemas.responses.user import Token, UserInDB


@api_v1.post("/register", response_model=CommonResponse)
def register(user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    db_user = user_repo.get_user_by_email(user.email)
    if db_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CommonResponse(
                message="Email already registered",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=None,
                error="Email already exists"
            ).dict()
        )
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    db_user = user_repo.create_user(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        phone_number=user.phone_number,
        profile_picture_url=user.profile_picture_url
    )
    access_token, refresh_token, refresh_expires_at = jwt_handler.create_tokens(db_user.id, db_user.email)
    return CommonResponse(
        message="User registered successfully",
        status_code=status.HTTP_200_OK,
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            refresh_token_expires_at=refresh_expires_at
        ).dict(),
        error=None
    )


@api_v1.post("/login", response_model=CommonResponse)
def login(user: UserLogin, user_repo: UserRepository = Depends(get_user_repository)):
    db_user = user_repo.get_user_by_email(user.email)
    if not db_user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Invalid email or password"
            ).dict()
        )

    if db_user.locked_until and db_user.locked_until > datetime.utcnow():
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=CommonResponse(
                message="Account is locked. Try again later.",
                status_code=status.HTTP_403_FORBIDDEN,
                data=None,
                error="Account locked due to too many failed login attempts"
            ).dict()
        )

    if not db_user.hashed_password or not bcrypt.checkpw(user.password.encode(), db_user.hashed_password.encode()):
        user_repo.increment_failed_login_attempts(db_user)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Invalid email or password"
            ).dict()
        )

    user_repo.reset_failed_login_attempts(db_user)
    user_repo.update_last_login(db_user)

    access_token, refresh_token, refresh_expires_at = jwt_handler.create_tokens(db_user.id, db_user.email)
    
    # Store user data in Redis for faster access
    user_data = UserInDB.from_orm(db_user).dict()
    redis_client.store_user_data(str(db_user.id), user_data, ttl_seconds=3600)
    
    return CommonResponse(
        message="Login successful",
        status_code=status.HTTP_200_OK,
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            refresh_token_expires_at=refresh_expires_at
        ).dict(),
        error=None
    )


@api_v1.get("/auth/google")
def auth_google():
    auth_url, state = social_login.get_google_auth_url()
    return CommonResponse(
        message="Google authentication URL generated",
        status_code=status.HTTP_200_OK,
        data={"authorization_url": auth_url, "state": state},
        error=None
    )


@api_v1.get("/callback/google", response_model=CommonResponse)
def google_callback(code: str, user_repo: UserRepository = Depends(get_user_repository)):
    try:
        user_info = social_login.handle_google_callback(code)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CommonResponse(
                message="Google authentication failed",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=None,
                error=str(e)
            ).dict()
        )

    email = user_info["email"]
    google_id = user_info["google_id"]
    db_user = user_repo.get_user_by_google_id(google_id)
    if not db_user:
        db_user = user_repo.create_user(
            email=email,
            username=user_info.get("name"),
            google_id=google_id
        )
    user_repo.update_last_login(db_user)
    access_token, refresh_token, refresh_expires_at = jwt_handler.create_tokens(db_user.id, db_user.email)
    return CommonResponse(
        message="Google login successful",
        status_code=status.HTTP_200_OK,
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            refresh_token_expires_at=refresh_expires_at
        ).dict(),
        error=None
    )


@api_v1.post("/refresh", response_model=CommonResponse)
def refresh_token(refresh_token: str = Header(..., alias="Refresh-Token"),
                  user_repo: UserRepository = Depends(get_user_repository)):
    payload = jwt_handler.verify_refresh_token(refresh_token)
    if isinstance(payload, JSONResponse):
        return payload

    email = payload.get("sub")
    user_id = payload.get("id")
    if email is None or user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CommonResponse(
                message="Invalid refresh token",
                status_code=status.HTTP_401_UNAUTHORIZED,
                data=None,
                error="Refresh token missing required fields"
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

    access_token = jwt_handler.create_access_token(user.id, user.email)
    return CommonResponse(
        message="Access token refreshed successfully",
        status_code=status.HTTP_200_OK,
        data=Token(
            access_token=access_token,
            refresh_token=refresh_token,  # Return the same refresh token
            token_type="bearer",
            refresh_token_expires_at=None  # Not needed during refresh
        ).dict(),
        error=None
    )


@api_v1.post("/logout", response_model=CommonResponse)
def logout(refresh_token: str = Header(..., alias="Refresh-Token"), 
           current_user=Depends(dependencies.get_current_user)):
    payload = jwt_handler.verify_refresh_token(refresh_token)
    if isinstance(payload, JSONResponse):
        return payload

    # Blacklist the refresh token
    expires_at = datetime.utcfromtimestamp(payload["exp"])
    redis_client.blacklist_token(refresh_token, expires_at)
    
    # Delete user data from Redis
    user_id = payload.get("id")
    if user_id:
        redis_client.delete_user_data(user_id)

    return CommonResponse(
        message="Logout successful",
        status_code=status.HTTP_200_OK,
        data=None,
        error=None
    )


@api_v1.get("/me", response_model=CommonResponse)
def read_users_me(current_user=Depends(dependencies.get_current_user)):
    if isinstance(current_user, JSONResponse):
        return current_user
    return CommonResponse(
        message="User data retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=UserInDB.from_orm(current_user).dict(),
        error=None
    )
