import base64
import binascii
from typing import TypeVar

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from pydantic import BaseModel

from auth.exceptions import InvalidEncryption

T = TypeVar("T", bound=BaseModel)


def decrypt_request(
    encrypted_message: str,
    key: str,
    model: type[T],
) -> T:
    try:
        json_data = decrypt_aes256(
            encoded_iv=encrypted_message[:24],
            encrypted_message=encrypted_message[24:],
            key=key,
        )
        return model.model_validate_json(json_data=json_data)
    except binascii.Error as e:
        raise InvalidEncryption("Invalid base64 encoded data.", original_exc=e)


def decrypt_aes256(encoded_iv: str, encrypted_message: str, key: str) -> str:
    iv = base64.b64decode(encoded_iv)
    ciphertext = base64.b64decode(encrypted_message)

    cipher = Cipher(algorithms.AES256(key.encode("utf-8")), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_message.decode("utf-8")
