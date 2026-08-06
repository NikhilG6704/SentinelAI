from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.audit_log import (
    AuditAction,
    AuditStatus,
)


class AuditLogCreate(BaseModel):
    entity_type: str = Field(max_length=100)

    entity_id: int

    action: AuditAction

    performed_by: str = Field(max_length=255)

    performed_at: datetime

    status: AuditStatus

    source_module: str = Field(max_length=100)

    ip_address: str | None = None

    metadata_json: dict | None = None

    details: str | None = None


class AuditLogResponse(BaseModel):
    id: int

    entity_type: str

    entity_id: int

    action: AuditAction

    performed_by: str

    performed_at: datetime

    status: AuditStatus

    source_module: str

    ip_address: str | None

    metadata_json: dict | None

    details: str | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )