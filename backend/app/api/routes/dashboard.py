from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.dashboard import (
    AgentSummary,
    DashboardHealth,
    DashboardOverview,
)
from app.schemas.response import SuccessResponse
from app.schemas.system_metric import SystemMetricResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/overview",
    response_model=SuccessResponse[DashboardOverview],
)
async def overview(
    db: Session = Depends(get_db),
):
    data = DashboardService.get_overview(db)

    return SuccessResponse(
        message="Dashboard overview retrieved successfully.",
        data=DashboardOverview(**data),
    )


@router.get(
    "/health",
    response_model=SuccessResponse[DashboardHealth],
)
async def health(
    db: Session = Depends(get_db),
):
    data = DashboardService.get_health(db)

    return SuccessResponse(
        message="Infrastructure health retrieved successfully.",
        data=DashboardHealth(**data),
    )


@router.get(
    "/agents",
    response_model=SuccessResponse[list[AgentSummary]],
)
async def agents(
    db: Session = Depends(get_db),
):
    data = DashboardService.get_agent_summary(db)

    return SuccessResponse(
        message="Agent summary retrieved successfully.",
        data=[
            AgentSummary(**agent)
            for agent in data
        ],
    )


@router.get(
    "/trends",
    response_model=SuccessResponse[list[SystemMetricResponse]],
)
async def trends(
    db: Session = Depends(get_db),
):
    metrics = DashboardService.get_trends(db)

    return SuccessResponse(
        message="Infrastructure trends retrieved successfully.",
        data=[
            SystemMetricResponse.model_validate(metric)
            for metric in metrics
        ],
    )