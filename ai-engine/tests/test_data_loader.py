from __future__ import annotations

import pandas as pd
import pytest

from preprocessing.data_loader import DataLoader


@pytest.mark.asyncio
async def test_fetch_dataframe(monkeypatch):
    """
    Verify that API responses are converted into DataFrames.
    """

    async def mock_request(self, endpoint, params=None):
        return [
            {
                "id": 1,
                "cpu_usage": 45.2,
                "memory_usage": 67.4,
            },
            {
                "id": 2,
                "cpu_usage": 50.1,
                "memory_usage": 70.8,
            },
        ]

    monkeypatch.setattr(
        DataLoader,
        "_request",
        mock_request,
    )

    loader = DataLoader()

    df = await loader.fetch_dataframe("/system-metrics")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "cpu_usage" in df.columns
    assert "memory_usage" in df.columns


@pytest.mark.asyncio
async def test_fetch_empty_dataframe(monkeypatch):
    """
    Verify that an empty API response produces an empty DataFrame.
    """

    async def mock_request(self, endpoint, params=None):
        return []

    monkeypatch.setattr(
        DataLoader,
        "_request",
        mock_request,
    )

    loader = DataLoader()

    df = await loader.fetch_dataframe("/system-metrics")

    assert isinstance(df, pd.DataFrame)
    assert df.empty


@pytest.mark.asyncio
async def test_load_assets(monkeypatch):
    """
    Verify that load_assets() delegates to fetch_dataframe().
    """

    async def mock_fetch_dataframe(
        self,
        endpoint,
        skip=0,
        limit=None,
        start_time=None,
        end_time=None,
    ):
        return pd.DataFrame(
            [
                {
                    "id": 1,
                    "hostname": "server-01",
                }
            ]
        )

    monkeypatch.setattr(
        DataLoader,
        "fetch_dataframe",
        mock_fetch_dataframe,
    )

    loader = DataLoader()

    df = await loader.load_assets()

    assert len(df) == 1
    assert "hostname" in df.columns