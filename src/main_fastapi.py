from logging.config import dictConfig

from fastapi import FastAPI

from api.common.routers import health_check
from api.v1.routers import devices, merchants
from config import settings
from utils.middlewares.auth_middleware import OKTATokenAuthorizationMiddleware
from utils.routers.base_router import API_V1_PREFIX

dictConfig(settings.logging)

app = FastAPI(
    title="weather-records-service",
    debug=settings.debug,
    exception_handlers={AuthException: auth_exception_handler},
    middleware=[spoton_context_middleware],
)

app.include_router(health_check.router, tags=["health"])
app.include_router(merchants.router, tags=["merchants"])
app.include_router(devices.router, tags=["devices"])

app.add_middleware(
    OKTATokenAuthorizationMiddleware,
    path_allowed_prefix=API_V1_PREFIX,
    skip_paths=["/api/v1/okta_information"],
)
