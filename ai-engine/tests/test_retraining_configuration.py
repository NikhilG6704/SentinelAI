from retraining.configuration import (
    RetrainingConfiguration,
)


def test_configuration_creation():
    config = RetrainingConfiguration()

    assert config.pipeline_name == "SentinelAI-Retraining"


def test_supported_models():
    config = RetrainingConfiguration()

    assert config.is_supported(
        "failure_prediction"
    )

    assert config.is_supported(
        "anomaly_detection"
    )

    assert not config.is_supported(
        "abc"
    )


def test_paths():
    config = RetrainingConfiguration()

    assert config.datasets_path.name == "datasets"
    assert config.versions_path.name == "dataset_versions"
    assert config.evaluations_path.name == "evaluation_reports"


def test_threshold():
    config = RetrainingConfiguration()

    assert config.minimum_f1_improvement == 0.02


def test_precision_rule():
    config = RetrainingConfiguration()

    assert config.allow_precision_drop is False


def test_keep_versions():
    config = RetrainingConfiguration()

    assert config.keep_previous_versions == 5


def test_default_stage():
    config = RetrainingConfiguration()

    assert config.default_stage == "Production"


def test_directory_creation():
    config = RetrainingConfiguration()

    config.ensure_directories()

    assert config.datasets_path.exists()
    assert config.versions_path.exists()
    assert config.evaluations_path.exists()