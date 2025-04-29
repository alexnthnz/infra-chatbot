import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Agent Model Inference Service"

    # Model generation settings (used for generation params)
    code_model_max_length: int = 512
    code_model_default_temperature: float = 0.7
    code_model_default_top_p: float = 0.95

    # Bedrock Knowledge Base
    bedrock_kb: str | None = os.getenv("BEDROCK_KB")

    # OpenSearch Serverless
    aws_region: str = os.getenv('AWS_REGION')
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = ""


settings = Settings()
