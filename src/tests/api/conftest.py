from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient

from auth.auth import extract_user_id_from_bearer
from auth.tokens import create_token_decoder, create_token_encoder, TokenDecoder, TokenEncoder
from db.connector import create_db_connector, DBConnector
from main import app

EXAMPLE_DATETIME = "2023-10-29T10:22:12.003Z"
EXAMPLE_CLIENT_ID = 2137

mock_db_connector = create_autospec(DBConnector)
mock_token_encoder = create_autospec(TokenEncoder)
mock_token_decoder = create_autospec(TokenDecoder)


async def override_db_connector() -> DBConnector:
    return mock_db_connector


async def override_token_encoder() -> TokenEncoder:
    return mock_token_encoder


async def override_token_decoder() -> TokenDecoder:
    return mock_token_decoder


async def override_client_id() -> int:
    return EXAMPLE_CLIENT_ID


app.dependency_overrides = {
    create_db_connector: override_db_connector,
    create_token_encoder: override_token_encoder,
    create_token_decoder: override_token_decoder,
    extract_user_id_from_bearer: override_client_id,
}


@pytest.fixture()
async def api_client() -> TestClient:
    return TestClient(app=app)
