from sqlalchemy import select

from db.connector import DBConnector
from db.engine import PostgresSession
from db.models.user import User, UserData


async def test_register_user(db_connector: DBConnector) -> None:
    user_data = UserData(login="test_login", password="test_password")  # noqa: S106
    
    await db_connector.register_user(user_data=user_data)

    async with PostgresSession() as session:
        result = await session.scalars(select(User).where(User.login == user_data.login))
        user = result.first()
    
    assert user is not None


async def test_user_exists(db_connector: DBConnector) -> None:
    user_data = UserData(login="test_login", password="test_password")  # noqa: S106
    
    do_exists = await db_connector.user_exists(user_data=user_data)
    assert do_exists is False
    
    async with PostgresSession() as session:
        user = User(
            login=user_data.login,
            password_hash="test_password_hash",
            devices=[],
        )
        session.add(user)
        await session.commit()

    do_exists = await db_connector.user_exists(user_data=user_data)
    assert do_exists is True
