from pydantic import BaseModel


class DeviceName(BaseModel):
    name: str


class DeviceData(DeviceName):
    device_id: int


class DeviceBearerToken(BaseModel):
    device_bearer_token: str


class DeviceDataWithBearer(DeviceData, DeviceBearerToken):
    pass
