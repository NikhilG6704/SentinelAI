"""
Notification Repository.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.notification import (
    Notification,
    NotificationPriority,
    NotificationStatus,
    NotificationType,
)


class NotificationRepository(BaseRepository[Notification]):
    """
    Repository for Notification management.
    """

    def __init__(self) -> None:
        super().__init__(Notification)

    def get_notifications(
        self,
        db: Session,
        *,
        status: NotificationStatus | None = None,
        priority: NotificationPriority | None = None,
        notification_type: NotificationType | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Notification]:

        query = db.query(Notification)

        if status:
            query = query.filter(
                Notification.status == status
            )

        if priority:
            query = query.filter(
                Notification.priority == priority
            )

        if notification_type:
            query = query.filter(
                Notification.notification_type == notification_type
            )

        return (
            query.order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        db: Session,
        notification: Notification,
    ) -> Notification:

        db.commit()
        db.refresh(notification)

        return notification

    def soft_delete(
        self,
        db: Session,
        notification: Notification,
    ) -> Notification:

        notification.is_active = False

        db.commit()
        db.refresh(notification)

        return notification