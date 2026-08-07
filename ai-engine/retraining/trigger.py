"""
Trigger interface for the SentinelAI retraining pipeline.
"""

from __future__ import annotations

from typing import Any

from retraining.pipeline import retraining_pipeline
from utils.logger import logger


class RetrainingTrigger:
    """
    Public interface for triggering retraining workflows.
    """

    def trigger_retraining(
        self,
        **pipeline_kwargs: Any,
    ) -> dict[str, Any]:
        """
        Trigger retraining for a single model.
        """

        logger.info(
            f"Retraining requested for "
            f"{pipeline_kwargs.get('model_name')}"
        )

        return retraining_pipeline.run(
            **pipeline_kwargs,
        )

    def trigger_full_pipeline(
        self,
        pipelines: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Execute multiple retraining pipelines.
        """

        logger.info(
            "Starting full retraining pipeline."
        )

        results: list[dict[str, Any]] = []

        for pipeline in pipelines:
            results.append(
                retraining_pipeline.run(
                    **pipeline,
                )
            )

        logger.success(
            "Full retraining pipeline completed."
        )

        return results


retraining_trigger = RetrainingTrigger()