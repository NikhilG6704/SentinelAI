from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from utils.logger import logger


class FeatureSelector:
    """
    Performs feature importance analysis and feature selection.
    """

    def __init__(
        self,
        random_state: int = 42,
    ) -> None:

        self.model = RandomForestClassifier(
            n_estimators=200,
            random_state=random_state,
            n_jobs=-1,
        )

        self.feature_importances_: pd.DataFrame | None = None

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> None:
        """
        Train the feature selector.
        """

        logger.info(
            "Calculating feature importance..."
        )

        self.model.fit(X, y)

        importance = pd.DataFrame(
            {
                "feature": X.columns,
                "importance": self.model.feature_importances_,
            }
        )

        importance = importance.sort_values(
            "importance",
            ascending=False,
        ).reset_index(drop=True)

        self.feature_importances_ = importance

        logger.success(
            "Feature importance calculated."
        )

    def top_features(
        self,
        k: int = 20,
    ) -> list[str]:
        """
        Return the top-k most important features.
        """

        if self.feature_importances_ is None:
            raise RuntimeError(
                "FeatureSelector has not been fitted."
            )

        return (
            self.feature_importances_
            .head(k)["feature"]
            .tolist()
        )

    def transform(
        self,
        X: pd.DataFrame,
        k: int = 20,
    ) -> pd.DataFrame:
        """
        Reduce the dataset to the top-k features.
        """

        features = self.top_features(k)

        return X[features]

    def fit_transform(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        k: int = 20,
    ) -> pd.DataFrame:

        self.fit(X, y)

        return self.transform(X, k)

    def feature_report(self) -> pd.DataFrame:
        """
        Return the complete feature importance table.
        """

        if self.feature_importances_ is None:
            raise RuntimeError(
                "FeatureSelector has not been fitted."
            )

        return self.feature_importances_.copy()

    def save_report(
        self,
        output_path: str,
    ) -> None:
        """
        Export feature importance report.
        """

        if self.feature_importances_ is None:
            raise RuntimeError(
                "FeatureSelector has not been fitted."
            )

        self.feature_importances_.to_csv(
            output_path,
            index=False,
        )

        logger.success(
            f"Feature report saved to {output_path}"
        )