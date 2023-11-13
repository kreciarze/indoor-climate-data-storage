from enum import auto, StrEnum

from jose import JOSEError, jwt

from auth.exceptions import InvalidClientType, TokenError
from settings import settings


class ClientType(StrEnum):
    USER = auto()
    DEVICE = auto()


class TokenEncoder:
    def __init__(self, service_secret: str) -> None:
        self.service_secret = service_secret

    def encode_user_token(self, user_id: int) -> str:
        return self.encode_token(
            client_type=ClientType.USER,
            client_id=user_id,
        )

    def encode_device_token(self, device_id: int) -> str:
        return self.encode_token(
            client_type=ClientType.DEVICE,
            client_id=device_id,
        )

    def encode_token(
        self,
        client_type: ClientType,
        client_id: int,
    ) -> str:
        try:
            return jwt.encode(
                claims={
                    "client_type": client_type,
                    "client_id": client_id,
                    # TODO: add expiration
                },
                key=self.service_secret,
            )
        except JOSEError as exc:
            raise TokenError(original_exc=exc)


class TokenDecoder:
    def __init__(self, service_secret: str) -> None:
        self.service_secret = service_secret

    def extract_client_id(
        self,
        token: str,
        expected_client_type: ClientType,
    ) -> int:
        data = self.decode_token(token=token)
        actual_client_type = data.get("client_type")
        if actual_client_type != expected_client_type:
            raise InvalidClientType(
                actual_client_type=actual_client_type,
                expected_client_type=expected_client_type,
            )

        return data["client_id"]

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token=token,
                key=self.service_secret,
                options={
                    "verify_signature": False,  # TODO: remove
                    "verify_aud": False,
                    "verify_iss": False,
                },
            )
        except JOSEError as exc:
            raise TokenError(original_exc=exc)


def create_token_encoder() -> TokenEncoder:
    return TokenEncoder(service_secret=settings.service_secret)


def create_token_decoder() -> TokenDecoder:
    return TokenDecoder(service_secret=settings.service_secret)
