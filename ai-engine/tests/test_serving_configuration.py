from pathlib import Path

import pytest

from serving.configuration import ServingConfiguration


@pytest.fixture
def config():
    return ServingConfiguration()


def test_service_name(config):
    assert config.service_name == "SentinelAI Serving"


def test_default_stage(config):
    assert config.default_stage == "Production"


def test_lazy_loading_enabled(config):
    assert config.lazy_loading is True


def test_cache_enabled(config):
    assert config.cache_enabled is True


def test_auto_reload(config):
    assert config.auto_reload is False


def test_cache_size(config):
    assert config.cache_size > 0


def test_cache_ttl(config):
    assert config.cache_ttl_seconds > 0


def test_project_root(config):
    assert config.project_root.exists()
    assert config.project_root.is_dir()


def test_cache_directory(config):
    path = config.cache_directory

    assert isinstance(path, Path)
    assert path.name == "serving_cache"


def test_supported_models(config):
    assert len(config.supported_models) == 5

    assert "anomaly_detection" in config.supported_models
    assert "failure_prediction" in config.supported_models
    assert "root_cause_analysis" in config.supported_models
    assert "recommendation_engine" in config.supported_models
    assert "decision_engine" in config.supported_models


def test_supported_model(config):
    assert config.is_supported("failure_prediction")


def test_unsupported_model(config):
    assert not config.is_supported("abc")


def test_supported_models_unique(config):
    assert len(config.supported_models) == len(
        set(config.supported_models)
    )