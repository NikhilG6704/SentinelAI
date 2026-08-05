"""
Notification Service.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.alert_repository import AlertRepository
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.notification_repository import (
    NotificationRepository,
)
from app.models.notification import (
    Notification,
    NotificationStatus,
)
from app.schemas.notification import (
    NotificationCreate,
    NotificationStatusUpdate,
)


class NotificationService:
    """
    Business logic for Notification management.
    """

    repository = NotificationRepository()
    alert_repository = AlertRepository()
    incident_repository = IncidentRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: NotificationCreate,
    ) -> Notification:

        if request.alert_id is not None:
            alert = cls.alert_repository.get_by_id(
                db,
                request.alert_id,
            )

            if alert is None:
                raise ValueError("Alert not found.")

        if request.incident_id is not None:
            incident = cls.incident_repository.get_by_id(
                db,
                request.incident_id,
            )

            if incident is None:
                raise ValueError("Incident not found.")

        notification = Notification(
            **request.model_dump(),
        )

        logger.info(
            "Notification created for recipient %s.",
            request.recipient,
        )

        return cls.repository.create(
            db,
            notification,
        )

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        notification_id: int,
    ) -> Notification | None:

        return cls.repository.get_by_id(
            db,
            notification_id,
        )

    @classmethod
    def get_notifications(
        cls,
        db: Session,
        **kwargs,
    ) -> list[Notification]:

        return cls.repository.get_notifications(
            db,
            **kwargs,
        )

    @classmethod
    def update_status(
        cls,
        db: Session,
        notification_id: int,
        request: NotificationStatusUpdate,
    ) -> Notification:

        notification = cls.repository.get_by_id(
            db,
            notification_id,
        )

        if notification is None:
            raise ValueError(
                "Notification not found."
            )

        notification.status = request.status

        notification.failure_reason = (
            request.failure_reason
        )

        if request.status == NotificationStatus.SENT:
            notification.sent_at = datetime.now(
                timezone.utc,
            )

        logger.info(
            "Notification %s updated to %s.",
            notification.id,
            request.status.value,
        )

        return cls.repository.update_status(
            db,
            notification,
        )

    @classmethod
    def delete(
        cls,
        db: Session,
        notification_id: int,
    ) -> Notification:

        notification = cls.repository.get_by_id(
            db,
            notification_id,
        )

        if notification is None:
            raise ValueError(
                "Notification not found."
            )

        logger.info(
            "Notification %s deleted.",
            notification.id,
        )

        return cls.repository.soft_delete(
            db,
            notification,
        )