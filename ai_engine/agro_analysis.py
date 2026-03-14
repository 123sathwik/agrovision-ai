"""
AgroVision AI: Unified Agro Intelligence Orchestrator.
Combines AI disease prediction with expert agricultural advice and real-time weather risk analysis.
"""
import os
import sys

# Ensure project root is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_engine.analyze_crop import analyze_crop
from ai_engine.groq_analysis import get_agricultural_advice
from services.environment_intelligence import get_environment_analysis
from services.disease_severity import calculate_severity
from services.disease_spread_predictor import predict_spread
from services.farmer_advisor import generate_farmer_advice
from services.npk_recommender import recommend_npk

def get_full_agro_analysis(image_path, location="Unknown"):
    """
    Orchestrates the complete agricultural analysis workflow.
    
    :param image_path: Path to the crop image.
    :param location: Location for weather analysis (city name or "lat,lon").
    :return: Unified dictionary with all analysis results.
    """
    print(f"[*] Starting Unified Agro Analysis for: {image_path}")
    print("image received")
    
    # Defaults
    disease_label = "Unknown Disease"
    confidence = 0
    heatmap_path = None
    severity_data = {"severity": "Unknown", "infected_area": 0.0}
    env_data = {}
    spread_data = {}
    npk_data = {}
    groq_data = {}
    rotation_data = {}
    
    try:
        # 2. Run disease detection
        print("disease detection started")
        try:
            prediction = analyze_crop(image_path)
            if prediction and "error" not in prediction:
                disease_label = prediction.get("disease", "Unknown Disease")
                confidence = prediction.get("confidence", 0)
                heatmap_path = prediction.get("heatmap_path")
            else:
                print("[-] Prediction error or empty.")
        except Exception as e:
            print("[-] Model Prediction Failed:", e)
        
        print("Disease detected:", disease_label)
        
        # 3. Generate heatmap & severity
        try:
            severity_data = calculate_severity(heatmap_path) if heatmap_path else {"severity": "Unknown", "infected_area": 0.0}
        except Exception as e:
            print("[-] Severity calculation failed:", e)
        
        parts = disease_label.split(" ")
        crop_name = parts[0] if len(parts) > 0 else "Unknown"
        disease_name = " ".join(parts[1:]) if len(parts) > 1 else "Healthy"
        
        # 4. Fetch weather data & 5. Run environmental intelligence
        print("weather fetched")
        if location and location != "Unknown":
            try:
                env_data = get_environment_analysis(location)
                print("Weather data:", env_data)
                spread_data = predict_spread(env_data.get("temperature", 0), env_data.get("humidity", 0))
            except Exception as e:
                print(f"[-] Failed to fetch environmental intelligence: {e}")
                
        # 6. Generate NPK recommendation
        print("NPK generated")
        try:
            npk_data = recommend_npk(disease_label)
            print("NPK result:", npk_data)
        except Exception as e:
            print("[-] NPK generation failed:", e)
    
        # 7. Generate Groq treatment plan
        try:
            groq_data = get_agricultural_advice(crop_name, disease_name)
        except Exception as e:
            print("[-] Groq advice generation failed:", e)
            
        try:
            from services.crop_rotation import get_rotation_recommendation
            rotation_data = get_rotation_recommendation(disease_label)
        except Exception as e:
            print("[-] Crop rotation generation failed:", e)
            
        treatment_plan = (
            f"**Root Causes:** {groq_data.get('causes', 'N/A')}\n\n"
            f"**Soil Health:** {groq_data.get('soil_health', 'N/A')}\n\n"
            f"**NPK Schedule:** {groq_data.get('npk_schedule', 'N/A')}\n\n"
            f"**Disease Control:** {groq_data.get('disease_control', 'N/A')}\n\n"
            f"**Weather Monitoring:** {groq_data.get('weather_monitoring', 'N/A')}\n\n"
            f"**Irrigation Management:** {groq_data.get('irrigation', 'N/A')}\n\n"
            f"**Crop Rotation:** {groq_data.get('crop_rotation', 'N/A')}\n\n"
            f"**Farm Hygiene:** {groq_data.get('farm_hygiene', 'N/A')}\n\n"
            f"**Monitoring Schedule:** {groq_data.get('monitoring', 'N/A')}"
        )
        
        try:
            farmer_advice = generate_farmer_advice(disease_label, severity_data.get("severity", "Unknown"))
        except Exception as e:
            print("[-] Farmer advice generation failed:", e)
            farmer_advice = "Advice unavailable"
    
        unified_response = {
            "disease": disease_label,
            "confidence": confidence,
            "npk": npk_data,
            "temperature": env_data.get("temperature"),
            "humidity": env_data.get("humidity"),
            "risk_level": env_data.get("risk", "Unknown"),
            "severity": severity_data,
            "spread_prediction": spread_data,
            "farmer_advice": farmer_advice,
            "next_crop": f"{rotation_data.get('next_crop', 'Unknown')} ({rotation_data.get('cycle', 'Unknown')})",
            "treatment": treatment_plan,
            "heatmap_path": heatmap_path
        }
        
        print("[+] Unified Agro Analysis Complete.")
        return unified_response

    except Exception as e:
        print("Analysis error:", e)
        return {
            "error": "Analysis Failed",
            "details": str(e),
            "disease": "Error",
            "confidence": 0,
            "temperature": 0,
            "humidity": 0,
            "risk_level": "Unknown",
            "npk": {},
            "severity": {"severity": "Unknown", "infected_area": 0.0},
            "spread_prediction": {},
            "farmer_advice": "Analysis unavailable",
            "next_crop": "Unknown",
            "treatment": "Unavailable",
            "heatmap_path": None
        }

if __name__ == "__main__":
    # Test Entry Point
    if len(sys.argv) > 1:
        img = sys.argv[1]
        loc = sys.argv[2] if len(sys.argv) > 2 else "Unknown"
        print(get_full_agro_analysis(img, loc))
    else:
        print("Usage: python ai_engine/agro_analysis.py <image_path> [location]")
