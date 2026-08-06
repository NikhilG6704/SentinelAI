from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Central configuration for the AI Engine.

    All configuration values should be accessed through this class.
    """

    # =========================
    # Project
    # =========================
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "SentinelAI AI Engine")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # =========================
    # Backend API
    # =========================
    API_BASE_URL: str = os.getenv(
        "API_BASE_URL",
        "http://localhost:8000/api/v1",
    )

    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    API_BATCH_SIZE: int = int(os.getenv("API_BATCH_SIZE", "500"))

    # =========================
    # Dataset Paths
    # =========================
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    DATASETS_DIR: Path = BASE_DIR / "datasets"

    PROCESSED_DATA_DIR: Path = DATASETS_DIR / "processed"

    FEATURES_DATA_DIR: Path = DATASETS_DIR / "features"

    # =========================
    # Export
    # =========================
    EXPORT_CSV: bool = os.getenv("EXPORT_CSV", "True").lower() == "true"

    EXPORT_PARQUET: bool = (
        os.getenv("EXPORT_PARQUET", "True").lower() == "true"
    )

    # =========================
    # Normalization
    # =========================
    DEFAULT_SCALER: str = os.getenv(
        "DEFAULT_SCALER",
        "standard",
    )

    # =========================
    # Logging
    # =========================
    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )


settings = Settings()

# Create required directories automatically
settings.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.FEATURES_DATA_DIR.mkdir(parents=True, exist_ok=True)