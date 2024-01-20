from pydantic import BaseModel


class DeviceName(BaseModel):
    name: str


class DeviceData(DeviceName):
    device_id: int


class DeviceCreateRequest(DeviceName):
    key: str


class DeviceActivateDecryptedMessage(BaseModel):
    serial_number: str


class DeviceActivateRequest(BaseModel):
    encrypted_message: str
