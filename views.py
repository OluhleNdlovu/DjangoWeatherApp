
from django.shortcuts import render
import requests # type: ignore
import os
from django.conf import settings

from settings import API_KEY

#from django.conf import settings
from .utils import cache_weather_data, is_cache_valid, read_cache_data

def get_lat_lon(city_name):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={settings.API_KEY}"
    response = requests.get(geo_url).json()
    if response:
        lat = response[0]['lat']
        lon = response[0]['lon']
        return lat, lon
    return None


def get_weather(request):
    if request.method == 'POST':
        city_name = request.POST.get('city_name')
        lat,lon = get_lat_lon(city_name)

        if lat and lon:
            filename = f"{city_name}-{lat}-{lon}.txt"
            #lat, lon = lat_lon
            # Fetch weather data using the lat and lon
            # Check cache validity and fetch new data if necessary
            # Render the result to the template
            if os.path.exists(filename) and is_cache_valid(filename):
                data = read_cache_data(filename)

            else:
                weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
                response = requests.get(weather_url).json()
                data = response
                cache_weather_data(city_name, lat, lon, str(data))  # Cache the data
                # Handle case where the city name is invalid
            # context = {'error': 'City not found'}
            context = {
                'city_name': city_name,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                # Add more data to the context as needed
            }
            return render(request, 'weather_app/userform.html', context)
    return render(request, 'weather_app/userform.html')

