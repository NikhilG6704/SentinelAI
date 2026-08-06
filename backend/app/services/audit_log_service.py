"""
Audit Log Service.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.audit_log_repository import AuditLogRepository
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate


class AuditLogService:
    """
    Business logic for Audit Trail.
    """

    repository = AuditLogRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: AuditLogCreate,
    ) -> AuditLog:

        audit_log = AuditLog(
            **request.model_dump(),
        )

        return cls.repository.create(
            db,
            audit_log,
        )

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        audit_log_id: int,
    ) -> AuditLog | None:

        return cls.repository.get_by_id(
            db,
            audit_log_id,
        )

    @classmethod
    def get_logs(
        cls,
        db: Session,
        **kwargs,
    ) -> list[AuditLog]:

        return cls.repository.get_logs(
            db,
            **kwargs,
        )