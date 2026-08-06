from __future__ import annotations

import pandas as pd

from failure_prediction.label_generator import LabelGenerator


def sample_dataset() -> pd.DataFrame:
    """
    Create a small synthetic dataset for label generation.
    """

    return pd.DataFrame(
        {
            "infrastructure_asset_id": [1, 1, 1, 2],
            "collection_timestamp": [
                "2026-08-06T10:00:00Z",
                "2026-08-06T10:10:00Z",
                "2026-08-06T10:40:00Z",
                "2026-08-06T10:00:00Z",
            ],
            "detected_at": [
                "2026-08-06T10:20:00Z",
                "2026-08-06T10:20:00Z",
                None,
                None,
            ],
        }
    )


def test_label_generation():
    """
    Verify labels are generated correctly.
    """

    generator = LabelGenerator(
        prediction_window_minutes=30,
    )

    dataset = generator.generate(
        sample_dataset(),
    )

    assert "failure_label" in dataset.columns

    assert dataset["failure_label"].sum() == 2


def test_class_distribution():
    """
    Verify class distribution is returned.
    """

    generator = LabelGenerator()

    dataset = generator.generate(
        sample_dataset(),
    )

    distribution = generator.class_distribution(
        dataset,
    )

    assert "label" in distribution.columns

    assert "count" in distribution.columns

    assert "percentage" in distribution.columns


def test_missing_columns():
    """
    Missing required columns should raise ValueError.
    """

    generator = LabelGenerator()

    invalid = pd.DataFrame(
        {
            "cpu": [1, 2, 3],
        }
    )

    try:
        generator.generate(invalid)
        assert False
    except ValueError:
        assert True