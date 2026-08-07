"""
Alert management for SentinelAI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from utils.logger import logger


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class MonitoringAlert:
    """
    Represents a monitoring alert.
    """

    source: str
    severity: AlertSeverity
    message: str
    timestamp: str
    metadata: dict[str, Any]


class AlertManager:
    """
    Generates monitoring alerts.
    """

    def __init__(self) -> None:
        self._history: list[MonitoringAlert] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_alert(
        self,
        *,
        source: str,
        severity: AlertSeverity,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> MonitoringAlert:

        alert = MonitoringAlert(
            source=source,
            severity=severity,
            message=message,
            timestamp=datetime.now(
                UTC
            ).isoformat(),
            metadata=metadata or {},
        )

        self._history.append(alert)

        logger.warning(
            f"[{severity}] {source}: {message}"
        )

        return alert

    def history(self) -> list[MonitoringAlert]:
        """
        Return alert history.
        """

        return list(self._history)

    def clear(self) -> None:
        """
        Clear alert history.
        """

        self._history.clear()

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def data_drift(
        self,
        metadata: dict[str, Any],
    ) -> MonitoringAlert:

        return self.create_alert(
            source="Data Drift",
            severity=AlertSeverity.WARNING,
            message="Feature distribution drift detected.",
            metadata=metadata,
        )

    def concept_drift(
        self,
        metadata: dict[str, Any],
    ) -> MonitoringAlert:

        return self.create_alert(
            source="Concept Drift",
            severity=AlertSeverity.WARNING,
            message="Prediction behaviour drift detected.",
            metadata=metadata,
        )

    def performance(
        self,
        metadata: dict[str, Any],
    ) -> MonitoringAlert:

        return self.create_alert(
            source="Performance",
            severity=AlertSeverity.CRITICAL,
            message="Model performance degraded.",
            metadata=metadata,
        )

    def latency(
        self,
        metadata: dict[str, Any],
    ) -> MonitoringAlert:

        return self.create_alert(
            source="Latency",
            severity=AlertSeverity.WARNING,
            message="Inference latency threshold exceeded.",
            metadata=metadata,
        )

    def resources(
        self,
        metadata: dict[str, Any],
    ) -> MonitoringAlert:

        return self.create_alert(
            source="Resources",
            severity=AlertSeverity.CRITICAL,
            message="System resource threshold exceeded.",
            metadata=metadata,
        )


alert_manager = AlertManager()