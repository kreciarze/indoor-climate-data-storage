from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    log_level: str = "INFO"
    logging_format: str = "%(name)s %(asctime)-15s %(levelname)s %(message)s"

    @property
    def _log_formatters(self) -> dict:
        if self.debug:
            return {
                "simple": {"format": self.logging_format},  # non-json for local dev
            }
        else:
            return {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": self.logging_format,
                },
            }

    @property
    def _log_filters(self) -> dict:
        return {"context_filter": {"()": "spoton.express.log.ContextFilter"}}

    @property
    def logging(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": self._log_formatters,
            "filters": self._log_filters,
            "handlers": {
                "stream": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple" if self.debug else "json",
                    "filters": ["context_filter"],
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
