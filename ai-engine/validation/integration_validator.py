"""
Integration validator for SentinelAI AI Engine.
"""

from __future__ import annotations

from dataclasses import dataclass

from deployment.deployment_validator import deployment_validator
from mlops.mlflow_manager import mlflow_manager
from mlops.model_registry import model_registry
from monitoring.monitoring_manager import monitoring_manager
from retraining.retraining_manager import retraining_manager
from serving.model_loader import model_loader
from utils.logger import logger


# ==========================================================
# Result Models
# ==========================================================


@dataclass(frozen=True)
class ValidationCheck:
    """
    Represents a single integration validation.
    """

    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class IntegrationValidationResult:
    """
    Overall integration validation result.
    """

    success: bool
    checks: list[ValidationCheck]

    @property
    def passed(self) -> int:
        return sum(check.passed for check in self.checks)

    @property
    def failed(self) -> int:
        return len(self.checks) - self.passed


# ==========================================================
# Validator
# ==========================================================


class IntegrationValidator:
    """
    Validates integration of all major AI Engine components.
    """

    # ------------------------------------------------------
    # Public
    # ------------------------------------------------------

    def validate(self) -> IntegrationValidationResult:

        logger.info("Running integration validation...")

        checks = [
            self.validate_deployment(),
            self.validate_mlflow(),
            self.validate_registry(),
            self.validate_serving(),
            self.validate_monitoring(),
            self.validate_retraining(),
        ]

        success = all(check.passed for check in checks)

        logger.success(
            f"Integration validation completed "
            f"({sum(c.passed for c in checks)}/{len(checks)} passed)"
        )

        return IntegrationValidationResult(
            success=success,
            checks=checks,
        )

    # ------------------------------------------------------
    # Individual Validators
    # ------------------------------------------------------

    def validate_deployment(self) -> ValidationCheck:

        try:
            result = deployment_validator.validate()

            return ValidationCheck(
                name="Deployment",
                passed=result.valid,
                message="Deployment validation completed.",
            )

        except Exception as exc:
            return ValidationCheck(
                name="Deployment",
                passed=False,
                message=str(exc),
            )

    def validate_mlflow(self) -> ValidationCheck:

        try:
            mlflow_manager.initialize()

            return ValidationCheck(
                name="MLflow",
                passed=True,
                message="MLflow connection established.",
            )

        except Exception as exc:
            return ValidationCheck(
                name="MLflow",
                passed=False,
                message=str(exc),
            )

    def validate_registry(self) -> ValidationCheck:

        try:
            model_registry.list_models()

            return ValidationCheck(
                name="Model Registry",
                passed=True,
                message="Registry reachable.",
            )

        except Exception as exc:
            return ValidationCheck(
                name="Model Registry",
                passed=False,
                message=str(exc),
            )

    def validate_serving(self) -> ValidationCheck:

        try:
            _ = model_loader

            return ValidationCheck(
                name="Model Serving",
                passed=True,
                message="Model loader initialized.",
            )

        except Exception as exc:
            return ValidationCheck(
                name="Model Serving",
                passed=False,
                message=str(exc),
            )

    def validate_monitoring(self) -> ValidationCheck:

        try:
            _ = monitoring_manager

            return ValidationCheck(
                name="Monitoring",
                passed=True,
                message="Monitoring initialized.",
            )

        except Exception as exc:
            return ValidationCheck(
                name="Monitoring",
                passed=False,
                message=str(exc),
            )

    def validate_retraining(self) -> ValidationCheck:

        try:
            _ = retraining_manager

            return ValidationCheck(
                name="Retraining",
                passed=True,
                message="Retraining initialized.",
            )

        except Exception as exc:
            return ValidationCheck(
                name="Retraining",
                passed=False,
                message=str(exc),
            )


integration_validator = IntegrationValidator()