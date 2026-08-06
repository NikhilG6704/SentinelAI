from __future__ import annotations

import numpy as np
import pandas as pd

from anomaly_detection.inference import InferenceEngine
from anomaly_detection.isolation_forest import (
    IsolationForestDetector,
)


def sample_data() -> pd.DataFrame:
    np.random.seed(42)

    return pd.DataFrame(
        np.random.normal(size=(100, 8)),
        columns=[f"feature_{i}" for i in range(8)],
    )


def test_inference_output():
    """
    Verify inference output format.
    """

    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    engine = InferenceEngine(detector)

    results = engine.predict(X)

    assert len(results) == len(X)

    first = results[0]

    expected_keys = {
        "status",
        "prediction",
        "confidence",
        "anomaly_score",
        "model_used",
        "timestamp",
    }

    assert expected_keys.issubset(first.keys())


def test_prediction_values():
    """
    Prediction values should follow
    SentinelAI conventions.
    """

    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    engine = InferenceEngine(detector)

    results = engine.predict(X)

    for result in results:

        assert result["prediction"] in (0, 1)

        assert result["status"] in (
            "Normal",
            "Anomaly",
        )


def test_confidence_range():
    """
    Confidence must always lie in [0, 1].
    """

    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    engine = InferenceEngine(detector)

    results = engine.predict(X)

    for result in results:

        assert 0.0 <= result["confidence"] <= 1.0


def test_model_name():
    """
    Returned model name should match detector.
    """

    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    engine = InferenceEngine(detector)

    result = engine.predict(X)[0]

    assert (
        result["model_used"]
        == "IsolationForestDetector"
    )