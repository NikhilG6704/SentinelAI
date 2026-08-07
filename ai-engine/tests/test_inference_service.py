from unittest.mock import patch

import pytest

from serving.inference_service import InferenceService


@pytest.fixture
def service():
    return InferenceService()


@patch("serving.inference_service.prediction_router")
def test_predict(
    mock_router,
    service,
):
    mock_router.predict.return_value = {
        "prediction": 1
    }

    payload = {
        "cpu": 95
    }

    result = service.predict(
        "failure_prediction",
        payload,
    )

    assert result == {
        "prediction": 1
    }

    mock_router.predict.assert_called_once_with(
        "failure_prediction",
        payload,
    )


def test_invalid_model(service):

    with pytest.raises(ValueError):
        service.predict(
            "invalid",
            {},
        )


@patch("serving.inference_service.model_loader")
def test_preload(
    mock_loader,
    service,
):
    service.preload(
        "failure_prediction"
    )

    mock_loader.load.assert_called_once_with(
        "failure_prediction"
    )


@patch("serving.inference_service.model_loader")
def test_reload(
    mock_loader,
    service,
):
    service.reload(
        "failure_prediction"
    )

    mock_loader.reload.assert_called_once_with(
        "failure_prediction"
    )


@patch("serving.inference_service.model_loader")
def test_unload(
    mock_loader,
    service,
):
    service.unload(
        "failure_prediction"
    )

    mock_loader.unload.assert_called_once_with(
        "failure_prediction"
    )


@patch("serving.inference_service.model_loader")
def test_unload_all(
    mock_loader,
    service,
):
    service.unload_all()

    mock_loader.unload_all.assert_called_once()


@patch("serving.inference_service.model_loader")
def test_is_loaded(
    mock_loader,
    service,
):
    mock_loader.is_loaded.return_value = True

    assert service.is_loaded(
        "failure_prediction"
    )

    mock_loader.is_loaded.assert_called_once_with(
        "failure_prediction"
    )