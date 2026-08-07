"""
Public trigger interface for the SentinelAI monitoring framework.
"""

from __future__ import annotations

from typing import Any

from monitoring.monitoring_manager import monitoring_manager
from utils.logger import logger


class MonitoringTrigger:
    """
    Public entry point for monitoring operations.
    """

    def run_monitoring(
        self,
        **monitoring_kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the monitoring workflow.
        """

        logger.info(
            "Starting monitoring workflow."
        )

        return monitoring_manager.monitor(
            **monitoring_kwargs,
        )

    def check_monitoring_status(
        self,
        monitoring_result: dict[str, Any],
    ) -> bool:
        """
        Return whether retraining is required.
        """

        return monitoring_result.get(
            "retraining_required",
            False,
        )

    def trigger_retraining_if_required(
        self,
        *,
        monitoring_result: dict[str, Any],
        **pipeline_kwargs: Any,
    ):
        """
        Trigger retraining if monitoring indicates it is required.
        """

        return monitoring_manager.trigger_retraining_if_required(
            monitoring_result=monitoring_result,
            **pipeline_kwargs,
        )


monitoring_trigger = MonitoringTrigger()