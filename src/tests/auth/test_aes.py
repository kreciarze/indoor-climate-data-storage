from auth.aes import decrypt_aes256
from tests.conftest import encrypt_aes256, EXAMPLE_AES_IV, EXAMPLE_AES_KEY


def test_aes() -> None:
    message = "test message"
    encrypted_message = encrypt_aes256(
        message=message,
        key=EXAMPLE_AES_KEY,
        iv=EXAMPLE_AES_IV,
    )
    decrypted_message = decrypt_aes256(
        encoded_iv=encrypted_message[:24],
        encrypted_message=encrypted_message[24:],
        key=EXAMPLE_AES_KEY,
    )
    assert decrypted_message == message
