from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.incident import (
    IncidentSeverity,
    IncidentStatus,
)


class IncidentCreate(BaseModel):
    infrastructure_asset_id: int
    monitoring_agent_id: int | None = None

    incident_title: str = Field(max_length=255)
    incident_description: str

    severity: IncidentSeverity


class IncidentUpdate(BaseModel):
    incident_title: str | None = Field(
        default=None,
        max_length=255,
    )
    incident_description: str | None = None
    severity: IncidentSeverity | None = None
    status: IncidentStatus | None = None


class IncidentResolve(BaseModel):
    resolution_summary: str


class IncidentResponse(BaseModel):
    id: int

    infrastructure_asset_id: int
    monitoring_agent_id: int | None

    incident_title: str
    incident_description: str

    severity: IncidentSeverity
    status: IncidentStatus

    detected_at: datetime
    resolved_at: datetime | None

    resolution_summary: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )