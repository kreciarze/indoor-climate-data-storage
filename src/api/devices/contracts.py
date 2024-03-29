from pydantic import BaseModel


class DeviceData(BaseModel):
    id: str  # noqa: A003
    user_id: int | None = None
    name: str | None = None
    activated: bool


class SerialNumber(BaseModel):
    serial_number: str


class DeviceKey(BaseModel):
    key: str


class DeviceAssignRequest(DeviceKey):
    name: str


class DeviceActivateRequest(BaseModel):
    encrypted_message: str
