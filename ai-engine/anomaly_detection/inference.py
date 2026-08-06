from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import numpy as np
import pandas as pd

from anomaly_detection.base_detector import BaseDetector
from utils.logger import logger


class InferenceEngine:
    """
    Unified inference engine for anomaly detection models.
    """

    def __init__(
        self,
        detector: BaseDetector,
    ) -> None:
        self.detector = detector

    @staticmethod
    def _confidence_from_scores(
        scores: np.ndarray,
    ) -> np.ndarray:
        """
        Convert anomaly scores to confidence values in [0, 1].
        """

        if len(scores) == 0:
            return np.array([])

        minimum = scores.min()
        maximum = scores.max()

        if np.isclose(maximum, minimum):
            return np.ones_like(scores)

        return (scores - minimum) / (maximum - minimum)

    def predict(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> list[dict[str, Any]]:
        """
        Run anomaly detection inference.
        """

        logger.info(
            f"Running inference using "
            f"{self.detector.__class__.__name__}"
        )

        predictions = self.detector.predict(X)
        scores = self.detector.anomaly_score(X)

        confidence = self._confidence_from_scores(scores)

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        results: list[dict[str, Any]] = []

        for prediction, score, conf in zip(
            predictions,
            scores,
            confidence,
        ):
            results.append(
                {
                    "status": (
                        "Anomaly"
                        if prediction == 1
                        else "Normal"
                    ),
                    "prediction": int(prediction),
                    "confidence": float(conf),
                    "anomaly_score": float(score),
                    "model_used": self.detector.__class__.__name__,
                    "timestamp": timestamp,
                }
            )

        logger.success(
            f"Inference completed "
            f"({len(results)} samples)."
        )

        return results