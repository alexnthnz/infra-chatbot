import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import bcrypt

from auth import jwt_handler, social_login, dependencies
from database import crud, database
from schemas.user import UserCreate, UserLogin, Token, UserInDB
from config.config import config

app = FastAPI(title="Authentication Service")
api_v1 = FastAPI()
app.mount("/api/v1", api_v1)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

database.Base.metadata.create_all(bind=database.engine)


@api_v1.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    db_user = crud.create_user(db, email=user.email, hashed_password=hashed_password)
    token = jwt_handler.create_jwt_token(db_user.id, db_user.email)
    return {"access_token": token, "token_type": "bearer"}


@api_v1.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user or not bcrypt.checkpw(user.password.encode(), db_user.hashed_password.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt_handler.create_jwt_token(db_user.id, db_user.email)
    return {"access_token": token, "token_type": "bearer"}


@api_v1.get("/auth/google")
def auth_google():
    auth_url, state = social_login.get_google_auth_url()
    return {"authorization_url": auth_url, "state": state}


@api_v1.get("/callback/google", response_model=Token)
def google_callback(code: str, db: Session = Depends(database.get_db)):
    user_info = social_login.handle_google_callback(code)
    email = user_info["email"]
    google_id = user_info["google_id"]
    db_user = crud.get_user_by_google_id(db, google_id)

    if not db_user:
        db_user = crud.create_user(db, email=email, google_id=google_id)
    token = jwt_handler.create_jwt_token(db_user.id, db_user.email)
    return {"access_token": token, "token_type": "bearer"}


@api_v1.get("/me", response_model=UserInDB)
def read_users_me(current_user=Depends(dependencies.get_current_user)):
    return current_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)
