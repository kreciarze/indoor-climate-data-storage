from __future__ import annotations

from sqlalchemy import Column, DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from settings import settings

metadata_obj = MetaData(schema=settings.postgres.db_schema)


class Base(DeclarativeBase):
    __name__: str
    metadata = metadata_obj

    @declared_attr.directive
    def __tablename__(cls: Base) -> str:
        return cls.__name__.lower()

    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        comment="Row created at",
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        comment="Row updated at",
        nullable=False,
    )
