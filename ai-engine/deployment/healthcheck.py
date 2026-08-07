"""
Health checks for SentinelAI deployment.
"""

from __future__ import annotations

from dataclasses import dataclass
from shutil import disk_usage
from typing import Any

import mlflow

from deployment.configuration import deployment_config
from mlops.model_registry import model_registry
from serving.cache import model_cache
from utils.logger import logger


@dataclass(frozen=True)
class HealthStatus:
    """
    Result of a health check.
    """

    healthy: bool
    details: dict[str, Any]


class HealthCheck:
    """
    Performs deployment health validation.
    """

    # ------------------------------------------------------------------
    # MLflow
    # ------------------------------------------------------------------

    def mlflow(self) -> HealthStatus:
        try:
            return HealthStatus(
                healthy=True,
                details={
                    "tracking_uri": mlflow.get_tracking_uri(),
                },
            )
        except Exception as exc:
            return HealthStatus(
                healthy=False,
                details={
                    "error": str(exc),
                },
            )

    # ------------------------------------------------------------------
    # Model Registry
    # ------------------------------------------------------------------

    def registry(self) -> HealthStatus:
        try:
            models = list(model_registry.client.search_registered_models())

            return HealthStatus(
                healthy=True,
                details={
                    "registered_models": len(models),
                },
            )

        except Exception as exc:
            return HealthStatus(
                healthy=False,
                details={
                    "error": str(exc),
                },
            )

    # ------------------------------------------------------------------
    # Model Cache
    # ------------------------------------------------------------------

    def cache(self) -> HealthStatus:
        stats = model_cache.stats()

        return HealthStatus(
            healthy=True,
            details=stats,
        )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def configuration(self) -> HealthStatus:
        try:
            deployment_config.ensure_directories()

            return HealthStatus(
                healthy=True,
                details={
                    "environment": deployment_config.environment,
                    "host": deployment_config.host,
                    "port": deployment_config.port,
                },
            )

        except Exception as exc:
            return HealthStatus(
                healthy=False,
                details={
                    "error": str(exc),
                },
            )

    # ------------------------------------------------------------------
    # Disk
    # ------------------------------------------------------------------

    def disk(self) -> HealthStatus:
        total, used, free = disk_usage(
            deployment_config.project_root
        )

        percent_used = (used / total) * 100

        return HealthStatus(
            healthy=percent_used < 90,
            details={
                "total_bytes": total,
                "used_bytes": used,
                "free_bytes": free,
                "percent_used": round(percent_used, 2),
            },
        )

    # ------------------------------------------------------------------
    # Overall
    # ------------------------------------------------------------------

    def overall(self) -> HealthStatus:
        checks = {
            "mlflow": self.mlflow(),
            "registry": self.registry(),
            "cache": self.cache(),
            "configuration": self.configuration(),
            "disk": self.disk(),
        }

        healthy = all(
            status.healthy
            for status in checks.values()
        )

        logger.info(
            f"Deployment health: {healthy}"
        )

        return HealthStatus(
            healthy=healthy,
            details={
                name: status.details
                for name, status in checks.items()
            },
        )


healthcheck = HealthCheck()