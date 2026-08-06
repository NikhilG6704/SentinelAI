from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from anomaly_detection.base_detector import BaseDetector
from utils.logger import logger


class IsolationForestDetector(BaseDetector):
    """
    Isolation Forest based anomaly detector.
    """

    def __init__(
        self,
        *,
        n_estimators: int = 200,
        contamination: float = 0.05,
        max_samples: str | int = "auto",
        random_state: int = 42,
        n_jobs: int = -1,
    ) -> None:

        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            max_samples=max_samples,
            random_state=random_state,
            n_jobs=n_jobs,
        )

        self.is_trained = False

    @staticmethod
    def _to_numpy(
        X: pd.DataFrame | np.ndarray,
    ) -> np.ndarray:

        if isinstance(X, pd.DataFrame):
            return X.to_numpy(dtype=np.float32)

        return np.asarray(X, dtype=np.float32)

    def train(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> None:

        logger.info("Training Isolation Forest...")

        X = self._to_numpy(X)

        self.model.fit(X)

        self.is_trained = True

        logger.success("Isolation Forest training completed.")

    def predict(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> np.ndarray:

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before prediction."
            )

        X = self._to_numpy(X)

        predictions = self.model.predict(X)

        # sklearn:
        #  1  -> normal
        # -1 -> anomaly

        return np.where(predictions == -1, 1, 0)

    def anomaly_score(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> np.ndarray:

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before scoring."
            )

        X = self._to_numpy(X)

        scores = self.model.score_samples(X)

        # Higher score = more anomalous
        return -scores

    def save(
        self,
        path: str | Path,
    ) -> None:

        if not self.is_trained:
            raise RuntimeError(
                "Cannot save an untrained model."
            )

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(self.model, path)

        logger.success(f"Model saved to {path}")

    def load(
        self,
        path: str | Path,
    ) -> None:

        path = Path(path)

        self.model = joblib.load(path)

        self.is_trained = True

        logger.success(f"Model loaded from {path}")