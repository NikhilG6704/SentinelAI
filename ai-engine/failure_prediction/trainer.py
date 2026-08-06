from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd

from utils.logger import logger


class FailurePredictionTrainer:
    """
    Orchestrates supervised model training.
    """

    def __init__(
        self,
        predictor,
        model_dir: str | Path,
    ) -> None:

        self.predictor = predictor
        self.model_dir = Path(model_dir)

    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> dict[str, Any]:
        """
        Train and persist the prediction model.
        """

        logger.info(
            f"Training {self.predictor.__class__.__name__}"
        )

        start = time.perf_counter()

        self.predictor.train(
            X,
            y,
        )

        training_time = time.perf_counter() - start

        extension = (
            ".joblib"
        )

        model_path = (
            self.model_dir
            / f"{self.predictor.__class__.__name__}{extension}"
        )

        self.predictor.save(model_path)

        logger.success(
            f"Training completed in "
            f"{training_time:.2f} seconds."
        )

        return {
            "model_name": self.predictor.__class__.__name__,
            "training_time_seconds": training_time,
            "model_path": str(model_path),
        }

    def load(
        self,
        model_path: str | Path,
    ) -> None:
        """
        Load an existing trained model.
        """

        self.predictor.load(model_path)

        logger.success(
            f"Loaded model from {model_path}"
        )