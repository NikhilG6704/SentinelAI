from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.repositories.monitoring_agent_repository import (
    MonitoringAgentRepository,
)
from app.db.repositories.system_metric_repository import (
    SystemMetricRepository,
)
from app.models.system_metric import SystemMetric
from app.schemas.system_metric import SystemMetricCreate


class SystemMetricService:

    repository = SystemMetricRepository()
    agent_repository = MonitoringAgentRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: SystemMetricCreate,
    ) -> SystemMetric:

        agent = cls.agent_repository.get_by_id(
            db,
            request.monitoring_agent_id,
        )

        if agent is None:
            raise ValueError("Monitoring agent not found.")

        metric = SystemMetric(
            **request.model_dump(),
            collection_timestamp=datetime.now(timezone.utc),
        )

        return cls.repository.create(
            db,
            metric,
        )

    @classmethod
    def get_all(cls, db: Session):
        return cls.repository.get_all(db)

    @classmethod
    def get_by_id(cls, db: Session, metric_id: int):
        return cls.repository.get_by_id(db, metric_id)

    @classmethod
    def get_by_agent(cls, db: Session, agent_id: int):
        return cls.repository.get_by_agent(
            db,
            agent_id,
        )