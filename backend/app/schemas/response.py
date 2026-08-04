"""
Reusable API response schemas.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """
    Standard error details.
    """

    code: int
    message: str


class SuccessResponse(BaseModel, Generic[T]):
    """
    Standard success response wrapper.
    """

    success: bool = True
    message: str
    data: T


class ErrorResponse(BaseModel):
    """
    Standard error response wrapper.
    """

    success: bool = False
    error: ErrorDetail