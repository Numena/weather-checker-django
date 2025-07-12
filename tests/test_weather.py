import requests

from bot import get_weather


# Imitate successful HTTP-request, return JSON
def test_get_weather_success(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return {
                    'name': 'London',
                    'main': {'temp': 22.5},
                    'weather': [{'description': 'clear sky','icon': '01d'}]
                }
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)

    result = get_weather('London')
    assert result['city'] == 'London'
    assert result['temperature'] == 22.5
    assert result['description'] == 'clear sky'
    assert result['icon'] == '01d'


# Imitate error with timeout
def test_get_weather_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout()

    monkeypatch.setattr(requests, 'get', mock_get)

    result = get_weather('Paris')
    assert result['error'] == 'Timeout'

# Imitate lost connection
def test_get_weather_connection_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(requests, 'get', mock_get)

    result = get_weather('Berlin')
    assert result['error'] == 'ConnectionError'

# Imitate HTTPError
def test_get_weather_http_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.HTTPError('404 Client Error')

    monkeypatch.setattr(requests,'get', mock_get)

    result = get_weather('UnknownCity')
    assert result['error'] == 'HTTPError'

def test_get_weather_unhandled_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise Exception('Unexpected crash')

    monkeypatch.setattr(requests, 'get', mock_get)

    result = get_weather('Tokyo')
    assert result['error'] == 'Unexpected crash'