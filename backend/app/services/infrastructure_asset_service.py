"""
Business logic for Infrastructure Asset management.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.infrastructure_asset import InfrastructureAsset
from app.schemas.infrastructure_asset import (
    InfrastructureAssetCreate,
    InfrastructureAssetUpdate,
)


class InfrastructureAssetService:
    """
    Service layer for Infrastructure Asset operations.
    """

    @staticmethod
    def create(
        db: Session,
        asset_data: InfrastructureAssetCreate,
    ) -> InfrastructureAsset:
        """
        Create a new infrastructure asset.
        """
        asset = InfrastructureAsset(
            hostname=asset_data.hostname,
            ip_address=str(asset_data.ip_address),
            operating_system=asset_data.operating_system,
            asset_type=asset_data.asset_type,
            environment=asset_data.environment,
            status=asset_data.status,
            location=asset_data.location,
            description=asset_data.description,
            is_active=True,
        )

        db.add(asset)
        db.commit()
        db.refresh(asset)

        return asset

    @staticmethod
    def get_all(db: Session) -> list[InfrastructureAsset]:
        """
        Return all active infrastructure assets.
        """
        return (
            db.query(InfrastructureAsset)
            .filter(InfrastructureAsset.is_active.is_(True))
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        asset_id: int,
    ) -> InfrastructureAsset | None:
        """
        Return a single infrastructure asset.
        """
        return (
            db.query(InfrastructureAsset)
            .filter(
                InfrastructureAsset.id == asset_id,
                InfrastructureAsset.is_active.is_(True),
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        asset: InfrastructureAsset,
        asset_data: InfrastructureAssetUpdate,
    ) -> InfrastructureAsset:
        """
        Update an existing infrastructure asset.
        """

        update_data = asset_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field == "ip_address" and value is not None:
                value = str(value)

            setattr(asset, field, value)

        db.commit()
        db.refresh(asset)

        return asset

    @staticmethod
    def soft_delete(
        db: Session,
        asset: InfrastructureAsset,
    ) -> InfrastructureAsset:
        """
        Soft delete an infrastructure asset.
        """

        asset.is_active = False

        db.commit()
        db.refresh(asset)

        return asset