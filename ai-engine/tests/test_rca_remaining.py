from unittest.mock import MagicMock, patch

from root_cause_analysis.evaluator import RCAEvaluator
from root_cause_analysis.model_selector import RCAModelSelector
from root_cause_analysis.trainer import RCATrainer


def test_evaluator():

    evaluator = RCAEvaluator()

    metrics = evaluator.evaluate(
        ["CPU", "Memory", "CPU"],
        ["CPU", "Memory", "Memory"],
    )

    assert "accuracy" in metrics
    assert "f1_score" in metrics


@patch("root_cause_analysis.trainer.ExperimentTracker")
def test_trainer(mock_tracker):

    tracker_instance = MagicMock()
    tracker_instance.run_id = "test_run"

    mock_tracker.return_value = tracker_instance

    trainer = RCATrainer()

    result = trainer.train([])

    assert trainer.is_trained

    assert result["model_name"] == "RootCauseModel"
    assert "training_time_seconds" in result
    assert "run_id" in result

    mock_tracker.assert_called_once()

    tracker_instance.__enter__.assert_called_once()
    tracker_instance.__exit__.assert_called_once()


def test_model_selector():

    selector = RCAModelSelector()

    model = selector.select(
        [
            "rule_based",
            "graph_based",
        ]
    )

    assert model == "rule_based"