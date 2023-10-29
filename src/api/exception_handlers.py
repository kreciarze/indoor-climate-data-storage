from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from auth.exceptions import TokenError
from auth.tokens import ClientType, InvalidClientType
from db.exceptions import DeviceNotExists, LoginAlreadyExists, UserNotExists


async def device_not_exists_handler(
    request: Request,
    exc: DeviceNotExists,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"User {exc.user_id} does not have device {exc.device_id}."},
    )


async def user_not_exists_handler(
    request: Request,
    exc: UserNotExists,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Could not find user with provided credentials."},
    )


async def login_already_exists_handler(
    request: Request,
    exc: LoginAlreadyExists,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "User with provided login already exists."},
    )


async def invalid_client_type_handler(
    request: Request,
    exc: InvalidClientType,
) -> JSONResponse:
    message = ""

    if exc.expected_client_type == ClientType.USER:
        message = "Only users are allowed to perform this action. "
    elif exc.expected_client_type == ClientType.DEVICE:
        message = "Only devices are allowed to perform this action. "

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": f"{message}Expected `{exc.expected_client_type}`, but got `{exc.actual_client_type}`."},
    )


async def token_error_handler(
    request: Request,
    exc: TokenError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "original_exception": exc.original_exc.__class__.__name__,
            "message": str(exc.original_exc),
        },
    )
