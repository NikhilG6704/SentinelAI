from unittest.mock import MagicMock, patch

from monitoring.monitoring_manager import MonitoringManager


@patch("monitoring.monitoring_manager.report_generator")
@patch("monitoring.monitoring_manager.resource_monitor")
@patch("monitoring.monitoring_manager.latency_monitor")
@patch("monitoring.monitoring_manager.performance_monitor")
@patch("monitoring.monitoring_manager.concept_drift_detector")
@patch("monitoring.monitoring_manager.data_drift_detector")
def test_monitor(
    mock_data,
    mock_concept,
    mock_perf,
    mock_latency,
    mock_resource,
    mock_report,
):
    mock_data.detect.return_value = MagicMock(
        drift_detected=False,
    )

    mock_concept.detect.return_value = MagicMock(
        drift_detected=False,
    )

    mock_perf.evaluate.return_value = MagicMock(
        performance_ok=True,
    )

    mock_latency.evaluate.return_value = MagicMock(
        latency_ok=True,
    )

    mock_resource.evaluate.return_value = MagicMock(
        resources_ok=True,
    )

    mock_report.generate.return_value = {}
    mock_report.save.return_value = "report.json"

    manager = MonitoringManager()

    result = manager.monitor(
        model_name="failure_prediction",
        reference_data=[],
        current_data=[],
        previous_predictions=[],
        current_predictions=[],
        previous_confidence=[],
        current_confidence=[],
        previous_labels=[],
        current_labels=[],
        y_true=[],
        y_pred=[],
        probabilities=[],
        latencies_ms=[],
    )

    assert "report" in result