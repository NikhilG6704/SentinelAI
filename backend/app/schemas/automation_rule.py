from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.automation_rule import (
    ActionType,
    MetricType,
    RuleOperator,
    RuleSeverity,
    TargetScope,
)


class AutomationRuleCreate(BaseModel):
    rule_name: str = Field(max_length=255)

    description: str = Field(min_length=1)

    metric_type: MetricType

    operator: RuleOperator

    threshold: float

    severity: RuleSeverity

    action_type: ActionType

    target_scope: TargetScope = TargetScope.GLOBAL

    priority: int = Field(default=1, ge=1)

    cooldown_minutes: int = Field(default=5, ge=0)

    created_by: str = Field(max_length=255)


class AutomationRuleUpdate(BaseModel):
    description: str | None = None

    metric_type: MetricType | None = None

    operator: RuleOperator | None = None

    threshold: float | None = None

    severity: RuleSeverity | None = None

    action_type: ActionType | None = None

    target_scope: TargetScope | None = None

    priority: int | None = Field(default=None, ge=1)

    cooldown_minutes: int | None = Field(default=None, ge=0)


class AutomationRuleResponse(BaseModel):
    id: int

    rule_name: str

    description: str

    metric_type: MetricType

    operator: RuleOperator

    threshold: float

    severity: RuleSeverity

    action_type: ActionType

    target_scope: TargetScope

    is_enabled: bool

    priority: int

    cooldown_minutes: int

    created_by: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )