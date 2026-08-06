from __future__ import annotations

import pandas as pd

from preprocessing.feature_engineering import FeatureEngineer


def test_cpu_features():
    """
    Verify CPU rolling features are generated.
    """

    metrics = pd.DataFrame(
        {
            "collection_timestamp": pd.date_range(
                "2026-08-01",
                periods=5,
                freq="min",
                tz="UTC",
            ),
            "cpu_usage": [10, 20, 30, 40, 50],
        }
    )

    engineer = FeatureEngineer()

    result = engineer.cpu_features(metrics)

    assert "cpu_moving_average" in result.columns
    assert "cpu_std" in result.columns


def test_memory_features():
    """
    Verify memory moving average is generated.
    """

    metrics = pd.DataFrame(
        {
            "memory_usage": [20, 30, 40, 50, 60],
        }
    )

    engineer = FeatureEngineer()

    result = engineer.memory_features(metrics)

    assert "memory_moving_average" in result.columns


def test_network_features():
    """
    Verify network features are generated.
    """

    metrics = pd.DataFrame(
        {
            "network_in": [100, 150, 200],
            "network_out": [50, 60, 70],
        }
    )

    engineer = FeatureEngineer()

    result = engineer.network_features(metrics)

    assert "network_total" in result.columns
    assert "network_utilization_trend" in result.columns


def test_alert_frequency():
    """
    Verify alert frequency is calculated correctly.
    """

    alerts = pd.DataFrame(
        {
            "infrastructure_asset_id": [1, 1, 2, 2, 2],
        }
    )

    engineer = FeatureEngineer()

    result = engineer.alert_frequency(alerts)

    assert "alert_frequency" in result.columns
    assert result["alert_frequency"].max() == 3


def test_mttr():
    """
    Verify MTTR calculation.
    """

    workflows = pd.DataFrame(
        {
            "started_at": pd.to_datetime(
                [
                    "2026-08-01T10:00:00Z",
                ]
            ),
            "completed_at": pd.to_datetime(
                [
                    "2026-08-01T10:10:00Z",
                ]
            ),
        }
    )

    engineer = FeatureEngineer()

    result = engineer.mttr(workflows)

    assert "mttr_seconds" in result.columns
    assert result["mttr_seconds"].iloc[0] == 600


def test_mtbf():
    """
    Verify MTBF calculation.
    """

    incidents = pd.DataFrame(
        {
            "infrastructure_asset_id": [1, 1],
            "detected_at": pd.to_datetime(
                [
                    "2026-08-01T10:00:00Z",
                    "2026-08-01T10:30:00Z",
                ]
            ),
        }
    )

    engineer = FeatureEngineer()

    result = engineer.mtbf(incidents)

    assert "mtbf_seconds" in result.columns
    assert result["mtbf_seconds"].iloc[1] == 1800