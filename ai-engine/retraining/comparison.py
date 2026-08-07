"""
Model comparison for the SentinelAI retraining pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from utils.logger import logger


@dataclass(frozen=True)
class ComparisonResult:
    """
    Result of comparing a production model with a newly trained model.
    """

    improved: bool
    metric_changes: dict[str, float]
    current_metrics: dict[str, float]
    candidate_metrics: dict[str, float]


class ModelComparison:
    """
    Compares production and candidate model metrics.
    """

    _METRICS = (
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
        "training_time",
        "inference_latency",
    )

    def compare(
        self,
        current: dict[str, Any],
        candidate: dict[str, Any],
    ) -> ComparisonResult:
        """
        Compare two model metric dictionaries.
        """

        changes: dict[str, float] = {}

        for metric in self._METRICS:

            current_value = float(
                current.get(metric, 0.0)
            )

            candidate_value = float(
                candidate.get(metric, 0.0)
            )

            changes[metric] = (
                candidate_value - current_value
            )

        improved = (
            candidate.get("f1_score", 0.0)
            > current.get("f1_score", 0.0)
        )

        logger.info(
            "Model comparison completed."
        )

        return ComparisonResult(
            improved=improved,
            metric_changes=changes,
            current_metrics=current,
            candidate_metrics=candidate,
        )


model_comparison = ModelComparison()