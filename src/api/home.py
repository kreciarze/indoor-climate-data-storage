from fastapi import status

from api.base_router import BaseRouter

router = BaseRouter()


@router.api_route(
    "/",
    status_code=status.HTTP_200_OK,
)
async def home() -> str:
    return "Welcome to Indoor Climate Data Storage API"
