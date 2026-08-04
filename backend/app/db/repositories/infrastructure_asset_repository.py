"""
Infrastructure Asset repository.
"""

from sqlalchemy.orm import Session

from app.db.repositories.base_repository import BaseRepository
from app.models.infrastructure_asset import InfrastructureAsset


class InfrastructureAssetRepository(
    BaseRepository[InfrastructureAsset]
):
    """
    Repository for Infrastructure Asset.
    """

    def __init__(self) -> None:
        super().__init__(InfrastructureAsset)

    def get_by_ip(
        self,
        db: Session,
        ip_address: str,
    ) -> InfrastructureAsset | None:
        return (
            db.query(InfrastructureAsset)
            .filter(
                InfrastructureAsset.ip_address == ip_address,
                InfrastructureAsset.is_active.is_(True),
            )
            .first()
        )