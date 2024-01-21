from datetime import datetime, timezone

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api.records.contracts import RecordData
from auth.exceptions import InvalidClientType
from auth.tokens import ClientType
from db.models.device import Device
from db.models.record import Record
from tests.api.conftest import EXAMPLE_CLIENT_ID, EXAMPLE_DATETIME, mock_db_connector
from tests.conftest import encrypt_aes256, EXAMPLE_AES_IV, EXAMPLE_AES_KEY


async def raise_invalid_client_type() -> None:
    raise InvalidClientType(
        actual_client_type=ClientType.USER,
        expected_client_type=ClientType.DEVICE,
    )


@pytest.mark.parametrize(
    "request_body",
    [
        {},
        {"device_id": 1},
        {"start_date": EXAMPLE_DATETIME},
        {"end_date": EXAMPLE_DATETIME},
        {"device_id": 1, "start_date": EXAMPLE_DATETIME},
        {"device_id": 1, "end_date": EXAMPLE_DATETIME},
        {"start_date": EXAMPLE_DATETIME, "end_date": EXAMPLE_DATETIME},
    ],
)
async def test_list_records(
    request_body: dict,
    api_client: TestClient,
) -> None:
    mock_db_connector.list_records.reset_mock()
    mock_db_connector.list_records.return_value = [
        Record(
            id=1,
            device_id=1,
            when=EXAMPLE_DATETIME,
            temperature=21.37,
            pressure=420,
        ),
    ]

    result = api_client.request(
        method="GET",
        url="/records",
        json=request_body,
    )

    assert result.status_code == status.HTTP_200_OK, result.text
    record_json = result.json()[0]
    assert record_json["device_id"] == 1
    assert "when" in record_json
    assert record_json["temperature"] == 21.37
    assert record_json["pressure"] == 420
    mock_db_connector.list_records.assert_awaited_once()


async def test_create_record(api_client: TestClient) -> None:
    DEVICE_ID = 1

    mock_db_connector.create_record.reset_mock()
    mock_db_connector.get_device.return_value = Device(
        id=DEVICE_ID,
        user_id=EXAMPLE_CLIENT_ID,
        name="device1",
        key=EXAMPLE_AES_KEY,
    )

    record_data = RecordData(
        when=EXAMPLE_DATETIME,
        temperature=21.37,
        pressure=420,
    )
    encrypted_message = encrypt_aes256(
        message=record_data.model_dump_json(),
        key=EXAMPLE_AES_KEY,
        iv=EXAMPLE_AES_IV,
    )

    result = api_client.request(
        method="POST",
        url="/records",
        json={
            "device_id": DEVICE_ID,
            "encrypted_message": encrypted_message,
        },
    )

    assert result.status_code == status.HTTP_201_CREATED, result.text
    mock_db_connector.create_record.assert_awaited_once_with(
        device_id=DEVICE_ID,
        when=datetime.strptime(EXAMPLE_DATETIME, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc),
        temperature=21.37,
        pressure=420.0,
    )
