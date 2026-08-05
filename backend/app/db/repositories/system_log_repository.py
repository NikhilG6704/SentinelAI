"""
System Log Repository.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.system_log import (
    LogLevel,
    SystemLog,
)


class SystemLogRepository(BaseRepository[SystemLog]):
    """
    Repository for System Logs.
    """

    def __init__(self) -> None:
        super().__init__(SystemLog)

    def search(
        self,
        db: Session,
        *,
        log_level: LogLevel | None = None,
        service_name: str | None = None,
        source: str | None = None,
        keyword: str | None = None,
        infrastructure_asset_id: int | None = None,
        monitoring_agent_id: int | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SystemLog]:

        query = db.query(SystemLog)

        if log_level:
            query = query.filter(SystemLog.log_level == log_level)

        if service_name:
            query = query.filter(
                SystemLog.service_name.ilike(f"%{service_name}%")
            )

        if source:
            query = query.filter(
                SystemLog.source.ilike(f"%{source}%")
            )

        if keyword:
            query = query.filter(
                or_(
                    SystemLog.message.ilike(f"%{keyword}%"),
                    SystemLog.service_name.ilike(f"%{keyword}%"),
                    SystemLog.source.ilike(f"%{keyword}%"),
                )
            )

        if infrastructure_asset_id:
            query = query.filter(
                SystemLog.infrastructure_asset_id
                == infrastructure_asset_id
            )

        if monitoring_agent_id:
            query = query.filter(
                SystemLog.monitoring_agent_id
                == monitoring_agent_id
            )

        if start_time:
            query = query.filter(
                SystemLog.event_timestamp >= start_time
            )

        if end_time:
            query = query.filter(
                SystemLog.event_timestamp <= end_time
            )

        return (
            query.order_by(SystemLog.event_timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def soft_delete(
        self,
        db: Session,
        log: SystemLog,
    ) -> SystemLog:

        log.is_active = False

        db.commit()
        db.refresh(log)

        return log