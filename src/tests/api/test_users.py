import pytest
from fastapi import status
from fastapi.testclient import TestClient

from db.exceptions import LoginAlreadyExists, UserNotExists
from db.models.user import User
from tests.api.conftest import mock_db_connector, mock_token_encoder


@pytest.mark.parametrize(
    ("request_body", "expected_status_code"),
    [
        pytest.param(
            {"login": "user", "password": "pass"},
            status.HTTP_201_CREATED,
            id="correct payload",
        ),
        pytest.param(
            {"password": "pass"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id="missing login",
        ),
        pytest.param(
            {"login": "user"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id="missing password",
        ),
    ],
)
async def test_register(
    request_body: dict,
    expected_status_code: int,
    api_client: TestClient,
) -> None:
    mock_db_connector.register_user.reset_mock()

    result = api_client.request(
        method="POST",
        url="/users/register",
        json=request_body,
    )

    assert result.status_code == expected_status_code, result.text
    if str(expected_status_code).startswith("2"):
        mock_db_connector.register_user.assert_awaited_once()
    else:
        mock_db_connector.register_user.assert_not_awaited()


async def test_register_login_exists(api_client: TestClient) -> None:
    mock_db_connector.register_user.reset_mock()
    mock_db_connector.register_user.side_effect = LoginAlreadyExists

    result = api_client.request(
        method="POST",
        url="/users/register",
        json={"login": "user", "password": "pass"},
    )

    assert result.status_code == status.HTTP_400_BAD_REQUEST, result.text
    assert result.json() == {"message": "User with provided login already exists."}
    mock_db_connector.register_user.assert_awaited_once()


async def test_login(api_client: TestClient) -> None:
    mock_db_connector.get_user.reset_mock()
    mock_token_encoder.encode_user_token.reset_mock()
    mock_db_connector.get_user.return_value = User(  # noqa: S106
        id=1,
        login="user",
        password_hash="pass_hash",
        devices=[],
    )
    mock_token_encoder.encode_user_token.return_value = "abc.def.gh"

    result = api_client.request(
        method="POST",
        url="/users/login",
        json={"login": "user", "password": "pass"},
    )

    assert result.status_code == status.HTTP_201_CREATED, result.text
    assert result.json() == {"user_bearer_token": "abc.def.gh"}
    mock_db_connector.get_user.assert_awaited_once_with(  # noqa: S106
        login="user",
        password="pass",
    )
    mock_token_encoder.encode_user_token.assert_awaited_with(user_id=1)


async def test_login_user_not_exists(api_client: TestClient) -> None:
    mock_db_connector.get_user.side_effect = UserNotExists

    result = api_client.request(
        method="POST",
        url="/users/login",
        json={"login": "user", "password": "pass"},
    )

    assert result.status_code == status.HTTP_401_UNAUTHORIZED, result.text
    assert result.json() == {"message": "Could not find user with provided credentials."}
