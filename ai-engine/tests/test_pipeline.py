from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from preprocessing.pipeline import PreprocessingPipeline


@pytest.fixture
def sample_datasets():
    """Minimal datasets required by the pipeline."""

    return {
        "assets": pd.DataFrame(
            {
                "id": [1],
                "hostname": ["server-01"],
            }
        ),
        "agents": pd.DataFrame(
            {
                "id": [1],
                "infrastructure_asset_id": [1],
                "last_heartbeat": pd.to_datetime(
                    ["2026-08-01T10:00:00Z"]
                ),
            }
        ),
        "metrics": pd.DataFrame(
            {
                "monitoring_agent_id": [1],
                "collection_timestamp": pd.to_datetime(
                    ["2026-08-01T10:00:00Z"]
                ),
                "cpu_usage": [50],
                "memory_usage": [60],
                "disk_usage": [70],
                "network_in": [100],
                "network_out": [150],
            }
        ),
        "alerts": pd.DataFrame(
            {
                "infrastructure_asset_id": [1],
            }
        ),
        "incidents": pd.DataFrame(
            {
                "infrastructure_asset_id": [1],
                "detected_at": pd.to_datetime(
                    ["2026-08-01T10:00:00Z"]
                ),
            }
        ),
        "logs": pd.DataFrame(
            {
                "infrastructure_asset_id": [1],
                "log_level": ["ERROR"],
            }
        ),
        "workflows": pd.DataFrame(
            {
                "started_at": pd.to_datetime(
                    ["2026-08-01T10:00:00Z"]
                ),
                "completed_at": pd.to_datetime(
                    ["2026-08-01T10:05:00Z"]
                ),
            }
        ),
        "audit_logs": pd.DataFrame(),
    }


def test_clean_data(sample_datasets):
    pipeline = PreprocessingPipeline()

    cleaned = pipeline.clean_data(sample_datasets)

    assert isinstance(cleaned, dict)
    assert "metrics" in cleaned


def test_feature_engineering(sample_datasets):
    pipeline = PreprocessingPipeline()

    features = pipeline.engineer_features(sample_datasets)

    assert "metrics" in features
    assert "cpu_moving_average" in features["metrics"].columns


def test_normalization(sample_datasets):
    pipeline = PreprocessingPipeline()

    engineered = pipeline.engineer_features(sample_datasets)

    sample_datasets.update(engineered)

    normalized = pipeline.normalize(sample_datasets)

    assert "metrics" in normalized


def test_export(tmp_path: Path):
    pipeline = PreprocessingPipeline()

    df = pd.DataFrame(
        {
            "cpu_usage": [10, 20],
        }
    )

    pipeline.export_dataset(
        df=df,
        output_dir=tmp_path,
        filename="metrics",
    )

    csv_exists = (tmp_path / "metrics.csv").exists()
    parquet_exists = (tmp_path / "metrics.parquet").exists()

    assert csv_exists or parquet_exists