from __future__ import annotations

from anomaly_detection.model_selector import ModelSelector


def test_select_best_using_f1():
    """
    Verify the selector chooses the model with
    the highest F1-score.
    """

    selector = ModelSelector()

    evaluations = [
        {
            "model": "IsolationForestDetector",
            "f1_score": 0.87,
            "inference_latency_ms": 3.2,
        },
        {
            "model": "AutoencoderDetector",
            "f1_score": 0.92,
            "inference_latency_ms": 5.6,
        },
    ]

    best = selector.select_best(evaluations)

    assert best["model"] == "AutoencoderDetector"


def test_latency_fallback():
    """
    If the primary metric is unavailable,
    choose the model with the lowest latency.
    """

    selector = ModelSelector()

    evaluations = [
        {
            "model": "IsolationForestDetector",
            "inference_latency_ms": 2.4,
        },
        {
            "model": "AutoencoderDetector",
            "inference_latency_ms": 5.7,
        },
    ]

    best = selector.select_best(evaluations)

    assert best["model"] == "IsolationForestDetector"


def test_model_ranking():
    """
    Verify models are ranked in descending order
    of the primary metric.
    """

    selector = ModelSelector()

    evaluations = [
        {
            "model": "IsolationForestDetector",
            "f1_score": 0.81,
        },
        {
            "model": "AutoencoderDetector",
            "f1_score": 0.95,
        },
        {
            "model": "FutureDetector",
            "f1_score": 0.88,
        },
    ]

    ranking = selector.ranking(evaluations)

    assert ranking[0]["model"] == "AutoencoderDetector"
    assert ranking[1]["model"] == "FutureDetector"
    assert ranking[2]["model"] == "IsolationForestDetector"


def test_empty_evaluations():
    """
    Empty evaluation lists should raise an error.
    """

    selector = ModelSelector()

    try:
        selector.select_best([])
        assert False
    except ValueError:
        assert True