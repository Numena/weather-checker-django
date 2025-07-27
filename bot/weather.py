import logging
import os
import httpx
import requests
from dotenv import load_dotenv
from bot.types import dataclass, WeatherInfo

load_dotenv()
logger = logging.getLogger(__name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather(city: str, lang: str = 'ru') -> WeatherInfo | None:
    if not OPENWEATHER_API_KEY:
        logger.error('API key for Openweather is not set')
        return None

    try:
        resp = requests.get('https://api.openweathermap.org/data/2.5/weather',
        params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric", "lang": lang}
        )

        resp.raise_for_status()
        d = resp.json()
        return WeatherInfo(
            city=d['name'],
            temperature=d['main']['temp'],
            description=d['weather'][0]['description'],
            icon=d['weather'][0]['icon'],
        )
    except requests.RequestException as e:
        logger.error(f'Weather fetch failed: {e}')
        return None

