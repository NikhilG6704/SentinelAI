from __future__ import annotations

from pathlib import Path
import gc
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

from utils.logger import logger


class XGBoostFailurePredictor:
    """
    XGBoost based infrastructure failure predictor.
    """

    def __init__(
        self,
        *,
        n_estimators: int = 300,
        learning_rate: float = 0.05,
        max_depth: int = 6,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8,
        random_state: int = 42,
        n_jobs: int = -1,
    ) -> None:

        self.model = XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            objective="binary:logistic",
            eval_metric="logloss",
            tree_method="hist",
            verbosity=0,
            random_state=random_state,
            n_jobs=1,
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
            "Training XGBoost..."
        )

        X = self._to_numpy(X)
        y = np.asarray(y)

        self.model.fit(X, y)

        self.is_trained = True

        logger.success(
            "XGBoost training completed."
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

    def close(self) -> None:
        """
        Explicitly release XGBoost resources.
        """

        if hasattr(self, "model"):
            del self.model

        gc.collect()


    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def load(
        self,
        path: str | Path,
    ) -> None:

        self.model = joblib.load(path)

        self.is_trained = True

        logger.success(
            f"Model loaded from {path}"
        )