from abc import ABC, abstractmethod
from typing import Optional

from weather_info.weather_info import WeatherInfo


class WeatherApiABC(ABC):
    @abstractmethod
    async def get_weather(self, city: str) -> Optional[WeatherInfo]:
        pass
