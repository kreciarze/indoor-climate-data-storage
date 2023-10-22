from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JOSEError
from starlette import status

from settings import settings

security = HTTPBearer()


async def has_access(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> None:
    token = credentials.credentials

    try:
        jwt.decode(
            token,
            key=settings.service_secret,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
            },
        )
    except JOSEError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
