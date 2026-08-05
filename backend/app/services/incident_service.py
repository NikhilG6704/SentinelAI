"""
Incident Service.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.incident_repository import IncidentRepository
from app.db.repositories.infrastructure_asset_repository import (
    InfrastructureAssetRepository,
)
from app.db.repositories.monitoring_agent_repository import (
    MonitoringAgentRepository,
)
from app.models.incident import (
    Incident,
    IncidentStatus,
)
from app.schemas.incident import (
    IncidentCreate,
    IncidentResolve,
    IncidentUpdate,
)


class IncidentService:
    """
    Business logic for Incident Management.
    """

    repository = IncidentRepository()
    asset_repository = InfrastructureAssetRepository()
    agent_repository = MonitoringAgentRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        request: IncidentCreate,
    ) -> Incident:

        asset = cls.asset_repository.get_by_id(
            db,
            request.infrastructure_asset_id,
        )

        if asset is None:
            raise ValueError("Infrastructure asset not found.")

        if request.monitoring_agent_id is not None:

            agent = cls.agent_repository.get_by_id(
                db,
                request.monitoring_agent_id,
            )

            if agent is None:
                raise ValueError("Monitoring agent not found.")

        incident = Incident(
            **request.model_dump(),
            status=IncidentStatus.OPEN,
            detected_at=datetime.now(timezone.utc),
        )

        logger.info(
            "Incident created for asset %s",
            request.infrastructure_asset_id,
        )

        return cls.repository.create(
            db,
            incident,
        )

    @classmethod
    def get_all(
        cls,
        db: Session,
        status=None,
        severity=None,
        skip: int = 0,
        limit: int = 100,
    ):
        return cls.repository.get_filtered(
            db,
            status=status,
            severity=severity,
            skip=skip,
            limit=limit,
        )

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        incident_id: int,
    ):
        return cls.repository.get_by_id(
            db,
            incident_id,
        )

    @classmethod
    def update(
        cls,
        db: Session,
        incident_id: int,
        request: IncidentUpdate,
    ):

        incident = cls.repository.get_by_id(
            db,
            incident_id,
        )

        if incident is None:
            raise ValueError("Incident not found.")

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():
            setattr(
                incident,
                key,
                value,
            )

        logger.info(
            "Incident %s updated.",
            incident.id,
        )

        return cls.repository.update(
            db,
            incident,
        )

    @classmethod
    def resolve(
        cls,
        db: Session,
        incident_id: int,
        request: IncidentResolve,
    ):

        incident = cls.repository.get_by_id(
            db,
            incident_id,
        )

        if incident is None:
            raise ValueError("Incident not found.")

        if incident.status == IncidentStatus.CLOSED:
            raise ValueError(
                "Closed incidents cannot be resolved."
            )

        logger.info(
            "Incident %s resolved.",
            incident.id,
        )

        return cls.repository.resolve(
            db,
            incident,
            request.resolution_summary,
        )

    @classmethod
    def close(
        cls,
        db: Session,
        incident_id: int,
    ):

        incident = cls.repository.get_by_id(
            db,
            incident_id,
        )

        if incident is None:
            raise ValueError("Incident not found.")

        if incident.status != IncidentStatus.RESOLVED:
            raise ValueError(
                "Incident must be resolved before closing."
            )

        logger.info(
            "Incident %s closed.",
            incident.id,
        )

        return cls.repository.close(
            db,
            incident,
        )