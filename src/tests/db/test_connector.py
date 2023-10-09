import pytest

from db.connector import DBConnector
from db.exceptions import UserNotExists


async def test_users_operations(db_connector: DBConnector) -> None:
    test_user_data = {
        "login": "test_login",
        "password": "test_password",  # noqa: S106
    }

    with pytest.raises(UserNotExists):
        await db_connector.get_user(**test_user_data)

    await db_connector.register_user(**test_user_data)

    user = await db_connector.get_user(**test_user_data)
    assert user.login == "test_login"
