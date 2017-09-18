
import requests
from app.domain.weather import city, InvalidCityNameError
from . import ExternalWeatherDataProviderNotInitialisedError, ExternalWeatherDataProviderBadAPIKey

_api_url: str = ''
_api_key: str = ''

_CITIES_IDS = {
    city.EDINBURGH: 3333229,
}


def init(api_url: str, api_key: str) -> None:
    global _api_url, _api_key
    _api_url = api_url
    _api_key = api_key


def get_weather_data(city_name: str) -> city.CityData: # work in progress, the result is None at the moment...
    global _api_url, _api_key

    # Let's start with some input checking...
    if not _api_url:
        raise ExternalWeatherDataProviderNotInitialisedError()
    if city_name not in city.AVAILABLE_CITIES_NAMES:
        raise InvalidCityNameError(city_name)

    # Go!
    endpoint_url = '{}/weather'.format(_api_url)
    endpoint_params = {
        'id': _CITIES_IDS[city_name],
        'APPID': _api_key,
    }

    api_response = requests.get(endpoint_url, params=endpoint_params)

    if api_response.status_code == 401 and 'Invalid API key' in api_response.text:
        raise ExternalWeatherDataProviderBadAPIKey(_api_key)

    raw_result = api_response.json()
    pass
