from typing import Annotated

from fastapi import Depends, status

from api.base_router import BaseRouter
from api.devices.contracts import DeviceActivateDecryptedMessage, DeviceActivateRequest, DeviceCreateRequest, DeviceData
from auth.aes import decrypt_request
from auth.auth import extract_user_id_from_bearer
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
    request: DeviceCreateRequest,
) -> DeviceData:
    device = await db_connector.create_device(
        user_id=user_id,
        name=request.name,
        key=request.key,
    )
    return DeviceData(
        device_id=device.id,
        name=device.name,
    )


@router.delete(
    path="/{device_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
) -> DeviceData:
    deleted_device = await db_connector.remove_device(
        user_id=user_id,
        device_id=device_id,
    )
    return DeviceData(
        device_id=deleted_device.id,
        name=deleted_device.name,
    )


@router.post(
    path="/{device_id}/activate",
    status_code=status.HTTP_201_CREATED,
)
async def activate_device(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
    request: DeviceActivateRequest,
) -> None:
    device = await db_connector.get_device_by_id(device_id=device_id)
    decrypted_message = decrypt_request(
        encrypted_message=request.encrypted_message,
        key=device.key,
        model=DeviceActivateDecryptedMessage,
    )
    await db_connector.activate_device(
        device=device,
        serial_number=decrypted_message.serial_number,
    )
