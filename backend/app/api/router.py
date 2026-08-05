"""
Central API Router.
"""

from fastapi import APIRouter
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.incident import router as incident_router
from app.api.routes.alert import router as alert_router
from app.api.routes.system_log import router as system_log_router
from app.api.routes.notification import router as notification_router
from app.api.routes.report import router as report_router
from app.api.routes.automation_rule import router as automation_rule_router
from app.api.routes.infrastructure_asset import (
    router as infrastructure_asset_router,
)
from app.api.routes.monitoring_agent import (
    router as monitoring_agent_router,
)
from app.api.routes.system_metric import (
    router as system_metric_router,
)
api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(infrastructure_asset_router)
api_router.include_router(monitoring_agent_router)
api_router.include_router(system_metric_router)
api_router.include_router(dashboard_router)
api_router.include_router(incident_router)
api_router.include_router(alert_router)
api_router.include_router(system_log_router)
api_router.include_router(notification_router)
api_router.include_router(report_router)
api_router.include_router(automation_rule_router)