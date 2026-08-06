from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np
import pandas as pd


class BaseDetector(ABC):
    """
    Abstract base class for all anomaly detection models.

    Every anomaly detector in SentinelAI must implement
    this interface to ensure a consistent training,
    evaluation, persistence, and inference workflow.
    """

    @abstractmethod
    def train(self, X: pd.DataFrame | np.ndarray) -> None:
        """
        Train the anomaly detection model.

        Parameters
        ----------
        X : pd.DataFrame | np.ndarray
            Training dataset.
        """
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> np.ndarray:
        """
        Predict anomalies.

        Returns
        -------
        np.ndarray
            Binary predictions:
                0 -> Normal
                1 -> Anomaly
        """
        raise NotImplementedError

    @abstractmethod
    def anomaly_score(
        self,
        X: pd.DataFrame | np.ndarray,
    ) -> np.ndarray:
        """
        Return anomaly scores.

        Higher score = more anomalous.
        """
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        path: str | Path,
    ) -> None:
        """
        Save the trained model.
        """
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        path: str | Path,
    ) -> None:
        """
        Load a previously trained model.
        """
        raise NotImplementedError