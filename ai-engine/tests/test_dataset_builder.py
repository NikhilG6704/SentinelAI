from __future__ import annotations

import pandas as pd

from failure_prediction.dataset_builder import DatasetBuilder


def test_dataset_builder(tmp_path):
    """
    Verify feature and incident datasets are merged correctly.
    """

    features = pd.DataFrame(
        {
            "infrastructure_asset_id": [1, 2],
            "collection_timestamp": [
                "2026-08-06T10:00:00Z",
                "2026-08-06T10:05:00Z",
            ],
            "cpu_usage": [60.2, 75.8],
        }
    )

    incidents = pd.DataFrame(
        {
            "infrastructure_asset_id": [1],
            "detected_at": [
                "2026-08-06T10:20:00Z",
            ],
        }
    )

    feature_file = tmp_path / "features.csv"
    incident_file = tmp_path / "incidents.csv"

    features.to_csv(feature_file, index=False)
    incidents.to_csv(incident_file, index=False)

    builder = DatasetBuilder(
        feature_path=feature_file,
        incident_path=incident_file,
    )

    dataset = builder.build()

    assert len(dataset) == 2

    assert "cpu_usage" in dataset.columns

    assert "detected_at" in dataset.columns


def test_dataset_export(tmp_path):
    """
    Verify dataset export works.
    """

    df = pd.DataFrame(
        {
            "a": [1, 2],
            "b": [3, 4],
        }
    )

    builder = DatasetBuilder(
        feature_path="dummy.csv",
        incident_path="dummy.csv",
    )

    output = tmp_path / "dataset.csv"

    builder.save(df, output)

    assert output.exists()