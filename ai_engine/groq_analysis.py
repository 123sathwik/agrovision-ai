import json
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_disease(crop, disease):
    """
    Detailed agricultural analysis using Groq LLM with 10-point template.
    """
    prompt = f"""
You are a senior agricultural scientist.

Provide a detailed crop disease action plan including:

1 Root cause analysis
2 Soil health
3 Exact NPK fertilizer schedule
4 Disease control methods (Organic & Chemical)
5 Weather monitoring
6 Irrigation adjustments
7 Crop rotation strategy
8 Farm hygiene recommendations
9 Monitoring schedule

Crop: {crop}
Disease: {disease}

CRITICAL: The output MUST be a minimum of 400 words in total length. Be extremely descriptive and thorough.

Return detailed structured response in JSON format ONLY with these exact keys:
{{
  "causes": "1 Root cause analysis",
  "soil_health": "2 Soil health",
  "npk_schedule": "3 Exact NPK fertilizer schedule",
  "disease_control": "4 Disease control methods",
  "weather_monitoring": "5 Weather monitoring",
  "irrigation": "6 Irrigation adjustments",
  "crop_rotation": "7 Crop rotation strategy",
  "farm_hygiene": "8 Farm hygiene recommendations",
  "monitoring": "9 Monitoring schedule"
}}
"""


    try:
        chat = client.chat.completions.create(
            messages=[{"role":"user","content":prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        response_text = chat.choices[0].message.content
        return json.loads(response_text)
    except Exception as e:
        print(f"[!] Error in Groq analysis: {e}")
        return {
            "causes": "N/A", "soil_health": "N/A", "npk_schedule": "N/A",
            "disease_control": "N/A", "weather_monitoring": "N/A",
            "irrigation": "N/A", "crop_rotation": "N/A",
            "farm_hygiene": "N/A", "monitoring": "N/A"
        }

def get_agricultural_advice(crop_name, disease_name):
    """Compatibility wrapper for agro_analysis.py"""
    return analyze_disease(crop_name, disease_name)

if __name__ == "__main__":
    # Internal test
    print("=== AgroVision AI: Groq Advice Engine Test (JSON) ===")
    res = get_agricultural_advice("Tomato", "Leaf Mold")
    print(json.dumps(res, indent=4))
