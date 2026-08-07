from unittest.mock import MagicMock, patch

from mlflow.exceptions import MlflowException

from mlops.model_registry import ModelRegistry


@patch("mlops.model_registry.MlflowClient")
def test_registry_creation(mock_client):
    registry = ModelRegistry()

    assert registry is not None
    mock_client.assert_called_once()


@patch("mlops.model_registry.mlflow.register_model")
@patch("mlops.model_registry.MlflowClient")
def test_register_model(
    mock_client,
    mock_register,
):
    client = MagicMock()
    mock_client.return_value = client

    client.get_registered_model.side_effect = MlflowException(
        "not found"
    )

    registry = ModelRegistry()

    registry.register_model(
        model_uri="runs:/123/model",
        model_key="random_forest",
    )

    client.create_registered_model.assert_called_once()
    mock_register.assert_called_once()


@patch("mlops.model_registry.MlflowClient")
def test_model_exists(mock_client):
    client = MagicMock()
    mock_client.return_value = client

    registry = ModelRegistry()

    assert registry.model_exists("random_forest")


@patch("mlops.model_registry.MlflowClient")
def test_model_not_exists(mock_client):
    client = MagicMock()

    client.get_registered_model.side_effect = MlflowException(
        "missing"
    )

    mock_client.return_value = client

    registry = ModelRegistry()

    assert not registry.model_exists("random_forest")


@patch("mlops.model_registry.MlflowClient")
def test_get_latest_version(mock_client):
    version = MagicMock()
    version.version = "5"

    client = MagicMock()
    client.get_latest_versions.return_value = [
        version
    ]

    mock_client.return_value = client

    registry = ModelRegistry()

    result = registry.get_latest_version(
        "random_forest"
    )

    assert result.version == "5"


@patch("mlops.model_registry.MlflowClient")
def test_get_version(mock_client):
    version = MagicMock()

    client = MagicMock()
    client.get_model_version.return_value = version

    mock_client.return_value = client

    registry = ModelRegistry()

    result = registry.get_version(
        "random_forest",
        1,
    )

    assert result == version


@patch("mlops.model_registry.MlflowClient")
def test_list_versions(mock_client):
    client = MagicMock()

    client.search_model_versions.return_value = [
        MagicMock(),
        MagicMock(),
    ]

    mock_client.return_value = client

    registry = ModelRegistry()

    versions = registry.list_versions(
        "random_forest"
    )

    assert len(versions) == 2


@patch("mlops.model_registry.MlflowClient")
def test_transition_stage(mock_client):
    client = MagicMock()
    mock_client.return_value = client

    registry = ModelRegistry()

    registry.transition_stage(
        "random_forest",
        1,
        "Production",
    )

    client.transition_model_version_stage.assert_called_once()


@patch("mlops.model_registry.MlflowClient")
def test_archive_model(mock_client):
    client = MagicMock()
    mock_client.return_value = client

    registry = ModelRegistry()

    registry.archive_model(
        "random_forest",
        1,
    )

    client.transition_model_version_stage.assert_called_once()


@patch("mlops.model_registry.MlflowClient")
def test_delete_model(mock_client):
    client = MagicMock()
    mock_client.return_value = client

    registry = ModelRegistry()

    registry.delete_registered_model(
        "random_forest"
    )

    client.delete_registered_model.assert_called_once()