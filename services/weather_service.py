import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    """
    Fetches real-time weather data for a given city via OpenWeather API, with fallback.
    """
    if "lat=" in city and "lon=" in city:
        # Assuming format "lat=XX&lon=YY" from geolocation
        url = f"https://api.openweathermap.org/data/2.5/weather?{city}&appid={API_KEY}&units=metric"
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
    try:
        r = requests.get(url)
        r.raise_for_status() # Ensure HTTP errors trigger the fallback
        data = r.json()

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"]
        }

    except Exception as e:
        print(f"[!] Weather API Error: {e}. Using fallback data.")
        return {
            "temperature": 28,
            "humidity": 70,
            "condition": "Unknown"
        }
