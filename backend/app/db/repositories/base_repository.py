"""
Generic repository implementation.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing reusable CRUD operations.
    """

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    def create(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_by_id(
        self,
        db: Session,
        obj_id: int,
    ) -> ModelType | None:
        return (
            db.query(self.model)
            .filter(
                self.model.id == obj_id,
                self.model.is_active.is_(True),
            )
            .first()
        )

    def get_all(
        self,
        db: Session,
    ) -> list[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.is_active.is_(True))
            .all()
        )

    def update(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:
        db.commit()
        db.refresh(obj)
        return obj

    def soft_delete(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:
        obj.is_active = False
        db.commit()
        db.refresh(obj)
        return obj