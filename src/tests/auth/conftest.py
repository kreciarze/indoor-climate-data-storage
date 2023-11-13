import pytest

from auth.tokens import TokenDecoder, TokenEncoder


@pytest.fixture()
async def token_encoder() -> TokenEncoder:
    return TokenEncoder(service_secret="test_secret")  # noqa: S106


@pytest.fixture()
async def token_decoder() -> TokenDecoder:
    return TokenDecoder(service_secret="test_secret")  # noqa: S106
