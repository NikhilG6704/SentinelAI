"""
Recovery Workflow Repository.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.recovery_workflow import (
    ExecutionStatus,
    RecoveryActionType,
    RecoveryWorkflow,
)


class RecoveryWorkflowRepository(BaseRepository[RecoveryWorkflow]):
    """
    Repository for Recovery Workflow management.
    """

    def __init__(self) -> None:
        super().__init__(RecoveryWorkflow)

    def get_workflows(
        self,
        db: Session,
        *,
        execution_status: ExecutionStatus | None = None,
        action_type: RecoveryActionType | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RecoveryWorkflow]:

        query = db.query(RecoveryWorkflow)

        if execution_status:
            query = query.filter(
                RecoveryWorkflow.execution_status == execution_status
            )

        if action_type:
            query = query.filter(
                RecoveryWorkflow.action_type == action_type
            )

        if hasattr(RecoveryWorkflow, "is_active"):
            query = query.filter(
                RecoveryWorkflow.is_active.is_(True)
            )

        return (
            query.order_by(
                RecoveryWorkflow.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        workflow: RecoveryWorkflow,
    ) -> RecoveryWorkflow:

        db.commit()
        db.refresh(workflow)

        return workflow

    def soft_delete(
        self,
        db: Session,
        workflow: RecoveryWorkflow,
    ) -> RecoveryWorkflow:

        if hasattr(workflow, "is_active"):
            workflow.is_active = False

        db.commit()
        db.refresh(workflow)

        return workflow