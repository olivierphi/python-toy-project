# pylint: disable=invalid-name

import asyncio
import os
import aiohttp
import pytest
import app.domain.weather.data as weather_data
import app.domain.weather.errors as weather_errors
from app.domain.weather.repository.external.openweather import OpenWeatherRepository
import app.domain.weather.repository.external.errors as repository_errors

VALID_API_KEY: str = os.getenv('TEST_OPENWEATHER_API_KEY', '')
INVALID_API_KEY: str = '123456'

def test_module_raise_error_if_used_without_prior_initialisation():
    sut = OpenWeatherRepository(None, None)
    with pytest.raises(repository_errors.ExternalWeatherDataProviderNotInitialisedError):
        sut.get_weather_data(weather_data.CityName.EDINBURGH)


def test_module_raise_error_if_used_with_an_unavailable_city_name():
    sut = OpenWeatherRepository('https://holygrail.com', '123')
    with pytest.raises(weather_errors.InvalidCityNameError):
        sut.get_weather_data('Camelot')


def test_module_raise_error_with_invalid_api_key():
    sut = OpenWeatherRepository('https://api.openweathermap.org/data/2.5', INVALID_API_KEY)
    with pytest.raises(repository_errors.ExternalWeatherDataProviderBadAPIKey):
        sut.get_weather_data(weather_data.CityName.EDINBURGH)


def test_module_can_retrieve_city_weather_data():
    if not VALID_API_KEY:
        raise EnvironmentError('Missing "TEST_OPENWEATHER_API_KEY" environment variable')
    sut = OpenWeatherRepository('https://api.openweathermap.org/data/2.5', VALID_API_KEY)
    result = sut.get_weather_data(weather_data.CityName.EDINBURGH)

    assert result.city_name in weather_data.CityName
    assert result.weather_type in weather_data.WeatherType
    assert result.humidity >= 0
    assert -60 < result.temperature < 60
    assert result.wind_speed >= 0


def test_module_can_retrieve_city_weather_data_asynchronously():
    if not VALID_API_KEY:
        raise EnvironmentError('Missing "TEST_OPENWEATHER_API_KEY" environment variable')
    sut = OpenWeatherRepository('https://api.openweathermap.org/data/2.5', VALID_API_KEY)

    city_names = (weather_data.CityName.EDINBURGH, weather_data.CityName.PARIS)
    results = []
    async def fetch_in_parallel(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            for city_name in city_names:
                result = await sut.get_weather_data_async(session, city_name)
                results.append(result)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(fetch_in_parallel(loop))

    assert len(results) == len(city_names)
    assert results[0].city_name == weather_data.CityName.EDINBURGH
    assert results[1].city_name == weather_data.CityName.PARIS
