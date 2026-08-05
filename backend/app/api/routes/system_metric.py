from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.response import SuccessResponse
from app.schemas.system_metric import (
    SystemMetricCreate,
    SystemMetricResponse,
)
from app.services.system_metric_service import SystemMetricService

router = APIRouter(
    prefix="/api/v1/system-metrics",
    tags=["System Metrics"],
)


@router.post(
    "",
    response_model=SuccessResponse[SystemMetricResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_metric(
    request: SystemMetricCreate,
    db: Session = Depends(get_db),
):
    try:
        metric = SystemMetricService.create(db, request)

        return SuccessResponse(
            message="Metric stored successfully.",
            data=SystemMetricResponse.model_validate(metric),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=SuccessResponse[list[SystemMetricResponse]],
)
async def get_metrics(
    db: Session = Depends(get_db),
):
    metrics = SystemMetricService.get_all(db)

    return SuccessResponse(
        message="Metrics retrieved successfully.",
        data=[
            SystemMetricResponse.model_validate(metric)
            for metric in metrics
        ],
    )


@router.get(
    "/{metric_id}",
    response_model=SuccessResponse[SystemMetricResponse],
)
async def get_metric(
    metric_id: int,
    db: Session = Depends(get_db),
):
    metric = SystemMetricService.get_by_id(
        db,
        metric_id,
    )

    if metric is None:
        raise HTTPException(
            status_code=404,
            detail="Metric not found.",
        )

    return SuccessResponse(
        message="Metric retrieved successfully.",
        data=SystemMetricResponse.model_validate(metric),
    )


@router.get(
    "/agent/{agent_id}",
    response_model=SuccessResponse[list[SystemMetricResponse]],
)
async def get_metrics_by_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    metrics = SystemMetricService.get_by_agent(
        db,
        agent_id,
    )

    return SuccessResponse(
        message="Agent metrics retrieved successfully.",
        data=[
            SystemMetricResponse.model_validate(metric)
            for metric in metrics
        ],
    )