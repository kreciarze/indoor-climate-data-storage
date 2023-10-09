from __future__ import annotations

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __name__: str

    @declared_attr
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
