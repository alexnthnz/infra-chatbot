import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import config

# pull in your existing logger or create one
logger = logging.getLogger(__name__)

DATABASE_URL = config.DATABASE_URL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: create a new DB session per request and close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection():
    """Verify we can connect and run a simple query."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "success", "detail": "Database connection OK"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def list_tables():
    """List all tables in the public schema."""
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema="public")
    return {"tables": tables}


def migrate_db():
    """
    Create all tables defined on Base.metadata.
    Accepts an optional Session for signature consistency.
    """
    try:
        # import all models so they're registered on Base.metadata
        from database import models

        Base.metadata.create_all(bind=engine)
        logger.info("Database migrations applied successfully")
        return {"status": "success", "detail": "Migrations applied"}
    except Exception as e:
        logger.error(f"Migration error: {e}", exc_info=True)
        return {"status": "error", "detail": str(e)}
