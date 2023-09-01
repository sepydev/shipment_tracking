import asyncio
import json
import unittest
from unittest.mock import MagicMock

from weather_info.python_weather_imp import WeatherInfoImp


class TestWeatherInfoImp(unittest.TestCase):

    def test_get_weather_cached(self):
        # Arrange
        city = "New York"
        weather_info_json = json.dumps({
            "city": "New York",
            "temperature": 75.0,
            "wind_speed": 10.0,
            "wind_direction": "NW",
            "pressure": 1015.0,
            "humidity": 60,
            "description": "Sunny",
        })

        weather_info_imp = WeatherInfoImp(redis_url="redis://localhost:6379")
        weather_info_imp.redis.get = MagicMock(return_value=weather_info_json)

        weather_info = asyncio.run(weather_info_imp.get_weather(city))

        # Assert
        self.assertIsNotNone(weather_info)
        self.assertEqual(weather_info.city, "New York")
        self.assertEqual(weather_info.temperature, 75.0)
        self.assertEqual(weather_info.wind_speed, 10.0)
        self.assertEqual(weather_info.wind_direction, "NW")
        self.assertEqual(weather_info.pressure, 1015.0)
        self.assertEqual(weather_info.humidity, 60)
        self.assertEqual(weather_info.description, "Sunny")

    def test_get_weather_not_cached(self):
        city = "New York"

        weather_info_imp = WeatherInfoImp(redis_url="redis://localhost:6379")
        weather_info_imp.redis.get = MagicMock(return_value=None)

        weather_info = asyncio.run(weather_info_imp.get_weather(city))
        self.assertIsNotNone(weather_info)
        self.assertEqual(weather_info.city, "New York")
        self.assertIsNotNone(weather_info.temperature)
        self.assertIsNotNone(weather_info.wind_speed)
        self.assertIsNotNone(weather_info.wind_direction)
        self.assertIsNotNone(weather_info.pressure)
        self.assertIsNotNone(weather_info.humidity)
        self.assertIsNotNone(weather_info.description)
