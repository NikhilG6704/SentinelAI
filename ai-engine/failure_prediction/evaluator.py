from __future__ import annotations

import time
from typing import Any

import numpy as np
import pandas as pd
import psutil
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from utils.logger import logger


class FailurePredictionEvaluator:
    """
    Evaluates supervised failure prediction models.
    """

    def __init__(
        self,
        predictor,
    ) -> None:

        self.predictor = predictor

    def evaluate(
        self,
        X: pd.DataFrame,
        y_true: np.ndarray | pd.Series,
    ) -> dict[str, Any]:

        logger.info(
            f"Evaluating "
            f"{self.predictor.__class__.__name__}"
        )

        process = psutil.Process()

        memory_before = process.memory_info().rss

        start = time.perf_counter()

        predictions = self.predictor.predict(X)

        probabilities = (
            self.predictor.predict_proba(X)[:, 1]
        )

        latency = time.perf_counter() - start

        memory_after = process.memory_info().rss

        result = {
            "model": self.predictor.__class__.__name__,
            "precision": precision_score(
                y_true,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                predictions,
                zero_division=0,
            ),
            "f1_score": f1_score(
                y_true,
                predictions,
                zero_division=0,
            ),
            "roc_auc": roc_auc_score(
                y_true,
                probabilities,
            ),
            "pr_auc": average_precision_score(
                y_true,
                probabilities,
            ),
            "confusion_matrix": confusion_matrix(
                y_true,
                predictions,
            ),
            "inference_latency_ms": latency * 1000,
            "memory_usage_mb": (
                memory_after - memory_before
            )
            / (1024 * 1024),
        }

        logger.success(
            "Evaluation completed."
        )

        return result

    @staticmethod
    def comparison_report(
        evaluations: list[dict[str, Any]],
    ) -> pd.DataFrame:
        """
        Generate a comparison table.
        """

        report = pd.DataFrame(evaluations)

        return report

    @staticmethod
    def save_report(
        report: pd.DataFrame,
        output_path: str,
    ) -> None:

        report.to_csv(
            output_path,
            index=False,
        )

        logger.success(
            f"Report saved to {output_path}"
        )