from fastapi import FastAPI
from .chat import router as chat_router
from .auth import router as auth_router

api_v1 = FastAPI()
api_v1.include_router(auth_router, prefix="/auth")
api_v1.include_router(chat_router, prefix="/chats")
