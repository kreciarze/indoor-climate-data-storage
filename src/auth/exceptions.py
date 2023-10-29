class InvalidClientType(Exception):
    def __init__(
        self,
        actual_client_type: str,
        expected_client_type: str,
    ) -> None:
        super().__init__()
        self.actual_client_type = actual_client_type
        self.expected_client_type = expected_client_type


class TokenError(Exception):
    def __init__(
        self,
        original_exc: Exception,
    ) -> None:
        super().__init__()
        self.original_exc = original_exc
