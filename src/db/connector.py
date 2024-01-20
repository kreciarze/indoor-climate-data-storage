import hashlib

from pydantic import AwareDatetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db.engine import DBSession
from db.exceptions import (
    DeviceAlreadyActivated,
    DeviceNotExists,
    InvalidSerialNumber,
    LoginAlreadyExists,
    UserNotExists,
)
from db.models.device import Device
from db.models.record import Record
from db.models.serial_number import SerialNumber
from db.models.user import User


class DBConnector:
    def __init__(self, session: DBSession) -> None:
        self._session = session

    async def register_user(
        self,
        login: str,
        password: str,
    ) -> None:
        password_hash = self.calculate_password_hash(password=password)
        user = User(
            login=login,
            password_hash=password_hash,
            devices=[],
        )
        try:
            self._session.add(user)
            await self._session.commit()
        except IntegrityError:
            raise LoginAlreadyExists()

    async def get_user(
        self,
        login: str,
        password: str,
    ) -> User:
        password_hash = self.calculate_password_hash(password=password)
        query = select(User).where(
            User.login == login,
            User.password_hash == password_hash,
        )
        user = await self._session.scalar(query)
        if user:
            return user

        raise UserNotExists()

    @staticmethod
    def calculate_password_hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def list_devices(
        self,
        user_id: int,
    ) -> list[Device]:
        query = select(Device).where(Device.user_id == user_id)
        return (await self._session.scalars(query)).all()

    async def create_device(
        self,
        user_id: int,
        name: str,
        key: str,
    ) -> Device:
        device = Device(
            user_id=user_id,
            name=name,
            key=key,
        )
        self._session.add(device)
        await self._session.commit()
        await self._session.refresh(device)
        return device

    async def remove_device(
        self,
        user_id: int,
        device_id: int,
    ) -> Device:
        device = await self.get_device(
            user_id=user_id,
            device_id=device_id,
        )
        await self._session.delete(device)
        await self._session.commit()
        return device

    async def get_device(
        self,
        user_id: int,
        device_id: int,
    ) -> Device:
        query = select(Device).where(
            Device.id == device_id,
            Device.user_id == user_id,
        )
        device = await self._session.scalar(query)
        if device:
            return device

        raise DeviceNotExists(
            user_id=user_id,
            device_id=device_id,
        )

    async def get_device_by_id(self, device_id: int) -> Device:
        query = select(Device).where(Device.id == device_id)
        device = await self._session.scalar(query)
        if device:
            return device

        raise DeviceNotExists(device_id=device_id)

    async def list_records(
        self,
        user_id: int,
        device_id: int | None,
        start_date: AwareDatetime | None,
        end_date: AwareDatetime | None,
    ) -> list[Record]:
        query = (
            select(Record)
            .join(Record.device)
            .where(
                Record.device_id == Device.id,
                Device.user_id == user_id,
            )
        )

        if device_id is not None:
            query = query.where(Record.device_id == device_id)

        if start_date:
            query = query.where(Record.when >= start_date)

        if end_date:
            query = query.where(Record.when <= end_date)

        return (await self._session.scalars(query)).all()

    async def create_record(
        self,
        device_id: int,
        when: AwareDatetime,
        temperature: float,
        pressure: float,
    ) -> None:
        record = Record(
            device_id=device_id,
            when=when,
            temperature=temperature,
            pressure=pressure,
        )
        self._session.add(record)
        await self._session.commit()

    async def activate_device(self, device: Device, serial_number: str) -> None:
        query = select(SerialNumber).where(SerialNumber.value == serial_number)
        serial_number = self._session.scalar(query)
        if not serial_number:
            raise InvalidSerialNumber()

        query = select(Device).where(Device.serial_number_value == serial_number)
        conflicting_device = self._session.scalar(query)
        if conflicting_device:
            raise DeviceAlreadyActivated()

        device.serial_number = serial_number
        self._session.add(device)
        self._session.commit()


async def create_db_connector() -> DBConnector:
    session = DBSession()
    try:
        yield DBConnector(session=session)
    finally:
        await session.close()
