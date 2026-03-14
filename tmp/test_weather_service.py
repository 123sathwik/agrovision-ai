import os
from dotenv import load_dotenv

# Load environment variables FIRST before importing the service
load_dotenv()

from services.weather_service import get_weather

def test_weather():
    city = "London"
    print(f"Testing weather fetch for {city}...")
    try:
        data = get_weather(city)
        print("Weather Data Received:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_weather()
