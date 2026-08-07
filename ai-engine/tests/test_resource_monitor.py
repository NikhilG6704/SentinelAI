from unittest.mock import MagicMock

from monitoring.resource_monitor import (
    ResourceMonitor,
    ResourceResult,
)


def test_monitor_creation():
    monitor = ResourceMonitor()

    assert monitor is not None


def test_evaluate():
    monitor = ResourceMonitor()

    result = monitor.evaluate()

    assert isinstance(
        result,
        ResourceResult,
    )

    assert result.cpu_percent >= 0
    assert result.memory_percent >= 0
    assert result.process_memory_mb >= 0


def test_model_load_measurement():
    monitor = ResourceMonitor()

    loader = MagicMock(
        return_value="model"
    )

    model, elapsed = monitor.measure_model_load(
        loader
    )

    assert model == "model"
    assert elapsed >= 0

    loader.assert_called_once()