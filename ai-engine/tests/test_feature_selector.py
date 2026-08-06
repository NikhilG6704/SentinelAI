from __future__ import annotations

import numpy as np
import pandas as pd

from failure_prediction.feature_selector import FeatureSelector


def sample_data():
    np.random.seed(42)

    X = pd.DataFrame(
        np.random.rand(200, 10),
        columns=[f"feature_{i}" for i in range(10)],
    )

    y = np.random.randint(0, 2, size=200)

    return X, y


def test_feature_selection():

    X, y = sample_data()

    selector = FeatureSelector()

    selector.fit(X, y)

    top = selector.top_features(5)

    assert len(top) == 5

    reduced = selector.transform(X, 5)

    assert reduced.shape[1] == 5


def test_feature_report():

    X, y = sample_data()

    selector = FeatureSelector()

    selector.fit(X, y)

    report = selector.feature_report()

    assert "feature" in report.columns

    assert "importance" in report.columns