from unittest.mock import patch

from monitoring.trigger import MonitoringTrigger


def test_creation():
    trigger = MonitoringTrigger()

    assert trigger is not None


@patch("monitoring.trigger.monitoring_manager")
def test_run(
    mock_manager,
):
    mock_manager.monitor.return_value = {
        "status": "ok",
    }

    trigger = MonitoringTrigger()

    result = trigger.run_monitoring()

    assert result["status"] == "ok"


@patch("monitoring.trigger.monitoring_manager")
def test_retraining(
    mock_manager,
):
    mock_manager.trigger_retraining_if_required.return_value = {
        "status": "triggered",
    }

    trigger = MonitoringTrigger()

    result = trigger.trigger_retraining_if_required(
        monitoring_result={
            "retraining_required": True,
        },
    )

    assert result["status"] == "triggered"


def test_status():
    trigger = MonitoringTrigger()

    assert trigger.check_monitoring_status(
        {
            "retraining_required": True,
        }
    )

    assert not trigger.check_monitoring_status(
        {}
    )