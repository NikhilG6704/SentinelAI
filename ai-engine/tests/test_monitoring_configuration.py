from monitoring.configuration import (
    MonitoringConfiguration,
)


def test_configuration_creation():
    config = MonitoringConfiguration()

    assert config.monitoring_name == "SentinelAI-Monitoring"


def test_supported_models():
    config = MonitoringConfiguration()

    assert config.is_supported(
        "failure_prediction"
    )

    assert config.is_supported(
        "anomaly_detection"
    )

    assert not config.is_supported(
        "invalid_model"
    )


def test_thresholds():
    config = MonitoringConfiguration()

    assert config.psi_threshold == 0.20
    assert config.js_threshold == 0.15
    assert config.ks_threshold == 0.05


def test_latency_thresholds():
    config = MonitoringConfiguration()

    assert config.max_average_latency_ms == 100.0
    assert config.max_p95_latency_ms == 200.0
    assert config.max_p99_latency_ms == 500.0


def test_resource_thresholds():
    config = MonitoringConfiguration()

    assert config.max_cpu_percent == 80.0
    assert config.max_memory_percent == 80.0


def test_directory_creation():
    config = MonitoringConfiguration()

    config.ensure_directories()

    assert config.monitoring_path.exists()
    assert config.alerts_path.exists()