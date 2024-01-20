from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.record import Record
    from db.models.serial_number import SerialNumber
    from db.models.user import User
else:
    Record = "Record"
    User = "User"
    SerialNumber = "SerialNumber"


class Device(Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    serial_number_value: Mapped[str | None] = mapped_column(ForeignKey("serialnumber.value"), nullable=True)
    name: Mapped[str] = mapped_column()
    key: Mapped[str] = mapped_column()

    user: Mapped[User] = relationship(back_populates="devices")
    records: Mapped[list[Record]] = relationship(back_populates="device", cascade="all, delete-orphan")
    serial_number: Mapped[SerialNumber] = relationship(foreign_keys=[serial_number_value])
