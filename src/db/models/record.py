from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.device import Device


class RecordModel(BaseModel):
    id: int  # noqa: A003
    device_id: int
    when: datetime
    temperature: float
    pressure: float


class Record(Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"), nullable=False)
    when: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    pressure: Mapped[float] = mapped_column(nullable=False)

    device: Mapped["Device"] = relationship(back_populates="records")

    def cast_to_model(self) -> RecordModel:
        return RecordModel(
            id=self.id,
            device_id=self.device_id,
            when=self.when,
            temperature=self.temperature,
            pressure=self.pressure,
        )
