"""
Automation Rule Service.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.automation_rule_repository import (
    AutomationRuleRepository,
)
from app.models.automation_rule import (
    AutomationRule,
)
from app.schemas.automation_rule import (
    AutomationRuleCreate,
    AutomationRuleUpdate,
)


class AutomationRuleService:
    """
    Business logic for Automation Rules.
    """

    repository = AutomationRuleRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: AutomationRuleCreate,
    ) -> AutomationRule:

        existing = cls.repository.get_by_rule_name(
            db,
            request.rule_name,
        )

        if existing is not None:
            raise ValueError(
                "Rule name already exists."
            )

        rule = AutomationRule(
            **request.model_dump(),
        )

        logger.info(
            "Automation rule '%s' created.",
            request.rule_name,
        )

        return cls.repository.create(
            db,
            rule,
        )

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        rule_id: int,
    ) -> AutomationRule | None:

        return cls.repository.get_by_id(
            db,
            rule_id,
        )

    @classmethod
    def get_rules(
        cls,
        db: Session,
        **kwargs,
    ) -> list[AutomationRule]:

        return cls.repository.get_rules(
            db,
            **kwargs,
        )

    @classmethod
    def update(
        cls,
        db: Session,
        rule_id: int,
        request: AutomationRuleUpdate,
    ) -> AutomationRule:

        rule = cls.repository.get_by_id(
            db,
            rule_id,
        )

        if rule is None:
            raise ValueError(
                "Automation rule not found."
            )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():
            setattr(rule, key, value)

        logger.info(
            "Automation rule %s updated.",
            rule.id,
        )

        return cls.repository.update(
            db,
            rule,
        )

    @classmethod
    def enable(
        cls,
        db: Session,
        rule_id: int,
    ) -> AutomationRule:

        rule = cls.repository.get_by_id(
            db,
            rule_id,
        )

        if rule is None:
            raise ValueError(
                "Automation rule not found."
            )

        rule.is_enabled = True

        logger.info(
            "Automation rule %s enabled.",
            rule.id,
        )

        return cls.repository.update(
            db,
            rule,
        )

    @classmethod
    def disable(
        cls,
        db: Session,
        rule_id: int,
    ) -> AutomationRule:

        rule = cls.repository.get_by_id(
            db,
            rule_id,
        )

        if rule is None:
            raise ValueError(
                "Automation rule not found."
            )

        rule.is_enabled = False

        logger.info(
            "Automation rule %s disabled.",
            rule.id,
        )

        return cls.repository.update(
            db,
            rule,
        )

    @classmethod
    def delete(
        cls,
        db: Session,
        rule_id: int,
    ) -> AutomationRule:

        rule = cls.repository.get_by_id(
            db,
            rule_id,
        )

        if rule is None:
            raise ValueError(
                "Automation rule not found."
            )

        logger.info(
            "Automation rule %s deleted.",
            rule.id,
        )

        return cls.repository.soft_delete(
            db,
            rule,
        )