from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.recovery_workflow import (
    ExecutionMode,
    ExecutionStatus,
    RecoveryActionType,
)


class RecoveryWorkflowCreate(BaseModel):
    workflow_name: str = Field(max_length=255)

    automation_rule_id: int

    incident_id: int | None = None

    infrastructure_asset_id: int

    action_type: RecoveryActionType

    executed_by: str = Field(max_length=255)


class RecoveryWorkflowResponse(BaseModel):
    id: int

    workflow_name: str

    automation_rule_id: int

    incident_id: int | None

    infrastructure_asset_id: int

    action_type: RecoveryActionType

    execution_mode: ExecutionMode

    execution_status: ExecutionStatus

    execution_log: str | None

    started_at: datetime | None

    completed_at: datetime | None

    executed_by: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class RecoveryWorkflowStatusUpdate(BaseModel):
    execution_status: ExecutionStatus