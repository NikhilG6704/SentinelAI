from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.system_log import LogLevel


class SystemLogCreate(BaseModel):
    infrastructure_asset_id: int
    monitoring_agent_id: int

    log_level: LogLevel

    source: str = Field(max_length=150)

    service_name: str = Field(max_length=150)

    message: str = Field(min_length=1)

    log_metadata: dict | None = None

    event_timestamp: datetime


class SystemLogUpdate(BaseModel):
    log_level: LogLevel | None = None
    source: str | None = None
    service_name: str | None = None
    message: str | None = None
    log_metadata: dict | None = None


class SystemLogResponse(BaseModel):
    id: int

    infrastructure_asset_id: int
    monitoring_agent_id: int

    log_level: LogLevel

    source: str

    service_name: str

    message: str

    log_metadata: dict | None

    event_timestamp: datetime

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )