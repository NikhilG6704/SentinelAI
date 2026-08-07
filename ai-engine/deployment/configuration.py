"""
Configuration for SentinelAI production deployment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os


@dataclass(frozen=True)
class DeploymentConfiguration:
    """
    Central deployment configuration.
    """

    # ------------------------------------------------------------------
    # Service
    # ------------------------------------------------------------------

    service_name: str = "SentinelAI-AI-Engine"

    environment: str = field(
        default_factory=lambda: os.getenv(
            "ENVIRONMENT",
            "production",
        )
    )

    host: str = field(
        default_factory=lambda: os.getenv(
            "HOST",
            "0.0.0.0",
        )
    )

    port: int = field(
        default_factory=lambda: int(
            os.getenv(
                "PORT",
                "8000",
            )
        )
    )

    debug: bool = field(
        default_factory=lambda: (
            os.getenv(
                "DEBUG",
                "false",
            ).lower()
            == "true"
        )
    )

    # ------------------------------------------------------------------
    # Project
    # ------------------------------------------------------------------

    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent
    )

    # ------------------------------------------------------------------
    # MLflow
    # ------------------------------------------------------------------

    tracking_uri: str = field(
        default_factory=lambda: os.getenv(
            "MLFLOW_TRACKING_URI",
            "sqlite:///mlflow.db",
        )
    )

    registry_uri: str = field(
        default_factory=lambda: os.getenv(
            "MLFLOW_REGISTRY_URI",
            "sqlite:///mlflow.db",
        )
    )

    # ------------------------------------------------------------------
    # Directories
    # ------------------------------------------------------------------

    model_directory: str = "models"

    artifact_directory: str = "artifacts"

    log_directory: str = "logs"

    # ------------------------------------------------------------------
    # Docker
    # ------------------------------------------------------------------

    docker_image: str = "sentinelai-ai-engine"

    docker_tag: str = "latest"

    # ------------------------------------------------------------------
    # Health Checks
    # ------------------------------------------------------------------

    health_interval_seconds: int = 30

    startup_timeout_seconds: int = 60

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    @property
    def models_path(self) -> Path:
        return self.project_root / self.model_directory

    @property
    def artifacts_path(self) -> Path:
        return self.project_root / self.artifact_directory

    @property
    def logs_path(self) -> Path:
        return self.project_root / self.log_directory

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def ensure_directories(self) -> None:
        self.models_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.artifacts_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logs_path.mkdir(
            parents=True,
            exist_ok=True,
        )


deployment_config = DeploymentConfiguration()