
import os
from scute import Container
from app.domain.weather.repository.external.openweather import OpenWeatherRepository

container = Container()

container['weather.weather_provider.open_weather.url'] = 'https://api.openweathermap.org/data/2.5'
container['weather.weather_provider.open_weather.api_key'] = os.environ['OPENWEATHER_API_KEY']

@container.bind_callable(
    dependencies=('weather.weather_provider.open_weather.url','weather.weather_provider.open_weather.api_key'),
    injection_id='weather_provider'
)
def _weather_provider(api_url: str, api_key: str) -> OpenWeatherRepository:
    return OpenWeatherRepository(api_url, api_key)
