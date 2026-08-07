from unittest.mock import MagicMock, patch

import pytest

from retraining.retraining_manager import RetrainingManager


@pytest.fixture
def manager():
    return RetrainingManager()


@pytest.fixture
def trainer():
    trainer = MagicMock()

    trainer.train.return_value = {
        "model_path": "models/random_forest.joblib",
        "accuracy": 0.95,
        "f1_score": 0.94,
    }

    return trainer


@patch("retraining.retraining_manager.model_registry")
@patch("retraining.retraining_manager.ExperimentTracker")
def test_retrain(
    mock_tracker,
    mock_registry,
    manager,
    trainer,
):
    tracker = MagicMock()
    tracker.__enter__.return_value = tracker
    tracker.__exit__.return_value = None
    tracker.run_id = "run123"

    mock_tracker.return_value = tracker

    result = manager.retrain(
        model_name="failure_prediction",
        trainer=trainer,
        train_args=([], []),
        dataset_version="v1",
    )

    assert result["model"] == "failure_prediction"
    assert result["dataset_version"] == "v1"

    trainer.train.assert_called_once()


@patch("retraining.retraining_manager.ExperimentTracker")
def test_invalid_model(
    mock_tracker,
    manager,
    trainer,
):
    with pytest.raises(ValueError):
        manager.retrain(
            model_name="invalid",
            trainer=trainer,
            train_args=([], []),
            dataset_version="v1",
        )


@patch("retraining.retraining_manager.model_registry")
@patch("retraining.retraining_manager.ExperimentTracker")
def test_register_called(
    mock_tracker,
    mock_registry,
    manager,
    trainer,
):
    tracker = MagicMock()
    tracker.__enter__.return_value = tracker
    tracker.__exit__.return_value = None
    tracker.run_id = "run123"

    mock_tracker.return_value = tracker

    manager.retrain(
        model_name="failure_prediction",
        trainer=trainer,
        train_args=([], []),
        dataset_version="v1",
    )

    mock_registry.register_model.assert_called_once()


@patch("retraining.retraining_manager.ExperimentTracker")
def test_training_kwargs(
    mock_tracker,
    manager,
):
    tracker = MagicMock()
    tracker.__enter__.return_value = tracker
    tracker.__exit__.return_value = None

    mock_tracker.return_value = tracker

    trainer = MagicMock()

    trainer.train.return_value = {}

    manager.retrain(
        model_name="failure_prediction",
        trainer=trainer,
        train_args=(1,),
        train_kwargs={"a": 2},
        dataset_version="v1",
    )

    trainer.train.assert_called_once_with(
        1,
        a=2,
    )


@patch("retraining.retraining_manager.ExperimentTracker")
def test_training_time(
    mock_tracker,
    manager,
):
    tracker = MagicMock()
    tracker.__enter__.return_value = tracker
    tracker.__exit__.return_value = None

    mock_tracker.return_value = tracker

    trainer = MagicMock()

    trainer.train.return_value = {}

    result = manager.retrain(
        model_name="failure_prediction",
        trainer=trainer,
        train_args=([], []),
        dataset_version="v1",
    )

    assert "training_time" in result