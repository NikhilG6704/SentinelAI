"""
Startup service for SentinelAI AI Engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import mlflow

from deployment.configuration import deployment_config
from deployment.deployment_validator import deployment_validator
from deployment.healthcheck import healthcheck
from serving.configuration import serving_config
from serving.model_loader import model_loader
from utils.logger import logger


@dataclass(frozen=True)
class StartupResult:
    """
    Result of startup initialization.
    """

    success: bool
    message: str
    details: dict[str, Any]


class StartupService:
    """
    Initializes the AI Engine for production.
    """

    # ------------------------------------------------------------------
    # Startup
    # ------------------------------------------------------------------

    def initialize(
        self,
        *,
        warm_models: bool = False,
    ) -> StartupResult:
        """
        Perform startup initialization.
        """

        logger.info(
            "Starting SentinelAI AI Engine..."
        )

        # Ensure required directories exist
        deployment_config.ensure_directories()

        # Validate deployment
        validation = deployment_validator.validate()

        if not validation.valid:
            return StartupResult(
                success=False,
                message="Deployment validation failed.",
                details=validation.details,
            )

        # Initialize MLflow
        mlflow.set_tracking_uri(
            deployment_config.tracking_uri,
        )

        mlflow.set_registry_uri(
            deployment_config.registry_uri,
        )

        # Warm model cache (optional)
        warmed_models: list[str] = []

        if warm_models:
            for model_name in serving_config.supported_models:
                try:
                    model_loader.load(model_name)
                    warmed_models.append(model_name)
                except Exception as exc:
                    logger.warning(
                        f"Failed to warm model "
                        f"'{model_name}': {exc}"
                    )

        # Final health verification
        overall_health = healthcheck.overall()

        if not overall_health.healthy:
            return StartupResult(
                success=False,
                message="Health checks failed.",
                details=overall_health.details,
            )

        logger.success(
            "SentinelAI AI Engine started successfully."
        )

        return StartupResult(
            success=True,
            message="Startup completed successfully.",
            details={
                "environment": deployment_config.environment,
                "tracking_uri": deployment_config.tracking_uri,
                "warmed_models": warmed_models,
                "health": overall_health.details,
            },
        )


startup_service = StartupService()

if __name__ == "__main__":
    result = startup_service.initialize(warm_models=True)

    if result.success:
        logger.success(result.message)
    else:
        logger.error(result.message)
        raise SystemExit(1)