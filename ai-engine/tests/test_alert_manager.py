from monitoring.alert_manager import (
    AlertManager,
    AlertSeverity,
    MonitoringAlert,
)


def test_creation():
    manager = AlertManager()

    assert manager is not None


def test_create_alert():
    manager = AlertManager()

    alert = manager.create_alert(
        source="Performance",
        severity=AlertSeverity.WARNING,
        message="Performance dropped.",
    )

    assert isinstance(
        alert,
        MonitoringAlert,
    )

    assert alert.source == "Performance"
    assert alert.severity == AlertSeverity.WARNING


def test_history():
    manager = AlertManager()

    manager.create_alert(
        source="Latency",
        severity=AlertSeverity.WARNING,
        message="High latency.",
    )

    assert len(manager.history()) == 1


def test_clear():
    manager = AlertManager()

    manager.create_alert(
        source="Resources",
        severity=AlertSeverity.CRITICAL,
        message="CPU high.",
    )

    manager.clear()

    assert manager.history() == []


def test_helper_methods():
    manager = AlertManager()

    manager.data_drift({})
    manager.concept_drift({})
    manager.performance({})
    manager.latency({})
    manager.resources({})

    assert len(manager.history()) == 5