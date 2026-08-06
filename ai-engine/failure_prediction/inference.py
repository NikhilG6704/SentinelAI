from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import numpy as np
import pandas as pd

from utils.logger import logger


class FailurePredictionInference:
    """
    Unified inference engine for failure prediction models.
    """

    def __init__(
        self,
        predictor,
        prediction_window_minutes: int = 30,
    ) -> None:

        self.predictor = predictor
        self.prediction_window_minutes = prediction_window_minutes

    @staticmethod
    def _risk_level(probability: float) -> str:
        """
        Convert probability into a human-readable risk level.
        """

        if probability < 0.30:
            return "Low"

        if probability < 0.70:
            return "Medium"

        return "High"

    def predict(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> list[dict[str, Any]]:
        """
        Predict infrastructure failure risk.
        """

        logger.info(
            f"Running inference using "
            f"{self.predictor.__class__.__name__}"
        )

        probabilities = self.predictor.predict_proba(X)[:, 1]

        predictions = self.predictor.predict(X)

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        results: list[dict[str, Any]] = []

        for prediction, probability in zip(
            predictions,
            probabilities,
        ):

            confidence = max(
                probability,
                1 - probability,
            )

            results.append(
                {
                    "prediction": int(prediction),
                    "failure_probability": round(
                        probability * 100,
                        2,
                    ),
                    "confidence_score": round(
                        confidence * 100,
                        2,
                    ),
                    "risk_level": self._risk_level(
                        probability
                    ),
                    "predicted_time_window": (
                        f"{self.prediction_window_minutes} minutes"
                    ),
                    "model_used": (
                        self.predictor.__class__.__name__
                    ),
                    "timestamp": timestamp,
                }
            )

        logger.success(
            f"Inference completed "
            f"({len(results)} samples)."
        )

        return results