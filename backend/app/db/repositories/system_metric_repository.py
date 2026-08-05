"""
System Metric Repository.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.system_metric import SystemMetric


class SystemMetricRepository(BaseRepository[SystemMetric]):
    """
    Repository for System Metrics.
    """

    def __init__(self) -> None:
        super().__init__(SystemMetric)

    def get_latest_by_agent(
        self,
        db: Session,
        agent_id: int,
    ) -> SystemMetric | None:
        """
        Return the latest metric for a monitoring agent.
        """
        return (
            db.query(SystemMetric)
            .filter(SystemMetric.monitoring_agent_id == agent_id)
            .order_by(SystemMetric.collection_timestamp.desc())
            .first()
        )

    def get_history(
        self,
        db: Session,
        agent_id: int,
        skip: int = 0,
        limit: int = 100,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[SystemMetric]:
        """
        Return historical metrics for a monitoring agent.
        """

        query = (
            db.query(SystemMetric)
            .filter(SystemMetric.monitoring_agent_id == agent_id)
        )

        if start_time is not None:
            query = query.filter(
                SystemMetric.collection_timestamp >= start_time
            )

        if end_time is not None:
            query = query.filter(
                SystemMetric.collection_timestamp <= end_time
            )

        return (
            query.order_by(SystemMetric.collection_timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_latest_metrics(
        self,
        db: Session,
        limit: int = 100,
    ) -> list[SystemMetric]:
        """
        Return the most recent metrics across all monitoring agents.
        """

        return (
            db.query(SystemMetric)
            .order_by(SystemMetric.collection_timestamp.desc())
            .limit(limit)
            .all()
        )

    def bulk_create(
        self,
        db: Session,
        metrics: list[SystemMetric],
    ) -> None:
        """
        Bulk insert metrics.
        """

        db.add_all(metrics)
        db.commit()