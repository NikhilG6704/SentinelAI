from __future__ import annotations

from enum import Enum

from sqlalchemy import (
    Boolean,
    Enum as SQLEnum,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class MetricType(str, Enum):
    CPU_USAGE = "CPU_USAGE"
    MEMORY_USAGE = "MEMORY_USAGE"
    DISK_USAGE = "DISK_USAGE"
    NETWORK_USAGE = "NETWORK_USAGE"
    LOG_ERROR_RATE = "LOG_ERROR_RATE"
    INCIDENT_COUNT = "INCIDENT_COUNT"


class RuleOperator(str, Enum):
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    EQ = "=="
    NE = "!="


class ActionType(str, Enum):
    CREATE_ALERT = "CREATE_ALERT"
    CREATE_INCIDENT = "CREATE_INCIDENT"
    RESTART_SERVICE = "RESTART_SERVICE"
    RESTART_CONTAINER = "RESTART_CONTAINER"
    REBOOT_SERVER = "REBOOT_SERVER"
    SCALE_SERVICE = "SCALE_SERVICE"
    SEND_NOTIFICATION = "SEND_NOTIFICATION"


class RuleSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TargetScope(str, Enum):
    GLOBAL = "Global"
    ASSET = "Asset"
    AGENT = "Agent"


class AutomationRule(BaseModel):
    """
    Automation Rule entity.
    """

    __tablename__ = "automation_rules"

    rule_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    metric_type: Mapped[MetricType] = mapped_column(
        SQLEnum(
            MetricType,
            name="metric_type_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    operator: Mapped[RuleOperator] = mapped_column(
        SQLEnum(
            RuleOperator,
            name="rule_operator_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    severity: Mapped[RuleSeverity] = mapped_column(
        SQLEnum(
            RuleSeverity,
            name="rule_severity_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    action_type: Mapped[ActionType] = mapped_column(
        SQLEnum(
            ActionType,
            name="action_type_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    target_scope: Mapped[TargetScope] = mapped_column(
        SQLEnum(
            TargetScope,
            name="target_scope_enum",
            native_enum=False,
        ),
        nullable=False,
        default=TargetScope.GLOBAL,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )


    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    cooldown_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5,
    )

    created_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )