from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.report import (
    ReportStatus,
    ReportType,
)


class ReportCreate(BaseModel):
    report_name: str = Field(max_length=255)

    report_type: ReportType

    generated_by: str = Field(max_length=255)

    report_period_start: datetime

    report_period_end: datetime

    report_metadata: dict | None = None


class ReportResponse(BaseModel):
    id: int

    report_name: str

    report_type: ReportType

    generated_by: str

    report_period_start: datetime

    report_period_end: datetime

    generated_at: datetime | None

    report_status: ReportStatus

    report_metadata: dict | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ReportSummary(BaseModel):
    infrastructure_summary: dict

    monitoring_summary: dict

    alert_summary: dict

    incident_summary: dict

    metrics_summary: dict


class ReportStatusUpdate(BaseModel):
    report_status: ReportStatus