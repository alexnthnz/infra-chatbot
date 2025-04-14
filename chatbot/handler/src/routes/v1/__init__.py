from fastapi import FastAPI
from .chat import router as chat_router
from .auth import router as auth_router

api_v1 = FastAPI()
api_v1.mount("/auth", auth_router)
api_v1.mount("/chats", chat_router)
