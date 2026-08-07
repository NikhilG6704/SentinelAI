"""
Dataset versioning for SentinelAI.

Generates reproducible dataset versions using file hashes and metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from retraining.configuration import retraining_config
from utils.logger import logger


@dataclass(frozen=True)
class DatasetVersion:
    """
    Immutable dataset version metadata.
    """

    version: str
    created_at: str
    rows: int
    columns: int
    schema: dict[str, str]
    checksum: str
    metadata_path: Path


class DatasetVersionManager:
    """
    Handles dataset versioning and metadata generation.
    """

    def __init__(self) -> None:
        retraining_config.ensure_directories()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_version(
        self,
        dataset: pd.DataFrame,
        *,
        dataset_name: str,
    ) -> DatasetVersion:
        """
        Create a new dataset version.
        """

        checksum = self._checksum(dataset)

        version = checksum[:12]

        created_at = datetime.now(
            UTC
        ).isoformat()

        metadata = {
            "version": version,
            "dataset": dataset_name,
            "created_at": created_at,
            "rows": len(dataset),
            "columns": len(dataset.columns),
            "schema": {
                column: str(dtype)
                for column, dtype
                in dataset.dtypes.items()
            },
            "checksum": checksum,
        }

        metadata_path = (
            retraining_config.versions_path
            / f"{dataset_name}_{version}.json"
        )

        metadata_path.write_text(
            json.dumps(
                metadata,
                indent=4,
            )
        )

        logger.success(
            f"Created dataset version {version}"
        )

        return DatasetVersion(
            version=version,
            created_at=created_at,
            rows=len(dataset),
            columns=len(dataset.columns),
            schema=metadata["schema"],
            checksum=checksum,
            metadata_path=metadata_path,
        )

    def load_metadata(
        self,
        metadata_path: str | Path,
    ) -> dict[str, Any]:

        metadata_path = Path(metadata_path)

        return json.loads(
            metadata_path.read_text()
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _checksum(
        dataset: pd.DataFrame,
    ) -> str:
        """
        SHA256 checksum of dataset contents.
        """

        csv = dataset.to_csv(
            index=False
        ).encode()

        return hashlib.sha256(csv).hexdigest()


dataset_version_manager = DatasetVersionManager()