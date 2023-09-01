from dataclasses import dataclass


@dataclass
class WeatherInfo:
    city: str
    temperature: float
    wind_speed: float
    wind_direction: str
    pressure: float
    humidity: float
    description: str