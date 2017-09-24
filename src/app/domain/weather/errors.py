
class InvalidCityNameError(Exception):

    def __init__(self, city_name: str):
        super()
        self.city_name = city_name
