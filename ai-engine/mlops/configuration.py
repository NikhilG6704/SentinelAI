"""
Centralized configuration for SentinelAI MLOps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class MLflowConfiguration:
    """
    Immutable configuration for the SentinelAI MLflow integration.
    """

    # ------------------------------------------------------------------
    # Project Metadata
    # ------------------------------------------------------------------

    project_name: str = "SentinelAI"
    project_version: str = "1.0.0"
    environment: str = "development"

    random_seed: int = 42

    # ------------------------------------------------------------------
    # Project Directories
    # ------------------------------------------------------------------

    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent
    )

    # ------------------------------------------------------------------
    # Experiment Names
    # ------------------------------------------------------------------

    experiments: dict[str, str] = field(
        default_factory=lambda: {
            "anomaly_detection": "SentinelAI-AnomalyDetection",
            "failure_prediction": "SentinelAI-FailurePrediction",
            "root_cause_analysis": "SentinelAI-RootCauseAnalysis",
            "recommendation_engine": "SentinelAI-RecommendationEngine",
            "decision_engine": "SentinelAI-DecisionEngine",
        }
    )

    # ------------------------------------------------------------------
    # Registered Model Names
    # ------------------------------------------------------------------

    models: dict[str, str] = field(
        default_factory=lambda: {
            # Service names
            "anomaly_detection": "IsolationForest",
            "failure_prediction": "RandomForest",
            "root_cause_analysis": "RootCauseModel",
            "recommendation_engine": "RecommendationModel",
            "decision_engine": "DecisionEngineModel",

            # Concrete model names
            "isolation_forest": "IsolationForest",
            "autoencoder": "Autoencoder",
            "random_forest": "RandomForest",
            "xgboost": "XGBoost",
            "root_cause": "RootCauseModel",
            "recommendation": "RecommendationModel",
        }
    )

    # ------------------------------------------------------------------
    # Lifecycle Stages
    # ------------------------------------------------------------------

    STAGE_DEVELOPMENT: str = "Development"
    STAGE_STAGING: str = "Staging"
    STAGE_PRODUCTION: str = "Production"
    STAGE_ARCHIVED: str = "Archived"

    stages: tuple[str, ...] = (
        "Development",
        "Staging",
        "Production",
        "Archived",
    )

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    @property
    def mlruns_directory(self) -> Path:
        return self.project_root / "mlruns"

    @property
    def artifact_directory(self) -> Path:
        return self.project_root / "artifacts"

    @property
    def tracking_uri(self) -> str:
        return f"sqlite:///{(self.project_root / 'mlflow.db').resolve()}"

    @property
    def registry_uri(self) -> str:
        return self.tracking_uri

    # ------------------------------------------------------------------
    # Experiment Helpers
    # ------------------------------------------------------------------

    def get_experiment_name(self, component: str) -> str:
        if component not in self.experiments:
            raise KeyError(
                f"Unknown experiment component: {component}"
            )

        return self.experiments[component]

    # ------------------------------------------------------------------
    # Model Helpers
    # ------------------------------------------------------------------

    def get_model_name(self, model_key: str) -> str:
        if model_key not in self.models:
            raise KeyError(
                f"Unknown model: {model_key}"
            )

        return self.models[model_key]

    def is_valid_stage(self, stage: str) -> bool:
        return stage in self.stages

    # ------------------------------------------------------------------
    # Tags
    # ------------------------------------------------------------------

    def default_tags(
        self,
        component: str,
    ) -> dict[str, str]:

        return {
            "project": self.project_name,
            "component": component,
            "environment": self.environment,
            "version": self.project_version,
        }

    # ------------------------------------------------------------------
    # Directory Management
    # ------------------------------------------------------------------

    def ensure_directories(self) -> None:
        self.mlruns_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.artifact_directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# Singleton instance used across SentinelAI
mlflow_config = MLflowConfiguration()