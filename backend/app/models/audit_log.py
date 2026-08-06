from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AuditAction(str, Enum):
    INFRASTRUCTURE_ASSET_CREATED = "INFRASTRUCTURE_ASSET_CREATED"
    MONITORING_AGENT_REGISTERED = "MONITORING_AGENT_REGISTERED"
    METRICS_RECEIVED = "METRICS_RECEIVED"
    ALERT_CREATED = "ALERT_CREATED"
    INCIDENT_CREATED = "INCIDENT_CREATED"
    INCIDENT_RESOLVED = "INCIDENT_RESOLVED"
    AUTOMATION_RULE_UPDATED = "AUTOMATION_RULE_UPDATED"
    RECOVERY_WORKFLOW_EXECUTED = "RECOVERY_WORKFLOW_EXECUTED"
    REPORT_GENERATED = "REPORT_GENERATED"
    NOTIFICATION_CREATED = "NOTIFICATION_CREATED"


class AuditStatus(str, Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    WARNING = "Warning"


class AuditLog(BaseModel):
    """
    Audit Trail entity.
    """

    __tablename__ = "audit_logs"

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    action: Mapped[AuditAction] = mapped_column(
        SQLEnum(
            AuditAction,
            name="audit_action_enum",
            native_enum=False,
        ),
        nullable=False,
        index=True,
    )

    performed_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    performed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    status: Mapped[AuditStatus] = mapped_column(
        SQLEnum(
            AuditStatus,
            name="audit_status_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    source_module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    metadata_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )