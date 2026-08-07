"""
Central MLflow manager for SentinelAI.

This module is the ONLY place that directly communicates with MLflow.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any

import mlflow
import mlflow.pytorch
import mlflow.sklearn
import mlflow.xgboost
from mlflow.entities import Run

from mlops.configuration import mlflow_config


class MLflowManager:
    """Wrapper around MLflow APIs."""

    def __init__(self) -> None:
        mlflow_config.ensure_directories()

        mlflow.set_tracking_uri(mlflow_config.tracking_uri)
        mlflow.set_registry_uri(mlflow_config.registry_uri)

    # ------------------------------------------------------------------ #
    # Experiments
    # ------------------------------------------------------------------ #

    def get_or_create_experiment(self, component: str) -> str:
        """
        Returns experiment id.
        """

        experiment_name = mlflow_config.get_experiment_name(component)

        experiment = mlflow.get_experiment_by_name(experiment_name)

        if experiment is not None:
            return experiment.experiment_id

        return mlflow.create_experiment(experiment_name)

    def set_experiment(self, component: str) -> None:
        mlflow.set_experiment(
            mlflow_config.get_experiment_name(component)
        )

    # ------------------------------------------------------------------ #
    # Runs
    # ------------------------------------------------------------------ #

    @contextmanager
    def start_run(
        self,
        run_name: str | None = None,
    ):
        run = mlflow.start_run(
            run_name=run_name,
            nested=False,
        )

        try:
            yield run
        finally:
            if mlflow.active_run():
                mlflow.end_run()

    def active_run(self) -> Run | None:
        return mlflow.active_run()

    # ------------------------------------------------------------------ #
    # Logging
    # ------------------------------------------------------------------ #

    def log_param(self, key: str, value: Any) -> None:
        mlflow.log_param(key, value)

    def log_params(self, params: dict[str, Any]) -> None:
        mlflow.log_params(params)

    def log_metric(
        self,
        key: str,
        value: float,
        step: int | None = None,
    ) -> None:
        if step is None:
            mlflow.log_metric(key, value)
        else:
            mlflow.log_metric(key, value, step=step)

    def log_metrics(
        self,
        metrics: dict[str, float],
        step: int | None = None,
    ) -> None:
        if step is None:
            mlflow.log_metrics(metrics)
        else:
            for key, value in metrics.items():
                mlflow.log_metric(key, value, step=step)

    def set_tag(self, key: str, value: str) -> None:
        mlflow.set_tag(key, value)

    def set_tags(self, tags: dict[str, str]) -> None:
        mlflow.set_tags(tags)

    # ------------------------------------------------------------------ #
    # Artifacts
    # ------------------------------------------------------------------ #

    def log_artifact(
        self,
        artifact_path: str | Path,
        destination: str | None = None,
    ) -> None:
        mlflow.log_artifact(
            str(artifact_path),
            artifact_path=destination,
        )

    def log_artifacts(
        self,
        directory: str | Path,
        destination: str | None = None,
    ) -> None:
        mlflow.log_artifacts(
            str(directory),
            artifact_path=destination,
        )

    # ------------------------------------------------------------------ #
    # Models
    # ------------------------------------------------------------------ #

    def log_sklearn_model(
        self,
        model: Any,
        artifact_path: str,
    ) -> None:
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=artifact_path,
        )

    def log_xgboost_model(
        self,
        model: Any,
        artifact_path: str,
    ) -> None:
        mlflow.xgboost.log_model(
            xgb_model=model,
            artifact_path=artifact_path,
        )

    def log_pytorch_model(
        self,
        model: Any,
        artifact_path: str,
    ) -> None:
        mlflow.pytorch.log_model(
            pytorch_model=model,
            artifact_path=artifact_path,
        )

    # ------------------------------------------------------------------ #
    # Utilities
    # ------------------------------------------------------------------ #

    def get_run_id(self) -> str | None:
        run = mlflow.active_run()

        if run is None:
            return None

        return run.info.run_id

    def get_tracking_uri(self) -> str:
        return mlflow.get_tracking_uri()

    def end_run(self) -> None:
        if mlflow.active_run():
            mlflow.end_run()


mlflow_manager = MLflowManager()