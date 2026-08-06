from __future__ import annotations

import pandas as pd

from preprocessing.normalization import Normalizer


def test_standard_scaler():
    """
    Verify StandardScaler normalizes numeric columns.
    """

    df = pd.DataFrame(
        {
            "cpu_usage": [10, 20, 30, 40, 50],
            "memory_usage": [50, 40, 30, 20, 10],
        }
    )

    normalizer = Normalizer(method="standard")

    result = normalizer.fit_transform(
        df,
        ["cpu_usage", "memory_usage"],
    )

    # Mean should be approximately zero
    assert abs(result["cpu_usage"].mean()) < 1e-9
    assert abs(result["memory_usage"].mean()) < 1e-9


def test_minmax_scaler():
    """
    Verify MinMaxScaler scales values to [0, 1].
    """

    df = pd.DataFrame(
        {
            "cpu_usage": [10, 20, 30, 40, 50],
        }
    )

    normalizer = Normalizer(method="minmax")

    result = normalizer.fit_transform(
        df,
        ["cpu_usage"],
    )

    assert result["cpu_usage"].min() == 0.0
    assert result["cpu_usage"].max() == 1.0


def test_inverse_transform():
    """
    Verify inverse transformation restores original values.
    """

    original = pd.DataFrame(
        {
            "cpu_usage": [10.0, 20.0, 30.0],
        }
    )

    normalizer = Normalizer()

    scaled = normalizer.fit_transform(
        original.copy(),
        ["cpu_usage"],
    )

    restored = normalizer.inverse_transform(
        scaled.copy(),
        ["cpu_usage"],
    )

    pd.testing.assert_series_equal(
        original["cpu_usage"],
        restored["cpu_usage"],
        check_names=False,
    )


def test_missing_columns():
    """
    Missing columns should not raise errors.
    """

    df = pd.DataFrame(
        {
            "cpu_usage": [10, 20],
        }
    )

    normalizer = Normalizer()

    result = normalizer.fit_transform(
        df,
        ["memory_usage"],
    )

    assert "cpu_usage" in result.columns
    assert "memory_usage" not in result.columns