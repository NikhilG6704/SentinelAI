from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.incident import (
    IncidentSeverity,
    IncidentStatus,
)
from app.schemas.incident import (
    IncidentCreate,
    IncidentResolve,
    IncidentResponse,
    IncidentUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.incident_service import IncidentService

router = APIRouter(
    prefix="/api/v1/incidents",
    tags=["Incidents"],
)


@router.post(
    "",
    response_model=SuccessResponse[IncidentResponse],
    status_code=201,
)
async def create_incident(
    request: IncidentCreate,
    db: Session = Depends(get_db),
):
    incident = IncidentService.create(
        db,
        request,
    )

    return SuccessResponse(
        message="Incident created successfully.",
        data=IncidentResponse.model_validate(incident),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[IncidentResponse]],
)
async def get_incidents(
    status: IncidentStatus | None = Query(default=None),
    severity: IncidentSeverity | None = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    incidents = IncidentService.get_all(
        db=db,
        status=status,
        severity=severity,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="Incidents retrieved successfully.",
        data=[
            IncidentResponse.model_validate(i)
            for i in incidents
        ],
    )


@router.get(
    "/{incident_id}",
    response_model=SuccessResponse[IncidentResponse],
)
async def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = IncidentService.get_by_id(
        db,
        incident_id,
    )

    return SuccessResponse(
        message="Incident retrieved successfully.",
        data=IncidentResponse.model_validate(incident),
    )


@router.put(
    "/{incident_id}",
    response_model=SuccessResponse[IncidentResponse],
)
async def update_incident(
    incident_id: int,
    request: IncidentUpdate,
    db: Session = Depends(get_db),
):
    incident = IncidentService.update(
        db,
        incident_id,
        request,
    )

    return SuccessResponse(
        message="Incident updated successfully.",
        data=IncidentResponse.model_validate(incident),
    )


@router.patch(
    "/{incident_id}/resolve",
    response_model=SuccessResponse[IncidentResponse],
)
async def resolve_incident(
    incident_id: int,
    request: IncidentResolve,
    db: Session = Depends(get_db),
):
    incident = IncidentService.resolve(
        db,
        incident_id,
        request,
    )

    return SuccessResponse(
        message="Incident resolved successfully.",
        data=IncidentResponse.model_validate(incident),
    )


@router.patch(
    "/{incident_id}/close",
    response_model=SuccessResponse[IncidentResponse],
)
async def close_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = IncidentService.close(
        db,
        incident_id,
    )

    return SuccessResponse(
        message="Incident closed successfully.",
        data=IncidentResponse.model_validate(incident),
    )