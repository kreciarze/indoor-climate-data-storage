from datetime import datetime
from typing import Annotated

from fastapi import Depends, status
from pydantic import BaseModel

from api.base_router import BaseRouter
from db.connector import create_db_connector, DBConnector, RecordQuery
from db.models.record import Record, RecordModel


class CreateRecordRequest(BaseModel):
    device_id: int
    when: datetime
    temperature: float
    pressure: float


router = BaseRouter(prefix="/records")


@router.get(
    path="",
    response_description="List of weather records in some period.",
    status_code=status.HTTP_200_OK,
)
async def get_records(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    record_query: RecordQuery,
) -> list[RecordModel]:
    return await db_connector.get_records(record_query=record_query)


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
)
async def create_record(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    create_record_request: CreateRecordRequest,
) -> None:
    record = Record(**create_record_request.model_dump())
    await db_connector.save_record(record=record)
