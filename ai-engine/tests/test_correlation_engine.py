from __future__ import annotations

import numpy as np
import pandas as pd

from root_cause_analysis.correlation_engine import (
    CorrelationEngine,
)


def sample_metrics() -> pd.DataFrame:

    np.random.seed(42)

    cpu = np.random.normal(70, 5, 100)

    memory = cpu * 0.9 + np.random.normal(0, 1, 100)

    disk = np.random.normal(40, 10, 100)

    return pd.DataFrame(
        {
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
        }
    )


def sample_alerts() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "alert_type": [
                "CPU",
                "CPU",
                "Memory",
                "Disk",
                "CPU",
            ]
        }
    )


def sample_incidents() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "severity": [
                "High",
                "Medium",
                "High",
                "Critical",
                "High",
            ]
        }
    )


def sample_predictions() -> pd.DataFrame:

    return pd.DataFrame(
        {
            "failure_probability": [
                0.15,
                0.65,
                0.82,
                0.91,
            ]
        }
    )


def test_metric_correlation():

    engine = CorrelationEngine()

    results = engine.correlate_metrics(
        sample_metrics(),
        threshold=0.8,
    )

    assert len(results) >= 1

    assert any(
        {
            r.source,
            r.target,
        }
        == {
            "cpu",
            "memory",
        }
        for r in results
    )


def test_alert_correlation():

    engine = CorrelationEngine()

    result = engine.correlate_alerts(
        sample_alerts()
    )

    assert result["CPU"] == 3

    assert result["Memory"] == 1


def test_incident_correlation():

    engine = CorrelationEngine()

    result = engine.correlate_incidents(
        sample_incidents()
    )

    assert result["High"] == 3

    assert result["Critical"] == 1


def test_prediction_correlation():

    engine = CorrelationEngine()

    result = engine.correlate_predictions(
        sample_predictions()
    )

    assert result[
        "maximum_failure_probability"
    ] == 0.91

    assert (
        result[
            "average_failure_probability"
        ]
        > 0.5
    )


def test_summary():

    engine = CorrelationEngine()

    engine.correlate_metrics(
        sample_metrics()
    )

    summary = engine.summarize()

    assert "results" in summary

    assert "total_correlations" in summary

    assert summary["total_correlations"] >= 1
