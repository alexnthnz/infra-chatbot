import os

from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    PORT: int = int(os.getenv("PORT", 8000))

    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # JWT configuration
    JWT_ACCESS_SECRET: str = os.getenv("JWT_ACCESS_SECRET")
    JWT_REFRESH_SECRET: str = os.getenv("JWT_REFRESH_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # Default to HS256 if not specified
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "your-app")
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "api://your-app")

    # Google OAuth configuration
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI")

    # Redis configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # AWS S3 configuration
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")  # Default region
    S3_BUCKET: str = os.getenv("S3_BUCKET")

    # Agent Service configuration
    AGENT_SERVICE_URL: str = os.getenv("AGENT_SERVICE_URL", "http://agent-service:8001")

    # Core Service configuration
    CORE_SERVICE_URL: str = os.getenv("CORE_SERVICE_URL", "http://core-service:8002")

    # Validate required environment variables
    def __post_init__(self):
        required_vars = [
            "DATABASE_URL",
            "JWT_ACCESS_SECRET",
            "JWT_REFRESH_SECRET",
            "JWT_ISSUER",
            "JWT_AUDIENCE",
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET",
            "GOOGLE_REDIRECT_URI",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "S3_BUCKET",
            "AGENT_SERVICE_URL",
            "CORE_SERVICE_URL",
        ]
        for var in required_vars:
            if not getattr(self, var):
                raise ValueError(f"Missing required environment variable: {var}")


# Instantiate the config object
config = Config()
