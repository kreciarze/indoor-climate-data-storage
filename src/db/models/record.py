from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.device import Device
else:
    Device = "Device"


class Record(Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"), nullable=False)
    when: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    pressure: Mapped[float] = mapped_column(nullable=False)

    device: Mapped[Device] = relationship(back_populates="records")
