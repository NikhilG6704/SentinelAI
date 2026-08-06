from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.audit_log import AuditAction
from app.schemas.audit_log import (
    AuditLogCreate,
    AuditLogResponse,
)
from app.schemas.response import SuccessResponse
from app.services.audit_log_service import AuditLogService

router = APIRouter(
    prefix="/api/v1/audit-logs",
    tags=["Audit Logs"],
)


@router.post(
    "",
    response_model=SuccessResponse[AuditLogResponse],
    status_code=201,
)
async def create_audit_log(
    request: AuditLogCreate,
    db: Session = Depends(get_db),
):
    audit_log = AuditLogService.create(
        db,
        request,
    )

    return SuccessResponse(
        message="Audit log created successfully.",
        data=AuditLogResponse.model_validate(audit_log),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[AuditLogResponse]],
)
async def get_audit_logs(
    action: AuditAction | None = Query(default=None),
    entity_type: str | None = None,
    performed_by: str | None = None,
    keyword: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logs = AuditLogService.get_logs(
        db=db,
        action=action,
        entity_type=entity_type,
        performed_by=performed_by,
        keyword=keyword,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="Audit logs retrieved successfully.",
        data=[
            AuditLogResponse.model_validate(log)
            for log in logs
        ],
    )


@router.get(
    "/{audit_log_id}",
    response_model=SuccessResponse[AuditLogResponse],
)
async def get_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
):
    audit_log = AuditLogService.get_by_id(
        db,
        audit_log_id,
    )

    return SuccessResponse(
        message="Audit log retrieved successfully.",
        data=AuditLogResponse.model_validate(audit_log),
    )