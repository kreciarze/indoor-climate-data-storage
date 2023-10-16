from logging.config import dictConfig

from fastapi import Depends, FastAPI

from api.devices import router as devices_router
from api.records import router as records_router
from api.users import router as users_router
from auth import has_access
from settings import settings

dictConfig(settings.logging)

app = FastAPI(
    title="indoor-climate-data-storage",
    debug=settings.debug,
)

protection = [Depends(has_access)]

app.include_router(users_router, tags=["users"])
app.include_router(devices_router, tags=["devices"], dependencies=protection)
app.include_router(records_router, tags=["records"], dependencies=protection)
