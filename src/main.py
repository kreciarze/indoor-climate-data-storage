from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.devices.routes import router as devices_router
from api.exception_handlers import (
    device_already_activated_handler,
    device_already_assigned_handler,
    device_not_exists_handler,
    invalid_client_type_handler,
    invalid_encryption_handler,
    invalid_serial_number_handler,
    login_already_exists_handler,
    serial_number_already_exists_handler,
    token_error_handler,
    user_not_exists_handler,
)
from api.home import router as home_router
from api.records.routes import router as records_router
from api.users.routes import router as users_router
from auth.exceptions import InvalidClientType, InvalidEncryption, TokenError
from db.exceptions import (
    DeviceAlreadyActivated,
    DeviceAlreadyAssigned,
    DeviceNotExists,
    InvalidSerialNumber,
    LoginAlreadyExists,
    SerialNumberAlreadyExists,
    UserNotExists,
)
from settings import settings

dictConfig(settings.logging)

app = FastAPI(
    title="indoor-climate-data-storage",
    version=settings.version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors.split("; "),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(DeviceNotExists, handler=device_not_exists_handler)
app.add_exception_handler(UserNotExists, handler=user_not_exists_handler)
app.add_exception_handler(LoginAlreadyExists, handler=login_already_exists_handler)
app.add_exception_handler(InvalidClientType, handler=invalid_client_type_handler)
app.add_exception_handler(TokenError, handler=token_error_handler)
app.add_exception_handler(InvalidEncryption, handler=invalid_encryption_handler)
app.add_exception_handler(InvalidSerialNumber, handler=invalid_serial_number_handler)
app.add_exception_handler(DeviceAlreadyActivated, handler=device_already_activated_handler)
app.add_exception_handler(SerialNumberAlreadyExists, handler=serial_number_already_exists_handler)
app.add_exception_handler(DeviceAlreadyAssigned, handler=device_already_assigned_handler)

app.include_router(home_router)
app.include_router(users_router, tags=["users"])
app.include_router(devices_router, tags=["devices"])
app.include_router(records_router, tags=["records"])
