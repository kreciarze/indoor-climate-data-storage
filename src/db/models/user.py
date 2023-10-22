from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.device import Device


class UserData(BaseModel):
    login: str
    password: str


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = Column(String(256), nullable=False)

    devices: Mapped[list[Device]] = relationship(back_populates="user")
