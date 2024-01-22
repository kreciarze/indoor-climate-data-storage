from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes

EXAMPLE_AES_KEY = "a" * 64
EXAMPLE_AES_IV = "b" * 32


def encrypt_aes256(
    key: str,
    iv: str,
    message: str,
) -> str:
    cipher = Cipher(
        algorithms.AES256(bytes.fromhex(key)),
        modes.CFB(bytes.fromhex(iv)),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode("utf-8")) + encryptor.finalize()
    return iv + ciphertext.hex()
