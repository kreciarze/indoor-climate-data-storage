from typing import TypeVar

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from pydantic import BaseModel

from auth.exceptions import InvalidEncryption

T = TypeVar("T", bound=BaseModel)


def decrypt_request(
    key: str,
    request: str,
    model: type[T],
) -> T:
    try:
        json_data = decrypt_aes256(
            key=key,
            iv=request[:32],
            message=request[32:],
        )
        return model.model_validate_json(json_data=json_data)
    except ValueError as e:
        raise InvalidEncryption("Invalid data, should be hex value.", original_exc=e)


def decrypt_aes256(
    key: str,
    iv: str,
    message: str,
) -> str:
    cipher = Cipher(algorithms.AES256(bytes.fromhex(key)), modes.CFB(bytes.fromhex(iv)), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(bytes.fromhex(message)) + decryptor.finalize()
    return decrypted_message.decode("utf-8")
