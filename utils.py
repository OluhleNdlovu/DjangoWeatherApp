import os
import time

def cache_weather_data(city_name, lat, lon, data):
    filename = f"{city_name}-{lat}-{lon}.txt"
    with open(filename, 'w') as file:
        file.write(f"{int(time.time())}\n")  # Save current timestamp
        file.write(data)

def is_cache_valid(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            timestamp = int(file.readline().strip())
            if time.time() - timestamp < 180 * 60:  # 180 minutes in seconds
                return True
    return False

def read_cache_data(filename):
    with open(filename, 'r') as file:
        file.readline()  # Skip the timestamp line
        data = file.read()
    return data
