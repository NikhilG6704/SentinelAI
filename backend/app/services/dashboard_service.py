from sqlalchemy.orm import Session

from app.db.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    repository = DashboardRepository()

    @classmethod
    def get_overview(cls, db: Session):
        return cls.repository.get_overview(db)

    @classmethod
    def get_health(cls, db: Session):
        return cls.repository.get_health(db)

    @classmethod
    def get_agent_summary(cls, db: Session):
        return cls.repository.get_agent_summary(db)

    @classmethod
    def get_trends(cls, db: Session):
        return cls.repository.get_trends(db)