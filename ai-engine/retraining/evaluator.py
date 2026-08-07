"""
Unified model evaluator for the SentinelAI retraining pipeline.
"""

from __future__ import annotations

import time
from typing import Any

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from retraining.configuration import retraining_config
from utils.logger import logger


class RetrainingEvaluator:
    """
    Evaluates newly trained models using a common interface.
    """

    def evaluate(
        self,
        model_name: str,
        model: Any,
        X_test: Any,
        y_test: Any,
    ) -> dict[str, float]:

        if not retraining_config.is_supported(model_name):
            raise ValueError(
                f"Unsupported model '{model_name}'."
            )

        start = time.perf_counter()

        predictions = model.predict(X_test)

        latency = (
            time.perf_counter() - start
        ) / max(len(predictions), 1)

        metrics = {
            "accuracy": accuracy_score(
                y_test,
                predictions,
            ),
            "precision": precision_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "f1_score": f1_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "inference_latency": latency,
        }

        if hasattr(
            model,
            "predict_proba",
        ):
            try:
                probabilities = model.predict_proba(
                    X_test
                )[:, 1]

                metrics["roc_auc"] = roc_auc_score(
                    y_test,
                    probabilities,
                )

            except Exception:
                pass

        logger.success(
            f"Evaluation completed for '{model_name}'."
        )

        return metrics


retraining_evaluator = RetrainingEvaluator()