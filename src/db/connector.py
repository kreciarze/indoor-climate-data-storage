import hashlib
import logging
from datetime import timedelta

from pydantic import AwareDatetime
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from db.engine import DBSession
from db.exceptions import (
    DeviceAlreadyActivated,
    DeviceNotExists,
    InvalidSerialNumber,
    LoginAlreadyExists,
    UserNotExists,
)
from db.models.activation_request import ActivationRequest
from db.models.device import Device
from db.models.record import Record
from db.models.user import User

logger = logging.getLogger(__name__)


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
        query = select(Device).where(
            Device.user_id == user_id,
            Device.activated,
        )
        return (await self._session.scalars(query)).all()

    async def create_device(self, serial_number: str) -> Device:
        device = Device(serial_number=serial_number)
        self._session.add(device)
        await self._session.commit()
        await self._session.refresh(device)
        logger.info(f"Created new device with ID: {device.id}.")
        return device

    async def assign_device(
        self,
        device: Device,
        user_id: int,
        name: str,
        key: str,
    ) -> Device:
        device.user_id = user_id
        device.name = name
        device.key = key
        await self._session.commit()
        await self._session.refresh(device)
        logger.info(f"Assigned device {device.name} with ID: {device.id} to user with ID {user_id}.")
        return device

    async def unassign_device(self, device: Device) -> Device:
        device.user_id = None
        device.name = None
        device.key = None
        device.activated = False
        await self._session.commit()
        await self._session.refresh(device)
        logger.info(f"Unassigned device {device.name} with ID: {device.id}.")
        return device

    async def enqueue_activation_request(
        self,
        device: Device,
        encrypted_message: str,
    ) -> None:
        query = select(ActivationRequest).where(ActivationRequest.device_id == device.id)
        activation_request = await self._session.scalar(query)

        if activation_request:
            activation_request.encrypted_message = encrypted_message
        else:
            activation_request = ActivationRequest(
                device_id=device.id,
                encrypted_message=encrypted_message,
            )
            self._session.add(activation_request)

        await self._session.commit()
        await self._session.refresh(device)
        logger.info(f"Saved activation request for device with ID: {device.id}.")

    async def dequeue_activation_request(self, device: Device) -> str | None:
        query = select(ActivationRequest).where(
            ActivationRequest.device_id == device.id,
            ActivationRequest.updated_at > func.now() - timedelta(minutes=5),
        )
        activation_request = await self._session.scalar(query)
        if activation_request:
            encrypted_message = activation_request.encrypted_message
            await self._session.delete(activation_request)
            await self._session.commit()
            await self._session.refresh(device)
            logger.info(f"Dequeued activation request for device with ID: {device.id}.")
            return encrypted_message

        return None

    async def activate_device(self, device: Device, serial_number: str) -> Device:
        if device.serial_number != serial_number:
            raise InvalidSerialNumber()

        if device.activated:
            raise DeviceAlreadyActivated()

        device.activated = True
        await self._session.commit()
        await self._session.refresh(device)
        logger.info(f"Activated device {device.name} with ID: {device.id} and serial number {serial_number}.")
        return device

    async def get_user_device(
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

    async def get_device(self, device_id: int) -> Device:
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
        logger.info(f"Saved record from device {device_id} from {when}.")


async def create_db_connector() -> DBConnector:
    session = DBSession()
    try:
        yield DBConnector(session=session)
    finally:
        await session.close()
