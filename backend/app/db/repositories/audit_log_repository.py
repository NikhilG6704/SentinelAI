"""
Audit Log Repository.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.audit_log import (
    AuditAction,
    AuditLog,
)


class AuditLogRepository(BaseRepository[AuditLog]):
    """
    Repository for Audit Log management.
    """

    def __init__(self) -> None:
        super().__init__(AuditLog)

    def get_logs(
        self,
        db: Session,
        *,
        action: AuditAction | None = None,
        entity_type: str | None = None,
        performed_by: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        keyword: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:

        query = db.query(AuditLog)

        if action:
            query = query.filter(
                AuditLog.action == action
            )

        if entity_type:
            query = query.filter(
                AuditLog.entity_type == entity_type
            )

        if performed_by:
            query = query.filter(
                AuditLog.performed_by == performed_by
            )

        if start_time:
            query = query.filter(
                AuditLog.performed_at >= start_time
            )

        if end_time:
            query = query.filter(
                AuditLog.performed_at <= end_time
            )

        if keyword:
            query = query.filter(
                or_(
                    AuditLog.details.ilike(f"%{keyword}%"),
                    AuditLog.source_module.ilike(f"%{keyword}%"),
                    AuditLog.entity_type.ilike(f"%{keyword}%"),
                )
            )

        return (
            query.order_by(
                AuditLog.performed_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )