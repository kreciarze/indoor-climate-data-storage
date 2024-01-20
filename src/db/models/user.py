from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.device import Device
else:
    Device = "Device"


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)

    devices: Mapped[list[Device]] = relationship(back_populates="user", cascade="all, delete-orphan")
