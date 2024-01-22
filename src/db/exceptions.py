class DeviceNotExists(Exception):
    def __init__(self, device_id: int, user_id: int | None = None) -> None:
        super().__init__()
        self.user_id = user_id
        self.device_id = device_id


class UserNotExists(Exception):
    pass


class LoginAlreadyExists(Exception):
    pass


class InvalidSerialNumber(Exception):
    pass


class DeviceAlreadyActivated(Exception):
    pass


class SerialNumberAlreadyExists(Exception):
    pass
