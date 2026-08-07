"""
Health service for the SentinelAI model serving layer.
"""

from __future__ import annotations

from typing import Any

import mlflow

from serving.cache import model_cache
from serving.configuration import serving_config
from utils.logger import logger


class HealthService:
    """
    Provides health and status information for the serving layer.
    """

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # MLflow
    # ------------------------------------------------------------------

    def mlflow_status(self) -> dict[str, Any]:
        """
        Check MLflow connectivity.
        """

        try:
            tracking_uri = mlflow.get_tracking_uri()

            return {
                "connected": True,
                "tracking_uri": tracking_uri,
            }

        except Exception as exc:
            logger.error(
                f"MLflow health check failed: {exc}"
            )

            return {
                "connected": False,
                "error": str(exc),
            }

    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------

    def cache_status(self) -> dict[str, Any]:
        """
        Return cache statistics.
        """

        return model_cache.stats()

    # ------------------------------------------------------------------
    # Models
    # ------------------------------------------------------------------

    def loaded_models(self) -> list[dict[str, Any]]:
        """
        Return metadata for loaded models.
        """

        models: list[dict[str, Any]] = []

        for cached in model_cache.items():
            models.append(
                {
                    "name": cached.name,
                    "version": cached.version,
                    "stage": cached.stage,
                    "loaded_at": cached.loaded_at.isoformat(),
                }
            )

        return models

    # ------------------------------------------------------------------
    # Overall Health
    # ------------------------------------------------------------------

    def status(self) -> dict[str, Any]:
        """
        Overall serving health.
        """

        return {
            "service": serving_config.service_name,
            "healthy": True,
            "mlflow": self.mlflow_status(),
            "cache": self.cache_status(),
            "loaded_models": self.loaded_models(),
        }


health_service = HealthService()