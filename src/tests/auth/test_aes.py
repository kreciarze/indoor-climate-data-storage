from api.devices.contracts import SerialNumber
from auth.aes import decrypt_request
from tests.conftest import encrypt_aes256, EXAMPLE_AES_IV, EXAMPLE_AES_KEY


def test_aes() -> None:
    message = SerialNumber(serial_number="dupsko")
    encrypted_message = encrypt_aes256(
        key=EXAMPLE_AES_KEY,
        iv=EXAMPLE_AES_IV,
        message=message.model_dump_json(),
    )
    decrypted_message = decrypt_request(
        key=EXAMPLE_AES_KEY,
        request=encrypted_message,
        model=SerialNumber,
    )
    assert decrypted_message == message
