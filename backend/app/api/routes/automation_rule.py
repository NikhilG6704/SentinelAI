from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.automation_rule import (
    MetricType,
    RuleSeverity,
)
from app.schemas.automation_rule import (
    AutomationRuleCreate,
    AutomationRuleResponse,
    AutomationRuleUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.automation_rule_service import (
    AutomationRuleService,
)

router = APIRouter(
    prefix="/api/v1/automation-rules",
    tags=["Automation Rules"],
)


@router.post(
    "",
    response_model=SuccessResponse[AutomationRuleResponse],
    status_code=201,
)
async def create_rule(
    request: AutomationRuleCreate,
    db: Session = Depends(get_db),
):
    rule = AutomationRuleService.create(
        db,
        request,
    )

    return SuccessResponse(
        message="Automation rule created successfully.",
        data=AutomationRuleResponse.model_validate(rule),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[AutomationRuleResponse]],
)
async def get_rules(
    is_enabled: bool | None = Query(default=None),
    metric_type: MetricType | None = Query(default=None),
    severity: RuleSeverity | None = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    rules = AutomationRuleService.get_rules(
        db=db,
        is_enabled=is_enabled,
        metric_type=metric_type,
        severity=severity,
        skip=skip,
        limit=limit,
    )

    return SuccessResponse(
        message="Automation rules retrieved successfully.",
        data=[
            AutomationRuleResponse.model_validate(rule)
            for rule in rules
        ],
    )


@router.get(
    "/{rule_id}",
    response_model=SuccessResponse[AutomationRuleResponse],
)
async def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    rule = AutomationRuleService.get_by_id(
        db,
        rule_id,
    )

    return SuccessResponse(
        message="Automation rule retrieved successfully.",
        data=AutomationRuleResponse.model_validate(rule),
    )


@router.put(
    "/{rule_id}",
    response_model=SuccessResponse[AutomationRuleResponse],
)
async def update_rule(
    rule_id: int,
    request: AutomationRuleUpdate,
    db: Session = Depends(get_db),
):
    rule = AutomationRuleService.update(
        db,
        rule_id,
        request,
    )

    return SuccessResponse(
        message="Automation rule updated successfully.",
        data=AutomationRuleResponse.model_validate(rule),
    )


@router.patch(
    "/{rule_id}/enable",
    response_model=SuccessResponse[AutomationRuleResponse],
)
async def enable_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    rule = AutomationRuleService.enable(
        db,
        rule_id,
    )

    return SuccessResponse(
        message="Automation rule enabled successfully.",
        data=AutomationRuleResponse.model_validate(rule),
    )


@router.patch(
    "/{rule_id}/disable",
    response_model=SuccessResponse[AutomationRuleResponse],
)
async def disable_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    rule = AutomationRuleService.disable(
        db,
        rule_id,
    )

    return SuccessResponse(
        message="Automation rule disabled successfully.",
        data=AutomationRuleResponse.model_validate(rule),
    )


@router.delete(
    "/{rule_id}",
    response_model=SuccessResponse[AutomationRuleResponse],
)
async def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    rule = AutomationRuleService.delete(
        db,
        rule_id,
    )

    return SuccessResponse(
        message="Automation rule deleted successfully.",
        data=AutomationRuleResponse.model_validate(rule),
    )