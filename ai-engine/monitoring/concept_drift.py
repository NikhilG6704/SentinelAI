"""
Concept drift detection for SentinelAI.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from utils.logger import logger


@dataclass(frozen=True)
class ConceptDriftResult:
    """
    Result of concept drift analysis.
    """

    prediction_shift: float
    confidence_shift: float
    error_rate_change: float

    prediction_drift: bool
    confidence_drift: bool
    error_drift: bool

    @property
    def drift_detected(self) -> bool:
        return (
            self.prediction_drift
            or self.confidence_drift
            or self.error_drift
        )


class ConceptDriftDetector:
    """
    Detects concept drift using prediction behaviour.
    """

    def __init__(
        self,
        *,
        prediction_threshold: float = 0.10,
        confidence_threshold: float = 0.10,
        error_threshold: float = 0.05,
    ) -> None:

        self.prediction_threshold = prediction_threshold
        self.confidence_threshold = confidence_threshold
        self.error_threshold = error_threshold

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect(
        self,
        *,
        previous_predictions: np.ndarray,
        current_predictions: np.ndarray,
        previous_confidence: np.ndarray,
        current_confidence: np.ndarray,
        previous_labels: np.ndarray,
        current_labels: np.ndarray,
    ) -> ConceptDriftResult:

        previous_predictions = np.asarray(
            previous_predictions
        )

        current_predictions = np.asarray(
            current_predictions
        )

        previous_confidence = np.asarray(
            previous_confidence
        )

        current_confidence = np.asarray(
            current_confidence
        )

        previous_labels = np.asarray(
            previous_labels
        )

        current_labels = np.asarray(
            current_labels
        )

        prediction_shift = abs(
            np.mean(current_predictions)
            - np.mean(previous_predictions)
        )

        confidence_shift = abs(
            np.mean(current_confidence)
            - np.mean(previous_confidence)
        )

        previous_error = np.mean(
            previous_predictions
            != previous_labels
        )

        current_error = np.mean(
            current_predictions
            != current_labels
        )

        error_change = abs(
            current_error
            - previous_error
        )

        result = ConceptDriftResult(
            prediction_shift=prediction_shift,
            confidence_shift=confidence_shift,
            error_rate_change=error_change,
            prediction_drift=bool(
                prediction_shift
                >= self.prediction_threshold
            ),
            confidence_drift=bool(
                confidence_shift
                >= self.confidence_threshold
            ),
            error_drift=bool(
                error_change
                >= self.error_threshold
            ),
        )

        logger.info(
            f"Concept drift detected={result.drift_detected}"
        )

        return result


concept_drift_detector = ConceptDriftDetector()