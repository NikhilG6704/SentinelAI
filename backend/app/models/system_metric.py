"""
System Metric ORM model.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class SystemMetric(BaseModel):
    """
    Stores one snapshot of system metrics collected
    from a monitoring agent.
    """

    __tablename__ = "system_metrics"

    monitoring_agent_id: Mapped[int] = mapped_column(
        ForeignKey("monitoring_agents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cpu_usage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    memory_usage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    disk_usage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    network_in: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    network_out: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    uptime_seconds: Mapped[int] = mapped_column(
        nullable=False,
    )

    collection_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    monitoring_agent = relationship(
        "MonitoringAgent",
        back_populates="metrics",
    )