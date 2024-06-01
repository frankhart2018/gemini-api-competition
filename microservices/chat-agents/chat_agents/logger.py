import requests
from datetime import datetime
from enum import Enum

from .singleton import singleton
from .environment import LOGGER_URL, LOGGER_TOKEN


class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@singleton
class Logger:
    def __init__(self) -> None:
        self.__url = LOGGER_URL
        self.__token = LOGGER_TOKEN

    def log(self, log_level: LogLevel, message: str) -> None:
        if not self.__url or not self.__token:
            raise RuntimeError("Logger URL and token must be set")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__token}",
        }

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        data = {"dt": current_time, "message": f"{log_level.value}: {message}"}

        response = requests.post(self.__url, headers=headers, json=data)
        if response.status_code != 202:
            print(f"Failed to log message: {message}")
