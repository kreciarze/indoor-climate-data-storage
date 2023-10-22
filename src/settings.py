from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    user: str = "postgres"
    password: str = "password"
    host: str = "postgres"
    port: str = "5915"
    db_name: str = "postgres"

    @property
    def uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_nested_delimiter="__",
    )

    debug: bool = False
    log_level: str = "INFO"
    logging_format: str = "%(name)s %(asctime)-15s %(levelname)s %(message)s"

    service_secret: str = "secret"
    postgres: DatabaseSettings = DatabaseSettings()

    @property
    def logging(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"simple": {"format": self.logging_format}},
            "filters": {},
            "handlers": {
                "stream": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                },
            },
            "root": {"handlers": ["stream"], "level": self.log_level},
            "loggers": {
                "app": {
                    "level": "DEBUG",
                    "handlers": [],
                    "propagate": True,
                },
                "uvicorn": {
                    "level": "INFO",
                    "handlers": ["stream"],
                },
            },
        }


settings = Settings()
