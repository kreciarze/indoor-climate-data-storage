from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.record import Record
    from db.models.user import User
else:
    Record = "Record"
    User = "User"


class Device(Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    serial_number: Mapped[str] = mapped_column(unique=True)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str | None] = mapped_column()
    key: Mapped[str | None] = mapped_column()

    activated: Mapped[bool] = mapped_column(default=False)

    user: Mapped[User] = relationship(back_populates="devices")
    records: Mapped[list[Record]] = relationship(back_populates="device", cascade="all, delete-orphan")
