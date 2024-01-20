import asyncio
from datetime import datetime

import pytest
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.connector import DBConnector
from db.models.base import Base
from db.models.device import Device
from db.models.record import Record
from db.models.serial_number import SerialNumber
from db.models.user import User
from tests.conftest import EXAMPLE_AES_KEY

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

models = [Device, Record, SerialNumber, User]

test_engine = create_async_engine(
    url=TEST_DB_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestDBSession = async_sessionmaker(
    autoflush=False,
    bind=test_engine,
    expire_on_commit=False,
)


async def setup_db() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(setup_db())


@pytest.fixture()
async def db_connector() -> DBConnector:
    session = TestDBSession()
    try:
        yield DBConnector(session=session)
    finally:
        await session.close()


async def create_test_device(
    session: TestDBSession,
    user_id: int,
    name: str,
) -> Device:
    device = Device(
        user_id=user_id,
        name=name,
        key=EXAMPLE_AES_KEY,
    )
    session.add(device)
    await session.commit()
    return device


async def create_test_record(
    session: TestDBSession,
    device_id: int,
    when: datetime,
    temperature: float,
    pressure: float,
) -> Record:
    record = Record(
        device_id=device_id,
        when=when,
        temperature=temperature,
        pressure=pressure,
    )
    session.add(record)
    await session.commit()
    return record


async def create_test_user(
    session: TestDBSession,
    login: str,
    password: str,
) -> User:
    user = User(login=login, password_hash=f"{password}_hash")
    session.add(user)
    await session.commit()
    return user


async def create_test_device_and_record(
    session: TestDBSession,
    user_id: int,
    device_name: str,
    record_when: datetime,
    temperature: float,
    pressure: float,
) -> tuple[Device, Record]:
    device = await create_test_device(session, user_id, device_name)
    record = await create_test_record(session, device.id, record_when, temperature, pressure)
    return device, record
