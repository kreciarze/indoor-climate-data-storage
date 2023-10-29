from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.tokens import ClientType, token_decoder

security = HTTPBearer()


async def extract_user_id_from_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> int:
    return await token_decoder.extract_client_id(
        token=credentials.credentials,
        expected_client_type=ClientType.USER,
    )


async def extract_device_id_from_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> int:
    return await token_decoder.extract_client_id(
        token=credentials.credentials,
        expected_client_type=ClientType.DEVICE,
    )
