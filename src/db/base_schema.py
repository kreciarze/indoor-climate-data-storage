from datetime import datetime

from pydantic import BaseModel


class BaseTimeModel(BaseModel):
    created_at: datetime | None
    updated_at: datetime | None
