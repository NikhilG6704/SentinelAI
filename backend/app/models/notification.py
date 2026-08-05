from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class NotificationType(str, Enum):
    EMAIL = "Email"
    SLACK = "Slack"
    TEAMS = "Teams"
    SMS = "SMS"
    IN_APP = "InApp"


class NotificationPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class NotificationStatus(str, Enum):
    PENDING = "Pending"
    SENT = "Sent"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class Notification(BaseModel):
    """
    Notification entity.
    """

    __tablename__ = "notifications"

    alert_id: Mapped[int | None] = mapped_column(
        ForeignKey("alerts.id"),
        nullable=True,
        index=True,
    )

    incident_id: Mapped[int | None] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    notification_type: Mapped[NotificationType] = mapped_column(
        SQLEnum(
            NotificationType,
            name="notification_type_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    priority: Mapped[NotificationPriority] = mapped_column(
        SQLEnum(
            NotificationPriority,
            name="notification_priority_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    status: Mapped[NotificationStatus] = mapped_column(
        SQLEnum(
            NotificationStatus,
            name="notification_status_enum",
            native_enum=False,
        ),
        nullable=False,
        default=NotificationStatus.PENDING,
    )

    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    alert = relationship(
        "Alert",
        back_populates="notifications",
    )

    incident = relationship(
        "Incident",
        back_populates="notifications",
    )