import pytest

from auth.tokens import ClientType, TokenDecoder


@pytest.mark.parametrize(
    ("token", "expected_client_type"),
    [
        pytest.param(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6InVzZXIiLCJjbGllbnRfaWQiOjF9."
            "aZB6xEArT6dNmybR6DyCSnslvER8WSvEstDDuQ35sFk",
            ClientType.USER,
            id="user type",
        ),
        pytest.param(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6ImRldmljZSIsImNsaWVudF9pZCI6MX0."
            "rgyVn5etFsiwc1VL96MQ1eVJY7-AUFiFs_TM2fTMZP4",
            ClientType.DEVICE,
            id="device type",
        ),
    ],
)
def test_extract_client_id(
    token: str,
    expected_client_type: ClientType,
    token_decoder: TokenDecoder,
) -> None:
    result = token_decoder.extract_client_id(
        token=token,
        expected_client_type=expected_client_type,
    )
    assert result == 1


@pytest.mark.parametrize(
    ("token", "expected_result"),
    [
        pytest.param(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6InVzZXIiLCJjbGllbnRfaWQiOjF9."
            "aZB6xEArT6dNmybR6DyCSnslvER8WSvEstDDuQ35sFk",
            {
                "client_type": ClientType.USER,
                "client_id": 1,
            },
            id="user with id=1",
        ),
        pytest.param(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6InVzZXIiLCJjbGllbnRfaWQiOjJ9."
            "w_u_7i8m9vnBYNsTffMR_GlO9d0slNt4Pib70LfrkJw",
            {
                "client_type": ClientType.USER,
                "client_id": 2,
            },
            id="user with id=2",
        ),
        pytest.param(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6ImRldmljZSIsImNsaWVudF9pZCI6MX0."
            "rgyVn5etFsiwc1VL96MQ1eVJY7-AUFiFs_TM2fTMZP4",
            {
                "client_type": ClientType.DEVICE,
                "client_id": 1,
            },
            id="device with id=1",
        ),
        pytest.param(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJjbGllbnRfdHlwZSI6ImRldmljZSIsImNsaWVudF9pZCI6Mn0."
            "3oXHMQ7hZynuRrEmlRo_QyFxQqXx4kCm0pUKbzoRSMc",
            {
                "client_type": ClientType.DEVICE,
                "client_id": 2,
            },
            id="device with id=2",
        ),
    ],
)
def test_decode_token(
    token: str,
    expected_result: dict,
    token_decoder: TokenDecoder,
) -> None:
    result = token_decoder.decode_token(token)
    assert result == expected_result
