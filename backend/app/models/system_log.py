from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SystemLog(BaseModel):
    """
    Infrastructure System Log.
    """

    __tablename__ = "system_logs"

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

    log_level: Mapped[LogLevel] = mapped_column(
        SQLEnum(
            LogLevel,
            name="log_level_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    service_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    log_metadata: Mapped[dict | None] = mapped_column(
    "metadata",
    JSON,
    nullable=True,
)

    infrastructure_asset = relationship(
        "InfrastructureAsset",
        back_populates="system_logs",
    )

    monitoring_agent = relationship(
        "MonitoringAgent",
        back_populates="system_logs",
    )