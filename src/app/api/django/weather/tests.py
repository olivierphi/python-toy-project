import json
from django.test import TestCase

# pylint: disable-all

class SimpleTest(TestCase):

    def test_current_weather_single_city(self):
        response = self.client.get('/weather/current/Edinburgh')
        self.assertEqual(response.status_code, 200)
        response_content: dict = json.loads(response.content)
        self.assertTrue('city' in response_content)
        self.assertTrue('weather' in response_content)
        self.assertTrue('temp' in response_content)
        self.assertTrue('wind' in response_content)
        self.assertTrue('humidity' in response_content)
        self.assertEqual(response_content['city'], 'EDINBURGH')

    def test_current_weather_all_cities(self):
        from app.domain.weather.data import CityName

        response = self.client.get('/weather/current/all')
        self.assertEqual(response.status_code, 200)
        response_content: dict = json.loads(response.content)
        self.assertEqual(len(response_content), len(CityName))
        for city_data in response_content:
            self.assertTrue('city' in city_data)
            self.assertTrue('weather' in city_data)
            self.assertTrue('temp' in city_data)
            self.assertTrue('wind' in city_data)
            self.assertTrue('humidity' in city_data)
            self.assertTrue(city_data['city'] in CityName.__dict__.keys())
