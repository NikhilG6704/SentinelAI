"""
Alert Repository.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.alert import (
    Alert,
    AlertSeverity,
    AlertStatus,
)


class AlertRepository(BaseRepository[Alert]):
    """
    Repository for Alert management.
    """

    def __init__(self) -> None:
        super().__init__(Alert)

    def get_filtered(
        self,
        db: Session,
        status: AlertStatus | None = None,
        severity: AlertSeverity | None = None,
        infrastructure_asset_id: int | None = None,
        monitoring_agent_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Alert]:

        query = db.query(Alert)

        if status is not None:
            query = query.filter(Alert.status == status)

        if severity is not None:
            query = query.filter(Alert.severity == severity)

        if infrastructure_asset_id is not None:
            query = query.filter(
                Alert.infrastructure_asset_id == infrastructure_asset_id
            )

        if monitoring_agent_id is not None:
            query = query.filter(
                Alert.monitoring_agent_id == monitoring_agent_id
            )

        return (
            query.order_by(Alert.triggered_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def acknowledge(
        self,
        db: Session,
        alert: Alert,
    ) -> Alert:

        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = datetime.utcnow()

        db.commit()
        db.refresh(alert)

        return alert

    def resolve(
        self,
        db: Session,
        alert: Alert,
        resolution_summary: str,
    ) -> Alert:

        alert.status = AlertStatus.RESOLVED
        alert.resolution_summary = resolution_summary
        alert.resolved_at = datetime.utcnow()

        db.commit()
        db.refresh(alert)

        return alert

    def soft_delete(
        self,
        db: Session,
        alert: Alert,
    ) -> Alert:

        alert.is_active = False

        db.commit()
        db.refresh(alert)

        return alert