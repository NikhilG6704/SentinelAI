from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.report import (
    ReportStatus,
    ReportType,
)
from app.schemas.report import (
    ReportCreate,
    ReportResponse,
    ReportSummary,
)
from app.schemas.response import SuccessResponse
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"],
)


@router.post(
    "",
    response_model=SuccessResponse[ReportResponse],
    status_code=201,
)
async def generate_report(
    request: ReportCreate,
    db: Session = Depends(get_db),
):
    report = ReportService.create(
        db,
        request,
    )

    return SuccessResponse(
        message="Report generated successfully.",
        data=ReportResponse.model_validate(report),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[ReportResponse]],
)
async def get_reports(
    report_type: ReportType | None = Query(default=None),
    report_status: ReportStatus | None = Query(default=None),
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    reports = ReportService.get_reports(
        db=db,
        report_type=report_type,
        report_status=report_status,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="Reports retrieved successfully.",
        data=[
            ReportResponse.model_validate(report)
            for report in reports
        ],
    )


@router.get(
    "/{report_id}",
    response_model=SuccessResponse[ReportResponse],
)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
):
    report = ReportService.get_by_id(
        db,
        report_id,
    )

    return SuccessResponse(
        message="Report retrieved successfully.",
        data=ReportResponse.model_validate(report),
    )


@router.get(
    "/{report_id}/summary",
    response_model=SuccessResponse[ReportSummary],
)
async def get_report_summary(
    report_id: int,
    db: Session = Depends(get_db),
):
    summary = ReportService.get_summary(
        db,
        report_id,
    )

    return SuccessResponse(
        message="Report summary retrieved successfully.",
        data=ReportSummary(**summary),
    )


@router.delete(
    "/{report_id}",
    response_model=SuccessResponse[ReportResponse],
)
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
):
    report = ReportService.delete(
        db,
        report_id,
    )

    return SuccessResponse(
        message="Report deleted successfully.",
        data=ReportResponse.model_validate(report),
    )