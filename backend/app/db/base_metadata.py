"""
Expose SQLAlchemy metadata for Alembic.
"""

from app.db.base import Base

# Import every ORM model so SQLAlchemy registers them.
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.infrastructure_asset import InfrastructureAsset
from app.models.monitoring_agent import MonitoringAgent
from app.models.system_metric import SystemMetric

target_metadata = Base.metadata