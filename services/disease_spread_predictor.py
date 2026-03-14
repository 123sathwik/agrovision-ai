"""
AgroVision AI: Disease Spread Predictor
Estimates the likelihood of disease transmission based on environmental factors.
"""

def predict_spread(temp, humidity):
    """
    Predicts disease spread risk using weather conditions.
    
    :param temp: Temperature in Celsius
    :param humidity: Relative humidity percentage
    :return: Dictionary containing the spread risk level and a farmer explanation.
    """
    if humidity > 85 and temp > 25:
        risk = "HIGH spread risk within 3–5 days"
        explanation = "Hot and highly humid conditions are optimal for rapid fungal and bacterial sporulation. Immediate preventative spraying and reduced watering are strongly advised."
    elif humidity > 70:
        risk = "MODERATE spread risk"
        explanation = "Elevated humidity favors gradual disease spread. Monitor crops closely, ensure good airflow, and apply organic preventatives if symptoms appear."
    else:
        risk = "LOW spread probability"
        explanation = "Current dry conditions are unfavorable for most disease pathogens. Maintain standard care and avoid over-irrigating foliage."

    return {
        "spread_risk": risk,
        "explanation": explanation
    }

if __name__ == "__main__":
    # Internal Test
    test_cases = [
        (28, 90),
        (22, 75),
        (30, 40)
    ]
    print("=== AgroVision AI: Disease Spread Predictor Test ===")
    for t, h in test_cases:
        print(f"Temp: {t}°C, Hum: {h}% -> {predict_spread(t, h)}")
