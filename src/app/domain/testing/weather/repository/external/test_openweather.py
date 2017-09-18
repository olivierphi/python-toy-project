# pylint: disable=invalid-name

import os
import pytest
from app.domain.weather import city, InvalidCityNameError
from app.domain.weather.repository.external import openweather, \
    ExternalWeatherDataProviderNotInitialisedError, \
    ExternalWeatherDataProviderBadAPIKey

VALID_API_KEY: str = os.getenv('TEST_OPENWEATHER_API_KEY', '')
INVALID_API_KEY: str = '123456'

def test_module_raise_error_if_used_without_prior_initialisation():
    with pytest.raises(ExternalWeatherDataProviderNotInitialisedError):
        openweather.get_weather_data(city.EDINBURGH)


def test_module_raise_error_if_used_with_an_unavailable_city_name():
    with pytest.raises(InvalidCityNameError):
        openweather.init('https://holygrail.com', '123')
        openweather.get_weather_data('Camelot')


def test_module_raise_error_with_invalid_api_key():
    with pytest.raises(ExternalWeatherDataProviderBadAPIKey):
        openweather.init('https://api.openweathermap.org/data/2.5', INVALID_API_KEY)
        openweather.get_weather_data(city.EDINBURGH)


def test_module_can_retrieve_city_weather_data():
    if not VALID_API_KEY:
        raise EnvironmentError('Missing "TEST_OPENWEATHER_API_KEY" environment variable')
    openweather.init('https://api.openweathermap.org/data/2.5', VALID_API_KEY)
    weather_data = openweather.get_weather_data(city.EDINBURGH)
