from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.recovery_workflow import (
    ExecutionStatus,
    RecoveryActionType,
)
from app.schemas.recovery_workflow import (
    RecoveryWorkflowCreate,
    RecoveryWorkflowResponse,
)
from app.schemas.response import SuccessResponse
from app.services.recovery_workflow_service import (
    RecoveryWorkflowService,
)

router = APIRouter(
    prefix="/api/v1/recovery-workflows",
    tags=["Recovery Workflows"],
)


@router.post(
    "",
    response_model=SuccessResponse[RecoveryWorkflowResponse],
    status_code=201,
)
async def create_workflow(
    request: RecoveryWorkflowCreate,
    db: Session = Depends(get_db),
):
    workflow = RecoveryWorkflowService.create(
        db,
        request,
    )

    return SuccessResponse(
        message="Recovery workflow created successfully.",
        data=RecoveryWorkflowResponse.model_validate(workflow),
    )


@router.post(
    "/{workflow_id}/execute",
    response_model=SuccessResponse[RecoveryWorkflowResponse],
)
async def execute_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    workflow = RecoveryWorkflowService.execute(
        db,
        workflow_id,
    )

    return SuccessResponse(
        message="Recovery workflow executed successfully.",
        data=RecoveryWorkflowResponse.model_validate(workflow),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[RecoveryWorkflowResponse]],
)
async def get_workflows(
    execution_status: ExecutionStatus | None = Query(default=None),
    action_type: RecoveryActionType | None = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    workflows = RecoveryWorkflowService.get_workflows(
        db=db,
        execution_status=execution_status,
        action_type=action_type,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="Recovery workflows retrieved successfully.",
        data=[
            RecoveryWorkflowResponse.model_validate(workflow)
            for workflow in workflows
        ],
    )


@router.get(
    "/{workflow_id}",
    response_model=SuccessResponse[RecoveryWorkflowResponse],
)
async def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    workflow = RecoveryWorkflowService.get_by_id(
        db,
        workflow_id,
    )

    return SuccessResponse(
        message="Recovery workflow retrieved successfully.",
        data=RecoveryWorkflowResponse.model_validate(workflow),
    )


@router.patch(
    "/{workflow_id}/cancel",
    response_model=SuccessResponse[RecoveryWorkflowResponse],
)
async def cancel_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    workflow = RecoveryWorkflowService.cancel(
        db,
        workflow_id,
    )

    return SuccessResponse(
        message="Recovery workflow cancelled successfully.",
        data=RecoveryWorkflowResponse.model_validate(workflow),
    )


@router.delete(
    "/{workflow_id}",
    response_model=SuccessResponse[RecoveryWorkflowResponse],
)
async def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    workflow = RecoveryWorkflowService.delete(
        db,
        workflow_id,
    )

    return SuccessResponse(
        message="Recovery workflow deleted successfully.",
        data=RecoveryWorkflowResponse.model_validate(workflow),
    )