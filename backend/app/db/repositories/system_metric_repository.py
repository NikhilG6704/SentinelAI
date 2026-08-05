from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.system_metric import SystemMetric


class SystemMetricRepository(BaseRepository[SystemMetric]):

    def __init__(self):
        super().__init__(SystemMetric)

    def get_by_agent(
        self,
        db: Session,
        agent_id: int,
    ):
        return (
            db.query(SystemMetric)
            .filter(SystemMetric.monitoring_agent_id == agent_id)
            .order_by(SystemMetric.collection_timestamp.desc())
            .all()
        )