from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SentinelAI API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for SentinelAI."
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()