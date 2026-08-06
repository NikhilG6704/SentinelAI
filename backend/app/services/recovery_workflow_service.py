"""
Recovery Workflow Service.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.automation_rule_repository import AutomationRuleRepository
from app.db.repositories.infrastructure_asset_repository import (
    InfrastructureAssetRepository,
)
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.recovery_workflow_repository import (
    RecoveryWorkflowRepository,
)
from app.models.recovery_workflow import (
    ExecutionMode,
    ExecutionStatus,
    RecoveryWorkflow,
)
from app.schemas.recovery_workflow import RecoveryWorkflowCreate


class RecoveryWorkflowService:
    """
    Business logic for Recovery Workflow Engine.
    """

    repository = RecoveryWorkflowRepository()
    automation_repository = AutomationRuleRepository()
    asset_repository = InfrastructureAssetRepository()
    incident_repository = IncidentRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: RecoveryWorkflowCreate,
    ) -> RecoveryWorkflow:

        rule = cls.automation_repository.get_by_id(
            db,
            request.automation_rule_id,
        )

        if rule is None:
            raise ValueError("Automation rule not found.")

        asset = cls.asset_repository.get_by_id(
            db,
            request.infrastructure_asset_id,
        )

        if asset is None:
            raise ValueError("Infrastructure asset not found.")

        if request.incident_id is not None:
            incident = cls.incident_repository.get_by_id(
                db,
                request.incident_id,
            )

            if incident is None:
                raise ValueError("Incident not found.")

        workflow = RecoveryWorkflow(
            **request.model_dump(),
            execution_mode=ExecutionMode.SIMULATION,
            execution_status=ExecutionStatus.PENDING,
        )

        logger.info(
            "Recovery workflow '%s' created.",
            workflow.workflow_name,
        )

        return cls.repository.create(
            db,
            workflow,
        )

    @classmethod
    def execute(
        cls,
        db: Session,
        workflow_id: int,
    ) -> RecoveryWorkflow:

        workflow = cls.repository.get_by_id(
            db,
            workflow_id,
        )

        if workflow is None:
            raise ValueError("Workflow not found.")

        if workflow.execution_status == ExecutionStatus.CANCELLED:
            raise ValueError(
                "Cancelled workflow cannot be executed."
            )

        workflow.execution_status = ExecutionStatus.RUNNING
        workflow.started_at = datetime.now(timezone.utc)

        workflow.execution_log = (
            f"[{workflow.started_at.isoformat()}] "
            f"Simulation started.\n"
            f"Simulated action: {workflow.action_type.value}"
        )

        workflow.execution_status = ExecutionStatus.COMPLETED
        workflow.completed_at = datetime.now(timezone.utc)

        workflow.execution_log += (
            f"\n[{workflow.completed_at.isoformat()}] "
            "Simulation completed successfully."
        )

        logger.info(
            "Recovery workflow %s executed in simulation mode.",
            workflow.id,
        )

        return cls.repository.update(
            db,
            workflow,
        )

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        workflow_id: int,
    ) -> RecoveryWorkflow | None:

        return cls.repository.get_by_id(
            db,
            workflow_id,
        )

    @classmethod
    def get_workflows(
        cls,
        db: Session,
        **kwargs,
    ) -> list[RecoveryWorkflow]:

        return cls.repository.get_workflows(
            db,
            **kwargs,
        )

    @classmethod
    def cancel(
        cls,
        db: Session,
        workflow_id: int,
    ) -> RecoveryWorkflow:

        workflow = cls.repository.get_by_id(
            db,
            workflow_id,
        )

        if workflow is None:
            raise ValueError("Workflow not found.")

        if workflow.execution_status != ExecutionStatus.PENDING:
            raise ValueError(
                "Only pending workflows can be cancelled."
            )

        workflow.execution_status = ExecutionStatus.CANCELLED

        logger.info(
            "Recovery workflow %s cancelled.",
            workflow.id,
        )

        return cls.repository.update(
            db,
            workflow,
        )

    @classmethod
    def delete(
        cls,
        db: Session,
        workflow_id: int,
    ) -> RecoveryWorkflow:

        workflow = cls.repository.get_by_id(
            db,
            workflow_id,
        )

        if workflow is None:
            raise ValueError("Workflow not found.")

        logger.info(
            "Recovery workflow %s deleted.",
            workflow.id,
        )

        return cls.repository.soft_delete(
            db,
            workflow,
        )