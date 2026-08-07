from pathlib import Path
from unittest.mock import MagicMock, patch

import mlflow

from mlops.mlflow_manager import MLflowManager


@patch("mlops.mlflow_manager.mlflow.set_tracking_uri")
@patch("mlops.mlflow_manager.mlflow.set_registry_uri")
def test_manager_initialization(
    mock_registry,
    mock_tracking,
):
    manager = MLflowManager()

    assert manager is not None
    assert mock_tracking.called
    assert mock_registry.called


@patch("mlops.mlflow_manager.mlflow.get_experiment_by_name")
@patch("mlops.mlflow_manager.mlflow.create_experiment")
def test_create_experiment(
    mock_create,
    mock_get,
):
    mock_get.return_value = None
    mock_create.return_value = "1"

    manager = MLflowManager()

    experiment_id = manager.get_or_create_experiment(
        "anomaly_detection"
    )

    assert experiment_id == "1"

    mock_create.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.get_experiment_by_name")
def test_existing_experiment(
    mock_get,
):
    experiment = MagicMock()
    experiment.experiment_id = "123"

    mock_get.return_value = experiment

    manager = MLflowManager()

    experiment_id = manager.get_or_create_experiment(
        "failure_prediction"
    )

    assert experiment_id == "123"


@patch("mlops.mlflow_manager.mlflow.set_experiment")
def test_set_experiment(
    mock_set,
):
    manager = MLflowManager()

    manager.set_experiment(
        "anomaly_detection"
    )

    mock_set.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.start_run")
@patch("mlops.mlflow_manager.mlflow.end_run")
def test_start_run(
    mock_end,
    mock_start,
):
    manager = MLflowManager()

    with manager.start_run("unit-test"):
        pass

    mock_start.assert_called_once()
    mock_end.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.log_param")
def test_log_param(
    mock_log,
):
    manager = MLflowManager()

    manager.log_param(
        "epochs",
        10,
    )

    mock_log.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.log_params")
def test_log_params(
    mock_log,
):
    manager = MLflowManager()

    manager.log_params(
        {
            "lr": 0.01,
            "batch": 32,
        }
    )

    mock_log.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.log_metric")
def test_log_metric(
    mock_log,
):
    manager = MLflowManager()

    manager.log_metric(
        "accuracy",
        0.95,
    )

    mock_log.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.log_metrics")
def test_log_metrics(
    mock_log,
):
    manager = MLflowManager()

    manager.log_metrics(
        {
            "accuracy": 0.95,
            "precision": 0.91,
        }
    )

    mock_log.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.set_tag")
def test_set_tag(
    mock_tag,
):
    manager = MLflowManager()

    manager.set_tag(
        "stage",
        "Development",
    )

    mock_tag.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.set_tags")
def test_set_tags(
    mock_tags,
):
    manager = MLflowManager()

    manager.set_tags(
        {
            "a": "1",
            "b": "2",
        }
    )

    mock_tags.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.log_artifact")
def test_log_artifact(
    mock_log,
):
    manager = MLflowManager()

    manager.log_artifact(
        Path("dummy.txt")
    )

    mock_log.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.log_artifacts")
def test_log_artifacts(
    mock_log,
):
    manager = MLflowManager()

    manager.log_artifacts(
        Path("artifacts")
    )

    mock_log.assert_called_once()


@patch("mlops.mlflow_manager.mlflow.active_run")
def test_get_run_id(
    mock_active,
):
    run = MagicMock()
    run.info.run_id = "abc123"

    mock_active.return_value = run

    manager = MLflowManager()

    assert manager.get_run_id() == "abc123"


@patch("mlops.mlflow_manager.mlflow.active_run")
def test_get_run_id_none(
    mock_active,
):
    mock_active.return_value = None

    manager = MLflowManager()

    assert manager.get_run_id() is None


@patch("mlops.mlflow_manager.mlflow.active_run")
@patch("mlops.mlflow_manager.mlflow.start_run")
@patch("mlops.mlflow_manager.mlflow.end_run")
def test_start_run(
    mock_end,
    mock_start,
    mock_active,
):
    mock_start.return_value = MagicMock()
    mock_active.return_value = MagicMock()

    manager = MLflowManager()

    with manager.start_run("unit-test") as run:
        assert run is not None

    mock_start.assert_called_once_with(
        run_name="unit-test",
        nested=False,
    )

    mock_active.assert_called()
    mock_end.assert_called_once()