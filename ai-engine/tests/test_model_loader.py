from unittest.mock import MagicMock, patch

import pytest

from serving.model_loader import ModelLoader


@pytest.fixture
def loader():
    return ModelLoader()


@patch("serving.model_loader.mlflow.pyfunc.load_model")
@patch("serving.model_loader.model_cache")
@patch("serving.model_loader.model_registry")
def test_load_model(
    mock_registry,
    mock_cache,
    mock_load,
    loader,
):
    loader._cache_key = MagicMock(
        return_value="failure_prediction:Production"
    )

    mock_cache.get.return_value = None
    mock_registry.get_registered_model_name.return_value = (
        "RandomForest"
    )

    model = MagicMock()
    mock_load.return_value = model

    result = loader.load(
        "failure_prediction"
    )

    assert result == model

    mock_load.assert_called_once()
    mock_cache.put.assert_called_once()


@patch("serving.model_loader.model_cache")
def test_cache_hit(
    mock_cache,
    loader,
):
    loader._cache_key = MagicMock(
        return_value="failure_prediction:Production"
    )

    cached = MagicMock()
    cached.model = MagicMock()

    mock_cache.get.return_value = cached

    result = loader.load(
        "failure_prediction"
    )

    assert result == cached.model


@patch("serving.model_loader.model_cache")
def test_reload(
    mock_cache,
    loader,
):
    loader._cache_key = MagicMock(
        return_value="failure_prediction:Production"
    )

    with patch.object(
        loader,
        "_load_from_registry",
        return_value=MagicMock(),
    ):
        loader.reload(
            "failure_prediction"
        )

    mock_cache.remove.assert_called_once_with(
        "failure_prediction:Production"
    )


@patch("serving.model_loader.model_cache")
def test_unload(
    mock_cache,
    loader,
):
    loader._cache_key = MagicMock(
        return_value="failure_prediction:Production"
    )

    loader.unload(
        "failure_prediction"
    )

    mock_cache.remove.assert_called_once_with(
        "failure_prediction:Production"
    )


@patch("serving.model_loader.model_cache")
def test_unload_all(
    mock_cache,
    loader,
):
    loader.unload_all()

    mock_cache.clear.assert_called_once()


@patch("serving.model_loader.model_cache")
def test_is_loaded(
    mock_cache,
    loader,
):
    loader._cache_key = MagicMock(
        return_value="failure_prediction:Production"
    )

    mock_cache.contains.return_value = True

    assert loader.is_loaded(
        "failure_prediction"
    )

    mock_cache.contains.assert_called_once_with(
        "failure_prediction:Production"
    )


def test_invalid_model(loader):

    with pytest.raises(ValueError):
        loader.load("invalid")


@patch("serving.model_loader.mlflow.pyfunc.load_model")
@patch("serving.model_loader.model_registry")
def test_load_specific_version(
    mock_registry,
    mock_load,
    loader,
):
    mock_registry.get_registered_model_name.return_value = (
        "RandomForest"
    )

    loader._load_from_registry(
        model_name="failure_prediction",
        stage=None,
        version=2,
    )

    mock_load.assert_called_once_with(
        "models:/RandomForest/2"
    )


@patch("serving.model_loader.mlflow.pyfunc.load_model")
@patch("serving.model_loader.model_registry")
def test_load_stage(
    mock_registry,
    mock_load,
    loader,
):
    mock_registry.get_registered_model_name.return_value = (
        "RandomForest"
    )

    loader._load_from_registry(
        model_name="failure_prediction",
        stage="Production",
        version=None,
    )

    mock_load.assert_called_once_with(
        "models:/RandomForest/Production"
    )