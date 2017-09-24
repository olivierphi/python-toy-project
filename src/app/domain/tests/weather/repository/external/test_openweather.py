# pylint: disable=invalid-name

import os
import pytest
from app.domain.weather import city
from app.domain.weather.errors import InvalidCityNameError
from app.domain.weather.repository.external.openweather import OpenWeatherRepository
from app.domain.weather.repository.external.errors import ExternalWeatherDataProviderNotInitialisedError, \
    ExternalWeatherDataProviderBadAPIKey

VALID_API_KEY: str = os.getenv('TEST_OPENWEATHER_API_KEY', '')
INVALID_API_KEY: str = '123456'

def test_module_raise_error_if_used_without_prior_initialisation():
    openweather_repo = OpenWeatherRepository(None, None)
    with pytest.raises(ExternalWeatherDataProviderNotInitialisedError):
        openweather_repo.get_weather_data(city.EDINBURGH)


def test_module_raise_error_if_used_with_an_unavailable_city_name():
    openweather_repo = OpenWeatherRepository('https://holygrail.com', '123')
    with pytest.raises(InvalidCityNameError):
        openweather_repo.get_weather_data('Camelot')


def test_module_raise_error_with_invalid_api_key():
    openweather_repo = OpenWeatherRepository('https://api.openweathermap.org/data/2.5', INVALID_API_KEY)
    with pytest.raises(ExternalWeatherDataProviderBadAPIKey):
        openweather_repo.get_weather_data(city.EDINBURGH)


def test_module_can_retrieve_city_weather_data():
    if not VALID_API_KEY:
        raise EnvironmentError('Missing "TEST_OPENWEATHER_API_KEY" environment variable')
    openweather_repo = OpenWeatherRepository('https://api.openweathermap.org/data/2.5', VALID_API_KEY)
    weather_data = openweather_repo.get_weather_data(city.EDINBURGH)
