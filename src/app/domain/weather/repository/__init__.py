
import abc
import aiohttp
import app.domain.weather.data as weather_data


class WeatherRepository(abc.ABC):

    @abc.abstractmethod
    async def get_weather_data_async(self, client_session: aiohttp.ClientSession, city_name: weather_data.CityName) -> weather_data.WeatherData:
        pass

    @abc.abstractmethod
    def get_weather_data(self, city_name: weather_data.CityName) -> weather_data.WeatherData:
        pass
