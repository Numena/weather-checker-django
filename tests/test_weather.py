from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from bot.weather import get_weather


# Imitate successful HTTP-request, return JSON
@pytest.mark.asyncio
@patch('bot.weather.httpx.AsyncClient')
async def test_get_weather_success(mock_async_client_cls):
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'name': 'Berlin',
        'main': {'temp': 21.0},
        'weather': [{'description': 'clear sky', 'icon': '01d'}]
    }

    mock_response.raise_for_status.return_value = None
    mock_client.get.return_value = mock_response
    mock_async_client_cls.return_value.__aenter__.return_value = mock_client

    result = await get_weather('Berlin')

    assert result['city'] == 'Berlin'
    assert result['temperature'] == pytest.approx(21.0, abs=0.001)
    assert result['description'] == 'clear sky'
    assert result['icon'] == '01d'

@pytest.mark.asyncio
@patch('bot.weather.requests.get')
async def test_get_weather_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception('HTTP Error')
    mock_get.return_value = mock_response

    result = await get_weather('InvalidCity')
    assert 'error' in result

