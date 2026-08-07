from pathlib import Path
from unittest.mock import patch

from mlops.artifact_manager import ArtifactManager


def test_artifact_manager_creation():
    manager = ArtifactManager()

    assert manager is not None
    assert manager.root.exists()


def test_timestamp():
    manager = ArtifactManager()

    timestamp = manager._timestamp()

    assert isinstance(timestamp, str)
    assert len(timestamp) == 15


def test_ensure_directory(tmp_path):
    manager = ArtifactManager()

    directory = tmp_path / "reports"

    result = manager._ensure_directory(directory)

    assert result.exists()
    assert result.is_dir()


def test_write_json(tmp_path):
    manager = ArtifactManager()

    file = tmp_path / "metrics.json"

    result = manager._write_json(
        {"accuracy": 0.95},
        file,
    )

    assert result.exists()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_log_file(mock_log):
    manager = ArtifactManager()

    manager.log_file("dummy.txt")

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifacts")
def test_log_directory(mock_log):
    manager = ArtifactManager()

    manager.log_directory("artifacts")

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_metrics_report(mock_log):
    manager = ArtifactManager()

    file = manager.log_metrics_report(
        {
            "accuracy": 0.9,
            "precision": 0.8,
        }
    )

    assert file.exists()

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_classification_report(mock_log):
    manager = ArtifactManager()

    file = manager.log_classification_report(
        {
            "accuracy": 0.95,
        }
    )

    assert file.exists()

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_confusion_matrix(mock_log):
    manager = ArtifactManager()

    manager.log_confusion_matrix(
        "cm.png"
    )

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_feature_importance(mock_log):
    manager = ArtifactManager()

    manager.log_feature_importance(
        "importance.png"
    )

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_roc_curve(mock_log):
    manager = ArtifactManager()

    manager.log_roc_curve(
        "roc.png"
    )

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_training_log(mock_log):
    manager = ArtifactManager()

    manager.log_training_log(
        "train.log"
    )

    mock_log.assert_called_once()


@patch("mlops.artifact_manager.mlflow_manager.log_artifact")
def test_model_file(mock_log):
    manager = ArtifactManager()

    manager.log_model_file(
        "model.joblib"
    )

    mock_log.assert_called_once()