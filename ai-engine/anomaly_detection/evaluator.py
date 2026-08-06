from __future__ import annotations

import time
from typing import Any

import numpy as np
import pandas as pd
import psutil
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from anomaly_detection.base_detector import BaseDetector
from utils.logger import logger


class ModelEvaluator:
    """
    Evaluates anomaly detection models.
    """

    def __init__(
        self,
        detector: BaseDetector,
    ) -> None:
        self.detector = detector

    def evaluate(
        self,
        X: pd.DataFrame,
        y_true: np.ndarray | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate a trained detector.

        If labels are available, classification metrics
        will also be calculated.
        """

        logger.info(
            f"Evaluating {self.detector.__class__.__name__}"
        )

        process = psutil.Process()

        memory_before = process.memory_info().rss

        start = time.perf_counter()

        predictions = self.detector.predict(X)

        latency = time.perf_counter() - start

        memory_after = process.memory_info().rss

        result: dict[str, Any] = {
            "model": self.detector.__class__.__name__,
            "inference_latency_ms": latency * 1000,
            "memory_usage_mb": (
                memory_after - memory_before
            )
            / (1024 * 1024),
        }

        if y_true is not None:

            result["accuracy"] = accuracy_score(
                y_true,
                predictions,
            )

            result["precision"] = precision_score(
                y_true,
                predictions,
                zero_division=0,
            )

            result["recall"] = recall_score(
                y_true,
                predictions,
                zero_division=0,
            )

            result["f1_score"] = f1_score(
                y_true,
                predictions,
                zero_division=0,
            )

            try:
                scores = self.detector.anomaly_score(X)

                result["roc_auc"] = roc_auc_score(
                    y_true,
                    scores,
                )

            except Exception:
                result["roc_auc"] = None

        logger.success(
            f"Evaluation completed for "
            f"{self.detector.__class__.__name__}"
        )

        return result

    @staticmethod
    def comparison_report(
        evaluations: list[dict[str, Any]],
    ) -> pd.DataFrame:
        """
        Generate a comparison table.
        """

        return pd.DataFrame(evaluations)