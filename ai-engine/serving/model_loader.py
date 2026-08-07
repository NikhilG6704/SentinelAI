"""
Model loader for SentinelAI.

Loads models from the MLflow Model Registry using lazy loading
and an in-memory cache.
"""

from __future__ import annotations

from typing import Any

import mlflow.pyfunc

from mlops.model_registry import model_registry
from serving.cache import model_cache
from serving.configuration import serving_config
from utils.logger import logger


class ModelLoader:
    """
    Loads models from the MLflow Model Registry.
    """

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _cache_key(
        self,
        model_name: str,
        stage: str | None,
        version: str | int | None,
    ) -> str:

        if version is not None:
            return f"{model_name}:v{version}"

        return f"{model_name}:{stage or serving_config.default_stage}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(
        self,
        model_name: str,
        *,
        stage: str | None = None,
        version: str | int | None = None,
        reload: bool = False,
    ) -> Any:

        if not serving_config.is_supported(model_name):
            raise ValueError(
                f"Unsupported model: {model_name}"
            )

        cache_key = self._cache_key(
            model_name,
            stage,
            version,
        )

        if not reload:

            cached = model_cache.get(cache_key)

            if cached is not None:
                return cached.model

        model = self._load_from_registry(
            model_name=model_name,
            stage=stage,
            version=version,
        )

        loaded_version = (
            str(version)
            if version is not None
            else (stage or serving_config.default_stage)
        )

        model_cache.put(
            model_name=cache_key,
            model=model,
            version=loaded_version,
            stage=stage or serving_config.default_stage,
        )

        logger.success(
            f"Loaded model '{model_name}' ({loaded_version})"
        )

        return model

    def reload(
        self,
        model_name: str,
        *,
        stage: str | None = None,
        version: str | int | None = None,
    ) -> Any:

        cache_key = self._cache_key(
            model_name,
            stage,
            version,
        )

        model_cache.remove(cache_key)

        return self.load(
            model_name,
            stage=stage,
            version=version,
            reload=True,
        )

    def unload(
        self,
        model_name: str,
        *,
        stage: str | None = None,
        version: str | int | None = None,
    ) -> None:

        cache_key = self._cache_key(
            model_name,
            stage,
            version,
        )

        model_cache.remove(cache_key)

    def unload_all(self) -> None:
        model_cache.clear()

    def is_loaded(
        self,
        model_name: str,
        *,
        stage: str | None = None,
        version: str | int | None = None,
    ) -> bool:

        cache_key = self._cache_key(
            model_name,
            stage,
            version,
        )

        return model_cache.contains(cache_key)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load_from_registry(
        self,
        *,
        model_name: str,
        stage: str | None,
        version: str | int | None,
    ) -> Any:

        registered_name = model_registry.get_registered_model_name(
            model_name
        )

        if version is not None:
            uri = f"models:/{registered_name}/{version}"
        else:
            uri = (
                f"models:/{registered_name}/"
                f"{stage or serving_config.default_stage}"
            )

        logger.info(
            f"Loading model from '{uri}'"
        )

        return mlflow.pyfunc.load_model(uri)


model_loader = ModelLoader()