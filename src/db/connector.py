from api.contracts import WeatherRecord, WeatherRecordQuery


class DBConnector:
    def __init__(self) -> None:
        pass

    def get_weather_records(
        self,
        query: WeatherRecordQuery,
    ) -> list[WeatherRecord]:
        pass

    def save_weather_record(self, weather_record: WeatherRecord) -> None:
        pass
