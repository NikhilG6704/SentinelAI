from unittest.mock import MagicMock, patch

from mlops.experiment_tracker import ExperimentTracker


@patch("mlops.experiment_tracker.mlflow_manager")
def test_tracker_context(mock_manager):
    context = MagicMock()
    mock_manager.start_run.return_value = context

    tracker = ExperimentTracker(
        component="anomaly_detection"
    )

    with tracker:
        pass

    mock_manager.get_or_create_experiment.assert_called_once()
    mock_manager.set_experiment.assert_called_once()
    context.__enter__.assert_called_once()
    context.__exit__.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_param(mock_manager):
    tracker = ExperimentTracker("anomaly_detection")

    tracker.log_param("epochs", 10)

    mock_manager.log_param.assert_called_once_with(
        "epochs",
        10,
    )


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_params(mock_manager):
    tracker = ExperimentTracker("anomaly_detection")

    tracker.log_params(
        {
            "lr": 0.01,
            "batch": 32,
        }
    )

    mock_manager.log_params.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_metric(mock_manager):
    tracker = ExperimentTracker("anomaly_detection")

    tracker.log_metric(
        "accuracy",
        0.95,
    )

    mock_manager.log_metric.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_metrics(mock_manager):
    tracker = ExperimentTracker("anomaly_detection")

    tracker.log_metrics(
        {
            "accuracy": 0.95,
            "precision": 0.92,
        }
    )

    mock_manager.log_metrics.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_artifact(mock_manager):
    tracker = ExperimentTracker("anomaly_detection")

    tracker.log_artifact("artifact.txt")

    mock_manager.log_artifact.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_artifacts(mock_manager):
    tracker = ExperimentTracker("anomaly_detection")

    tracker.log_artifacts("artifacts")

    mock_manager.log_artifacts.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_sklearn_model(mock_manager):
    tracker = ExperimentTracker("failure_prediction")

    model = MagicMock()

    tracker.log_sklearn_model(model)

    mock_manager.log_sklearn_model.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_xgboost_model(mock_manager):
    tracker = ExperimentTracker("failure_prediction")

    model = MagicMock()

    tracker.log_xgboost_model(model)

    mock_manager.log_xgboost_model.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_log_pytorch_model(mock_manager):
    tracker = ExperimentTracker("anomaly_detection")

    model = MagicMock()

    tracker.log_pytorch_model(model)

    mock_manager.log_pytorch_model.assert_called_once()


@patch("mlops.experiment_tracker.mlflow_manager")
def test_run_id(mock_manager):
    mock_manager.get_run_id.return_value = "run123"

    tracker = ExperimentTracker("anomaly_detection")

    assert tracker.run_id == "run123"


@patch("mlops.experiment_tracker.mlflow_manager")
def test_hyperparameters(mock_manager):
    context = MagicMock()
    mock_manager.start_run.return_value = context

    tracker = ExperimentTracker(
        component="failure_prediction",
        hyperparameters={
            "n_estimators": 100,
            "max_depth": 5,
        },
    )

    with tracker:
        pass

    assert mock_manager.log_params.call_count >= 2


@patch("mlops.experiment_tracker.mlflow_manager")
def test_failed_run(mock_manager):
    context = MagicMock()
    mock_manager.start_run.return_value = context

    tracker = ExperimentTracker(
        component="anomaly_detection"
    )

    try:
        with tracker:
            raise RuntimeError("failure")
    except RuntimeError:
        pass

    mock_manager.set_tag.assert_any_call(
        "status",
        "failed",
    )


@patch("mlops.experiment_tracker.mlflow_manager")
def test_successful_run(mock_manager):
    context = MagicMock()
    mock_manager.start_run.return_value = context

    tracker = ExperimentTracker(
        component="anomaly_detection"
    )

    with tracker:
        pass

    mock_manager.set_tag.assert_any_call(
        "status",
        "completed",
    )