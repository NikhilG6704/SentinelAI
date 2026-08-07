"""
Monitoring report generation for SentinelAI.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from monitoring.configuration import monitoring_config
from utils.logger import logger


class ReportGenerator:
    """
    Generates structured monitoring reports.
    """

    def __init__(self) -> None:
        monitoring_config.ensure_directories()

    # ------------------------------------------------------------------
    # Report Generation
    # ------------------------------------------------------------------

    def generate(
        self,
        *,
        model_name: str,
        data_drift: Any,
        concept_drift: Any,
        performance: Any,
        latency: Any,
        resources: Any,
        alerts: list[Any],
    ) -> dict[str, Any]:
        """
        Generate a monitoring report.
        """

        report = {
            "model": model_name,
            "generated_at": datetime.now(
                UTC
            ).isoformat(),
            "data_drift": asdict(data_drift),
            "concept_drift": asdict(concept_drift),
            "performance": asdict(performance),
            "latency": asdict(latency),
            "resources": asdict(resources),
            "alerts": [
                asdict(alert)
                for alert in alerts
            ],
            "recommended_action": self._recommend_action(
                data_drift=data_drift,
                concept_drift=concept_drift,
                performance=performance,
                latency=latency,
                resources=resources,
            ),
        }

        logger.success(
            f"Monitoring report generated for '{model_name}'."
        )

        return report

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(
        self,
        report: dict[str, Any],
    ) -> Path:
        """
        Save a report as JSON.
        """

        timestamp = datetime.now(
            UTC
        ).strftime("%Y%m%d_%H%M%S")

        filename = (
            f"{report['model']}_{timestamp}.json"
        )

        path = (
            monitoring_config.monitoring_path
            / filename
        )

        path.write_text(
            json.dumps(
                report,
                indent=4,
            )
        )

        logger.success(
            f"Saved report to {path}"
        )

        return path

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _recommend_action(
        *,
        data_drift,
        concept_drift,
        performance,
        latency,
        resources,
    ) -> str:

        if (
            data_drift.drift_detected
            or concept_drift.drift_detected
        ):
            return "Trigger retraining."

        if not performance.performance_ok:
            return "Investigate model performance."

        if not latency.latency_ok:
            return "Investigate inference latency."

        if not resources.resources_ok:
            return "Investigate system resources."

        return "No action required."


report_generator = ReportGenerator()