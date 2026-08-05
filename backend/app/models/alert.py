from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class AlertSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class AlertStatus(str, Enum):
    ACTIVE = "Active"
    ACKNOWLEDGED = "Acknowledged"
    RESOLVED = "Resolved"


class MetricType(str, Enum):
    CPU = "CPU"
    MEMORY = "Memory"
    DISK = "Disk"
    NETWORK = "Network"
    CUSTOM = "Custom"


class Alert(BaseModel):
    """
    Infrastructure Alert.
    """

    __tablename__ = "alerts"

    infrastructure_asset_id: Mapped[int] = mapped_column(
        ForeignKey("infrastructure_assets.id"),
        nullable=False,
        index=True,
    )

    monitoring_agent_id: Mapped[int] = mapped_column(
        ForeignKey("monitoring_agents.id"),
        nullable=False,
        index=True,
    )

    system_metric_id: Mapped[int | None] = mapped_column(
        ForeignKey("system_metrics.id"),
        nullable=True,
        index=True,
    )

    incident_id: Mapped[int | None] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=True,
        index=True,
    )

    alert_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    alert_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    severity: Mapped[AlertSeverity] = mapped_column(
        SQLEnum(
            AlertSeverity,
            name="alert_severity_enum",
        ),
        nullable=False,
    )

    status: Mapped[AlertStatus] = mapped_column(
        SQLEnum(
            AlertStatus,
            name="alert_status_enum",
        ),
        nullable=False,
        default=AlertStatus.ACTIVE,
    )

    metric_name: Mapped[MetricType] = mapped_column(
        SQLEnum(
            MetricType,
            name="metric_type_enum",
        ),
        nullable=False,
    )

    metric_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    threshold_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolution_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    infrastructure_asset = relationship(
        "InfrastructureAsset",
        back_populates="alerts",
    )

    monitoring_agent = relationship(
        "MonitoringAgent",
        back_populates="alerts",
    )

    system_metric = relationship(
        "SystemMetric",
        back_populates="alerts",
    )

    incident = relationship(
        "Incident",
        back_populates="alerts",
    )
    notifications = relationship(
        "Notification",
        back_populates="alert",
        cascade="all, delete-orphan",
    )