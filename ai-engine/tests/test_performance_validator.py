from validation.performance_validator import performance_validator


def test_performance_validator():

    metrics = performance_validator.validate()

    assert metrics.startup_time >= 0
    assert metrics.average_load_time >= 0
    assert metrics.p95_load_time >= 0
    assert metrics.p99_load_time >= 0

    assert metrics.cpu_percent >= 0
    assert metrics.memory_percent >= 0