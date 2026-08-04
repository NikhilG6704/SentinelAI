"""
Health and root endpoints.

Contains endpoints used to verify that the application
is running correctly.
"""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/", summary="Root Endpoint")
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns basic application information.
    """
    return {
        "application": settings.PROJECT_NAME,
        "status": "running",
        "version": settings.VERSION,
    }


@router.get("/health", summary="Health Check")
async def health() -> dict[str, str]:
    """
    Health check endpoint.

    Used to verify that the API is running.
    """
    return {
        "status": "healthy",
    }