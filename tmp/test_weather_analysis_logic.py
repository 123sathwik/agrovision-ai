"""
Verification script for services/weather_analysis.py.
Tests the rule-based risk analysis logic with various meteorological scenarios.
"""
from services.weather_analysis import analyze_weather_risk

def test_weather_analysis_logic():
    print("=== Verifying Weather Risk Analysis Logic ===\n")
    
    # scenario 1: High Fungal Risk (High humidity + Rain)
    print("[*] Testing High Fungal Risk scenario...")
    res1 = analyze_weather_risk(temp=22, humidity=85, rain_probability=0.8)
    assert res1["disease_risk"] == "High"
    assert "fungicide" in res1["recommendation"].lower()
    print("[+] High Fungal Risk: OK")

    # scenario 2: High Temperature (Pest Risk)
    print("[*] Testing Pest Risk scenario...")
    res2 = analyze_weather_risk(temp=32, humidity=40, rain_probability=0.0)
    assert res2["disease_risk"] == "Moderate"
    assert "pest" in res2["recommendation"].lower()
    print("[+] Pest Risk: OK")

    # scenario 3: Stable conditions
    print("[*] Testing Stable Conditions scenario...")
    res3 = analyze_weather_risk(temp=20, humidity=50, rain_probability=0.1)
    assert res3["disease_risk"] == "Low"
    assert "stable" in res3["recommendation"].lower()
    print("[+] Stable Conditions: OK")

    # scenario 4: Moderate moisture risk
    print("[*] Testing Moderate Moisture scenario...")
    res4 = analyze_weather_risk(temp=22, humidity=75, rain_probability=0.1)
    assert res4["disease_risk"] == "Moderate"
    print("[+] Moderate Moisture: OK")

    print("\n[SUCCESS] Weather risk analysis logic verified!")

if __name__ == "__main__":
    try:
        test_weather_analysis_logic()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        exit(1)
