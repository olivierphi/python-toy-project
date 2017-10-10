
import app.domain.weather.data as weather_data

class InvalidCityNameError(Exception):

    def __init__(self, city_name: weather_data.CityName):
        super()
        self.city_name = city_name
