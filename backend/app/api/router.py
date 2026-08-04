"""
Central API Router.

This module is responsible for registering all API routers
used by the SentinelAI application.
"""

from fastapi import APIRouter

from app.api.routes.health import router as health_router

api_router = APIRouter()

# Register routers
api_router.include_router(health_router)