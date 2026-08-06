from __future__ import annotations

import pandas as pd

from utils.logger import logger


class FeatureEngineer:
    """
    Generate machine learning features from
    infrastructure monitoring datasets.
    """

    def __init__(
        self,
        rolling_window: int = 5,
    ) -> None:
        self.rolling_window = rolling_window

    def cpu_features(
        self,
        metrics: pd.DataFrame,
    ) -> pd.DataFrame:

        if "cpu_usage" not in metrics.columns:
            return metrics

        metrics = metrics.sort_values("collection_timestamp")

        metrics["cpu_moving_average"] = (
            metrics["cpu_usage"]
            .rolling(self.rolling_window, min_periods=1)
            .mean()
        )

        metrics["cpu_std"] = (
            metrics["cpu_usage"]
            .rolling(self.rolling_window, min_periods=1)
            .std()
            .fillna(0)
        )

        return metrics

    def memory_features(
        self,
        metrics: pd.DataFrame,
    ) -> pd.DataFrame:

        if "memory_usage" not in metrics.columns:
            return metrics

        metrics["memory_moving_average"] = (
            metrics["memory_usage"]
            .rolling(self.rolling_window, min_periods=1)
            .mean()
        )

        return metrics

    def disk_features(
        self,
        metrics: pd.DataFrame,
    ) -> pd.DataFrame:

        if "disk_usage" not in metrics.columns:
            return metrics

        metrics["disk_utilization_trend"] = (
            metrics["disk_usage"]
            .diff()
            .fillna(0)
        )

        return metrics

    def network_features(
        self,
        metrics: pd.DataFrame,
    ) -> pd.DataFrame:

        if (
            "network_in" not in metrics.columns
            or "network_out" not in metrics.columns
        ):
            return metrics

        metrics["network_total"] = (
            metrics["network_in"]
            + metrics["network_out"]
        )

        metrics["network_utilization_trend"] = (
            metrics["network_total"]
            .diff()
            .fillna(0)
        )

        return metrics

    def heartbeat_delay(
        self,
        agents: pd.DataFrame,
    ) -> pd.DataFrame:

        if "last_heartbeat" not in agents.columns:
            return agents

        agents["heartbeat_delay_seconds"] = (
            pd.Timestamp.utcnow()
            - agents["last_heartbeat"]
        ).dt.total_seconds()

        return agents

    def alert_frequency(
        self,
        alerts: pd.DataFrame,
    ) -> pd.DataFrame:

        if alerts.empty:
            return alerts

        frequency = (
            alerts.groupby("infrastructure_asset_id")
            .size()
            .rename("alert_frequency")
        )

        return alerts.merge(
            frequency,
            on="infrastructure_asset_id",
        )

    def incident_frequency(
        self,
        incidents: pd.DataFrame,
    ) -> pd.DataFrame:

        if incidents.empty:
            return incidents

        frequency = (
            incidents.groupby("infrastructure_asset_id")
            .size()
            .rename("incident_frequency")
        )

        return incidents.merge(
            frequency,
            on="infrastructure_asset_id",
        )

    def error_count(
        self,
        logs: pd.DataFrame,
    ) -> pd.DataFrame:

        if logs.empty:
            return logs

        errors = (
            logs["log_level"]
            .eq("ERROR")
            .groupby(logs["infrastructure_asset_id"])
            .sum()
            .rename("error_count")
        )

        return logs.merge(
            errors,
            on="infrastructure_asset_id",
        )

    def mttr(
        self,
        workflows: pd.DataFrame,
    ) -> pd.DataFrame:

        if workflows.empty:
            return workflows

        workflows["mttr_seconds"] = (
            workflows["completed_at"]
            - workflows["started_at"]
        ).dt.total_seconds()

        return workflows

    def mtbf(
        self,
        incidents: pd.DataFrame,
    ) -> pd.DataFrame:

        if incidents.empty:
            return incidents

        incidents = incidents.sort_values(
            "detected_at"
        )

        incidents["mtbf_seconds"] = (
            incidents.groupby("infrastructure_asset_id")[
                "detected_at"
            ]
            .diff()
            .dt.total_seconds()
        )

        return incidents

    def generate(
        self,
        *,
        metrics: pd.DataFrame,
        agents: pd.DataFrame,
        alerts: pd.DataFrame,
        incidents: pd.DataFrame,
        logs: pd.DataFrame,
        workflows: pd.DataFrame,
    ) -> dict[str, pd.DataFrame]:
        """
        Execute the complete feature engineering pipeline.
        """

        logger.info("Generating AI features...")

        metrics = self.cpu_features(metrics)
        metrics = self.memory_features(metrics)
        metrics = self.disk_features(metrics)
        metrics = self.network_features(metrics)

        agents = self.heartbeat_delay(agents)

        alerts = self.alert_frequency(alerts)

        incidents = self.incident_frequency(incidents)
        incidents = self.mtbf(incidents)

        logs = self.error_count(logs)

        workflows = self.mttr(workflows)

        logger.success("Feature engineering completed.")

        return {
            "metrics": metrics,
            "agents": agents,
            "alerts": alerts,
            "incidents": incidents,
            "logs": logs,
            "workflows": workflows,
        }