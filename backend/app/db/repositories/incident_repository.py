"""
Incident Repository.
"""

from __future__ import annotations
from sqlalchemy import func

from app.db.repositories.base_repository import BaseRepository
from app.models.incident import (
    Incident,
    IncidentStatus,
)


class IncidentRepository(BaseRepository[Incident]):
    """
    Repository for Incident management.
    """

    def __init__(self) -> None:
        super().__init__(Incident)

    def resolve(
        self,
        db,
        incident: Incident,
        resolution_summary: str,
    ) -> Incident:
        """
        Resolve an incident.
        """

        incident.status = IncidentStatus.RESOLVED
        incident.resolution_summary = resolution_summary
        incident.resolved_at = func.now()

        db.commit()
        db.refresh(incident)

        return incident

    def close(
        self,
        db,
        incident: Incident,
    ) -> Incident:
        """
        Close an incident.
        """

        incident.status = IncidentStatus.CLOSED

        db.commit()
        db.refresh(incident)

        return incident

    def update(
        self,
        db,
        incident: Incident,
    ) -> Incident:
        """
        Update an incident.
        """

        db.commit()
        db.refresh(incident)

        return incident

    def get_filtered(
        self,
        db,
        status: IncidentStatus | None = None,
        severity=None,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Return filtered incidents.
        """

        query = db.query(Incident)

        if status is not None:
            query = query.filter(
                Incident.status == status,
            )

        if severity is not None:
            query = query.filter(
                Incident.severity == severity,
            )

        return (
            query.order_by(
                Incident.detected_at.desc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )