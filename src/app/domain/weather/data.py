
from typing import NamedTuple
import enum

@enum.unique
class CityName(enum.Enum):
    EDINBURGH = 1
    LONDON = 2
    PARIS = 3
    FIRENZE = 4
    AMSTERDAM = 5


# @link https://docs.python.org/3/library/enum.html#using-automatic-values
class AutoName(enum.Enum):
    # pylint: disable=no-self-argument, unused-argument
    def _generate_next_value_(name, start, count, last_values):
        return name


@enum.unique
class WeatherType(AutoName):
    SUNNY = enum.auto()
    FEW_CLOUDS = enum.auto()
    SCATTERED_CLOUDS = enum.auto()
    BROKEN_CLOUDS = enum.auto()
    SHOWER_RAIN = enum.auto()
    RAIN = enum.auto()
    THUNDERSTORM = enum.auto()
    SNOW = enum.auto()
    MIST = enum.auto()


class WeatherData(NamedTuple):
    # pylint: disable=too-few-public-methods
    city_name: CityName
    weather_type: WeatherType
    wind_speed: float
    temperature: float
    humidity: int
