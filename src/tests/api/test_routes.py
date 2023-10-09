from datetime import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockFixture

from api.contracts import WeatherRecordQuery
from db.connector import DBConnector


@pytest.mark.parametrize(
    "query",
    [
        WeatherRecordQuery(),
        WeatherRecordQuery(device_id=1),
        WeatherRecordQuery(start_date=datetime.now()),
        WeatherRecordQuery(end_date=datetime.now()),
        WeatherRecordQuery(device_id=1, start_date=datetime.now()),
        WeatherRecordQuery(device_id=1, end_date=datetime.now()),
        WeatherRecordQuery(start_date=datetime.now(), end_date=datetime.now()),
    ],
)
async def test_get_weather_records(
    query: WeatherRecordQuery,
    api_client: TestClient,
    mocker: MockFixture,
) -> None:
    mock = mocker.patch.object(
        DBConnector,
        "get_weather_records",
        return_value=[],
    )

    result = api_client.request(
        method="GET",
        url="/weather_records/",
        json=query.model_dump(),
    )

    mock.assert_called_once_with(query=query)
    assert result.status_code == status.HTTP_200_OK
    assert result.json() == []
