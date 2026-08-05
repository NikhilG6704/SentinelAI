"""
Automation Rule Repository.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.automation_rule import (
    AutomationRule,
    MetricType,
    RuleSeverity,
)


class AutomationRuleRepository(BaseRepository[AutomationRule]):
    """
    Repository for Automation Rules.
    """

    def __init__(self) -> None:
        super().__init__(AutomationRule)

    def get_by_rule_name(
        self,
        db: Session,
        rule_name: str,
    ) -> AutomationRule | None:

        return (
            db.query(AutomationRule)
            .filter(
                AutomationRule.rule_name == rule_name,
                AutomationRule.is_active.is_(True),
            )
            .first()
        )

    def get_rules(
        self,
        db: Session,
        *,
        is_enabled: bool | None = None,
        metric_type: MetricType | None = None,
        severity: RuleSeverity | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AutomationRule]:

        query = db.query(AutomationRule).filter(
            AutomationRule.is_active.is_(True)
        )

        if is_enabled is not None:
            query = query.filter(
                AutomationRule.is_enabled == is_enabled
            )

        if metric_type:
            query = query.filter(
                AutomationRule.metric_type == metric_type
            )

        if severity:
            query = query.filter(
                AutomationRule.severity == severity
            )

        return (
            query.order_by(
                AutomationRule.priority.desc(),
                AutomationRule.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        rule: AutomationRule,
    ) -> AutomationRule:

        db.commit()
        db.refresh(rule)

        return rule

    def soft_delete(
        self,
        db: Session,
        rule: AutomationRule,
    ) -> AutomationRule:

        rule.is_active = False

        db.commit()
        db.refresh(rule)

        return rule