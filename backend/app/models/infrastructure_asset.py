"""
Infrastructure Asset ORM model.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import AssetStatus, AssetType, EnvironmentType
from app.models.base import BaseModel
from sqlalchemy.orm import relationship


class InfrastructureAsset(BaseModel):
    """
    Represents an infrastructure asset monitored by SentinelAI.
    """

    __tablename__ = "infrastructure_assets"

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        unique=True,
        index=True,
    )

    operating_system: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    asset_type: Mapped[AssetType] = mapped_column(
        Enum(AssetType, name="asset_type_enum"),
        nullable=False,
    )

    environment: Mapped[EnvironmentType] = mapped_column(
        Enum(EnvironmentType, name="environment_type_enum"),
        nullable=False,
    )

    status: Mapped[AssetStatus] = mapped_column(
        Enum(AssetStatus, name="asset_status_enum"),
        nullable=False,
        default=AssetStatus.HEALTHY,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    monitoring_agents = relationship(
        "MonitoringAgent",
        back_populates="infrastructure_asset",
        cascade="all, delete-orphan",
    )
    incidents = relationship(
        "Incident",
        back_populates="infrastructure_asset",
    )
    alerts = relationship(
        "Alert",
        back_populates="infrastructure_asset",
    )
    system_logs = relationship(
        "SystemLog",
        back_populates="infrastructure_asset",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<InfrastructureAsset("
            f"id={self.id}, "
            f"hostname='{self.hostname}', "
            f"ip='{self.ip_address}')>"
        )