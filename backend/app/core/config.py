from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "SentinelAI API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for SentinelAI."

    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
print(settings.model_dump())