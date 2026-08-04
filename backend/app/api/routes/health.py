"""
Health and root endpoints.
"""

from pydantic import BaseModel
from fastapi import APIRouter

from app.core.config import settings
from app.schemas.response import SuccessResponse

router = APIRouter(tags=["Health"])


class RootData(BaseModel):
    application: str
    version: str
    status: str


class HealthData(BaseModel):
    status: str


@router.get(
    "/",
    summary="Root Endpoint",
    response_model=SuccessResponse[RootData],
)
async def root() -> SuccessResponse[RootData]:
    """
    Root endpoint.

    Returns basic application information.
    """
    return SuccessResponse(
        message="SentinelAI Backend Running",
        data=RootData(
            application=settings.PROJECT_NAME,
            version=settings.VERSION,
            status="running",
        ),
    )


@router.get(
    "/health",
    summary="Health Check",
    response_model=SuccessResponse[HealthData],
)
async def health() -> SuccessResponse[HealthData]:
    """
    Health check endpoint.
    """
    return SuccessResponse(
        message="Health Check Successful",
        data=HealthData(
            status="healthy",
        ),
    )