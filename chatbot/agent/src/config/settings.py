from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv
import os


env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # AWS Bedrock settings
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION_NAME: str = os.getenv("AWS_REGION_NAME", "us-east-1")
    AWS_BEDROCK_MODEL_ID: str = os.getenv(
        "AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
    )

    # Application settings
    app_name: str = "Agent Model Inference Service"

    # Model configuration
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.0

    # Legacy model settings (kept for compatibility)
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    internet_classifier_model: str = "facebook/bart-large-mnli"

    candidate_labels: List[str] = ["requires internet access", "does not require internet access"]
    prompt_categories: List[str] = [
        "declarative",
        "interrogative",
        "imperative",
        "exclamatory",
        "conversational",
    ]

    class Config:
        # Load variables from a .env file if present
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global settings instance
settings = Settings()
