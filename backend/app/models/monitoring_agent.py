"""
Monitoring Agent ORM model.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean
from app.models.base import BaseModel


class AgentStatus(str, Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"


class MonitoringAgent(BaseModel):
    """
    Represents a monitoring agent installed on an infrastructure asset.
    """

    __tablename__ = "monitoring_agents"

    infrastructure_asset_id: Mapped[int] = mapped_column(
        ForeignKey("infrastructure_assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    agent_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    agent_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    registration_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    last_heartbeat: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[AgentStatus] = mapped_column(
        SQLEnum(
            AgentStatus,
            name="agent_status_enum",
            native_enum=False,
        ),
        nullable=False,
        default=AgentStatus.ONLINE,
    )
    metrics = relationship(
        "SystemMetric",
        back_populates="monitoring_agent",
        cascade="all, delete-orphan",
    )

    infrastructure_asset = relationship(
        "InfrastructureAsset",
        back_populates="monitoring_agents",
    )
    incidents = relationship(
        "Incident",
        back_populates="monitoring_agent",
    )
    alerts = relationship(
        "Alert",
        back_populates="monitoring_agent",
    )
    system_logs = relationship(
        "SystemLog",
        back_populates="monitoring_agent",
        cascade="all, delete-orphan",
    )

    is_active: Mapped[bool] = mapped_column(
    Boolean,
    nullable=False,
    default=True,
)
