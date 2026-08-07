"""
Artifact manager for SentinelAI MLflow integration.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from datetime import datetime
from mlops.configuration import mlflow_config
from mlops.mlflow_manager import mlflow_manager


class ArtifactManager:
    """
    Handles creation and logging of MLflow artifacts.
    """
    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    def __init__(self) -> None:
        self.root = mlflow_config.artifact_directory
        self.root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _ensure_directory(self, directory: Path) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def _write_json(
        self,
        data: dict[str, Any],
        filepath: Path,
    ) -> Path:
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return filepath

    # ------------------------------------------------------------------ #
    # Generic Logging
    # ------------------------------------------------------------------ #

    def log_file(
        self,
        file_path: str | Path,
        destination: str | None = None,
    ) -> None:
        mlflow_manager.log_artifact(file_path, destination)

    def log_directory(
        self,
        directory: str | Path,
        destination: str | None = None,
    ) -> None:
        mlflow_manager.log_artifacts(directory, destination)

    # ------------------------------------------------------------------ #
    # Reports
    # ------------------------------------------------------------------ #

    def log_metrics_report(
        self,
        metrics: dict[str, Any],
    ) -> Path:

        report_dir = self._ensure_directory(
            self.root / "reports"
        )

        file = report_dir / f"metrics_{self._timestamp()}.json"

        self._write_json(metrics, file)

        mlflow_manager.log_artifact(
            file,
            "reports",
        )

        return file

    def log_classification_report(
        self,
        report: dict[str, Any],
    ) -> Path:

        report_dir = self._ensure_directory(
            self.root / "reports"
        )

        file = (
            report_dir
            / f"classification_report_{self._timestamp()}.json"
        )

        self._write_json(report, file)

        mlflow_manager.log_artifact(
            file,
            "reports",
        )

        return file

    # ------------------------------------------------------------------ #
    # Images
    # ------------------------------------------------------------------ #

    def log_confusion_matrix(
        self,
        image_path: str | Path,
    ) -> None:

        mlflow_manager.log_artifact(
            image_path,
            "plots",
        )

    def log_roc_curve(
        self,
        image_path: str | Path,
    ) -> None:

        mlflow_manager.log_artifact(
            image_path,
            "plots",
        )

    def log_feature_importance(
        self,
        image_path: str | Path,
    ) -> None:

        mlflow_manager.log_artifact(
            image_path,
            "plots",
        )

    # ------------------------------------------------------------------ #
    # Logs
    # ------------------------------------------------------------------ #

    def log_training_log(
        self,
        log_file: str | Path,
    ) -> None:

        mlflow_manager.log_artifact(
            log_file,
            "logs",
        )

    # ------------------------------------------------------------------ #
    # Models
    # ------------------------------------------------------------------ #

    def log_model_file(
        self,
        model_path: str | Path,
    ) -> None:

        mlflow_manager.log_artifact(
            model_path,
            "models",
        )


artifact_manager = ArtifactManager()