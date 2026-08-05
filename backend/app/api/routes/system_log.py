from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.system_log import LogLevel
from app.schemas.response import SuccessResponse
from app.schemas.system_log import (
    SystemLogCreate,
    SystemLogResponse,
)
from app.services.system_log_service import SystemLogService

router = APIRouter(
    prefix="/api/v1/system-logs",
    tags=["System Logs"],
)


@router.post(
    "",
    response_model=SuccessResponse[SystemLogResponse],
    status_code=201,
)
async def create_log(
    request: SystemLogCreate,
    db: Session = Depends(get_db),
):
    log = SystemLogService.create(
        db,
        request,
    )

    return SuccessResponse(
        message="System log stored successfully.",
        data=SystemLogResponse.model_validate(log),
    )


@router.get(
    "/{log_id}",
    response_model=SuccessResponse[SystemLogResponse],
)
async def get_log(
    log_id: int,
    db: Session = Depends(get_db),
):
    log = SystemLogService.get_by_id(
        db,
        log_id,
    )

    return SuccessResponse(
        message="System log retrieved successfully.",
        data=SystemLogResponse.model_validate(log),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[SystemLogResponse]],
)
async def search_logs(
    log_level: LogLevel | None = Query(default=None),
    service_name: str | None = None,
    source: str | None = None,
    keyword: str | None = None,
    infrastructure_asset_id: int | None = None,
    monitoring_agent_id: int | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logs = SystemLogService.search(
        db=db,
        log_level=log_level,
        service_name=service_name,
        source=source,
        keyword=keyword,
        infrastructure_asset_id=infrastructure_asset_id,
        monitoring_agent_id=monitoring_agent_id,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="System logs retrieved successfully.",
        data=[
            SystemLogResponse.model_validate(log)
            for log in logs
        ],
    )


@router.delete(
    "/{log_id}",
    response_model=SuccessResponse[SystemLogResponse],
)
async def delete_log(
    log_id: int,
    db: Session = Depends(get_db),
):
    log = SystemLogService.delete(
        db,
        log_id,
    )

    return SuccessResponse(
        message="System log deleted successfully.",
        data=SystemLogResponse.model_validate(log),
    )