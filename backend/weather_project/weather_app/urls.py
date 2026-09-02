# weather_app/urls.py

from django.urls import path
from .views import register, current_weather, forecast_weather

urlpatterns = [
    path('accounts/register/', register, name='register'),
    path('weather/current/', current_weather, name='current_weather'),
    path('weather/forecast/', forecast_weather, name='forecast_weather'),
]