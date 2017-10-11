
import re
import requests
import aiohttp
import app.domain.weather.data as weather_data
import app.domain.weather.errors as weather_errors
import app.domain.weather.repository.external.errors as repository_errors

_CITIES_IDS = {
    weather_data.CityName.EDINBURGH: 3333229,
    weather_data.CityName.LONDON: 2643743,
    weather_data.CityName.PARIS: 6455259,
    weather_data.CityName.FIRENZE: 6542285,
    weather_data.CityName.AMSTERDAM: 2759794,
}

_ICONS_WEATHER_TYPE_MAPPING = {
    '01': weather_data.WeatherType.SUNNY,
    '02': weather_data.WeatherType.FEW_CLOUDS,
    '03': weather_data.WeatherType.SCATTERED_CLOUDS,
    '04': weather_data.WeatherType.BROKEN_CLOUDS,
    '09': weather_data.WeatherType.SHOWER_RAIN,
    '10': weather_data.WeatherType.RAIN,
    '11': weather_data.WeatherType.THUNDERSTORM,
    '13': weather_data.WeatherType.SNOW,
    '50': weather_data.WeatherType.MIST,
}


class OpenWeatherRepository:

    def __init__(self, api_url: str, api_key: str):
        self._api_url = api_url
        self._api_key = api_key

    async def get_weather_data_async(self, client_session: aiohttp.ClientSession, city_name: weather_data.CityName) -> weather_data.WeatherData:

        endpoint_url, endpoint_params = self._init_weather_data_request(city_name).values()

        async with client_session.get(endpoint_url, params=endpoint_params) as api_response:
            response_text = await api_response.text()

            if api_response.status == 401 and 'Invalid API key' in response_text:
                raise repository_errors.ExternalWeatherDataProviderBadAPIKey(self._api_key)

            raw_result = await api_response.json()

            return self._convert_json_response_to_weather_data(city_name, raw_result)

    def get_weather_data(self, city_name: weather_data.CityName) -> weather_data.WeatherData:

        endpoint_url, endpoint_params = self._init_weather_data_request(city_name).values()

        api_response = requests.get(endpoint_url, params=endpoint_params)

        if api_response.status_code == 401 and 'Invalid API key' in api_response.text:
            raise repository_errors.ExternalWeatherDataProviderBadAPIKey(self._api_key)

        raw_result = api_response.json()

        return self._convert_json_response_to_weather_data(city_name, raw_result)

    def _init_weather_data_request(self, city_name: weather_data.CityName) -> dict:
        # Let's start with some input checking...
        if not self._api_url:
            raise repository_errors.ExternalWeatherDataProviderNotInitialisedError()
        if not isinstance(city_name, weather_data.CityName):
            raise weather_errors.InvalidCityNameError(city_name)
        if city_name not in weather_data.CityName:
            raise weather_errors.InvalidCityNameError(city_name)

        # Go!
        endpoint_url = '{}/weather'.format(self._api_url)
        endpoint_params = {
            'id': _CITIES_IDS[city_name],
            'APPID': self._api_key,
            'units': 'metric',
        }

        return {
            'url': endpoint_url,
            'params': endpoint_params,
        }

    def _convert_json_response_to_weather_data(self, city_name: weather_data.CityName, json_data: dict) -> weather_data.WeatherData:
        icon_data = json_data['weather'][0]['icon']
        icon_data_num = re.sub(r'^(\d+)(d|n)$', r'\1', icon_data)
        return weather_data.WeatherData(
            city_name=city_name,
            weather_type=_ICONS_WEATHER_TYPE_MAPPING[icon_data_num],
            wind_speed=float(json_data['wind']['speed']),
            temperature=float(json_data['main']['temp']),
            humidity=int(json_data['main']['humidity']),
        )
