from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient

from auth.auth import extract_device_id_from_bearer, extract_user_id_from_bearer
from db.connector import create_db_connector, DBConnector
from main import app

EXAMPLE_DATETIME = "2023-10-29T10:22:12.003Z"
EXAMPLE_CLIENT_ID = 1

mock_db_connector = create_autospec(DBConnector)


async def override_db_connector() -> DBConnector:
    return mock_db_connector


async def override_client_id() -> int:
    return EXAMPLE_CLIENT_ID


app.dependency_overrides = {
    create_db_connector: override_db_connector,
    extract_user_id_from_bearer: override_client_id,
    extract_device_id_from_bearer: override_client_id,
}


@pytest.fixture()
async def api_client() -> TestClient:
    return TestClient(app=app)
