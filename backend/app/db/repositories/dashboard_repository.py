from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.infrastructure_asset import InfrastructureAsset
from app.models.monitoring_agent import MonitoringAgent
from app.models.system_metric import SystemMetric


class DashboardRepository:

    @staticmethod
    def get_overview(db: Session):

        total_assets = db.query(func.count(InfrastructureAsset.id)).scalar() or 0

        total_agents = db.query(func.count(MonitoringAgent.id)).scalar() or 0

        online_agents = (
            db.query(func.count(MonitoringAgent.id))
            .filter(MonitoringAgent.status == "ONLINE")
            .scalar()
            or 0
        )

        offline_agents = total_agents - online_agents

        total_metrics = db.query(func.count(SystemMetric.id)).scalar() or 0

        healthy_assets = (
            db.query(func.count(InfrastructureAsset.id))
            .filter(InfrastructureAsset.status == "Healthy")
            .scalar()
            or 0
        )

        warning_assets = (
            db.query(func.count(InfrastructureAsset.id))
            .filter(InfrastructureAsset.status == "Warning")
            .scalar()
            or 0
        )

        critical_assets = (
            db.query(func.count(InfrastructureAsset.id))
            .filter(InfrastructureAsset.status == "Critical")
            .scalar()
            or 0
        )

        return {
            "total_assets": total_assets,
            "total_agents": total_agents,
            "online_agents": online_agents,
            "offline_agents": offline_agents,
            "total_metrics": total_metrics,
            "healthy_assets": healthy_assets,
            "warning_assets": warning_assets,
            "critical_assets": critical_assets,
        }

    @staticmethod
    def get_health(db: Session):

        avg_cpu = db.query(func.avg(SystemMetric.cpu_usage)).scalar() or 0

        avg_memory = db.query(func.avg(SystemMetric.memory_usage)).scalar() or 0

        avg_disk = db.query(func.avg(SystemMetric.disk_usage)).scalar() or 0

        avg_network = (
            db.query(
                func.avg(
                    (SystemMetric.network_in + SystemMetric.network_out) / 2
                )
            ).scalar()
            or 0
        )

        health_score = round(
            100 - ((avg_cpu + avg_memory + avg_disk) / 3),
            2,
        )

        return {
            "average_cpu_usage": round(avg_cpu, 2),
            "average_memory_usage": round(avg_memory, 2),
            "average_disk_usage": round(avg_disk, 2),
            "average_network_usage": round(avg_network, 2),
            "health_score": max(0, health_score),
        }

    @staticmethod
    def get_agent_summary(db: Session):

        agents = db.query(MonitoringAgent).all()

        summaries = []

        for agent in agents:

            latest_metric = (
                db.query(SystemMetric)
                .filter(SystemMetric.monitoring_agent_id == agent.id)
                .order_by(desc(SystemMetric.collection_timestamp))
                .first()
            )

            summaries.append(
                {
                    "agent_id": agent.id,
                    "hostname": (
                        agent.infrastructure_asset.hostname
                        if agent.infrastructure_asset
                        else "Unknown"
                    ),
                    "latest_cpu": (
                        latest_metric.cpu_usage
                        if latest_metric
                        else 0
                    ),
                    "latest_memory": (
                        latest_metric.memory_usage
                        if latest_metric
                        else 0
                    ),
                    "latest_disk": (
                        latest_metric.disk_usage
                        if latest_metric
                        else 0
                    ),
                    "status": (
                        agent.status.value
                        if hasattr(agent.status, "value")
                        else str(agent.status)
                    ),
                    "last_heartbeat": agent.last_heartbeat,
                }
            )

        return summaries

    @staticmethod
    def get_trends(db: Session):

        return (
            db.query(SystemMetric)
            .order_by(SystemMetric.collection_timestamp.desc())
            .limit(100)
            .all()
        )