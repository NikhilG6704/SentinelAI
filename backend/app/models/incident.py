from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class IncidentSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class IncidentStatus(str, Enum):
    OPEN = "Open"
    INVESTIGATING = "Investigating"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class Incident(BaseModel):
    """
    Infrastructure Incident.
    """

    __tablename__ = "incidents"

    infrastructure_asset_id: Mapped[int] = mapped_column(
        ForeignKey("infrastructure_assets.id"),
        nullable=False,
        index=True,
    )

    monitoring_agent_id: Mapped[int | None] = mapped_column(
        ForeignKey("monitoring_agents.id"),
        nullable=True,
        index=True,
    )

    # Alert module will be added later.
    alert_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    incident_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    incident_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    severity: Mapped[IncidentSeverity] = mapped_column(
        SQLEnum(
            IncidentSeverity,
            name="incident_severity_enum",
        ),
        nullable=False,
    )

    status: Mapped[IncidentStatus] = mapped_column(
        SQLEnum(
            IncidentStatus,
            name="incident_status_enum",
        ),
        nullable=False,
        default=IncidentStatus.OPEN,
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
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
        back_populates="incidents",
    )

    monitoring_agent = relationship(
        "MonitoringAgent",
        back_populates="incidents",
    )