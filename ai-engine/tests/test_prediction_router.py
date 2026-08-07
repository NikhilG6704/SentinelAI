from unittest.mock import MagicMock, patch

import pytest

from serving.prediction_router import PredictionRouter


@pytest.fixture
def router():
    return PredictionRouter()


@patch("serving.prediction_router.model_loader")
def test_predict(mock_loader, router):
    model = MagicMock()
    model.predict.return_value = {"prediction": 1}

    mock_loader.load.return_value = model

    payload = {"cpu": 90}

    result = router.predict(
        "failure_prediction",
        payload,
    )

    assert result == {"prediction": 1}

    mock_loader.load.assert_called_once_with(
        "failure_prediction"
    )

    model.predict.assert_called_once_with(
        payload
    )


def test_invalid_model(router):

    with pytest.raises(ValueError):
        router.predict(
            "invalid_model",
            {},
        )


@patch("serving.prediction_router.model_loader")
def test_predict_without_predict_method(
    mock_loader,
    router,
):
    model = MagicMock(spec=[])

    mock_loader.load.return_value = model

    with pytest.raises(AttributeError):
        router.predict(
            "failure_prediction",
            {},
        )


@patch("serving.prediction_router.model_loader")
def test_multiple_predictions(
    mock_loader,
    router,
):
    model = MagicMock()

    model.predict.side_effect = [
        1,
        0,
        1,
    ]

    mock_loader.load.return_value = model

    assert router.predict(
        "failure_prediction",
        {}
    ) == 1

    assert router.predict(
        "failure_prediction",
        {}
    ) == 0

    assert router.predict(
        "failure_prediction",
        {}
    ) == 1

    assert model.predict.call_count == 3