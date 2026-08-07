"""
Prediction router for SentinelAI.
"""

from __future__ import annotations

from typing import Any

from serving.configuration import serving_config
from serving.model_loader import model_loader


class PredictionRouter:
    """
    Routes prediction requests to the appropriate loaded model.
    """

    def __init__(self) -> None:
        pass

    def predict(
        self,
        model_name: str,
        payload: Any,
    ) -> Any:
        """
        Route a prediction request to the requested model.
        """

        if not serving_config.is_supported(model_name):
            raise ValueError(
                f"Unsupported model '{model_name}'."
            )

        model = model_loader.load(model_name)

        if not hasattr(model, "predict"):
            raise AttributeError(
                f"{model_name} does not implement predict()."
            )

        return model.predict(payload)


prediction_router = PredictionRouter()