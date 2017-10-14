import aiohttp
from django import http
from app.domain.weather.data import CityName, WeatherData
from app.api.django.weather import services as weather_services

# pylint: disable=unused-argument


def city_current_weather(request, city_name: str):
    city_name = city_name.upper()
    if city_name not in CityName.__dict__:
        raise http.Http404("No weather data for this city")

    weather_provider = weather_services.weather_provider()
    weather_data = weather_provider.get_weather_data(CityName[city_name])

    return http.JsonResponse(_get_city_weather_json(weather_data))


def all_cities_current_weather(request):
    loop = weather_services.asyncio_loop()
    weather_provider = weather_services.weather_provider()

    all_data = []

    async def fetch_in_parallel(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            for city_name in CityName:
                result = await weather_provider.get_weather_data_async(session, city_name)
                all_data.append(_get_city_weather_json(result))

    loop.run_until_complete(fetch_in_parallel(loop))

    return http.JsonResponse(all_data, safe=False)


def _get_city_weather_json(weather_data: WeatherData) -> dict:
    return {
        'city': weather_data.city_name.name,
        'weather': weather_data.weather_type.name,
        'temp': weather_data.temperature,
        'wind': weather_data.wind_speed,
        'humidity': weather_data.humidity
    }
