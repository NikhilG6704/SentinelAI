from pathlib import Path

import pandas as pd

from retraining.dataset_versioning import (
    DatasetVersion,
    DatasetVersionManager,
)


def sample_dataset():
    return pd.DataFrame(
        {
            "cpu": [10, 20, 30],
            "memory": [50, 60, 70],
            "failure": [0, 1, 0],
        }
    )


def test_create_version():
    manager = DatasetVersionManager()

    version = manager.create_version(
        sample_dataset(),
        dataset_name="failure_prediction",
    )

    assert isinstance(
        version,
        DatasetVersion,
    )

    assert len(version.version) == 12


def test_metadata_file_created():
    manager = DatasetVersionManager()

    version = manager.create_version(
        sample_dataset(),
        dataset_name="failure_prediction",
    )

    assert version.metadata_path.exists()


def test_load_metadata():
    manager = DatasetVersionManager()

    version = manager.create_version(
        sample_dataset(),
        dataset_name="failure_prediction",
    )

    metadata = manager.load_metadata(
        version.metadata_path
    )

    assert metadata["version"] == version.version
    assert metadata["rows"] == 3
    assert metadata["columns"] == 3


def test_checksum_stable():
    manager = DatasetVersionManager()

    checksum1 = manager._checksum(
        sample_dataset()
    )

    checksum2 = manager._checksum(
        sample_dataset()
    )

    assert checksum1 == checksum2


def test_checksum_changes():
    manager = DatasetVersionManager()

    df1 = sample_dataset()

    df2 = sample_dataset()

    df2.loc[0, "cpu"] = 999

    assert (
        manager._checksum(df1)
        != manager._checksum(df2)
    )


def test_schema():
    manager = DatasetVersionManager()

    version = manager.create_version(
        sample_dataset(),
        dataset_name="failure_prediction",
    )

    assert "cpu" in version.schema
    assert "memory" in version.schema
    assert "failure" in version.schema


def test_metadata_path():
    manager = DatasetVersionManager()

    version = manager.create_version(
        sample_dataset(),
        dataset_name="failure_prediction",
    )

    assert isinstance(
        version.metadata_path,
        Path,
    )