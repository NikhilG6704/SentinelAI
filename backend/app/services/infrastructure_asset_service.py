"""
Business logic for Infrastructure Asset management.
"""

from sqlalchemy.orm import Session

from app.db.repositories.infrastructure_asset_repository import (
    InfrastructureAssetRepository,
)
from app.models.infrastructure_asset import InfrastructureAsset
from app.schemas.infrastructure_asset import (
    InfrastructureAssetCreate,
    InfrastructureAssetUpdate,
)


class InfrastructureAssetService:
    """
    Service layer for Infrastructure Asset operations.
    """

    repository = InfrastructureAssetRepository()

    @classmethod
    def create(
        cls,
        db: Session,
        asset_data: InfrastructureAssetCreate,
    ) -> InfrastructureAsset:

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

        return cls.repository.create(db, asset)

    @classmethod
    def get_all(
        cls,
        db: Session,
    ) -> list[InfrastructureAsset]:
        return cls.repository.get_all(db)

    @classmethod
    def get_by_id(
        cls,
        db: Session,
        asset_id: int,
    ) -> InfrastructureAsset | None:
        return cls.repository.get_by_id(db, asset_id)

    @classmethod
    def update(
        cls,
        db: Session,
        asset: InfrastructureAsset,
        asset_data: InfrastructureAssetUpdate,
    ) -> InfrastructureAsset:

        update_data = asset_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field == "ip_address" and value is not None:
                value = str(value)

            setattr(asset, field, value)

        return cls.repository.update(db, asset)

    @classmethod
    def soft_delete(
        cls,
        db: Session,
        asset: InfrastructureAsset,
    ) -> InfrastructureAsset:
        return cls.repository.soft_delete(db, asset)