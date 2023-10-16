from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings

engine = create_async_engine(
    url=settings.postgres.uri,
    echo=settings.debug,
    poolclass=NullPool,
)
PostgresSession = async_sessionmaker(bind=engine)
