"""
Automated retraining pipeline for SentinelAI.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from retraining.comparison import model_comparison
from retraining.dataset_versioning import dataset_version_manager
from retraining.evaluator import retraining_evaluator
from retraining.promotion_manager import promotion_manager
from retraining.retraining_manager import retraining_manager
from utils.logger import logger


class RetrainingPipeline:
    """
    End-to-end automated retraining pipeline.
    """

    def run(
        self,
        *,
        model_name: str,
        trainer: Any,
        model: Any,
        dataset: pd.DataFrame,
        X_train: Any,
        y_train: Any,
        X_test: Any,
        y_test: Any,
        current_metrics: dict[str, float],
    ) -> dict[str, Any]:
        """
        Execute the complete retraining workflow.
        """

        logger.info(
            f"Starting retraining pipeline for '{model_name}'."
        )

        # ----------------------------------------------------------
        # Dataset Versioning
        # ----------------------------------------------------------

        dataset_version = dataset_version_manager.create_version(
            dataset,
            dataset_name=model_name,
        )

        # ----------------------------------------------------------
        # Retraining
        # ----------------------------------------------------------

        training_result = retraining_manager.retrain(
            model_name=model_name,
            trainer=trainer,
            train_args=(X_train, y_train),
            dataset_version=dataset_version.version,
        )

        # ----------------------------------------------------------
        # Evaluation
        # ----------------------------------------------------------

        candidate_metrics = retraining_evaluator.evaluate(
            model_name=model_name,
            model=model,
            X_test=X_test,
            y_test=y_test,
        )

        candidate_metrics["training_time"] = training_result[
            "training_time"
        ]

        # ----------------------------------------------------------
        # Comparison
        # ----------------------------------------------------------

        comparison = model_comparison.compare(
            current=current_metrics,
            candidate=candidate_metrics,
        )

        # ----------------------------------------------------------
        # Promotion Decision
        # ----------------------------------------------------------

        decision = promotion_manager.should_promote(
            comparison
        )

        logger.success(
            f"Retraining pipeline completed for '{model_name}'."
        )

        return {
            "dataset_version": dataset_version.version,
            "training": training_result,
            "candidate_metrics": candidate_metrics,
            "comparison": comparison,
            "promotion": decision,
        }


retraining_pipeline = RetrainingPipeline()