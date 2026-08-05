"""
Monitoring Agent Repository.
"""

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.monitoring_agent import MonitoringAgent


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