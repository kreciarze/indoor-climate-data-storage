import asyncio

import pytest
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.connector import DBConnector
from db.models.base import Base

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    url=TEST_DB_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestDBSession = async_sessionmaker(
    autoflush=False,
    bind=test_engine,
)


async def setup_db() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(setup_db())


@pytest.fixture()
async def db_connector() -> DBConnector:
    session = TestDBSession()
    try:
        yield DBConnector(session=session)
    finally:
        await session.close()
