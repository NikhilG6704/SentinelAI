from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd

from anomaly_detection.base_detector import BaseDetector
from utils.logger import logger


class AnomalyTrainer:
    """
    Orchestrates anomaly detector training.

    Responsibilities:
        - Train detector
        - Measure training time
        - Save trained model
        - Return training metadata
    """

    def __init__(
        self,
        detector: BaseDetector,
        model_dir: str | Path,
    ) -> None:
        self.detector = detector
        self.model_dir = Path(model_dir)

    def train(
        self,
        X: pd.DataFrame,
    ) -> dict[str, Any]:
        """
        Train and persist the detector.
        """

        logger.info(
            f"Starting training for "
            f"{self.detector.__class__.__name__}"
        )

        start_time = time.perf_counter()

        self.detector.train(X)

        training_time = time.perf_counter() - start_time

        model_path = (
            self.model_dir /
            f"{self.detector.__class__.__name__}.model"
        )

        self.detector.save(model_path)

        logger.success(
            f"Training completed in "
            f"{training_time:.2f} seconds."
        )

        return {
            "model_name": self.detector.__class__.__name__,
            "training_time_seconds": training_time,
            "model_path": str(model_path),
        }

    def load(
        self,
        model_path: str | Path,
    ) -> None:
        """
        Load an existing model.
        """

        self.detector.load(model_path)

        logger.success(
            f"Loaded model from {model_path}"
        )