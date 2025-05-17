import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import database
from routes.v1 import api_v1

# Configure logging for Lambda with explicit CloudWatch compatibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Ensure logs go to stdout for CloudWatch
    ],
    force=True,  # Force reconfiguration to avoid conflicts
)
logger = logging.getLogger("handler_service")
logger.setLevel(logging.INFO)  # Explicitly set to INFO

# FastAPI app
app = FastAPI(title="Handler Service")

database.migrate_db()

app.mount("/api/v1", api_v1)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Service is running.",
        "database": {
            "status": database.check_db_connection(),
            "message": "Database connection is healthy.",
            "tables": database.list_tables(),
        },
    }


@app.get("/migrate")
def migrate():
    """Run migrations."""
    database.migrate_db()
    return {"status": "ok", "message": "Migrations applied."}
