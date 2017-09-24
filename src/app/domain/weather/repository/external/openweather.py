
import requests
from app.domain.weather import city
from app.domain.weather.errors import InvalidCityNameError
from .errors import ExternalWeatherDataProviderNotInitialisedError, ExternalWeatherDataProviderBadAPIKey

_CITIES_IDS = {
    city.EDINBURGH: 3333229,
}


class OpenWeatherRepository:

    def __init__(self, api_url: str, api_key: str):
        self._api_url = api_url
        self._api_key = api_key

    def get_weather_data(self, city_name: str) -> city.CityData: # work in progress, the result is None at the moment...

        # Let's start with some input checking...
        if not self._api_url:
            raise ExternalWeatherDataProviderNotInitialisedError()
        if city_name not in city.AVAILABLE_CITIES_NAMES:
            raise InvalidCityNameError(city_name)

        # Go!
        endpoint_url = '{}/weather'.format(self._api_url)
        endpoint_params = {
            'id': _CITIES_IDS[city_name],
            'APPID': self._api_key,
        }

        api_response = requests.get(endpoint_url, params=endpoint_params)

        if api_response.status_code == 401 and 'Invalid API key' in api_response.text:
            raise ExternalWeatherDataProviderBadAPIKey(self._api_key)

        raw_result = api_response.json()
        pass
