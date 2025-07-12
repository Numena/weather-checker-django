import logging
import os
import httpx
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather(city: str) -> dict:
    if not OPENWEATHER_API_KEY:
        logger.error('API key for Openweather is not set')
        return {'error': 'APIKeyMissing'}

    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang':'en'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                'city': data.get('name'),
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }

        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error for {city}: {e}")
            return {'error': 'HTTPError'}

        except requests.exceptions.Timeout:
            logger.warning(f'Timeout while fetching weather city {city}')
            return {'error': 'Timeout'}

        except requests.exceptions.ConnectionError:
            logger.warning(f'Connection error for {city}')
            return {'error': 'ConnectionError'}

        except Exception as e:
            logger.error(f'Unknown error for {city}: {e}')
            return {'error': str(e)}
