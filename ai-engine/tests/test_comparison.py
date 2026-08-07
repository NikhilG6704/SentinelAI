from retraining.comparison import (
    ComparisonResult,
    ModelComparison,
)


def current_metrics():
    return {
        "precision": 0.90,
        "recall": 0.88,
        "f1_score": 0.89,
        "roc_auc": 0.94,
        "training_time": 15.0,
        "inference_latency": 0.010,
    }


def better_metrics():
    return {
        "precision": 0.92,
        "recall": 0.91,
        "f1_score": 0.915,
        "roc_auc": 0.96,
        "training_time": 14.5,
        "inference_latency": 0.009,
    }


def worse_metrics():
    return {
        "precision": 0.85,
        "recall": 0.80,
        "f1_score": 0.82,
        "roc_auc": 0.88,
        "training_time": 20.0,
        "inference_latency": 0.020,
    }


def test_compare_improved():
    comparison = ModelComparison()

    result = comparison.compare(
        current=current_metrics(),
        candidate=better_metrics(),
    )

    assert isinstance(
        result,
        ComparisonResult,
    )

    assert result.improved


def test_compare_not_improved():
    comparison = ModelComparison()

    result = comparison.compare(
        current=current_metrics(),
        candidate=worse_metrics(),
    )

    assert not result.improved


def test_metric_changes():
    comparison = ModelComparison()

    result = comparison.compare(
        current=current_metrics(),
        candidate=better_metrics(),
    )

    assert "precision" in result.metric_changes
    assert "recall" in result.metric_changes
    assert "f1_score" in result.metric_changes
    assert "roc_auc" in result.metric_changes
    assert "training_time" in result.metric_changes
    assert "inference_latency" in result.metric_changes


def test_current_metrics():
    comparison = ModelComparison()

    result = comparison.compare(
        current=current_metrics(),
        candidate=better_metrics(),
    )

    assert result.current_metrics == current_metrics()


def test_candidate_metrics():
    comparison = ModelComparison()

    result = comparison.compare(
        current=current_metrics(),
        candidate=better_metrics(),
    )

    assert result.candidate_metrics == better_metrics()