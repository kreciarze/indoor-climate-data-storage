from datetime import datetime

from pydantic import BaseModel


class WeatherRecordQuery(BaseModel):
    device_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class WeatherRecord(BaseModel):
    device_id: int
    when: datetime
    temperature: float
    pressure: float
