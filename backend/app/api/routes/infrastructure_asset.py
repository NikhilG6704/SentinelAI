"""
Infrastructure Asset API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.infrastructure_asset import (
    InfrastructureAssetCreate,
    InfrastructureAssetResponse,
    InfrastructureAssetUpdate,
)
from app.schemas.response import SuccessResponse
from app.services.infrastructure_asset_service import InfrastructureAssetService

router = APIRouter(
    prefix="/api/v1/infrastructure-assets",
    tags=["Infrastructure Assets"],
)


@router.post(
    "",
    response_model=SuccessResponse[InfrastructureAssetResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_asset(
    asset: InfrastructureAssetCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new infrastructure asset.
    """
    created_asset = InfrastructureAssetService.create(db, asset)

    return SuccessResponse(
        message="Infrastructure asset created successfully.",
        data=InfrastructureAssetResponse.model_validate(created_asset),
    )


@router.get(
    "",
    response_model=SuccessResponse[list[InfrastructureAssetResponse]],
)
async def get_assets(
    db: Session = Depends(get_db),
):
    """
    Retrieve all infrastructure assets.
    """
    assets = InfrastructureAssetService.get_all(db)

    return SuccessResponse(
        message="Infrastructure assets retrieved successfully.",
        data=[
            InfrastructureAssetResponse.model_validate(asset)
            for asset in assets
        ],
    )


@router.get(
    "/{asset_id}",
    response_model=SuccessResponse[InfrastructureAssetResponse],
)
async def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve an infrastructure asset by ID.
    """
    asset = InfrastructureAssetService.get_by_id(db, asset_id)

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Infrastructure asset not found.",
        )

    return SuccessResponse(
        message="Infrastructure asset retrieved successfully.",
        data=InfrastructureAssetResponse.model_validate(asset),
    )


@router.put(
    "/{asset_id}",
    response_model=SuccessResponse[InfrastructureAssetResponse],
)
async def update_asset(
    asset_id: int,
    asset_update: InfrastructureAssetUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an infrastructure asset.
    """
    asset = InfrastructureAssetService.get_by_id(db, asset_id)

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Infrastructure asset not found.",
        )

    updated_asset = InfrastructureAssetService.update(
        db,
        asset,
        asset_update,
    )

    return SuccessResponse(
        message="Infrastructure asset updated successfully.",
        data=InfrastructureAssetResponse.model_validate(updated_asset),
    )


@router.delete(
    "/{asset_id}",
    response_model=SuccessResponse[InfrastructureAssetResponse],
)
async def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    """
    Soft delete an infrastructure asset.
    """
    asset = InfrastructureAssetService.get_by_id(db, asset_id)

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Infrastructure asset not found.",
        )

    deleted_asset = InfrastructureAssetService.soft_delete(db, asset)

    return SuccessResponse(
        message="Infrastructure asset deleted successfully.",
        data=InfrastructureAssetResponse.model_validate(deleted_asset),
    )