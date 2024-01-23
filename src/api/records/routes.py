from typing import Annotated

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from pydantic import AwareDatetime

from api.base_router import BaseRouter
from api.records.contracts import RecordCreateRequest, RecordData, RecordDataWithDeviceId
from auth.aes import decrypt_request
from auth.auth import extract_user_id_from_bearer
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
    device_id: str | None = None,
    start_date: AwareDatetime | None = None,
    end_date: AwareDatetime | None = None,
) -> list[RecordDataWithDeviceId]:
    records = await db_connector.list_records(
        user_id=user_id,
        device_id=device_id,
        start_date=start_date,
        end_date=end_date,
    )
    return [
        RecordDataWithDeviceId(
            device_id=str(record.device_id),
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
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    request: RecordCreateRequest,
) -> JSONResponse:
    device = await db_connector.get_device(device_id=request.device_id)
    if device.activated is False or device.key is None:
        return JSONResponse(
            content={"message": "Device is not activated yet."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    decrypted_message = decrypt_request(
        request=request.encrypted_message,
        key=device.key,
        model=RecordData,
    )
    await db_connector.create_record(
        device_id=request.device_id,
        when=decrypted_message.when,
        temperature=decrypted_message.temperature,
        pressure=decrypted_message.pressure,
    )
    return JSONResponse(
        content={"message": "Record created."},
        status_code=status.HTTP_201_CREATED,
    )
