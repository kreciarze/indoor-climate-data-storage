from typing import Annotated

from fastapi import Depends, status

from api.base_router import BaseRouter
from api.users.contracts import UserBearerToken, UserData
from auth.tokens import create_token_encoder, TokenEncoder
from db.connector import create_db_connector, DBConnector

router = BaseRouter(prefix="/users")


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    user_data: UserData,
) -> None:
    await db_connector.register_user(
        login=user_data.login,
        password=user_data.password,
    )


@router.post(
    path="/login",
    status_code=status.HTTP_201_CREATED,
)
async def login(
    db_connector: Annotated[DBConnector, Depends(create_db_connector)],
    token_encoder: Annotated[TokenEncoder, Depends(create_token_encoder)],
    user_data: UserData,
) -> UserBearerToken:
    user = await db_connector.get_user(
        login=user_data.login,
        password=user_data.password,
    )
    bearer_token = token_encoder.encode_user_token(user_id=user.id)
    return UserBearerToken(user_bearer_token=bearer_token)
