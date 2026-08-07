"""
Deployment validation for SentinelAI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from deployment.configuration import deployment_config
from deployment.healthcheck import healthcheck
from utils.logger import logger


@dataclass(frozen=True)
class ValidationResult:
    """
    Deployment validation result.
    """

    valid: bool
    checks: dict[str, bool]
    details: dict[str, Any]


class DeploymentValidator:
    """
    Validates deployment readiness.
    """

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Run all deployment validation checks.
        """

        deployment_config.ensure_directories()

        mlflow_status = healthcheck.mlflow()
        registry_status = healthcheck.registry()
        configuration_status = healthcheck.configuration()
        disk_status = healthcheck.disk()

        checks = {
            "mlflow": mlflow_status.healthy,
            "registry": registry_status.healthy,
            "configuration": configuration_status.healthy,
            "disk": disk_status.healthy,
        }

        valid = all(checks.values())

        result = ValidationResult(
            valid=valid,
            checks=checks,
            details={
                "mlflow": mlflow_status.details,
                "registry": registry_status.details,
                "configuration": configuration_status.details,
                "disk": disk_status.details,
            },
        )

        logger.info(
            f"Deployment validation passed={valid}"
        )

        return result

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def is_ready(self) -> bool:
        """
        Return True if deployment is production ready.
        """

        return self.validate().valid


deployment_validator = DeploymentValidator()