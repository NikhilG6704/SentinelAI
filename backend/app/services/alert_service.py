"""
Alert Service.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.alert_repository import AlertRepository
from app.db.repositories.infrastructure_asset_repository import (
    InfrastructureAssetRepository,
)
from app.db.repositories.monitoring_agent_repository import (
    MonitoringAgentRepository,
)
from app.db.repositories.system_metric_repository import (
    SystemMetricRepository,
)
from app.models.alert import (
    Alert,
    AlertStatus,
)
from app.schemas.alert import (
    AlertCreate,
    AlertResolve,
    AlertUpdate,
)


class AlertService:
    """
    Business logic for Alert Management.
    """

    repository = AlertRepository()
    asset_repository = InfrastructureAssetRepository()
    agent_repository = MonitoringAgentRepository()
    metric_repository = SystemMetricRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: AlertCreate,
    ) -> Alert:

        asset = cls.asset_repository.get_by_id(
            db,
            request.infrastructure_asset_id,
        )

        if asset is None:
            raise ValueError("Infrastructure asset not found.")

        agent = cls.agent_repository.get_by_id(
            db,
            request.monitoring_agent_id,
        )

        if agent is None:
            raise ValueError("Monitoring agent not found.")

        if request.system_metric_id is not None:
            metric = cls.metric_repository.get_by_id(
                db,
                request.system_metric_id,
            )

            if metric is None:
                raise ValueError("System metric not found.")

        alert = Alert(
            **request.model_dump(),
            status=AlertStatus.ACTIVE,
            triggered_at=datetime.now(timezone.utc),
        )

        logger.info(
            "Alert created for asset %s",
            request.infrastructure_asset_id,
        )

        return cls.repository.create(
            db,
            alert,
        )

    @classmethod
    def get_all(
        cls,
        db: Session,
        status=None,
        severity=None,
        infrastructure_asset_id=None,
        monitoring_agent_id=None,
        skip: int = 0,
        limit: int = 100,
    ):
        return cls.repository.get_filtered(
            db=db,
            status=status,
            severity=severity,
            infrastructure_asset_id=infrastructure_asset_id,
            monitoring_agent_id=monitoring_agent_id,
            skip=skip,
            limit=limit,
        )

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        alert_id: int,
    ):
        return cls.repository.get_by_id(
            db,
            alert_id,
        )

    @classmethod
    def update(
        cls,
        db: Session,
        alert_id: int,
        request: AlertUpdate,
    ):

        alert = cls.repository.get_by_id(
            db,
            alert_id,
        )

        if alert is None:
            raise ValueError("Alert not found.")

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():
            setattr(alert, key, value)

        logger.info(
            "Alert %s updated.",
            alert.id,
        )

        return cls.repository.update(
            db,
            alert,
        )

    @classmethod
    def acknowledge(
        cls,
        db: Session,
        alert_id: int,
    ):

        alert = cls.repository.get_by_id(
            db,
            alert_id,
        )

        if alert is None:
            raise ValueError("Alert not found.")

        if alert.status != AlertStatus.ACTIVE:
            raise ValueError(
                "Only active alerts can be acknowledged."
            )

        logger.info(
            "Alert %s acknowledged.",
            alert.id,
        )

        return cls.repository.acknowledge(
            db,
            alert,
        )

    @classmethod
    def resolve(
        cls,
        db: Session,
        alert_id: int,
        request: AlertResolve,
    ):

        alert = cls.repository.get_by_id(
            db,
            alert_id,
        )

        if alert is None:
            raise ValueError("Alert not found.")

        if alert.status == AlertStatus.RESOLVED:
            raise ValueError(
                "Alert is already resolved."
            )

        logger.info(
            "Alert %s resolved.",
            alert.id,
        )

        return cls.repository.resolve(
            db,
            alert,
            request.resolution_summary,
        )

    @classmethod
    def delete(
        cls,
        db: Session,
        alert_id: int,
    ):

        alert = cls.repository.get_by_id(
            db,
            alert_id,
        )

        if alert is None:
            raise ValueError("Alert not found.")

        logger.info(
            "Alert %s deleted.",
            alert.id,
        )

        return cls.repository.soft_delete(
            db,
            alert,
        )