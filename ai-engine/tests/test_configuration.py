from pathlib import Path

import pytest

from mlops.configuration import MLflowConfiguration


@pytest.fixture
def config():
    return MLflowConfiguration()


def test_project_metadata(config):
    assert config.project_name == "SentinelAI"
    assert config.project_version == "1.0.0"
    assert config.environment == "development"


def test_random_seed(config):
    assert config.random_seed == 42


def test_project_root_exists(config):
    assert config.project_root.exists()
    assert config.project_root.is_dir()


def test_tracking_uri(config):
    assert isinstance(config.tracking_uri, str)
    assert len(config.tracking_uri) > 0


def test_registry_uri(config):
    assert config.registry_uri == config.tracking_uri


def test_mlruns_directory(config):
    assert isinstance(config.mlruns_directory, Path)
    assert config.mlruns_directory.name == "mlruns"


def test_artifact_directory(config):
    assert isinstance(config.artifact_directory, Path)
    assert config.artifact_directory.name == "artifacts"


def test_get_experiment_name(config):
    assert (
        config.get_experiment_name("anomaly_detection")
        == "SentinelAI-AnomalyDetection"
    )

    assert (
        config.get_experiment_name("failure_prediction")
        == "SentinelAI-FailurePrediction"
    )

    assert (
        config.get_experiment_name("root_cause_analysis")
        == "SentinelAI-RootCauseAnalysis"
    )


def test_invalid_experiment(config):
    with pytest.raises(KeyError):
        config.get_experiment_name("invalid")


def test_get_model_name(config):
    assert (
        config.get_model_name("isolation_forest")
        == "IsolationForest"
    )

    assert (
        config.get_model_name("autoencoder")
        == "Autoencoder"
    )

    assert (
        config.get_model_name("random_forest")
        == "RandomForest"
    )

    assert (
        config.get_model_name("xgboost")
        == "XGBoost"
    )


def test_invalid_model(config):
    with pytest.raises(KeyError):
        config.get_model_name("invalid")


def test_default_tags(config):
    tags = config.default_tags(
        "failure_prediction"
    )

    assert tags["project"] == "SentinelAI"
    assert tags["environment"] == "development"
    assert tags["component"] == "failure_prediction"
    assert tags["version"] == "1.0.0"


def test_stage_validation(config):
    assert config.is_valid_stage("Development")
    assert config.is_valid_stage("Staging")
    assert config.is_valid_stage("Production")
    assert config.is_valid_stage("Archived")

    assert not config.is_valid_stage("Testing")


def test_ensure_directories(config):
    config.ensure_directories()

    assert config.mlruns_directory.exists()
    assert config.artifact_directory.exists()


def test_all_experiments_unique(config):
    values = list(config.experiments.values())

    assert len(values) == len(set(values))


def test_all_models_present(config):
    required = {
        "anomaly_detection",
        "failure_prediction",
        "root_cause_analysis",
        "recommendation_engine",
        "decision_engine",
        "isolation_forest",
        "autoencoder",
        "random_forest",
        "xgboost",
    }

    assert required.issubset(config.models.keys())