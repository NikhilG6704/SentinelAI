from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import pandas as pd

from mlops.artifact_manager import artifact_manager
from mlops.experiment_tracker import ExperimentTracker
from mlops.model_registry import model_registry
from utils.logger import logger


class FailurePredictionTrainer:
    """
    Orchestrates supervised model training with MLflow tracking.
    """

    def __init__(
        self,
        predictor,
        model_dir: str | Path,
    ) -> None:

        self.predictor = predictor
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        dataset_version: str = "v1",
        feature_version: str = "v1",
        hyperparameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        model_name = self.predictor.__class__.__name__

        logger.info(f"Training {model_name}")

        tracker = ExperimentTracker(
            component="failure_prediction",
            run_name=model_name,
            dataset_version=dataset_version,
            feature_version=feature_version,
            hyperparameters=hyperparameters or {},
        )

        with tracker:

            start = time.perf_counter()

            self.predictor.train(X, y)

            training_time = time.perf_counter() - start

            model_path = (
                self.model_dir
                / f"{model_name}.joblib"
            )

            self.predictor.save(model_path)

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

            tracker.log_param(
                "target_classes",
                y.nunique(),
            )

            artifact_manager.log_model_file(model_path)

            # Log native ML model
            if model_name == "RandomForestFailurePredictor":
                tracker.log_sklearn_model(
                    self.predictor.model,
                    artifact_path="model",
                )

            elif model_name == "XGBoostFailurePredictor":
                tracker.log_xgboost_model(
                    self.predictor.model,
                    artifact_path="model",
            )

            run_id = tracker.run_id

            if run_id is not None:

                registry_key = {
                    "RandomForestPredictor": "random_forest",
                    "XGBoostPredictor": "xgboost",
                }.get(model_name)

                if registry_key is not None:

                    model_registry.register_model(
                        model_uri=f"runs:/{run_id}/model",
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

        self.predictor.load(model_path)

        logger.success(
            f"Loaded model from {model_path}"
        )