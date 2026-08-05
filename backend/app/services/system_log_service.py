"""
System Log Service.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.infrastructure_asset_repository import (
    InfrastructureAssetRepository,
)
from app.db.repositories.monitoring_agent_repository import (
    MonitoringAgentRepository,
)
from app.db.repositories.system_log_repository import (
    SystemLogRepository,
)
from app.models.system_log import (
    LogLevel,
    SystemLog,
)
from app.schemas.system_log import (
    SystemLogCreate,
)


class SystemLogService:
    """
    Business logic for System Logs.
    """

    repository = SystemLogRepository()
    asset_repository = InfrastructureAssetRepository()
    agent_repository = MonitoringAgentRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: SystemLogCreate,
    ) -> SystemLog:

        asset = cls.asset_repository.get_by_id(
            db,
            request.infrastructure_asset_id,
        )

        if asset is None:
            raise ValueError("Infrastructure asset not found.")

        agent = cls.agent_repository.get_by_id(
            db,
            request.monitoring_agent_id,
        )

        if agent is None:
            raise ValueError("Monitoring agent not found.")

        log = SystemLog(
            **request.model_dump(),
        )

        logger.info(
            "System log received from agent %s.",
            request.monitoring_agent_id,
        )

        return cls.repository.create(
            db,
            log,
        )

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        log_id: int,
    ):

        return cls.repository.get_by_id(
            db,
            log_id,
        )

    @classmethod
    def search(
        cls,
        db: Session,
        **kwargs,
    ):

        return cls.repository.search(
            db,
            **kwargs,
        )

    @classmethod
    def delete(
        cls,
        db: Session,
        log_id: int,
    ):

        log = cls.repository.get_by_id(
            db,
            log_id,
        )

        if log is None:
            raise ValueError(
                "System log not found."
            )

        logger.info(
            "System log %s deleted.",
            log.id,
        )

        return cls.repository.soft_delete(
            db,
            log,
        )