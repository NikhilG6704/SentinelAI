from __future__ import annotations

from datetime import timedelta

import pandas as pd

from utils.logger import logger


class LabelGenerator:
    """
    Generate supervised labels for failure prediction.

    Label:
        1 -> Failure occurs within prediction window.
        0 -> No failure occurs within prediction window.
    """

    def __init__(
        self,
        prediction_window_minutes: int = 30,
    ) -> None:

        self.prediction_window = timedelta(
            minutes=prediction_window_minutes
        )

    def generate(
        self,
        dataset: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info(
            f"Generating labels using "
            f"{self.prediction_window} window..."
        )

        required_columns = [
            "infrastructure_asset_id",
            "collection_timestamp",
            "detected_at",
        ]

        missing = [
            col
            for col in required_columns
            if col not in dataset.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        dataset = dataset.copy()

        dataset["collection_timestamp"] = pd.to_datetime(
            dataset["collection_timestamp"],
            utc=True,
        )

        dataset["detected_at"] = pd.to_datetime(
            dataset["detected_at"],
            utc=True,
            errors="coerce",
        )

        dataset["failure_label"] = 0

        grouped = dataset.groupby(
            "infrastructure_asset_id"
        )

        for _, group in grouped:

            incident_times = (
                group["detected_at"]
                .dropna()
                .sort_values()
                .tolist()
            )

            if not incident_times:
                continue

            for idx in group.index:

                timestamp = dataset.loc[
                    idx,
                    "collection_timestamp",
                ]

                for incident_time in incident_times:

                    if (
                        timestamp
                        <= incident_time
                        <= timestamp
                        + self.prediction_window
                    ):
                        dataset.loc[
                            idx,
                            "failure_label",
                        ] = 1

                        break

        positives = dataset[
            "failure_label"
        ].sum()

        logger.success(
            f"Generated labels "
            f"(Positive={positives}, "
            f"Negative={len(dataset)-positives})"
        )

        return dataset

    def class_distribution(
        self,
        dataset: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Return label distribution.
        """

        distribution = (
            dataset["failure_label"]
            .value_counts()
            .rename_axis("label")
            .reset_index(name="count")
        )

        distribution["percentage"] = (
            distribution["count"]
            / distribution["count"].sum()
            * 100
        )

        return distribution