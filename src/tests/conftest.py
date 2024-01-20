import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes

EXAMPLE_AES_KEY = "a" * 32
EXAMPLE_AES_IV = "b" * 16


def encrypt_aes256(message: str, key: str, iv: str) -> str:
    encoded_message = message.encode("utf-8")
    encoded_key = key.encode("utf-8")
    encoded_iv = iv.encode("utf-8")
    cipher = Cipher(algorithms.AES256(encoded_key), modes.CFB(encoded_iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(encoded_message) + encryptor.finalize()
    return base64.b64encode(encoded_iv).decode("utf-8") + base64.b64encode(ciphertext).decode("utf-8")
