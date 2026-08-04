"""
Pydantic schemas for Infrastructure Asset.
"""

from __future__ import annotations

from datetime import datetime
from ipaddress import IPv4Address
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import AssetStatus, AssetType, EnvironmentType


class InfrastructureAssetBase(BaseModel):
    """
    Shared Infrastructure Asset fields.
    """

    hostname: str = Field(..., min_length=1, max_length=255)
    ip_address: IPv4Address
    operating_system: str = Field(..., min_length=1, max_length=100)

    asset_type: AssetType
    environment: EnvironmentType
    status: AssetStatus = AssetStatus.HEALTHY

    location: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class InfrastructureAssetCreate(InfrastructureAssetBase):
    """
    Request schema for creating an infrastructure asset.
    """

    pass


class InfrastructureAssetUpdate(BaseModel):
    """
    Request schema for updating an infrastructure asset.
    """

    hostname: Optional[str] = Field(default=None, min_length=1, max_length=255)
    ip_address: Optional[IPv4Address] = None
    operating_system: Optional[str] = Field(default=None, min_length=1, max_length=100)

    asset_type: Optional[AssetType] = None
    environment: Optional[EnvironmentType] = None
    status: Optional[AssetStatus] = None

    location: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class InfrastructureAssetResponse(InfrastructureAssetBase):
    """
    Response schema.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool

    created_at: datetime
    updated_at: datetime