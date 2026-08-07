"""
Unified inference service for SentinelAI.
"""

from __future__ import annotations

from typing import Any

from serving.configuration import serving_config
from serving.model_loader import model_loader
from serving.prediction_router import prediction_router
from utils.logger import logger


class InferenceService:
    """
    Unified interface for all model inference.

    Example:
        result = inference_service.predict(
            "failure_prediction",
            payload,
        )
    """

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict(
        self,
        model_name: str,
        payload: Any,
    ) -> Any:
        """
        Perform inference using the requested model.
        """

        if not serving_config.is_supported(model_name):
            raise ValueError(
                f"Unsupported model '{model_name}'."
            )

        logger.info(
            f"Inference request received for '{model_name}'."
        )

        return prediction_router.predict(
            model_name,
            payload,
        )

    # ------------------------------------------------------------------
    # Model Management
    # ------------------------------------------------------------------

    def preload(
        self,
        model_name: str,
    ) -> None:
        """
        Load a model into memory.
        """

        model_loader.load(model_name)

    def reload(
        self,
        model_name: str,
    ) -> None:
        """
        Reload a model from MLflow.
        """

        model_loader.reload(model_name)

    def unload(
        self,
        model_name: str,
    ) -> None:
        """
        Remove a model from cache.
        """

        model_loader.unload(model_name)

    def unload_all(self) -> None:
        """
        Clear the serving cache.
        """

        model_loader.unload_all()

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def is_loaded(
        self,
        model_name: str,
    ) -> bool:
        """
        Check whether a model is cached.
        """

        return model_loader.is_loaded(model_name)


inference_service = InferenceService()