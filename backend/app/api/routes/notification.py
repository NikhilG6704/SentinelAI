from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.notification import (
    NotificationPriority,
    NotificationStatus,
    NotificationType,
)
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationStatusUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notifications"],
)


@router.post(
    "",
    response_model=SuccessResponse[NotificationResponse],
    status_code=201,
)
async def create_notification(
    request: NotificationCreate,
    db: Session = Depends(get_db),
):
    notification = NotificationService.create(
        db,
        request,
    )

    return SuccessResponse(
        message="Notification created successfully.",
        data=NotificationResponse.model_validate(notification),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[NotificationResponse]],
)
async def get_notifications(
    status: NotificationStatus | None = Query(default=None),
    priority: NotificationPriority | None = Query(default=None),
    notification_type: NotificationType | None = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    notifications = NotificationService.get_notifications(
        db=db,
        status=status,
        priority=priority,
        notification_type=notification_type,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="Notifications retrieved successfully.",
        data=[
            NotificationResponse.model_validate(notification)
            for notification in notifications
        ],
    )


@router.get(
    "/{notification_id}",
    response_model=SuccessResponse[NotificationResponse],
)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = NotificationService.get_by_id(
        db,
        notification_id,
    )

    return SuccessResponse(
        message="Notification retrieved successfully.",
        data=NotificationResponse.model_validate(notification),
    )


@router.patch(
    "/{notification_id}/status",
    response_model=SuccessResponse[NotificationResponse],
)
async def update_notification_status(
    notification_id: int,
    request: NotificationStatusUpdate,
    db: Session = Depends(get_db),
):
    notification = NotificationService.update_status(
        db,
        notification_id,
        request,
    )

    return SuccessResponse(
        message="Notification status updated successfully.",
        data=NotificationResponse.model_validate(notification),
    )


@router.delete(
    "/{notification_id}",
    response_model=SuccessResponse[NotificationResponse],
)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = NotificationService.delete(
        db,
        notification_id,
    )

    return SuccessResponse(
        message="Notification deleted successfully.",
        data=NotificationResponse.model_validate(notification),
    )