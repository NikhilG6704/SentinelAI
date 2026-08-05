from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.alert import (
    AlertSeverity,
    AlertStatus,
)
from app.schemas.alert import (
    AlertCreate,
    AlertResolve,
    AlertResponse,
    AlertUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.alert_service import AlertService

router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["Alerts"],
)


@router.post(
    "",
    response_model=SuccessResponse[AlertResponse],
    status_code=201,
)
async def create_alert(
    request: AlertCreate,
    db: Session = Depends(get_db),
):
    alert = AlertService.create(db, request)

    return SuccessResponse(
        message="Alert created successfully.",
        data=AlertResponse.model_validate(alert),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[AlertResponse]],
)
async def get_alerts(
    status: AlertStatus | None = Query(default=None),
    severity: AlertSeverity | None = Query(default=None),
    infrastructure_asset_id: int | None = Query(default=None),
    monitoring_agent_id: int | None = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    alerts = AlertService.get_all(
        db=db,
        status=status,
        severity=severity,
        infrastructure_asset_id=infrastructure_asset_id,
        monitoring_agent_id=monitoring_agent_id,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="Alerts retrieved successfully.",
        data=[
            AlertResponse.model_validate(alert)
            for alert in alerts
        ],
    )


@router.get(
    "/{alert_id}",
    response_model=SuccessResponse[AlertResponse],
)
async def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = AlertService.get_by_id(
        db,
        alert_id,
    )

    return SuccessResponse(
        message="Alert retrieved successfully.",
        data=AlertResponse.model_validate(alert),
    )


@router.put(
    "/{alert_id}",
    response_model=SuccessResponse[AlertResponse],
)
async def update_alert(
    alert_id: int,
    request: AlertUpdate,
    db: Session = Depends(get_db),
):
    alert = AlertService.update(
        db,
        alert_id,
        request,
    )

    return SuccessResponse(
        message="Alert updated successfully.",
        data=AlertResponse.model_validate(alert),
    )


@router.patch(
    "/{alert_id}/acknowledge",
    response_model=SuccessResponse[AlertResponse],
)
async def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = AlertService.acknowledge(
        db,
        alert_id,
    )

    return SuccessResponse(
        message="Alert acknowledged successfully.",
        data=AlertResponse.model_validate(alert),
    )


@router.patch(
    "/{alert_id}/resolve",
    response_model=SuccessResponse[AlertResponse],
)
async def resolve_alert(
    alert_id: int,
    request: AlertResolve,
    db: Session = Depends(get_db),
):
    alert = AlertService.resolve(
        db,
        alert_id,
        request,
    )

    return SuccessResponse(
        message="Alert resolved successfully.",
        data=AlertResponse.model_validate(alert),
    )


@router.delete(
    "/{alert_id}",
    response_model=SuccessResponse[AlertResponse],
)
async def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = AlertService.delete(
        db,
        alert_id,
    )

    return SuccessResponse(
        message="Alert deleted successfully.",
        data=AlertResponse.model_validate(alert),
    )