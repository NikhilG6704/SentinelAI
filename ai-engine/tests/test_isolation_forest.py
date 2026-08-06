from __future__ import annotations

import numpy as np
import pandas as pd

from anomaly_detection.isolation_forest import (
    IsolationForestDetector,
)


def sample_data() -> pd.DataFrame:
    np.random.seed(42)

    return pd.DataFrame(
        np.random.normal(size=(200, 8)),
        columns=[f"feature_{i}" for i in range(8)],
    )


def test_training():
    detector = IsolationForestDetector()

    detector.train(sample_data())

    assert detector.is_trained


def test_prediction():
    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    predictions = detector.predict(X)

    assert len(predictions) == len(X)

    assert set(predictions).issubset({0, 1})


def test_anomaly_scores():
    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    scores = detector.anomaly_score(X)

    assert len(scores) == len(X)


def test_save_load(tmp_path):
    detector = IsolationForestDetector()

    X = sample_data()

    detector.train(X)

    model_path = tmp_path / "iforest.joblib"

    detector.save(model_path)

    loaded = IsolationForestDetector()

    loaded.load(model_path)

    predictions = loaded.predict(X)

    assert len(predictions) == len(X)