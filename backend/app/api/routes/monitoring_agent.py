"""
Monitoring Agent API.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.monitoring_agent import (
    MonitoringAgentCreate,
    MonitoringAgentResponse,
    MonitoringAgentUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.monitoring_agent_service import MonitoringAgentService

router = APIRouter(
    prefix="/api/v1/monitoring-agents",
    tags=["Monitoring Agents"],
)


@router.post(
    "/register",
    response_model=SuccessResponse[MonitoringAgentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def register_agent(
    request: MonitoringAgentCreate,
    db: Session = Depends(get_db),
):
    agent = MonitoringAgentService.create(db, request)

    return SuccessResponse(
        message="Monitoring agent registered successfully.",
        data=MonitoringAgentResponse.model_validate(agent),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[MonitoringAgentResponse]],
)
async def get_agents(
    db: Session = Depends(get_db),
):
    agents = MonitoringAgentService.get_all(db)

    return SuccessResponse(
        message="Monitoring agents retrieved successfully.",
        data=[
            MonitoringAgentResponse.model_validate(agent)
            for agent in agents
        ],
    )


@router.get(
    "/{agent_id}",
    response_model=SuccessResponse[MonitoringAgentResponse],
)
async def get_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    agent = MonitoringAgentService.get_by_id(db, agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Monitoring agent not found.",
        )

    return SuccessResponse(
        message="Monitoring agent retrieved successfully.",
        data=MonitoringAgentResponse.model_validate(agent),
    )


@router.get(
    "/asset/{asset_id}",
    response_model=SuccessResponse[list[MonitoringAgentResponse]],
)
async def get_agents_by_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    agents = MonitoringAgentService.get_by_asset(
        db,
        asset_id,
    )

    return SuccessResponse(
        message="Monitoring agents retrieved successfully.",
        data=[
            MonitoringAgentResponse.model_validate(agent)
            for agent in agents
        ],
    )


@router.put(
    "/{agent_id}",
    response_model=SuccessResponse[MonitoringAgentResponse],
)
async def update_agent(
    agent_id: int,
    request: MonitoringAgentUpdate,
    db: Session = Depends(get_db),
):
    agent = MonitoringAgentService.get_by_id(
        db,
        agent_id,
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Monitoring agent not found.",
        )

    updated = MonitoringAgentService.update(
        db,
        agent,
        request,
    )

    return SuccessResponse(
        message="Monitoring agent updated successfully.",
        data=MonitoringAgentResponse.model_validate(updated),
    )


@router.delete(
    "/{agent_id}",
    response_model=SuccessResponse[MonitoringAgentResponse],
)
async def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    agent = MonitoringAgentService.get_by_id(
        db,
        agent_id,
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Monitoring agent not found.",
        )

    deleted = MonitoringAgentService.soft_delete(
        db,
        agent,
    )

    return SuccessResponse(
        message="Monitoring agent deleted successfully.",
        data=MonitoringAgentResponse.model_validate(deleted),
    )