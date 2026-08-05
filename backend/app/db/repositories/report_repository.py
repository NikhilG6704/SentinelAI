"""
Report Repository.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.infrastructure_asset import InfrastructureAsset
from app.models.monitoring_agent import MonitoringAgent
from app.models.report import (
    Report,
    ReportStatus,
    ReportType,
)
from app.models.system_metric import SystemMetric


class ReportRepository(BaseRepository[Report]):
    """
    Repository for Report management.
    """

    def __init__(self) -> None:
        super().__init__(Report)

    def get_reports(
        self,
        db: Session,
        *,
        report_type: ReportType | None = None,
        report_status: ReportStatus | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Report]:

        query = db.query(Report)

        if report_type:
            query = query.filter(
                Report.report_type == report_type
            )

        if report_status:
            query = query.filter(
                Report.report_status == report_status
            )

        if start_date:
            query = query.filter(
                Report.report_period_start >= start_date
            )

        if end_date:
            query = query.filter(
                Report.report_period_end <= end_date
            )

        return (
            query.order_by(
                Report.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_summary(
        self,
        db: Session,
    ) -> dict:

        infrastructure_summary = {
            "total_assets": db.query(
                func.count(InfrastructureAsset.id)
            ).scalar() or 0,
            "healthy_assets": db.query(
                func.count(InfrastructureAsset.id)
            ).filter(
                InfrastructureAsset.status == "Healthy"
            ).scalar() or 0,
        }

        monitoring_summary = {
            "total_agents": db.query(
                func.count(MonitoringAgent.id)
            ).scalar() or 0,
            "online_agents": db.query(
                func.count(MonitoringAgent.id)
            ).filter(
                MonitoringAgent.status == "Online"
            ).scalar() or 0,
        }

        alert_summary = {
            "total_alerts": db.query(
                func.count(Alert.id)
            ).scalar() or 0,
            "active_alerts": db.query(
                func.count(Alert.id)
            ).filter(
                Alert.status == "Active"
            ).scalar() or 0,
        }

        incident_summary = {
            "total_incidents": db.query(
                func.count(Incident.id)
            ).scalar() or 0,
            "open_incidents": db.query(
                func.count(Incident.id)
            ).filter(
                Incident.status == "Open"
            ).scalar() or 0,
        }

        metrics_summary = {
            "total_metrics": db.query(
                func.count(SystemMetric.id)
            ).scalar() or 0,
            "average_cpu": round(
                db.query(
                    func.avg(SystemMetric.cpu_usage)
                ).scalar() or 0,
                2,
            ),
            "average_memory": round(
                db.query(
                    func.avg(SystemMetric.memory_usage)
                ).scalar() or 0,
                2,
            ),
            "average_disk": round(
                db.query(
                    func.avg(SystemMetric.disk_usage)
                ).scalar() or 0,
                2,
            ),
        }

        return {
            "infrastructure_summary": infrastructure_summary,
            "monitoring_summary": monitoring_summary,
            "alert_summary": alert_summary,
            "incident_summary": incident_summary,
            "metrics_summary": metrics_summary,
        }

    def soft_delete(
        self,
        db: Session,
        report: Report,
    ) -> Report:

        report.is_active = False

        db.commit()
        db.refresh(report)

        return report