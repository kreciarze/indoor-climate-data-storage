from datetime import datetime, timezone

import pytest

from db.connector import DBConnector
from db.exceptions import DeviceNotExists, LoginAlreadyExists, UserNotExists
from tests.db.conftest import create_test_device, create_test_device_and_record, create_test_user


async def test_register_user(db_connector: DBConnector) -> None:
    await db_connector.register_user("test_user", "test_password")
    user = await db_connector.get_user("test_user", "test_password")
    assert user.login == "test_user"


async def test_register_existing_user(db_connector: DBConnector) -> None:
    await db_connector.register_user("existing_user", "password")
    with pytest.raises(LoginAlreadyExists):
        await db_connector.register_user("existing_user", "password")


async def test_get_user(db_connector: DBConnector) -> None:
    await db_connector.register_user("get_user_test", "password")
    user = await db_connector.get_user("get_user_test", "password")
    assert user.login == "get_user_test"


async def test_get_nonexistent_user(db_connector: DBConnector) -> None:
    with pytest.raises(UserNotExists):
        await db_connector.get_user("nonexistent_user", "password")


async def test_list_devices(db_connector: DBConnector) -> None:
    user = await create_test_user(db_connector._session, "list_devices_user", "password")
    device1 = await create_test_device(db_connector._session, user.id, "Device1")
    device2 = await create_test_device(db_connector._session, user.id, "Device2")

    devices = await db_connector.list_devices(user_id=user.id)

    assert len(devices) == 2
    assert any(device.id == device1.id for device in devices)
    assert any(device.id == device2.id for device in devices)


async def test_create_device(db_connector: DBConnector) -> None:
    user = await create_test_user(db_connector._session, "create_device_user", "password")
    device_name = "TestDevice"

    device = await db_connector.create_device(user_id=user.id, name=device_name)

    assert device.name == device_name
    assert device.user_id == user.id


async def test_remove_device(db_connector: DBConnector) -> None:
    user = await create_test_user(db_connector._session, "remove_device_user", "password")
    device = await create_test_device(db_connector._session, user.id, "DeviceToRemove")

    removed_device = await db_connector.remove_device(user_id=user.id, device_id=device.id)
    remaining_devices = await db_connector.list_devices(user_id=user.id)

    assert removed_device.id == device.id
    assert removed_device not in remaining_devices


async def test_get_device(db_connector: DBConnector) -> None:
    user = await create_test_user(db_connector._session, "get_device_user", "password")
    device = await create_test_device(db_connector._session, user.id, "GetDevice")

    retrieved_device = await db_connector.get_device(user_id=user.id, device_id=device.id)

    assert retrieved_device.id == device.id


async def test_get_nonexistent_device(db_connector: DBConnector) -> None:
    user = await create_test_user(db_connector._session, "nonexistent_device_user", "password")

    with pytest.raises(DeviceNotExists):
        await db_connector.get_device(user_id=user.id, device_id=999)


async def test_list_records(db_connector: DBConnector) -> None:
    user = await create_test_user(db_connector._session, "list_records_user", "password")
    device, record = await create_test_device_and_record(
        db_connector._session,
        user.id,
        "TestDevice",
        datetime(2023, 1, 1, tzinfo=timezone.utc),
        25.0,
        1013.25,
    )

    records = await db_connector.list_records(user_id=user.id, device_id=device.id, start_date=None, end_date=None)

    assert len(records) == 1
    assert records[0].temperature == 25.0
    assert records[0].pressure == 1013.25


async def test_create_record(db_connector: DBConnector) -> None:
    user = await create_test_user(db_connector._session, "create_record_user", "password")
    device = await create_test_device(db_connector._session, user.id, "CreateRecordDevice")

    await db_connector.create_record(
        device_id=device.id,
        when=datetime(2023, 1, 1, tzinfo=timezone.utc),
        temperature=25.0,
        pressure=1013.25,
    )

    records = await db_connector.list_records(user_id=user.id, device_id=device.id, start_date=None, end_date=None)

    assert len(records) == 1
    assert records[0].temperature == 25.0
    assert records[0].pressure == 1013.25
