"""
Configuration for the SentinelAI monitoring framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class MonitoringConfiguration:
    """
    Central configuration for model monitoring.
    """

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    monitoring_name: str = "SentinelAI-Monitoring"

    monitoring_directory: str = "monitoring_reports"

    alert_directory: str = "alerts"

    # ------------------------------------------------------------------
    # Drift Thresholds
    # ------------------------------------------------------------------

    psi_threshold: float = 0.20

    js_threshold: float = 0.15

    ks_threshold: float = 0.05

    # ------------------------------------------------------------------
    # Performance Thresholds
    # ------------------------------------------------------------------

    minimum_precision: float = 0.90

    minimum_recall: float = 0.90

    minimum_f1: float = 0.90

    minimum_roc_auc: float = 0.90

    # ------------------------------------------------------------------
    # Latency Thresholds
    # ------------------------------------------------------------------

    max_average_latency_ms: float = 100.0

    max_p95_latency_ms: float = 200.0

    max_p99_latency_ms: float = 500.0

    # ------------------------------------------------------------------
    # Resource Thresholds
    # ------------------------------------------------------------------

    max_cpu_percent: float = 80.0

    max_memory_percent: float = 80.0

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
    # Project
    # ------------------------------------------------------------------

    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent
    )

    @property
    def monitoring_path(self) -> Path:
        return self.project_root / self.monitoring_directory

    @property
    def alerts_path(self) -> Path:
        return self.project_root / self.alert_directory

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def is_supported(
        self,
        model_name: str,
    ) -> bool:
        return model_name in self.supported_models

    def ensure_directories(self) -> None:
        self.monitoring_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.alerts_path.mkdir(
            parents=True,
            exist_ok=True,
        )


monitoring_config = MonitoringConfiguration()