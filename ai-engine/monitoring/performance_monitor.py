"""
Performance monitoring for SentinelAI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from monitoring.configuration import monitoring_config
from utils.logger import logger


@dataclass(frozen=True)
class PerformanceResult:
    """
    Performance monitoring result.
    """

    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    false_positive_rate: float
    false_negative_rate: float

    performance_ok: bool


class PerformanceMonitor:
    """
    Monitors deployed model performance.
    """

    def evaluate(
        self,
        *,
        y_true: Any,
        y_pred: Any,
        probabilities: Any | None = None,
    ) -> PerformanceResult:

        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)

        precision = precision_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        f1 = f1_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        roc_auc = 0.0

        if probabilities is not None:
            try:
                roc_auc = roc_auc_score(
                    y_true,
                    probabilities,
                )
            except Exception:
                roc_auc = 0.0

        tn, fp, fn, tp = confusion_matrix(
            y_true,
            y_pred,
            labels=[0, 1],
        ).ravel()

        fpr = fp / (fp + tn) if (fp + tn) else 0.0
        fnr = fn / (fn + tp) if (fn + tp) else 0.0

        performance_ok = (
            precision >= monitoring_config.minimum_precision
            and recall >= monitoring_config.minimum_recall
            and f1 >= monitoring_config.minimum_f1
            and (
                roc_auc == 0.0
                or roc_auc >= monitoring_config.minimum_roc_auc
            )
        )

        result = PerformanceResult(
            precision=precision,
            recall=recall,
            f1_score=f1,
            roc_auc=roc_auc,
            false_positive_rate=fpr,
            false_negative_rate=fnr,
            performance_ok=performance_ok,
        )

        logger.info(
            f"Performance OK={result.performance_ok}"
        )

        return result


performance_monitor = PerformanceMonitor()