"""
Monitoring Agent Repository.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.monitoring_agent import (
    AgentStatus,
    MonitoringAgent,
)


class MonitoringAgentRepository(BaseRepository[MonitoringAgent]):
    """
    Repository for Monitoring Agents.
    """

    def __init__(self) -> None:
        super().__init__(MonitoringAgent)

    def get_by_registration_token(
        self,
        db: Session,
        token: str,
    ) -> MonitoringAgent | None:

        return (
            db.query(MonitoringAgent)
            .filter(
                MonitoringAgent.registration_token == token,
                MonitoringAgent.is_active.is_(True),
            )
            .first()
        )

    def get_by_asset(
        self,
        db: Session,
        infrastructure_asset_id: int,
    ) -> list[MonitoringAgent]:

        return (
            db.query(MonitoringAgent)
            .filter(
                MonitoringAgent.infrastructure_asset_id == infrastructure_asset_id,
                MonitoringAgent.is_active.is_(True),
            )
            .all()
        )

    def update_heartbeat(
        self,
        db: Session,
        agent: MonitoringAgent,
    ) -> MonitoringAgent:
        """
        Update the monitoring agent heartbeat and mark it online.
        """

        agent.last_heartbeat = datetime.now(timezone.utc)
        agent.status = AgentStatus.ONLINE

        db.commit()
        db.refresh(agent)

        return agent

    def set_status(
        self,
        db: Session,
        agent: MonitoringAgent,
        status: AgentStatus,
    ) -> MonitoringAgent:
        """
        Update the monitoring agent status.
        """

        agent.status = status

        db.commit()
        db.refresh(agent)

        return agent

    def deactivate(
        self,
        db: Session,
        agent: MonitoringAgent,
    ) -> MonitoringAgent:
        """
        Soft delete a monitoring agent.
        """

        agent.is_active = False

        db.commit()
        db.refresh(agent)

        return agent