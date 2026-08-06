from __future__ import annotations

import numpy as np
import pandas as pd

from anomaly_detection.evaluator import ModelEvaluator
from anomaly_detection.isolation_forest import (
    IsolationForestDetector,
)


def sample_data() -> pd.DataFrame:
    np.random.seed(42)

    return pd.DataFrame(
        np.random.normal(size=(200, 8)),
        columns=[f"feature_{i}" for i in range(8)],
    )


def sample_labels() -> np.ndarray:
    """
    Synthetic labels for testing.

    0 -> Normal
    1 -> Anomaly
    """

    labels = np.zeros(200, dtype=int)

    labels[-20:] = 1

    return labels


def test_evaluation():
    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    evaluator = ModelEvaluator(detector)

    result = evaluator.evaluate(
        X,
        sample_labels(),
    )

    assert "precision" in result
    assert "recall" in result
    assert "f1_score" in result
    assert "inference_latency_ms" in result
    assert "memory_usage_mb" in result


def test_comparison_report():
    report = ModelEvaluator.comparison_report(
        [
            {
                "model": "IsolationForest",
                "f1_score": 0.82,
            },
            {
                "model": "Autoencoder",
                "f1_score": 0.91,
            },
        ]
    )

    assert len(report) == 2

    assert "model" in report.columns

    assert "f1_score" in report.columns