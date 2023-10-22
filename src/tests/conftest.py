import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
async def api_client() -> TestClient:
    return TestClient(app=app)
