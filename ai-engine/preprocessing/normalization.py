from __future__ import annotations

from typing import Iterable

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from utils.constants import (
    MINMAX_SCALER,
    STANDARD_SCALER,
    SUPPORTED_SCALERS,
)
from utils.logger import logger


class Normalizer:
    """
    Normalize numerical features for machine learning.
    """

    def __init__(self, method: str = STANDARD_SCALER) -> None:
        if method not in SUPPORTED_SCALERS:
            raise ValueError(
                f"Unsupported scaler '{method}'. "
                f"Supported scalers: {SUPPORTED_SCALERS}"
            )

        self.method = method

        if method == STANDARD_SCALER:
            self.scaler = StandardScaler()
        else:
            self.scaler = MinMaxScaler()

    def fit_transform(
        self,
        df: pd.DataFrame,
        columns: Iterable[str],
    ) -> pd.DataFrame:
        """
        Fit the scaler and transform the specified columns.
        """

        columns = [col for col in columns if col in df.columns]

        if not columns:
            logger.warning("No valid columns found for normalization.")
            return df

        df = df.copy()

        df[columns] = self.scaler.fit_transform(df[columns])

        logger.success(
            f"{self.method} normalization applied to {len(columns)} columns."
        )

        return df

    def transform(
        self,
        df: pd.DataFrame,
        columns: Iterable[str],
    ) -> pd.DataFrame:
        """
        Transform new data using an already fitted scaler.
        """

        columns = [col for col in columns if col in df.columns]

        if not columns:
            return df

        df = df.copy()

        df[columns] = self.scaler.transform(df[columns])

        return df

    def inverse_transform(
        self,
        df: pd.DataFrame,
        columns: Iterable[str],
    ) -> pd.DataFrame:
        """
        Convert normalized values back to their original scale.
        """

        columns = [col for col in columns if col in df.columns]

        if not columns:
            return df

        df = df.copy()

        df[columns] = self.scaler.inverse_transform(df[columns])

        return df