from django.conf import urls

from . import views

# pylint: disable=invalid-name
urlpatterns = [
    urls.url(r'^all$', views.all_cities_current_weather, name='all_cities_current_weather'),
    urls.url(r'^(?P<city_name>\w+)$', views.city_current_weather, name='city_current_weather'),
]
