from typing import Annotated

from fastapi import Depends, status
from pydantic import AwareDatetime

from api.base_router import BaseRouter
from api.records.contracts import AssignedRecordData, RecordData
from auth.auth import extract_device_id_from_bearer, extract_user_id_from_bearer
from db.connector import create_db_connector, DBConnector

router = BaseRouter(prefix="/records")


@router.get(
    path="",
    response_description="List of weather records in some period.",
    status_code=status.HTTP_200_OK,
)
async def list_records(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int | None = None,
    start_date: AwareDatetime | None = None,
    end_date: AwareDatetime | None = None,
) -> list[AssignedRecordData]:
    records = await db_connector.list_records(
        user_id=user_id,
        device_id=device_id,
        start_date=start_date,
        end_date=end_date,
    )
    return [
        AssignedRecordData(
            device_id=record.device_id,
            when=record.when,
            temperature=record.temperature,
            pressure=record.pressure,
        )
        for record in records
    ]


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
)
async def create_record(
    device_id: Annotated[int, Depends(extract_device_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    record_data: RecordData,
) -> None:
    await db_connector.create_record(
        device_id=device_id,
        when=record_data.when,
        temperature=record_data.temperature,
        pressure=record_data.pressure,
    )
