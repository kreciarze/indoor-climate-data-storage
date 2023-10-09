class DeviceNotExists(Exception):
    def __init__(self, user_id: int, device_id: int) -> None:
        super().__init__()
        self.user_id = user_id
        self.device_id = device_id


class UserNotExists(Exception):
    pass


class LoginAlreadyExists(Exception):
    pass
