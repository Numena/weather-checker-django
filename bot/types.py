from dataclasses import dataclass


@dataclass
class WeatherInfo:
    city: str
    temperature: float
    description: str
    icon: str