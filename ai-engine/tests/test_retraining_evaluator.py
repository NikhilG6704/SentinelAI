from unittest.mock import MagicMock

import numpy as np
import pytest

from retraining.evaluator import RetrainingEvaluator


@pytest.fixture
def evaluator():
    return RetrainingEvaluator()


@pytest.fixture
def model():
    m = MagicMock()

    m.predict.return_value = np.array(
        [0, 1, 1, 0]
    )

    m.predict_proba.return_value = np.array(
        [
            [0.9, 0.1],
            [0.1, 0.9],
            [0.2, 0.8],
            [0.8, 0.2],
        ]
    )

    return m


@pytest.fixture
def X():
    return np.random.rand(4, 3)


@pytest.fixture
def y():
    return np.array(
        [0, 1, 1, 0]
    )


def test_evaluate(
    evaluator,
    model,
    X,
    y,
):
    metrics = evaluator.evaluate(
        model_name="failure_prediction",
        model=model,
        X_test=X,
        y_test=y,
    )

    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1_score"] == 1.0
    assert "roc_auc" in metrics
    assert "inference_latency" in metrics


def test_invalid_model(
    evaluator,
    model,
    X,
    y,
):
    with pytest.raises(ValueError):
        evaluator.evaluate(
            model_name="invalid",
            model=model,
            X_test=X,
            y_test=y,
        )


def test_without_predict_proba(
    evaluator,
    X,
    y,
):
    class DummyModel:

        def predict(self, X):
            return np.array(
                [0, 1, 1, 0]
            )

    metrics = evaluator.evaluate(
        model_name="failure_prediction",
        model=DummyModel(),
        X_test=X,
        y_test=y,
    )

    assert "roc_auc" not in metrics