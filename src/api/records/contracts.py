from pydantic import AwareDatetime, BaseModel


class RecordData(BaseModel):
    when: AwareDatetime
    temperature: float
    pressure: float


class RecordDataWithDeviceId(RecordData):
    device_id: str


class RecordCreateRequest(BaseModel):
    device_id: str
    encrypted_message: str
