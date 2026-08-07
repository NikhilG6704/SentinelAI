"""
Configuration for the SentinelAI automated retraining pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class RetrainingConfiguration:
    """
    Central configuration for automated retraining.
    """

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    pipeline_name: str = "SentinelAI-Retraining"

    dataset_directory: str = "datasets"

    version_directory: str = "dataset_versions"

    evaluation_directory: str = "evaluation_reports"

    minimum_f1_improvement: float = 0.02

    allow_precision_drop: bool = False

    keep_previous_versions: int = 5

    default_stage: str = "Production"

    # ------------------------------------------------------------------
    # Supported Models
    # ------------------------------------------------------------------

    supported_models: tuple[str, ...] = (
        "anomaly_detection",
        "failure_prediction",
        "root_cause_analysis",
        "recommendation_engine",
        "decision_engine",
    )

    # ------------------------------------------------------------------
    # Project Paths
    # ------------------------------------------------------------------

    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent
    )

    @property
    def datasets_path(self) -> Path:
        return self.project_root / self.dataset_directory

    @property
    def versions_path(self) -> Path:
        return self.project_root / self.version_directory

    @property
    def evaluations_path(self) -> Path:
        return self.project_root / self.evaluation_directory

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def is_supported(self, model_name: str) -> bool:
        return model_name in self.supported_models

    def ensure_directories(self) -> None:
        self.datasets_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.versions_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.evaluations_path.mkdir(
            parents=True,
            exist_ok=True,
        )


retraining_config = RetrainingConfiguration()