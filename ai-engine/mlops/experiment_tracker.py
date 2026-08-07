"""
High-level experiment tracker built on top of MLflowManager.
"""

from __future__ import annotations

import platform
import random
import time
from contextlib import AbstractContextManager
from datetime import UTC, datetime
from typing import Any

import numpy as np

from mlops.configuration import mlflow_config
from mlops.mlflow_manager import mlflow_manager


class ExperimentTracker(AbstractContextManager):
    """
    High-level experiment tracker.

    Usage:
        tracker = ExperimentTracker(...)

        with tracker:
            ...
            tracker.log_metrics(...)
            tracker.log_model(...)
    """

    def __init__(
        self,
        component: str,
        run_name: str | None = None,
        dataset_version: str = "unknown",
        feature_version: str = "v1",
        random_seed: int | None = None,
        hyperparameters: dict[str, Any] | None = None,
        tags: dict[str, str] | None = None,
    ) -> None:

        self.component = component
        self.run_name = run_name

        self.dataset_version = dataset_version
        self.feature_version = feature_version

        self.random_seed = (
            random_seed
            if random_seed is not None
            else mlflow_config.random_seed
        )

        self.hyperparameters = hyperparameters or {}
        self.tags = tags or {}

        self._start_time: float | None = None
        self._run_context = None

    # ------------------------------------------------------------------ #
    # Context Manager
    # ------------------------------------------------------------------ #

    def __enter__(self):

        mlflow_manager.get_or_create_experiment(self.component)
        mlflow_manager.set_experiment(self.component)

        self._run_context = mlflow_manager.start_run(
            run_name=self.run_name
        )

        self._run_context.__enter__()

        self._start_time = time.perf_counter()

        self._initialize_run()

        return self

    def __exit__(self, exc_type, exc, traceback):

        if self._start_time is not None:
            duration = time.perf_counter() - self._start_time

            mlflow_manager.log_metric(
                "training_duration_seconds",
                round(duration, 3),
            )

        if exc is not None:
            mlflow_manager.set_tag(
                "status",
                "failed",
            )

            mlflow_manager.set_tag(
                "exception_type",
                exc.__class__.__name__,
            )

            mlflow_manager.set_tag(
                "exception_message",
                str(exc),
            )
        else:
            mlflow_manager.set_tag(
                "status",
                "completed",
            )

        if self._run_context:
            self._run_context.__exit__(
                exc_type,
                exc,
                traceback,
            )

    # ------------------------------------------------------------------ #
    # Initialization
    # ------------------------------------------------------------------ #

    def _initialize_run(self) -> None:

        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

        mlflow_manager.log_params(
            {
                "dataset_version": self.dataset_version,
                "feature_version": self.feature_version,
                "random_seed": self.random_seed,
            }
        )

        if self.hyperparameters:
            mlflow_manager.log_params(
                self.hyperparameters
            )

        default_tags = mlflow_config.default_tags(
            self.component
        )

        default_tags.update(
            {
                "python_version": platform.python_version(),
                "platform": platform.platform(),
                "started_at": datetime.now(UTC).isoformat(),
            }
        )

        default_tags.update(self.tags)

        mlflow_manager.set_tags(default_tags)

    # ------------------------------------------------------------------ #
    # Logging
    # ------------------------------------------------------------------ #

    def log_param(
        self,
        key: str,
        value: Any,
    ) -> None:
        mlflow_manager.log_param(key, value)

    def log_params(
        self,
        params: dict[str, Any],
    ) -> None:
        mlflow_manager.log_params(params)

    def log_metric(
        self,
        key: str,
        value: float,
        step: int | None = None,
    ) -> None:
        mlflow_manager.log_metric(
            key,
            value,
            step,
        )

    def log_metrics(
        self,
        metrics: dict[str, float],
        step: int | None = None,
    ) -> None:
        mlflow_manager.log_metrics(
            metrics,
            step,
        )

    def log_artifact(
        self,
        artifact_path: str,
        destination: str | None = None,
    ) -> None:
        mlflow_manager.log_artifact(
            artifact_path,
            destination,
        )

    def log_artifacts(
        self,
        directory: str,
        destination: str | None = None,
    ) -> None:
        mlflow_manager.log_artifacts(
            directory,
            destination,
        )

    # ------------------------------------------------------------------ #
    # Models
    # ------------------------------------------------------------------ #

    def log_sklearn_model(
        self,
        model: Any,
        artifact_path: str = "model",
    ) -> None:
        mlflow_manager.log_sklearn_model(
            model,
            artifact_path,
        )

    def log_xgboost_model(
        self,
        model: Any,
        artifact_path: str = "model",
    ) -> None:
        mlflow_manager.log_xgboost_model(
            model,
            artifact_path,
        )

    def log_pytorch_model(
        self,
        model: Any,
        artifact_path: str = "model",
    ) -> None:
        mlflow_manager.log_pytorch_model(
            model,
            artifact_path,
        )

    # ------------------------------------------------------------------ #
    # Utility
    # ------------------------------------------------------------------ #

    @property
    def run_id(self) -> str | None:
        return mlflow_manager.get_run_id()