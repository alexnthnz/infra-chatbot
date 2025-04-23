from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Agent Model Inference Service"

    # Model generation settings (used for generation params)
    code_model_max_length: int = 512
    code_model_default_temperature: float = 0.7
    code_model_default_top_p: float = 0.95

    # Bedrock Knowledge Base
    bedrock_kb: str | None = None  # Optional, validated in RAGService

    # OpenSearch Serverless
    opensearch_endpoint: str  # e.g., https://<collection-id>.<region>.aoss.amazonaws.com
    aws_region: str  # e.g., us-east-1

    # xAI API
    xai_api_key: str  # Required for ChatXAI

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = ""


settings = Settings()
