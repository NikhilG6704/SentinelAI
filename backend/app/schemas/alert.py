from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.alert import (
    AlertSeverity,
    AlertStatus,
    MetricType,
)


class AlertCreate(BaseModel):
    infrastructure_asset_id: int
    monitoring_agent_id: int
    system_metric_id: int | None = None
    incident_id: int | None = None

    alert_title: str = Field(max_length=255)
    alert_description: str

    severity: AlertSeverity

    metric_name: MetricType
    metric_value: float
    threshold_value: float


class AlertUpdate(BaseModel):
    alert_title: str | None = None
    alert_description: str | None = None
    severity: AlertSeverity | None = None


class AlertAcknowledge(BaseModel):
    pass


class AlertResolve(BaseModel):
    resolution_summary: str


class AlertResponse(BaseModel):
    id: int

    infrastructure_asset_id: int
    monitoring_agent_id: int

    system_metric_id: int | None
    incident_id: int | None

    alert_title: str
    alert_description: str

    severity: AlertSeverity
    status: AlertStatus

    metric_name: MetricType
    metric_value: float
    threshold_value: float

    triggered_at: datetime
    acknowledged_at: datetime | None
    resolved_at: datetime | None

    resolution_summary: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )