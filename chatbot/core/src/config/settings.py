from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Agent Model Inference Service"

    # Code generation model settings
    code_model_name: str = "Salesforce/codegen-350M-mono"
    code_model_max_length: int = 512
    code_model_default_temperature: float = 0.7
    code_model_default_top_p: float = 0.95

    class Config:
        # Load variables from a .env file if present
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global settings instance
settings = Settings()
