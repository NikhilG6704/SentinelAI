"""
MLflow Model Registry manager for SentinelAI.
"""

from __future__ import annotations

from typing import Optional
from mlflow.exceptions import MlflowException
import mlflow
from mlflow import MlflowClient
from mlflow.entities.model_registry import ModelVersion

from mlops.configuration import mlflow_config


class ModelRegistry:
    """
    Wrapper around the MLflow Model Registry.
    """

    def __init__(self) -> None:
        self.client = MlflowClient(
            tracking_uri=mlflow_config.tracking_uri,
            registry_uri=mlflow_config.registry_uri,
        )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_model(
        self,
        model_uri: str,
        model_key: str,
    ) -> ModelVersion:
        """
        Register a model in the MLflow Registry.

        Parameters
        ----------
        model_uri
            Example:
                runs:/<run_id>/model

        model_key
            Example:
                isolation_forest
        """

        model_name = mlflow_config.get_model_name(model_key)

        try:
            self.client.get_registered_model(model_name)
        except MlflowException:
            self.client.create_registered_model(model_name)

        return mlflow.register_model(
            model_uri=model_uri,
            name=model_name,
        )

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get_latest_version(
        self,
        model_key: str,
    ) -> Optional[ModelVersion]:

        model_name = mlflow_config.get_model_name(model_key)

        versions = self.client.get_latest_versions(model_name)

        if not versions:
            return None

        return max(
            versions,
            key=lambda version: int(version.version),
        )

    def get_version(
        self,
        model_key: str,
        version: str | int,
    ) -> ModelVersion:

        model_name = mlflow_config.get_model_name(model_key)

        return self.client.get_model_version(
            name=model_name,
            version=str(version),
        )

    def get_production_model(
        self,
        model_key: str,
    ) -> Optional[ModelVersion]:

        model_name = mlflow_config.get_model_name(model_key)

        versions = self.client.get_latest_versions(
            model_name,
            stages=["Production"],
        )

        if not versions:
            return None

        return versions[0]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def transition_stage(
        self,
        model_key: str,
        version: str | int,
        stage: str,
        archive_existing_versions: bool = False,
    ) -> None:

        model_name = mlflow_config.get_model_name(model_key)

        self.client.transition_model_version_stage(
            name=model_name,
            version=str(version),
            stage=stage,
            archive_existing_versions=archive_existing_versions,
        )

    def archive_model(
        self,
        model_key: str,
        version: str | int,
    ) -> None:

        self.transition_stage(
            model_key=model_key,
            version=version,
            stage="Archived",
        )

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_versions(
        self,
        model_key: str,
    ) -> list[ModelVersion]:

        model_name = mlflow_config.get_model_name(model_key)

        return list(
            self.client.search_model_versions(
                f"name='{model_name}'"
            )
        )

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def model_exists(
        self,
        model_key: str,
    ) -> bool:

        model_name = mlflow_config.get_model_name(model_key)

        try:
            self.client.get_registered_model(model_name)
            return True
        except MlflowException:
            return False

    def delete_registered_model(
        self,
        model_key: str,
    ) -> None:

        model_name = mlflow_config.get_model_name(model_key)

        self.client.delete_registered_model(model_name)

    def get_registered_model_name(
        self,
        model_key: str,
    ) -> str:
        """
        Return the registered model name for a model key.
        """
        return mlflow_config.get_model_name(model_key)


model_registry = ModelRegistry()