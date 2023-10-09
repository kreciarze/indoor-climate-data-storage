from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette_context.middleware import RawContextMiddleware

from api import routes
from settings import settings

dictConfig(settings.logging)

app = FastAPI(
    title="weather-records-service",
    debug=settings.debug,
    middleware=[Middleware(RawContextMiddleware, plugins=())],
)

app.include_router(routes.router, tags=["weather records"])
