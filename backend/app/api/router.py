"""
Central API Router.
"""

from fastapi import APIRouter
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.incident import router as incident_router
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