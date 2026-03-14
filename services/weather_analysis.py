"""
AgroVision AI: Weather Analysis Service.
Interprets meteorological data to assess disease and pest risks for crops.
"""
from services.weather_service import get_weather_data

def analyze_weather_risk(temp, humidity, rain_probability):
    """
    Applies refined threshold heuristics for agricultural risks.
    """
    # 1. Fungal Risk (Humidity based)
    if humidity > 85:
        fungal_risk = "HIGH"
        fungal_advice = "High fungal risk due to extreme humidity (>85%). Apply preventive measures."
    elif 65 <= humidity <= 85:
        fungal_risk = "MEDIUM"
        fungal_advice = "Moderate fungal risk. Monitor leaf surfaces closely."
    else:
        fungal_risk = "LOW"
        fungal_advice = "Stable conditions. Fungal risk is low."

    # 2. Pest Risk (Temperature based)
    pest_risk = "NORMAL"
    pest_advice = ""
    if temp > 32:
        pest_risk = "HIGH"
        pest_advice = " Increased pest activity risk due to high temperatures (>32°C)."

    # 3. Consolidate Risk and Advice
    risk_level = fungal_risk
    if pest_risk == "HIGH" and risk_level != "HIGH":
        risk_level = "ELEVATED (Pests)"
    
    recommendation = fungal_advice + pest_advice
    if rain_probability > 0.5:
        recommendation += " High rain probability; ensure proper drainage."

    return {
        "weather_risk": risk_level,
        "advice": recommendation
    }

def get_weather_analysis(location):
    """
    Fetches data and runs the upgraded risk analysis.
    """
    weather_data = get_weather_data(location)
    
    if not weather_data:
        return {
            "weather_risk": "Unknown",
            "advice": "Unable to fetch local weather data."
        }

    analysis = analyze_weather_risk(
        weather_data["temperature"],
        weather_data["humidity"],
        weather_data["rain_probability"]
    )

    return {
        **weather_data,
        **analysis
    }

if __name__ == "__main__":
    # Local test
    print("=== AgroVision AI: Weather Analysis Engine Test ===")
    test_location = "London"
    report = get_weather_analysis(test_location)
    print(f"Analysis for {test_location}: {report}")
