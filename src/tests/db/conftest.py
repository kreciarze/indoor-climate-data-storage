import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from db.connector import DBConnector
from db.engine import engine


@pytest.fixture()
async def db_connector() -> DBConnector:
    connection = engine.connect()
    await connection.start()
    transaction = connection.begin()
    session = AsyncSession(bind=connection)
    try:
        yield DBConnector(postgres_session=session)
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()
