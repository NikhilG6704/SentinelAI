from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class CorrelationResult:
    source: str
    target: str
    correlation_score: float
    evidence_type: str


class CorrelationEngine:
    """
    Correlates infrastructure signals such as metrics,
    alerts, incidents, logs, and AI predictions.
    """

    def __init__(self) -> None:
        self.results: list[CorrelationResult] = []

    @staticmethod
    def _numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        return df.select_dtypes(include=[np.number])

    def correlate_metrics(
        self,
        metrics: pd.DataFrame,
        threshold: float = 0.7,
    ) -> list[CorrelationResult]:

        self.results.clear()

        metrics = self._numeric_columns(metrics)

        corr = metrics.corr(method="pearson")

        columns = corr.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                score = corr.iloc[i, j]

                if abs(score) >= threshold:

                    self.results.append(
                        CorrelationResult(
                            source=columns[i],
                            target=columns[j],
                            correlation_score=float(score),
                            evidence_type="metric",
                        )
                    )

        return self.results

    def correlate_alerts(
        self,
        alerts: pd.DataFrame,
    ) -> dict[str, int]:

        if "alert_type" not in alerts.columns:
            return {}

        return alerts["alert_type"].value_counts().to_dict()

    def correlate_incidents(
        self,
        incidents: pd.DataFrame,
    ) -> dict[str, int]:

        if "severity" not in incidents.columns:
            return {}

        return incidents["severity"].value_counts().to_dict()

    def correlate_predictions(
        self,
        predictions: pd.DataFrame,
    ) -> dict[str, float]:

        if "failure_probability" not in predictions.columns:
            return {}

        return {
            "average_failure_probability":
                float(predictions["failure_probability"].mean()),
            "maximum_failure_probability":
                float(predictions["failure_probability"].max()),
        }

    def summarize(
        self,
    ) -> dict[str, Any]:

        return {
            "total_correlations": len(self.results),
            "results": self.results,
        }