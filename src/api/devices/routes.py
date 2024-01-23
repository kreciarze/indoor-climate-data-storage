from typing import Annotated

from fastapi import Depends, status

from api.base_router import BaseRouter
from api.devices.contracts import DeviceActivateRequest, DeviceAssignRequest, DeviceData, DeviceKey, SerialNumber
from auth.aes import decrypt_request
from auth.auth import extract_user_id_from_bearer
from db.connector import create_db_connector, DBConnector
from db.models.device import Device

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
            id=str(device.id),
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
    return DeviceData(
        id=str(device.id),
        user_id=device.user_id,
        name=device.name,
        activated=device.activated,
    )


@router.patch(
    path="/{device_id}/assign",
    response_description="Assign device to user.",
    status_code=status.HTTP_200_OK,
)
async def assign_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: str,
    request: DeviceAssignRequest,
) -> DeviceData:
    device = await db_connector.get_device(device_id=device_id)
    device = await db_connector.assign_device(
        device=device,
        user_id=user_id,
        name=request.name,
        key=request.key,
    )

    encoded_message = await db_connector.dequeue_activation_request(device=device)
    if encoded_message:
        device = await activate(
            db_connector=db_connector,
            device=device,
            encoded_message=encoded_message,
        )

    return DeviceData(
        id=str(device.id),
        user_id=device.user_id,
        name=device.name,
        activated=device.activated,
    )


@router.patch(
    path="/{device_id}/unassign",
    status_code=status.HTTP_200_OK,
)
async def unassign_device(
    user_id: Annotated[int, Depends(extract_user_id_from_bearer)],
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: str,
) -> DeviceData:
    device = await db_connector.get_user_device(user_id=user_id, device_id=device_id)
    device = await db_connector.unassign_device(device=device)
    return DeviceData(
        id=str(device.id),
        user_id=device.user_id,
        name=device.name,
        activated=device.activated,
    )


@router.patch(
    path="/{device_id}/activate",
    response_description="Activate device.",
    status_code=status.HTTP_200_OK,
)
async def activate_device(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    device_id: str,
    request: DeviceActivateRequest,
) -> DeviceData:
    device = await db_connector.get_device(device_id=device_id)

    if device.key:
        device = await activate(
            db_connector=db_connector,
            device=device,
            encoded_message=request.encrypted_message,
        )
    else:
        await db_connector.enqueue_activation_request(
            device=device,
            encrypted_message=request.encrypted_message,
        )

    return DeviceData(
        id=str(device.id),
        user_id=device.user_id,
        name=device.name,
        activated=device.activated,
    )


async def activate(
    db_connector: DBConnector,
    device: Device,
    encoded_message: str,
) -> Device:
    decrypted_message = decrypt_request(
        key=device.key,
        request=encoded_message,
        model=SerialNumber,
    )
    return await db_connector.activate_device(
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
    device_id: str,
) -> DeviceKey:
    device = await db_connector.get_user_device(user_id=user_id, device_id=device_id)
    return DeviceKey(key=device.key)
