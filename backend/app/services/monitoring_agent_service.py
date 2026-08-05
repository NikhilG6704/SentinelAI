"""
Monitoring Agent Service.
"""

from datetime import datetime, timezone
import secrets

from sqlalchemy.orm import Session

from app.db.repositories.monitoring_agent_repository import (
    MonitoringAgentRepository,
)
from app.models.monitoring_agent import (
    AgentStatus,
    MonitoringAgent,
)
from app.schemas.monitoring_agent import (
    MonitoringAgentCreate,
    MonitoringAgentUpdate,
)


class MonitoringAgentService:

    repository = MonitoringAgentRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        agent_data: MonitoringAgentCreate,
    ) -> MonitoringAgent:

        token = secrets.token_hex(32)

        agent = MonitoringAgent(
            infrastructure_asset_id=agent_data.infrastructure_asset_id,
            agent_name=agent_data.agent_name,
            agent_version=agent_data.agent_version,
            registration_token=token,
            last_heartbeat=datetime.now(timezone.utc),
            status=AgentStatus.ONLINE,
            is_active=True,
        )

        return cls.repository.create(db, agent)

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
        agent_id: int,
    ):

        return cls.repository.get_by_id(db, agent_id)

    @classmethod
    def get_by_asset(
        cls,
        db: Session,
        asset_id: int,
    ):

        return cls.repository.get_by_asset(db, asset_id)

    @classmethod
    def update(
        cls,
        db: Session,
        agent: MonitoringAgent,
        data: MonitoringAgentUpdate,
    ):

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(agent, key, value)

        return cls.repository.update(db, agent)

    @classmethod
    def heartbeat(
        cls,
        db: Session,
        agent: MonitoringAgent,
    ):

        agent.last_heartbeat = datetime.now(timezone.utc)
        agent.status = AgentStatus.ONLINE

        return cls.repository.update(db, agent)

    @classmethod
    def soft_delete(
        cls,
        db: Session,
        agent: MonitoringAgent,
    ):

        return cls.repository.soft_delete(db, agent)