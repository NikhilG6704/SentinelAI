from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from utils.logger import logger


class RandomForestFailurePredictor:
    """
    Random Forest based infrastructure failure predictor.
    """

    def __init__(
        self,
        *,
        n_estimators: int = 300,
        max_depth: int | None = None,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        class_weight: str = "balanced",
        random_state: int = 42,
        n_jobs: int = -1,
    ) -> None:

        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            class_weight=class_weight,
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
        y: pd.Series | np.ndarray,
    ) -> None:

        logger.info(
            "Training Random Forest..."
        )

        X = self._to_numpy(X)
        y = np.asarray(y)

        self.model.fit(X, y)

        self.is_trained = True

        logger.success(
            "Random Forest training completed."
        )

    def predict(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> np.ndarray:

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained first."
            )

        X = self._to_numpy(X)

        return self.model.predict(X)

    def predict_proba(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> np.ndarray:

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained first."
            )

        X = self._to_numpy(X)

        return self.model.predict_proba(X)

    def feature_importance(self) -> np.ndarray:

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained first."
            )

        return self.model.feature_importances_

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

        joblib.dump(
            self.model,
            path,
        )

        logger.success(
            f"Model saved to {path}"
        )

    def load(
        self,
        path: str | Path,
    ) -> None:

        self.model = joblib.load(path)

        self.is_trained = True

        logger.success(
            f"Model loaded from {path}"
        )