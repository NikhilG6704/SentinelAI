"""
Import all ORM models so Alembic can discover metadata.
"""

from app.db.base import Base

from app.models.infrastructure_asset import InfrastructureAsset
from app.models.monitoring_agent import MonitoringAgent
# Later:
# from app.models.system_metric import SystemMetric

target_metadata = Base.metadata