from pathlib import Path

from monitoring.alert_manager import (
    AlertSeverity,
    MonitoringAlert,
)
from monitoring.concept_drift import ConceptDriftResult
from monitoring.data_drift import DriftResult
from monitoring.latency_monitor import LatencyResult
from monitoring.performance_monitor import PerformanceResult
from monitoring.report_generator import ReportGenerator
from monitoring.resource_monitor import ResourceResult


def sample_report():
    generator = ReportGenerator()

    report = generator.generate(
        model_name="failure_prediction",
        data_drift=DriftResult(
            0.1, 0.1, 0.1, 0.5,
            False, False, False,
        ),
        concept_drift=ConceptDriftResult(
            0.0, 0.0, 0.0,
            False, False, False,
        ),
        performance=PerformanceResult(
            1, 1, 1, 1,
            0, 0, True,
        ),
        latency=LatencyResult(
            10, 10, 10, 10, 10,
            True,
        ),
        resources=ResourceResult(
            10, 10, 100, 5,
            True,
        ),
        alerts=[
            MonitoringAlert(
                "Performance",
                AlertSeverity.INFO,
                "OK",
                "now",
                {},
            )
        ],
    )

    return generator, report


def test_generate():
    _, report = sample_report()

    assert report["model"] == "failure_prediction"


def test_save():
    generator, report = sample_report()

    path = generator.save(report)

    assert isinstance(path, Path)
    assert path.exists()