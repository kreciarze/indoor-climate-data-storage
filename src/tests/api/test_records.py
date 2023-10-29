import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.api.conftest import EXAMPLE_DATETIME, mock_db_connector


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

    result = api_client.request(
        method="GET",
        url="/records/",
        json=request_body,
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == []
    mock_db_connector.list_records.assert_awaited_once()
