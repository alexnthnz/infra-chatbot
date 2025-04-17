from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os


env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # Application settings
    app_name: str = "Agent Model Inference Service"

    # Model configuration
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
