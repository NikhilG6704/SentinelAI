"""
Retraining manager for SentinelAI.

Coordinates model retraining using the existing AI training pipelines.
"""

from __future__ import annotations

import time
from typing import Any

from mlops.experiment_tracker import ExperimentTracker
from mlops.model_registry import model_registry
from retraining.configuration import retraining_config
from utils.logger import logger


class RetrainingManager:
    """
    Orchestrates retraining of supported AI models.
    """

    def retrain(
        self,
        *,
        model_name: str,
        trainer: Any,
        train_args: tuple[Any, ...],
        train_kwargs: dict[str, Any] | None = None,
        dataset_version: str,
    ) -> dict[str, Any]:
        """
        Retrain a model using an existing trainer.

        Parameters
        ----------
        model_name
            Supported pipeline name.

        trainer
            Existing trainer instance.

        train_args
            Positional arguments passed to trainer.train().

        train_kwargs
            Keyword arguments passed to trainer.train().

        dataset_version
            Dataset version identifier.
        """

        if not retraining_config.is_supported(model_name):
            raise ValueError(
                f"Unsupported model '{model_name}'."
            )

        train_kwargs = train_kwargs or {}

        tracker = ExperimentTracker(
            component=model_name,
            run_name=f"retraining-{dataset_version}",
        )

        logger.info(
            f"Starting retraining for '{model_name}'."
        )

        start = time.perf_counter()

        with tracker:

            tracker.log_param(
                "dataset_version",
                dataset_version,
            )

            tracker.log_param(
                "pipeline",
                "automated_retraining",
            )

            result = trainer.train(
                *train_args,
                **train_kwargs,
            )

            duration = (
                time.perf_counter()
                - start
            )

            tracker.log_metric(
                "training_time",
                duration,
            )

            if isinstance(result, dict):

                for key, value in result.items():

                    if isinstance(
                        value,
                        (int, float),
                    ):
                        tracker.log_metric(
                            key,
                            value,
                        )

            model_path = None

            if isinstance(result, dict):
                model_path = result.get(
                    "model_path"
                )

            if model_path:

                tracker.log_artifact(
                    model_path
                )

                run_id = tracker.run_id

                if run_id is not None:

                    model_uri = (
                        f"runs:/{run_id}/model"
                    )

                    try:
                        model_registry.register_model(
                            model_uri=model_uri,
                            model_key=model_name,
                        )
                    except Exception as exc:
                        logger.warning(
                            f"Model registration skipped: {exc}"
                        )

        logger.success(
            f"Retraining completed for '{model_name}'."
        )

        return {
            "model": model_name,
            "dataset_version": dataset_version,
            "training_time": duration,
            "result": result,
        }


retraining_manager = RetrainingManager()