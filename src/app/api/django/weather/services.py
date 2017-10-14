import asyncio
import os
from app.domain.weather.repository import WeatherRepository
from app.domain.weather.repository.external.openweather import OpenWeatherRepository

PARAMETERS = {
    'weather.weather_provider.open_weather.url': 'https://api.openweathermap.org/data/2.5',
    'weather.weather_provider.open_weather.api_key': os.environ['OPENWEATHER_API_KEY'],
}


# pylint: disable=invalid-name
_services_singleton_instances = {}


def _cache_service_singleton(func):
    def wrapped_function():
        if func not in _services_singleton_instances:
            _services_singleton_instances[func] = func()
        return _services_singleton_instances[func]

    return wrapped_function


@_cache_service_singleton
def weather_provider() -> WeatherRepository:
    api_url: str = PARAMETERS['weather.weather_provider.open_weather.url']
    api_key: str = PARAMETERS['weather.weather_provider.open_weather.api_key']

    return OpenWeatherRepository(api_url, api_key)


@_cache_service_singleton
def asyncio_loop():
    return asyncio.new_event_loop()
