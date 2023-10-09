from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings

engine = create_async_engine(
    url=settings.postgres.uri,
    echo=settings.debug,
    poolclass=NullPool,
)
DBSession = async_sessionmaker(
    autoflush=False,
    bind=engine,
)
