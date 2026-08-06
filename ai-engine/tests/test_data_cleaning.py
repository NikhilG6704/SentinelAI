from __future__ import annotations

import pandas as pd

from preprocessing.data_cleaning import DataCleaner


def test_remove_duplicates():
    df = pd.DataFrame(
        {
            "cpu_usage": [20, 20, 50],
            "memory_usage": [40, 40, 60],
        }
    )

    cleaned = DataCleaner.remove_duplicates(df)

    assert len(cleaned) == 2


def test_clip_percentage_columns():
    df = pd.DataFrame(
        {
            "cpu_usage": [120, -10, 50],
            "memory_usage": [130, 25, -5],
            "disk_usage": [150, 75, -20],
        }
    )

    cleaned = DataCleaner.clip_percentage_columns(
        df,
        [
            "cpu_usage",
            "memory_usage",
            "disk_usage",
        ],
    )

    assert cleaned["cpu_usage"].max() <= 100
    assert cleaned["cpu_usage"].min() >= 0

    assert cleaned["memory_usage"].max() <= 100
    assert cleaned["memory_usage"].min() >= 0

    assert cleaned["disk_usage"].max() <= 100
    assert cleaned["disk_usage"].min() >= 0


def test_fill_missing_numeric():
    df = pd.DataFrame(
        {
            "cpu_usage": [10, None, 30],
        }
    )

    cleaned = DataCleaner.fill_missing_numeric(df)

    assert cleaned["cpu_usage"].isna().sum() == 0