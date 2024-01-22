from fastapi import status
from fastapi.testclient import TestClient

from api.devices.contracts import SerialNumber
from auth.auth import extract_user_id_from_bearer
from auth.exceptions import InvalidClientType
from auth.tokens import ClientType
from db.models.device import Device
from main import app
from tests.api.conftest import EXAMPLE_CLIENT_ID, mock_db_connector
from tests.conftest import encrypt_aes256, EXAMPLE_AES_IV, EXAMPLE_AES_KEY


async def raise_invalid_client_type() -> None:
    raise InvalidClientType(
        actual_client_type=ClientType.DEVICE,
        expected_client_type=ClientType.USER,
    )


async def test_validating_user_type(
    api_client: TestClient,
    fastapi_dep,
) -> None:
    with fastapi_dep(app).override({extract_user_id_from_bearer: raise_invalid_client_type}):
        result = api_client.request(
            method="GET",
            url="/devices",
        )

    assert result.status_code == status.HTTP_403_FORBIDDEN, result.text
    assert result.json() == {
        "message": "Only users are allowed to perform this action. Expected `user`, but got `device`.",
    }


async def test_list_devices(api_client: TestClient) -> None:
    mock_db_connector.list_devices.reset_mock()

    result = api_client.request(
        method="GET",
        url="/devices",
    )

    assert result.status_code == status.HTTP_200_OK, result.text
    assert result.json() == []
    mock_db_connector.list_devices.assert_awaited_once()


async def test_assign_device(api_client: TestClient) -> None:
    DEVICE_ID = 1
    device = Device(
        id=DEVICE_ID,
        user_id=EXAMPLE_CLIENT_ID,
        name="device1",
        key=EXAMPLE_AES_KEY,
        activated=False,
    )
    mock_db_connector.get_device.reset_mock()
    mock_db_connector.get_device.return_value = device
    mock_db_connector.assign_device.reset_mock()
    mock_db_connector.assign_device.return_value = device
    mock_db_connector.dequeue_activation_request.reset_mock()
    mock_db_connector.dequeue_activation_request.return_value = None

    result = api_client.request(
        method="PATCH",
        url=f"/devices/{DEVICE_ID}/assign",
        json={
            "name": "device1",
            "key": EXAMPLE_AES_KEY,
        },
    )

    assert result.status_code == status.HTTP_200_OK, result.text
    assert result.json() == {
        "id": DEVICE_ID,
        "user_id": EXAMPLE_CLIENT_ID,
        "name": "device1",
        "activated": False,
    }
    mock_db_connector.get_device.assert_awaited_once_with(device_id=DEVICE_ID)
    mock_db_connector.assign_device.assert_awaited_once_with(
        device=device,
        user_id=EXAMPLE_CLIENT_ID,
        name="device1",
        key=EXAMPLE_AES_KEY,
    )
    mock_db_connector.dequeue_activation_request.assert_awaited_once_with(device=device)


async def test_activate_device(api_client: TestClient) -> None:
    device = Device(
        id=1,
        user_id=EXAMPLE_CLIENT_ID,
        name="device1",
        key=EXAMPLE_AES_KEY,
        activated=False,
    )
    mock_db_connector.get_device.reset_mock()
    mock_db_connector.get_device.return_value = device
    mock_db_connector.activate_device.reset_mock()
    mock_db_connector.activate_device.return_value = device

    record_data = SerialNumber(serial_number="krecikpukawtaborecik")
    encrypted_message = encrypt_aes256(
        message=record_data.model_dump_json(),
        key=EXAMPLE_AES_KEY,
        iv=EXAMPLE_AES_IV,
    )

    result = api_client.request(
        method="PATCH",
        url="/devices/1/activate",
        json={"encrypted_message": encrypted_message},
    )

    assert result.status_code == status.HTTP_200_OK, result.text
    mock_db_connector.get_device.assert_awaited_once_with(device_id=device.id)
    mock_db_connector.activate_device.assert_awaited_once_with(
        device=device,
        serial_number="krecikpukawtaborecik",
    )
