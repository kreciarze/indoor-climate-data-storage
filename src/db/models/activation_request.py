from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.device import Device
else:
    Device = "Device"


class ActivationRequest(Base):
    device_id: Mapped[str] = mapped_column(ForeignKey("device.id"), primary_key=True, nullable=False)
    encrypted_message: Mapped[str] = mapped_column(nullable=False)

    device: Mapped[Device] = relationship()
