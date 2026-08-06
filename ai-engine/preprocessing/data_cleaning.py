from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from utils.constants import TIMESTAMP_COLUMNS
from utils.logger import logger


class DataCleaner:
    """
    Cleans infrastructure datasets before feature engineering.
    """

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows.
        """

        before = len(df)

        df = df.drop_duplicates()

        removed = before - len(df)

        logger.info(f"Removed {removed} duplicate records.")

        return df

    @staticmethod
    def standardize_timestamps(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert all timestamp columns to UTC.
        """

        for column in TIMESTAMP_COLUMNS:

            if column not in df.columns:
                continue

            df[column] = pd.to_datetime(
                df[column],
                utc=True,
                errors="coerce",
            )

        logger.info("Timestamp normalization completed.")

        return df

    @staticmethod
    def remove_invalid_records(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Remove rows containing invalid timestamps.
        """

        timestamp_columns = [
            col
            for col in TIMESTAMP_COLUMNS
            if col in df.columns
        ]

        if timestamp_columns:

            before = len(df)

            df = df.dropna(
                subset=timestamp_columns
            )

            logger.info(
                f"Removed {before-len(df)} invalid timestamp records."
            )

        return df

    @staticmethod
    def fill_missing_numeric(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Fill missing numeric values using column median.
        """

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns

        for column in numeric_columns:

            median = df[column].median()

            df[column] = df[column].fillna(median)

        logger.info("Numeric missing values filled.")

        return df

    @staticmethod
    def fill_missing_categorical(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Fill missing categorical values using mode.
        """

        categorical_columns = df.select_dtypes(
            include="object"
        ).columns

        for column in categorical_columns:

            if df[column].dropna().empty:
                continue

            mode = df[column].mode().iloc[0]

            df[column] = df[column].fillna(mode)

        logger.info("Categorical missing values filled.")

        return df

    @staticmethod
    def clip_percentage_columns(
        df: pd.DataFrame,
        columns: Iterable[str],
    ) -> pd.DataFrame:
        """
        Ensure utilization percentages stay between 0 and 100.
        """

        for column in columns:

            if column not in df.columns:
                continue

            df[column] = df[column].clip(
                lower=0,
                upper=100,
            )

        logger.info("Percentage columns validated.")

        return df

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """
        Execute the complete cleaning pipeline.
        """

        logger.info("Starting data cleaning pipeline...")

        df = DataCleaner.remove_duplicates(df)

        df = DataCleaner.standardize_timestamps(df)

        df = DataCleaner.remove_invalid_records(df)

        df = DataCleaner.fill_missing_numeric(df)

        df = DataCleaner.fill_missing_categorical(df)

        df = DataCleaner.clip_percentage_columns(
            df,
            [
                "cpu_usage",
                "memory_usage",
                "disk_usage",
            ],
        )

        logger.success("Data cleaning completed.")

        return df