from __future__ import annotations

from typing import Any

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class RCAEvaluator:
    """
    Evaluates Root Cause Analysis predictions.
    """

    def evaluate(
        self,
        y_true: list[str],
        y_pred: list[str],
    ) -> dict[str, float]:

        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0,
            ),
            "f1_score": f1_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0,
            ),
        }