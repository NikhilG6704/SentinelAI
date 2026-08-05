from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.notification import (
    NotificationPriority,
    NotificationStatus,
    NotificationType,
)


class NotificationCreate(BaseModel):
    alert_id: int | None = None
    incident_id: int | None = None

    title: str = Field(max_length=255)

    message: str = Field(min_length=1)

    notification_type: NotificationType

    recipient: str = Field(max_length=255)

    priority: NotificationPriority

    scheduled_at: datetime | None = None


class NotificationStatusUpdate(BaseModel):
    status: NotificationStatus

    failure_reason: str | None = None


class NotificationResponse(BaseModel):
    id: int

    alert_id: int | None

    incident_id: int | None

    title: str

    message: str

    notification_type: NotificationType

    recipient: str

    priority: NotificationPriority

    status: NotificationStatus

    scheduled_at: datetime | None

    sent_at: datetime | None

    failure_reason: str | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )