from __future__ import annotations

from typing import Any

from utils.logger import logger


class ModelSelector:
    """
    Selects the best anomaly detection model based on
    evaluation metrics.
    """

    def __init__(
        self,
        primary_metric: str = "f1_score",
    ) -> None:
        self.primary_metric = primary_metric

    def select_best(
        self,
        evaluations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Select the best-performing model.

        Falls back to inference latency if the primary
        metric is unavailable.
        """

        if not evaluations:
            raise ValueError(
                "No evaluation results provided."
            )

        logger.info(
            f"Selecting best model using "
            f"'{self.primary_metric}'."
        )

        available = [
            e
            for e in evaluations
            if self.primary_metric in e
            and e[self.primary_metric] is not None
        ]

        if available:

            best = max(
                available,
                key=lambda x: x[self.primary_metric],
            )

        else:

            logger.warning(
                f"Metric '{self.primary_metric}' "
                "not available. Falling back to "
                "lowest inference latency."
            )

            best = min(
                evaluations,
                key=lambda x: x["inference_latency_ms"],
            )

        logger.success(
            f"Selected model: {best['model']}"
        )

        return best

    def ranking(
        self,
        evaluations: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Return all models ranked by the primary metric.
        """

        return sorted(
            evaluations,
            key=lambda x: x.get(
                self.primary_metric,
                float("-inf"),
            ),
            reverse=True,
        )