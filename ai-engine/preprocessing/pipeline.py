from __future__ import annotations

import asyncio
from pathlib import Path

import pandas as pd

from config.settings import settings
from preprocessing.data_cleaning import DataCleaner
from preprocessing.data_loader import DataLoader
from preprocessing.feature_engineering import FeatureEngineer
from preprocessing.normalization import Normalizer
from utils.logger import logger


class PreprocessingPipeline:
    """
    End-to-end preprocessing pipeline.

    Workflow:
        Load Data
            ↓
        Clean Data
            ↓
        Generate Features
            ↓
        Normalize
            ↓
        Export CSV / Parquet
    """

    def __init__(self) -> None:
        self.loader = DataLoader()
        self.cleaner = DataCleaner()
        self.engineer = FeatureEngineer()

        self.normalizer = Normalizer(
            method=settings.DEFAULT_SCALER
        )

    async def load_data(self) -> dict[str, pd.DataFrame]:
        """
        Load all datasets concurrently.
        """

        logger.info("Loading datasets from backend...")

        (
            assets,
            agents,
            metrics,
            alerts,
            incidents,
            logs,
            workflows,
            audit_logs,
        ) = await asyncio.gather(
            self.loader.load_assets(),
            self.loader.load_agents(),
            self.loader.load_metrics(),
            self.loader.load_alerts(),
            self.loader.load_incidents(),
            self.loader.load_logs(),
            self.loader.load_workflows(),
            self.loader.load_audit_logs(),
        )

        logger.success("All datasets loaded successfully.")

        return {
            "assets": assets,
            "agents": agents,
            "metrics": metrics,
            "alerts": alerts,
            "incidents": incidents,
            "logs": logs,
            "workflows": workflows,
            "audit_logs": audit_logs,
        }

    def clean_data(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> dict[str, pd.DataFrame]:
        """
        Clean every dataset.
        """

        logger.info("Cleaning datasets...")

        cleaned = {}

        for name, df in datasets.items():
            cleaned[name] = self.cleaner.clean(df)

        logger.success("All datasets cleaned.")

        return cleaned

    def engineer_features(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> dict[str, pd.DataFrame]:
        """
        Generate AI features.
        """

        return self.engineer.generate(
            metrics=datasets["metrics"],
            agents=datasets["agents"],
            alerts=datasets["alerts"],
            incidents=datasets["incidents"],
            logs=datasets["logs"],
            workflows=datasets["workflows"],
        )

    def normalize(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> dict[str, pd.DataFrame]:
        """
        Normalize numerical metric features.
        """

        metrics = datasets["metrics"]

        numeric_columns = [
            col
            for col in metrics.columns
            if pd.api.types.is_numeric_dtype(metrics[col])
        ]

        datasets["metrics"] = self.normalizer.fit_transform(
            metrics,
            numeric_columns,
        )

        logger.success("Normalization completed.")

        return datasets

    def export_dataset(
        self,
        df: pd.DataFrame,
        output_dir: Path,
        filename: str,
    ) -> None:
        """
        Export DataFrame as CSV and/or Parquet.
        """

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        if settings.EXPORT_CSV:
            csv_path = output_dir / f"{filename}.csv"
            df.to_csv(csv_path, index=False)

        if settings.EXPORT_PARQUET:
            parquet_path = output_dir / f"{filename}.parquet"
            df.to_parquet(parquet_path, index=False)

        logger.info(f"Exported {filename}")

    def export(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> None:
        """
        Export all processed datasets.
        """

        logger.info("Exporting datasets...")

        for name, df in datasets.items():

            if name == "metrics":
                directory = settings.FEATURES_DATA_DIR
            else:
                directory = settings.PROCESSED_DATA_DIR

            self.export_dataset(
                df,
                directory,
                name,
            )

        logger.success("Dataset export completed.")

    async def run(self) -> dict[str, pd.DataFrame]:
        """
        Execute the complete preprocessing pipeline.
        """

        datasets = await self.load_data()

        datasets = self.clean_data(datasets)

        feature_sets = self.engineer_features(datasets)

        datasets.update(feature_sets)

        datasets = self.normalize(datasets)

        self.export(datasets)

        logger.success(
            "AI preprocessing pipeline completed successfully."
        )

        return datasets