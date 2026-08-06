from __future__ import annotations

import numpy as np
import pandas as pd

from failure_prediction.random_forest import (
    RandomForestFailurePredictor,
)


def sample_data():

    np.random.seed(42)

    X = pd.DataFrame(
        np.random.rand(200, 8),
    )

    y = np.random.randint(0, 2, 200)

    return X, y


def test_training():

    X, y = sample_data()

    model = RandomForestFailurePredictor()

    model.train(X, y)

    assert model.is_trained


def test_prediction():

    X, y = sample_data()

    model = RandomForestFailurePredictor()

    model.train(X, y)

    pred = model.predict(X)

    assert len(pred) == len(X)


def test_probability():

    X, y = sample_data()

    model = RandomForestFailurePredictor()

    model.train(X, y)

    proba = model.predict_proba(X)

    assert proba.shape[1] == 2


def test_save_load(tmp_path):

    X, y = sample_data()

    model = RandomForestFailurePredictor()

    model.train(X, y)

    path = tmp_path / "rf.joblib"

    model.save(path)

    loaded = RandomForestFailurePredictor()

    loaded.load(path)

    pred = loaded.predict(X)

    assert len(pred) == len(X)