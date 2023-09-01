import json
from dataclasses import asdict
from typing import Optional

import python_weather
import redis

from weather_info.weather_abstract import WeatherApiABC
from weather_info.weather_info import WeatherInfo


class WeatherInfoImp(WeatherApiABC):
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.redis = redis.from_url(self.redis_url)

    async def get_weather(self, city: str) -> Optional[WeatherInfo]:
        weather_info = self.redis.get(city)
        if weather_info:
            return WeatherInfo(**json.loads(weather_info))

        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            # fetch a weather forecast from a city
            weather = await client.get(city)
            weather_info = WeatherInfo(
                city=city,
                temperature=weather.current.temperature,
                wind_speed=weather.current.wind_speed,
                wind_direction=weather.current.wind_direction.name,
                pressure=weather.current.pressure,
                humidity=weather.current.humidity,
                description=weather.current.description,
            )
            self.redis.set(city, json.dumps(asdict(weather_info)), ex=60 * 60 * 2)
            return weather_info
