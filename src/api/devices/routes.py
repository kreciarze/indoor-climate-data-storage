import logging
from typing import Annotated

from fastapi import Depends, status

from api.base_router import BaseRouter
from api.devices.contracts import DeviceActivateRequest, DeviceData, DeviceKey, SerialNumber
from auth.aes import decrypt_request
from auth.auth import extract_user_id_from_bearer
from db.connector import create_db_connector, DBConnector

logger = logging.getLogger(__name__)


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
    return [
        DeviceData(
            id=device.id,
            user_id=device.user_id,
            name=device.name,
            activated=device.activated,
        )
        for device in devices
    ]


@router.post(
    path="",
    description="Use to register new device.",
    response_description="Created device.",
    status_code=status.HTTP_201_CREATED,
)
async def create_device(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    request: SerialNumber,
) -> DeviceData:
    device = await db_connector.create_device(serial_number=request.serial_number)
    logger.info(f"Created new device with ID: {device.id}.")
    return DeviceData(
        id=device.id,
        user_id=device.user_id,
        name=device.name,
        activated=device.activated,
    )


@router.post(
    path="/{device_id}/assign",
    response_description="Assign device to user.",
    status_code=status.HTTP_200_OK,
)
async def assign_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
    request: DeviceKey,
) -> DeviceData:
    device = await db_connector.get_device(device_id=device_id)
    device = await db_connector.assign_device(device=device, user_id=user_id, key=request.key)
    logger.info(f"Assigned device {device.name} with ID: {device.id} to user with ID {user_id}.")
    return DeviceData(
        id=device.id,
        user_id=device.user_id,
        name=device.name,
        activated=device.activated,
    )


@router.post(
    path="/{device_id}/unassign",
    status_code=status.HTTP_200_OK,
)
async def unassign_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
) -> DeviceData:
    device = await db_connector.get_user_device(user_id=user_id, device_id=device_id)
    device = await db_connector.unassign_device(device=device)
    logger.info(f"Unassigned device {device.name} with ID: {device.id}.")
    return DeviceData(
        id=device.id,
        user_id=device.user_id,
        name=device.name,
        activated=device.activated,
    )


@router.post(path="/{device_id}/activate", response_description="Activate device.", status_code=status.HTTP_200_OK)
async def activate_device(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
    request: DeviceActivateRequest,
) -> None:
    device = await db_connector.get_device(device_id=device_id)
    decrypted_message = decrypt_request(
        encrypted_message=request.encrypted_message,
        key=device.key,
        model=SerialNumber,
    )
    logger.info(
        f"Activated device {device.name} with ID: {device.id} and serial number {decrypted_message.serial_number}.",
    )
    await db_connector.activate_device(
        device=device,
        serial_number=decrypted_message.serial_number,
    )


@router.get(
    path="/{device_id}/device-key",
    status_code=status.HTTP_200_OK,
)
async def get_device_key(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: int,
) -> DeviceKey:
    device = await db_connector.get_user_device(user_id=user_id, device_id=device_id)
    return DeviceKey(key=device.key)
