from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Agent Model Inference Service"

    # Model configuration
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    internet_classifier_model: str = "facebook/bart-large-mnli"
    candidate_labels: List[str] = ["requires internet access", "does not require internet access"]

    class Config:
        # Load variables from a .env file if present
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global settings instance
settings = Settings()
