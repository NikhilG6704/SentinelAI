from __future__ import annotations

import numpy as np
import pandas as pd

from failure_prediction.evaluator import (
    FailurePredictionEvaluator,
)
from failure_prediction.random_forest import (
    RandomForestFailurePredictor,
)


def sample_data():

    np.random.seed(42)

    X = pd.DataFrame(
        np.random.rand(300, 10),
    )

    y = np.random.randint(0, 2, 300)

    return X, y


def test_evaluation():

    X, y = sample_data()

    model = RandomForestFailurePredictor()

    model.train(X, y)

    evaluator = FailurePredictionEvaluator(model)

    result = evaluator.evaluate(X, y)

    assert "precision" in result

    assert "recall" in result

    assert "f1_score" in result

    assert "roc_auc" in result

    assert "pr_auc" in result


def test_report():

    report = FailurePredictionEvaluator.comparison_report(
        [
            {
                "model": "RF",
                "f1_score": 0.9,
            },
            {
                "model": "XGB",
                "f1_score": 0.94,
            },
        ]
    )

    assert len(report) == 2