from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.monitoring_agent_repository import (
    MonitoringAgentRepository,
)
from app.db.repositories.system_metric_repository import (
    SystemMetricRepository,
)
from app.models.system_metric import SystemMetric
from app.schemas.system_metric import SystemMetricCreate


class SystemMetricService:
    """
    Business logic for System Metrics.
    """

    repository = SystemMetricRepository()
    agent_repository = MonitoringAgentRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: SystemMetricCreate,
    ) -> SystemMetric:
        """
        Store a metrics snapshot and update the agent heartbeat.
        """

        agent = cls.agent_repository.get_by_id(
            db,
            request.monitoring_agent_id,
        )

        if agent is None:
            logger.warning(
                "Metrics rejected: Monitoring agent %s not found.",
                request.monitoring_agent_id,
            )
            raise ValueError("Monitoring agent not found.")

        if not agent.is_active:
            logger.warning(
                "Metrics rejected: Monitoring agent %s is inactive.",
                agent.id,
            )
            raise ValueError("Monitoring agent is inactive.")

        metric = SystemMetric(
            **request.model_dump(),
            collection_timestamp=datetime.now(timezone.utc),
        )

        metric = cls.repository.create(
            db,
            metric,
        )

        cls.agent_repository.update_heartbeat(
            db,
            agent,
        )

        logger.info(
            "Metrics received successfully for agent %s",
            agent.id,
        )

        return metric

    @classmethod
    def get_all(
        cls,
        db: Session,
    ):
        return cls.repository.get_all(db)

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        metric_id: int,
    ):
        return cls.repository.get_by_id(
            db,
            metric_id,
        )

    @classmethod
    def get_by_agent(
        cls,
        db: Session,
        agent_id: int,
    ):
        return cls.repository.get_by_agent(
            db,
            agent_id,
        )

    @classmethod
    def get_latest(
        cls,
        db: Session,
        agent_id: int,
    ):
        return cls.repository.get_latest_by_agent(
            db,
            agent_id,
        )

    @classmethod
    def get_history(
        cls,
        db: Session,
        agent_id: int,
        skip: int = 0,
        limit: int = 100,
        start_time=None,
        end_time=None,
    ):
        return cls.repository.get_history(
            db=db,
            agent_id=agent_id,
            skip=skip,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
        )

    @classmethod
    def bulk_create(
        cls,
        db: Session,
        metrics: list[SystemMetric],
    ) -> None:
        cls.repository.bulk_create(
            db,
            metrics,
        )