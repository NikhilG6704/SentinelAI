from unittest.mock import MagicMock, patch

from serving.health import HealthService


def test_health_creation():
    service = HealthService()

    assert service is not None


@patch("serving.health.mlflow")
def test_mlflow_status(
    mock_mlflow,
):
    mock_mlflow.get_tracking_uri.return_value = (
        "sqlite:///mlflow.db"
    )

    service = HealthService()

    status = service.mlflow_status()

    assert status["connected"] is True
    assert status["tracking_uri"] == "sqlite:///mlflow.db"


@patch("serving.health.model_cache")
def test_cache_status(
    mock_cache,
):
    mock_cache.stats.return_value = {
        "size": 2,
        "hits": 10,
        "misses": 1,
    }

    service = HealthService()

    status = service.cache_status()

    assert status["size"] == 2
    assert status["hits"] == 10


@patch("serving.health.model_cache")
def test_loaded_models(
    mock_cache,
):
    model = MagicMock()

    model.name = "failure_prediction"
    model.version = "2"
    model.stage = "Production"

    from datetime import datetime

    model.loaded_at = datetime.now()

    mock_cache.items.return_value = [
        model
    ]

    service = HealthService()

    models = service.loaded_models()

    assert len(models) == 1
    assert models[0]["name"] == "failure_prediction"
    assert models[0]["version"] == "2"


@patch.object(
    HealthService,
    "mlflow_status",
)
@patch.object(
    HealthService,
    "cache_status",
)
@patch.object(
    HealthService,
    "loaded_models",
)
def test_status(
    mock_models,
    mock_cache,
    mock_mlflow,
):
    mock_mlflow.return_value = {
        "connected": True
    }

    mock_cache.return_value = {
        "size": 1
    }

    mock_models.return_value = []

    service = HealthService()

    status = service.status()

    assert status["healthy"] is True
    assert "mlflow" in status
    assert "cache" in status
    assert "loaded_models" in status


@patch("serving.health.mlflow")
def test_mlflow_failure(
    mock_mlflow,
):
    mock_mlflow.get_tracking_uri.side_effect = Exception(
        "Connection failed"
    )

    service = HealthService()

    status = service.mlflow_status()

    assert status["connected"] is False
    assert "error" in status