from fastapi import status
from fastapi.testclient import TestClient

from auth.auth import extract_user_id_from_bearer
from auth.exceptions import InvalidClientType
from auth.tokens import ClientType
from db.exceptions import DeviceNotExists
from db.models.device import Device
from main import app
from tests.api.conftest import EXAMPLE_CLIENT_ID, mock_db_connector, mock_token_encoder


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


async def test_create_device(api_client: TestClient) -> None:
    mock_db_connector.create_device.reset_mock()
    mock_token_encoder.encode_device_token.reset_mock()
    mock_db_connector.create_device.return_value = Device(
        id=1,
        user_id=EXAMPLE_CLIENT_ID,
        name="device1",
    )
    mock_token_encoder.encode_device_token.return_value = "abc.def.gh"

    result = api_client.request(
        method="POST",
        url="/devices",
        json={"name": "device1"},
    )

    assert result.status_code == status.HTTP_201_CREATED, result.text
    assert result.json() == {
        "device_id": 1,
        "name": "device1",
        "device_bearer_token": "abc.def.gh",
    }
    mock_db_connector.create_device.assert_awaited_once_with(
        user_id=EXAMPLE_CLIENT_ID,
        name="device1",
    )
    mock_token_encoder.encode_device_token.assert_called_with(device_id=1)


async def test_remove_device(api_client: TestClient) -> None:
    mock_db_connector.remove_device.reset_mock()
    mock_db_connector.remove_device.return_value = Device(
        id=1,
        user_id=EXAMPLE_CLIENT_ID,
        name="device1",
    )

    result = api_client.request(
        method="DELETE",
        url="/devices/1",
    )

    assert result.status_code == status.HTTP_200_OK, result.text
    assert result.json() == {
        "device_id": 1,
        "name": "device1",
    }
    mock_db_connector.remove_device.assert_awaited_once()


async def test_remove_device_not_exists(api_client: TestClient) -> None:
    mock_db_connector.remove_device.reset_mock()
    mock_db_connector.remove_device.side_effect = DeviceNotExists(
        user_id=EXAMPLE_CLIENT_ID,
        device_id=1,
    )

    result = api_client.request(
        method="DELETE",
        url="/devices/1",
    )

    assert result.status_code == status.HTTP_404_NOT_FOUND, result.text
    assert result.json() == {"message": "User 2137 does not have device 1."}
    mock_db_connector.remove_device.assert_awaited_once()


async def test_login_device(api_client: TestClient) -> None:
    mock_db_connector.get_device.reset_mock()
    mock_token_encoder.encode_device_token.reset_mock()
    mock_token_encoder.encode_device_token.return_value = "abc.def.gh"

    result = api_client.request(
        method="POST",
        url="/devices/1/login",
    )

    assert result.status_code == status.HTTP_201_CREATED, result.text
    assert result.json() == {"device_bearer_token": "abc.def.gh"}
    mock_db_connector.get_device.assert_awaited_once_with(
        user_id=EXAMPLE_CLIENT_ID,
        device_id=1,
    )
    mock_token_encoder.encode_device_token.assert_called_with(device_id=1)
