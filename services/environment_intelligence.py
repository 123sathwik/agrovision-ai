"""
AgroVision AI: Environment Intelligence Service.
Analyzes weather conditions to calculate crop disease risks and provides explanation text for farmers.
"""

from services.weather_service import get_weather

def get_environment_analysis(city):
    """
    Analyzes weather data to assess disease risk based on a given city.
    """
    try:
        weather = get_weather(city)
        temp = weather["temperature"]
        humidity = weather["humidity"]

        if humidity > 85 and temp > 25:
            risk = "HIGH fungal disease risk"
        elif humidity > 70:
            risk = "MODERATE disease risk"
        else:
            risk = "LOW risk"

        return {
            "temperature": temp,
            "humidity": humidity,
            "risk": risk
        }
    except Exception as e:
        print(f"Error getting environment analysis: {e}")
        return {
            "temperature": 0,
            "humidity": 0,
            "risk": "Unknown"
        }

def environmental_intelligence(weather, disease):
    """
    Assesses specific fungal outbreaks based on the identified disease and current weather.
    """
    humidity = weather.get("humidity", 0)
    temp = weather.get("temperature", 0)

    if disease.lower().find("blight") != -1 and humidity > 80:
        risk = "Very high fungal outbreak risk"
    elif humidity > 75:
        risk = "Fungal disease conditions favorable"
    else:
        risk = "Stable crop environment"

    return risk

if __name__ == "__main__":
    # Test cases
    test_weather_high = {"temperature": 26, "humidity": 90}
    test_weather_mod = {"temperature": 20, "humidity": 75}
    test_weather_low = {"temperature": 18, "humidity": 50}

    print("HIGH Risk Test:", analyze_environment(test_weather_high))
    print("MOD Risk Test:", analyze_environment(test_weather_mod))
    print("LOW Risk Test:", analyze_environment(test_weather_low))
