import numpy as np

from monitoring.latency_monitor import (
    LatencyMonitor,
    LatencyResult,
)


def test_monitor_creation():
    monitor = LatencyMonitor()

    assert monitor is not None


def test_latency_statistics():
    monitor = LatencyMonitor()

    latencies = np.array(
        [50, 60, 70, 80, 90]
    )

    result = monitor.evaluate(
        latencies
    )

    assert isinstance(
        result,
        LatencyResult,
    )

    assert result.average_ms == np.mean(
        latencies
    )

    assert result.median_ms == np.median(
        latencies
    )


def test_percentiles():
    monitor = LatencyMonitor()

    latencies = np.arange(
        1,
        101,
    )

    result = monitor.evaluate(
        latencies
    )

    assert result.p95_ms >= result.average_ms
    assert result.p99_ms >= result.p95_ms


def test_maximum():
    monitor = LatencyMonitor()

    latencies = np.array(
        [10, 20, 30, 999]
    )

    result = monitor.evaluate(
        latencies
    )

    assert result.maximum_ms == 999


def test_latency_ok():
    monitor = LatencyMonitor()

    latencies = np.array(
        [10, 20, 30]
    )

    result = monitor.evaluate(
        latencies
    )

    assert result.latency_ok


def test_latency_not_ok():
    monitor = LatencyMonitor()

    latencies = np.array(
        [600, 700, 800]
    )

    result = monitor.evaluate(
        latencies
    )

    assert not result.latency_ok