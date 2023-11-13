import pytest

from auth.tokens import TokenEncoder


@pytest.mark.parametrize(
    ("user_id", "expected_token"),
    [
        pytest.param(
            1,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6InVzZXIiLCJjbGllbnRfaWQiOjF9."
            "aZB6xEArT6dNmybR6DyCSnslvER8WSvEstDDuQ35sFk",
            id="user with id=1",
        ),
        pytest.param(
            2,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6InVzZXIiLCJjbGllbnRfaWQiOjJ9."
            "w_u_7i8m9vnBYNsTffMR_GlO9d0slNt4Pib70LfrkJw",
            id="user with id=2",
        ),
    ],
)
def test_encode_user_token(
    user_id: int,
    expected_token: str,
    token_encoder: TokenEncoder,
) -> None:
    token = token_encoder.encode_user_token(user_id=user_id)
    assert token == expected_token


@pytest.mark.parametrize(
    ("device_id", "expected_token"),
    [
        pytest.param(
            1,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6ImRldmljZSIsImNsaWVudF9pZCI6MX0."
            "rgyVn5etFsiwc1VL96MQ1eVJY7-AUFiFs_TM2fTMZP4",
            id="device with id=1",
        ),
        pytest.param(
            2,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6ImRldmljZSIsImNsaWVudF9pZCI6Mn0."
            "3oXHMQ7hZynuRrEmlRo_QyFxQqXx4kCm0pUKbzoRSMc",
            id="device with id=2",
        ),
    ],
)
def test_encode_device_token(
    device_id: int,
    expected_token: str,
    token_encoder: TokenEncoder,
) -> None:
    token = token_encoder.encode_device_token(device_id=device_id)
    assert token == expected_token
