import numpy as np

from monitoring.performance_monitor import (
    PerformanceMonitor,
    PerformanceResult,
)


def test_monitor_creation():
    monitor = PerformanceMonitor()

    assert monitor is not None


def test_perfect_prediction():
    monitor = PerformanceMonitor()

    y_true = np.array(
        [0, 1, 1, 0]
    )

    y_pred = np.array(
        [0, 1, 1, 0]
    )

    probabilities = np.array(
        [0.1, 0.9, 0.8, 0.2]
    )

    result = monitor.evaluate(
        y_true=y_true,
        y_pred=y_pred,
        probabilities=probabilities,
    )

    assert isinstance(
        result,
        PerformanceResult,
    )

    assert result.precision == 1.0
    assert result.recall == 1.0
    assert result.f1_score == 1.0
    assert result.performance_ok


def test_imperfect_prediction():
    monitor = PerformanceMonitor()

    y_true = np.array(
        [0, 1, 1, 0]
    )

    y_pred = np.array(
        [1, 0, 1, 0]
    )

    probabilities = np.array(
        [0.8, 0.2, 0.9, 0.1]
    )

    result = monitor.evaluate(
        y_true=y_true,
        y_pred=y_pred,
        probabilities=probabilities,
    )

    assert result.precision < 1.0
    assert result.recall < 1.0
    assert result.f1_score < 1.0


def test_without_probabilities():
    monitor = PerformanceMonitor()

    y_true = np.array(
        [0, 1, 1, 0]
    )

    y_pred = np.array(
        [0, 1, 1, 0]
    )

    result = monitor.evaluate(
        y_true=y_true,
        y_pred=y_pred,
    )

    assert result.roc_auc == 0.0


def test_false_rates():
    monitor = PerformanceMonitor()

    y_true = np.array(
        [0, 1, 0, 1]
    )

    y_pred = np.array(
        [1, 1, 0, 0]
    )

    result = monitor.evaluate(
        y_true=y_true,
        y_pred=y_pred,
    )

    assert 0.0 <= result.false_positive_rate <= 1.0
    assert 0.0 <= result.false_negative_rate <= 1.0


def test_result_fields():
    monitor = PerformanceMonitor()

    y_true = np.array(
        [0, 1]
    )

    y_pred = np.array(
        [0, 1]
    )

    result = monitor.evaluate(
        y_true=y_true,
        y_pred=y_pred,
    )

    assert hasattr(
        result,
        "precision",
    )

    assert hasattr(
        result,
        "recall",
    )

    assert hasattr(
        result,
        "f1_score",
    )

    assert hasattr(
        result,
        "roc_auc",
    )

    assert hasattr(
        result,
        "false_positive_rate",
    )

    assert hasattr(
        result,
        "false_negative_rate",
    )