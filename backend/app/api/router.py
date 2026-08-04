"""
Central API Router.
"""

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.infrastructure_asset import (
    router as infrastructure_asset_router,
)

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(infrastructure_asset_router)