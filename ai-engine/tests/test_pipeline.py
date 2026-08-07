from unittest.mock import MagicMock, patch

from retraining.pipeline import RetrainingPipeline


@patch("retraining.pipeline.promotion_manager")
@patch("retraining.pipeline.model_comparison")
@patch("retraining.pipeline.retraining_evaluator")
@patch("retraining.pipeline.retraining_manager")
@patch("retraining.pipeline.dataset_version_manager")
def test_pipeline(
    mock_version,
    mock_manager,
    mock_evaluator,
    mock_comparison,
    mock_promotion,
):
    version = MagicMock()
    version.version = "v1"

    mock_version.create_version.return_value = version

    mock_manager.retrain.return_value = {
        "training_time": 10.0
    }

    mock_evaluator.evaluate.return_value = {
        "precision": 0.95,
        "recall": 0.94,
        "f1_score": 0.95,
        "roc_auc": 0.98,
        "inference_latency": 0.01,
    }

    comparison = MagicMock()
    comparison.improved = True

    mock_comparison.compare.return_value = comparison

    promotion = MagicMock()
    promotion.promote = True

    mock_promotion.should_promote.return_value = promotion

    pipeline = RetrainingPipeline()

    result = pipeline.run(
        model_name="failure_prediction",
        trainer=MagicMock(),
        model=MagicMock(),
        dataset=MagicMock(),
        X_train=[],
        y_train=[],
        X_test=[],
        y_test=[],
        current_metrics={},
    )

    assert result["dataset_version"] == "v1"
    assert result["promotion"] == promotion


def test_pipeline_creation():
    pipeline = RetrainingPipeline()

    assert pipeline is not None