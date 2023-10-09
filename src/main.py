from logging.config import dictConfig

from fastapi import FastAPI

from api.devices.routes import router as devices_router
from api.exception_handlers import (
    device_not_exists_handler,
    invalid_client_type_handler,
    login_already_exists_handler,
    token_error_handler,
    user_not_exists_handler,
)
from api.records.routes import router as records_router
from api.users.routes import router as users_router
from auth.exceptions import InvalidClientType, TokenError
from db.exceptions import DeviceNotExists, LoginAlreadyExists, UserNotExists
from settings import settings

dictConfig(settings.logging)

app = FastAPI(
    title="indoor-climate-data-storage",
    debug=settings.debug,
)

app.add_exception_handler(DeviceNotExists, handler=device_not_exists_handler)
app.add_exception_handler(UserNotExists, handler=user_not_exists_handler)
app.add_exception_handler(LoginAlreadyExists, handler=login_already_exists_handler)
app.add_exception_handler(InvalidClientType, handler=invalid_client_type_handler)
app.add_exception_handler(TokenError, handler=token_error_handler)

app.include_router(users_router, tags=["users"])
app.include_router(devices_router, tags=["devices"])
app.include_router(records_router, tags=["records"])
