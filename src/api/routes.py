from typing import Annotated

from fastapi import Depends, status

from api.base_router import BaseRouter
from api.contracts import WeatherRecord, WeatherRecordQuery
from db.connector import DBConnector

router = BaseRouter()


@router.get(
    "/weather_records/",
    response_description="List of weather records in some period.",
    status_code=status.HTTP_200_OK,
)
async def get_weather_records(
    db_connector: Annotated[DBConnector, Depends(DBConnector)],
    weather_record_query: WeatherRecordQuery,
) -> list[WeatherRecord]:
    return db_connector.get_weather_records(query=weather_record_query)


@router.post(
    "/weather_records/",
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_weather_record(
    db_connector: Annotated[DBConnector, Depends(DBConnector)],
    weather_record: WeatherRecord,
) -> None:
    db_connector.save_weather_record(weather_record=weather_record)
