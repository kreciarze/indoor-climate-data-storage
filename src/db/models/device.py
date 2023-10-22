from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base, BaseTimeModel

if TYPE_CHECKING:
    from db.models.record import Record
    from db.models.user import User


class DeviceModel(BaseTimeModel):
    id: int  # noqa: A003
    user_id: int


class Device(Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="devices")
    records: Mapped[list["Record"]] = relationship(back_populates="device")
