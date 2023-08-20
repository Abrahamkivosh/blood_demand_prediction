import requests
import os
import requests
from dotenv import load_dotenv
from django.core.cache import cache


# Load environment variables from .env file
load_dotenv()
# Access the API key from the environment
OPENWEATHER_API_KEY = os.getenv("OPENWEATHERAPI")


def get_location(city_name):
    # Check if the data is already cached
    cache_key = f"weather_forecast_{city_name}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city_name,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Request temperature in Celsius
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_list = data["list"]
        forecast_data = []

        for forecast in forecast_list:
            forecast_data.append({
                "date": forecast["dt_txt"],
                "name": data["city"]["name"],
                "latitude": data["city"]["coord"]["lat"],
                "longitude": data["city"]["coord"]["lon"],
                # "temperature": forecast["main"]["temp"],
                # "humidity": forecast["main"]["humidity"],
                "population": data["city"].get("population")
            })

        # Cache the data for one day (86400 seconds)
        cache.set(cache_key, forecast_data, timeout=86400)

        # get first object in the array forecast_data
        forecast_dt =  forecast_data[0]

        return forecast_dt
    else:
        print("Failed to fetch weather forecast. Status code:", response.status_code)
        return None
