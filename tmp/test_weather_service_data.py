"""
Verification script for services/weather_service.py.
Mocks the OpenWeather API to verify data parsing and output structure.
"""
import json
from unittest.mock import patch, MagicMock
from services.weather_service import get_weather_data

def test_weather_service_data():
    print("=== Verifying Weather Data Service ===\n")
    
    # 1. Mock Successful API Response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "main": {"temp": 28.5, "humidity": 75},
        "wind": {"speed": 5.4},
        "clouds": {"all": 80},
        "rain": {"1h": 2.5} # Explicit rain
    }
    
    with patch('services.weather_service.requests.get', return_value=mock_response):
        with patch('services.weather_service.OPENWEATHER_API_KEY', 'fake_key'):
            print("[*] Testing successful weather data fetch...")
            result = get_weather_data("London")
            
            assert result["temperature"] == 28.5
            assert result["humidity"] == 75
            assert result["wind_speed"] == 5.4
            assert result["rain_probability"] == 1.0 # Due to rain presence
            print("[+] Data Parsing: OK")

    # 2. Mock Cloudy (No Rain) Response
    mock_response.json.return_value = {
        "main": {"temp": 20.0, "humidity": 50},
        "wind": {"speed": 2.0},
        "clouds": {"all": 40},
        # No rain key
    }
    
    with patch('services.weather_service.requests.get', return_value=mock_response):
        with patch('services.weather_service.OPENWEATHER_API_KEY', 'fake_key'):
            print("[*] Testing cloud-based rain probability heuristic...")
            result = get_weather_data("London")
            assert result["rain_probability"] == 0.2 # 40% clouds * 0.5
            print("[+] Probability Heuristic: OK")

    print("\n[SUCCESS] Weather data service logic verified!")

if __name__ == "__main__":
    try:
        test_weather_service_data()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
