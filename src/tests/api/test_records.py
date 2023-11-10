from datetime import datetime, timezone

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from auth.auth import extract_device_id_from_bearer
from auth.exceptions import InvalidClientType
from auth.tokens import ClientType
from db.models.record import Record
from main import app
from tests.api.conftest import EXAMPLE_CLIENT_ID, EXAMPLE_DATETIME, mock_db_connector


async def raise_invalid_client_type() -> None:
    raise InvalidClientType(
        actual_client_type=ClientType.USER,
        expected_client_type=ClientType.DEVICE,
    )


async def test_validating_user_type(
    api_client: TestClient,
    fastapi_dep,
) -> None:
    with fastapi_dep(app).override({extract_device_id_from_bearer: raise_invalid_client_type}):
        result = api_client.request(
            method="POST",
            url="/records",
            json={
                "when": EXAMPLE_DATETIME,
                "temperature": 21.37,
                "pressure": 1,
            },
        )

    assert result.status_code == status.HTTP_403_FORBIDDEN, result.text
    assert result.json() == {
        "message": "Only devices are allowed to perform this action. Expected `device`, but got `user`.",
    }


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
    mock_db_connector.create_record.reset_mock()

    result = api_client.request(
        method="POST",
        url="/records",
        json={
            "when": EXAMPLE_DATETIME,
            "temperature": 21.37,
            "pressure": 420,
        },
    )

    assert result.status_code == status.HTTP_201_CREATED, result.text
    mock_db_connector.create_record.assert_awaited_once_with(
        device_id=EXAMPLE_CLIENT_ID,
        when=datetime.strptime(EXAMPLE_DATETIME, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc),
        temperature=21.37,
        pressure=420,
    )
