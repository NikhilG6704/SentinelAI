from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd

from anomaly_detection.base_detector import BaseDetector
from mlops.artifact_manager import artifact_manager
from mlops.experiment_tracker import ExperimentTracker
from mlops.model_registry import model_registry
from utils.logger import logger


class AnomalyTrainer:
    """
    Orchestrates anomaly detector training with MLflow tracking.
    """

    def __init__(
        self,
        detector: BaseDetector,
        model_dir: str | Path,
    ) -> None:
        self.detector = detector
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

    def train(
        self,
        X: pd.DataFrame,
        dataset_version: str = "v1",
        feature_version: str = "v1",
        hyperparameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        model_name = self.detector.__class__.__name__

        logger.info(f"Starting training for {model_name}")

        tracker = ExperimentTracker(
            component="anomaly_detection",
            run_name=model_name,
            dataset_version=dataset_version,
            feature_version=feature_version,
            hyperparameters=hyperparameters or {},
        )

        with tracker:

            start = time.perf_counter()

            self.detector.train(X)

            training_time = time.perf_counter() - start

            model_path = (
                self.model_dir /
                f"{model_name}.model"
            )

            self.detector.save(model_path)

            tracker.log_metric(
                "training_time_seconds",
                training_time,
            )

            tracker.log_param(
                "training_samples",
                len(X),
            )

            tracker.log_param(
                "feature_count",
                X.shape[1],
            )

            artifact_manager.log_model_file(model_path)

            run_id = tracker.run_id

            if run_id is not None:

                model_uri = f"runs:/{run_id}/models"

                registry_key = {
                    "IsolationForest": "isolation_forest",
                    "Autoencoder": "autoencoder",
                }.get(model_name)

                if registry_key is not None:
                    model_registry.register_model(
                        model_uri=model_uri,
                        model_key=registry_key,
                    )

            logger.success(
                f"Training completed in "
                f"{training_time:.2f} seconds."
            )

            return {
                "model_name": model_name,
                "training_time_seconds": training_time,
                "model_path": str(model_path),
                "run_id": run_id,
            }

    def load(
        self,
        model_path: str | Path,
    ) -> None:

        self.detector.load(model_path)

        logger.success(
            f"Loaded model from {model_path}"
        )