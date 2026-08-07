"""
Configuration for the SentinelAI Model Serving Layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ServingConfiguration:
    """
    Central configuration for the model serving layer.
    """

    # ------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------

    service_name: str = "SentinelAI Serving"

    default_stage: str = "Production"

    lazy_loading: bool = True

    cache_enabled: bool = True

    auto_reload: bool = False

    cache_size: int = 32

    cache_ttl_seconds: int = 3600

    # ------------------------------------------------------------------
    # Directories
    # ------------------------------------------------------------------

    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent
    )

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
    # Helpers
    # ------------------------------------------------------------------

    def is_supported(self, model_name: str) -> bool:
        """
        Return True if the requested model is supported.
        """
        return model_name in self.supported_models

    @property
    def cache_directory(self) -> Path:
        """
        Reserved for future on-disk cache.
        """
        return self.project_root / "serving_cache"


serving_config = ServingConfiguration()