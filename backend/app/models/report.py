from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    DateTime,
    Enum as SQLEnum,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ReportType(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    METRICS = "Metrics"
    INCIDENTS = "Incidents"
    ALERTS = "Alerts"
    LOGS = "Logs"
    EXECUTIVE = "Executive"


class ReportStatus(str, Enum):
    PENDING = "Pending"
    GENERATED = "Generated"
    FAILED = "Failed"


class Report(BaseModel):
    """
    Generated report metadata.
    """

    __tablename__ = "reports"

    report_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    report_type: Mapped[ReportType] = mapped_column(
        SQLEnum(
            ReportType,
            name="report_type_enum",
            native_enum=False,
        ),
        nullable=False,
    )

    generated_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    report_period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    report_period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    report_status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(
            ReportStatus,
            name="report_status_enum",
            native_enum=False,
        ),
        nullable=False,
        default=ReportStatus.PENDING,
    )

    report_metadata: Mapped[dict | None] = mapped_column(
        "report_metadata",
        JSON,
        nullable=True,
    )