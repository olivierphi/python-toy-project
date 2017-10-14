
import flask
import aiohttp
from .container import container
from app.domain.weather.data import CityName

# pylint: disable=invalid-name
current_weather = flask.Blueprint('current weather', __name__)

@current_weather.route('/<string:city_name>', methods=['GET'])
def get_city_weather(city_name: str):
    city_name = city_name.upper()
    if city_name not in CityName.__dict__:
        flask.abort(404, 'No weather data for this city')

    weather_provider = container['weather_provider']
    weather_data = weather_provider.get_weather_data(CityName[city_name])
    return flask.jsonify(_get_city_weather_json(weather_data))


@current_weather.route('/all', methods=['GET'])
def get_all_cities_weather():
    loop = container['loop']
    weather_provider = container['weather_provider']

    all_data = []

    async def fetch_in_parallel(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            for city_name in CityName:
                result = await weather_provider.get_weather_data_async(session, city_name)
                all_data.append(_get_city_weather_json(result))

    loop.run_until_complete(fetch_in_parallel(loop))

    return flask.jsonify(all_data)


def _get_city_weather_json(weather_data) -> dict:
    return {
        'city': weather_data.city_name.name,
        'weather': weather_data.weather_type.name,
        'temp': weather_data.temperature,
        'wind': weather_data.wind_speed,
        'humidity': weather_data.humidity
    }
