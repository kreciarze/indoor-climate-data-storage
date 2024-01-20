from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class SerialNumber(Base):
    value: Mapped[str] = mapped_column(primary_key=True)
