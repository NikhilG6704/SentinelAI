from __future__ import annotations

from typing import Any

import httpx
import pandas as pd

from config.settings import settings
from utils.constants import (
    ALERTS_ENDPOINT,
    AUDIT_LOGS_ENDPOINT,
    INFRASTRUCTURE_ASSETS_ENDPOINT,
    INCIDENTS_ENDPOINT,
    MONITORING_AGENTS_ENDPOINT,
    RECOVERY_WORKFLOWS_ENDPOINT,
    SYSTEM_LOGS_ENDPOINT,
    SYSTEM_METRICS_ENDPOINT,
)
from utils.logger import logger


class DataLoader:
    """
    Loads datasets from SentinelAI backend APIs.

    This class is the ONLY source of data for the AI Engine.
    Database access is strictly prohibited.
    """

    def __init__(self) -> None:
        self.base_url = settings.API_BASE_URL
        self.timeout = settings.API_TIMEOUT
        self.batch_size = settings.API_BATCH_SIZE

    async def _request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch data from a backend endpoint.
        """

        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            logger.info(f"Fetching {endpoint}")

            response = await client.get(url, params=params)

            response.raise_for_status()

            payload = response.json()

            # Some endpoints return {"success": True, "data": [...]}
            if isinstance(payload, dict):

                if "data" in payload:
                    return payload["data"]

                return [payload]

            if isinstance(payload, list):
                return payload

            raise ValueError(f"Unexpected response format from {endpoint}")

    async def fetch_dataframe(
        self,
        endpoint: str,
        skip: int = 0,
        limit: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> pd.DataFrame:
        """
        Fetch a dataset and return a DataFrame.
        """

        params: dict[str, Any] = {
            "skip": skip,
            "limit": limit or self.batch_size,
        }

        if start_time:
            params["start_time"] = start_time

        if end_time:
            params["end_time"] = end_time

        records = await self._request(endpoint, params)

        df = pd.DataFrame(records)

        logger.success(
            f"{endpoint}: loaded {len(df)} records."
        )

        return df

    async def load_assets(self) -> pd.DataFrame:
        return await self.fetch_dataframe(
            INFRASTRUCTURE_ASSETS_ENDPOINT
        )

    async def load_agents(self) -> pd.DataFrame:
        return await self.fetch_dataframe(
            MONITORING_AGENTS_ENDPOINT
        )

    async def load_metrics(
        self,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> pd.DataFrame:
        return await self.fetch_dataframe(
            SYSTEM_METRICS_ENDPOINT,
            start_time=start_time,
            end_time=end_time,
        )

    async def load_alerts(self) -> pd.DataFrame:
        return await self.fetch_dataframe(
            ALERTS_ENDPOINT
        )

    async def load_incidents(self) -> pd.DataFrame:
        return await self.fetch_dataframe(
            INCIDENTS_ENDPOINT
        )

    async def load_logs(
        self,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> pd.DataFrame:
        return await self.fetch_dataframe(
            SYSTEM_LOGS_ENDPOINT,
            start_time=start_time,
            end_time=end_time,
        )

    async def load_workflows(self) -> pd.DataFrame:
        return await self.fetch_dataframe(
            RECOVERY_WORKFLOWS_ENDPOINT
        )

    async def load_audit_logs(
        self,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> pd.DataFrame:
        return await self.fetch_dataframe(
            AUDIT_LOGS_ENDPOINT,
            start_time=start_time,
            end_time=end_time,
        )