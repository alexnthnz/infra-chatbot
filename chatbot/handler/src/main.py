import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from database import database
from config.config import config
from routes.v1 import api_v1

app = FastAPI(title="Authentication Service")

app.mount("/api/v1", api_v1)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

database.Base.metadata.create_all(bind=database.engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)
