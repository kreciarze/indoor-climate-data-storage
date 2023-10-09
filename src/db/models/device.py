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
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column()

    user: Mapped[User] = relationship(back_populates="devices")
    records: Mapped[list[Record]] = relationship(back_populates="device")
