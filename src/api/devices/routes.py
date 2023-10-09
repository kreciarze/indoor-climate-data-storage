from typing import Annotated

from fastapi import Depends, status

from api.base_router import BaseRouter
from api.devices.contracts import DeviceBearerToken, DeviceData, DeviceDataWithBearer, DeviceName
from auth.auth import extract_user_id_from_bearer
from auth.tokens import token_encoder
from db.connector import create_db_connector, DBConnector

router = BaseRouter(prefix="/devices")


@router.get(
    path="",
    response_description="List of devices attached to user account.",
    status_code=status.HTTP_200_OK,
)
async def list_devices(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
) -> list[DeviceData]:
    devices = await db_connector.list_devices(user_id=user_id)
    return [DeviceData(name=device.name, device_id=device.id) for device in devices]


@router.post(
    path="",
    response_description="Created device.",
    status_code=status.HTTP_201_CREATED,
)
async def create_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_name: DeviceName,
) -> DeviceDataWithBearer:
    device = await db_connector.create_device(
        user_id=user_id,
        name=device_name.name,
    )
    bearer_token = await token_encoder.encode_device_token(device_id=device.id)
    return DeviceDataWithBearer(
        device_id=device.id,
        name=device.name,
        device_bearer_token=bearer_token,
    )


@router.delete(
    path="/{device_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
) -> None:
    await db_connector.remove_device(
        user_id=user_id,
        device_id=device_id,
    )


@router.post(
    path="/{device_id}/login",
    response_description="Bearer token for device authentication.",
    status_code=status.HTTP_201_CREATED,
)
async def login_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
) -> DeviceBearerToken:
    await db_connector.get_device(user_id=user_id, device_id=device_id)
    bearer_token = await token_encoder.encode_device_token(device_id=device_id)
    return DeviceBearerToken(device_bearer_token=bearer_token)
