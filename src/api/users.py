from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from api.base_router import BaseRouter
from db.connector import create_db_connector, DBConnector
from db.models.user import UserData


class LoginResponse(BaseModel):
    bearer_token: str


router = BaseRouter(prefix="/users")


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    user_data: UserData,
) -> None:
    try:
        await db_connector.register_user(user_data=user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with provided login already exists.",
        )


@router.post(
    path="/login",
    status_code=status.HTTP_201_CREATED,
)
async def login(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    user_data: UserData,
) -> LoginResponse:
    result = await db_connector.user_exists(user_data=user_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found for provided credentials.",
        )
    bearer_token = "siema"
    return LoginResponse(bearer_token=bearer_token)
