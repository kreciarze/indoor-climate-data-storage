from pydantic import AwareDatetime, BaseModel


class RecordData(BaseModel):
    when: AwareDatetime
    temperature: float
    pressure: float


class AssignedRecordData(RecordData):
    device_id: int
    when: AwareDatetime
    temperature: float
    pressure: float
