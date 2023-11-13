from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.tokens import ClientType, create_token_decoder, TokenDecoder

security = HTTPBearer()


async def extract_user_id_from_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    token_decoder: Annotated[TokenDecoder, Depends(create_token_decoder)],
) -> int:
    return token_decoder.extract_client_id(
        token=credentials.credentials,
        expected_client_type=ClientType.USER,
    )


async def extract_device_id_from_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    token_decoder: Annotated[TokenDecoder, Depends(create_token_decoder)],
) -> int:
    return token_decoder.extract_client_id(
        token=credentials.credentials,
        expected_client_type=ClientType.DEVICE,
    )
