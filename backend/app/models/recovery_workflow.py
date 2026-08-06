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


class RecoveryActionType(str, Enum):
    RESTART_SERVICE = "RESTART_SERVICE"
    RESTART_CONTAINER = "RESTART_CONTAINER"
    RESTART_VM = "RESTART_VM"
    REBOOT_SERVER = "REBOOT_SERVER"
    CLEAR_CACHE = "CLEAR_CACHE"
    RESTART_MONITORING_AGENT = "RESTART_MONITORING_AGENT"
    SEND_NOTIFICATION = "SEND_NOTIFICATION"


class ExecutionMode(str, Enum):
    SIMULATION = "Simulation"


class ExecutionStatus(str, Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class RecoveryWorkflow(BaseModel):
    """
    Recovery Workflow entity.
    """

    __tablename__ = "recovery_workflows"

    workflow_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    automation_rule_id: Mapped[int] = mapped_column(
        ForeignKey("automation_rules.id"),
        nullable=False,
        index=True,
    )

    incident_id: Mapped[int | None] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=True,
        index=True,
    )

    infrastructure_asset_id: Mapped[int] = mapped_column(
        ForeignKey("infrastructure_assets.id"),
        nullable=False,
        index=True,
    )

    action_type: Mapped[RecoveryActionType] = mapped_column(
        SQLEnum(
            RecoveryActionType,
            name="recovery_action_type_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    execution_mode: Mapped[ExecutionMode] = mapped_column(
        SQLEnum(
            ExecutionMode,
            name="execution_mode_enum",
            native_enum=False,
        ),
        nullable=False,
        default=ExecutionMode.SIMULATION,
    )

    execution_status: Mapped[ExecutionStatus] = mapped_column(
        SQLEnum(
            ExecutionStatus,
            name="execution_status_enum",
            native_enum=False,
        ),
        nullable=False,
        default=ExecutionStatus.PENDING,
    )

    execution_log: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    executed_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    automation_rule = relationship(
        "AutomationRule",
    )

    incident = relationship(
        "Incident",
    )

    infrastructure_asset = relationship(
        "InfrastructureAsset",
    )