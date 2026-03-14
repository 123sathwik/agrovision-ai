"""
Service to provide fertilizer recommendations and nutrient advice based on detected diseases.
Utilizes the local fertilizer_db.json for structured data.
"""
import json
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fertilizer_db.json")

def get_fertilizer_advice(disease_name):
    """
    Retrieves fertilizer and treatment advice for a specific disease.
    :param disease_name: The internal class name (e.g., 'Tomato___Early_blight').
    :return: Dictionary containing treatment details.
    """
    try:
        with open(DATABASE_PATH, 'r') as f:
            db = json.load(f)
        
        # Exact match
        if disease_name in db["diseases"]:
            return db["diseases"][disease_name]
        
        # Case-insensitive partial match fallback
        for key in db["diseases"]:
            if disease_name.lower().replace(" ", "_") == key.lower():
                return db["diseases"][key]
        
        # Default fallback
        print(f"[!] Warning: No specific data for '{disease_name}', using defaults.")
        return db["default"]
        
    except FileNotFoundError:
        print(f"[-] Error: Fertilizer database not found at {DATABASE_PATH}")
        return {
            "fertilizer": "Consult a local specialist",
            "npk_ratio": "Unknown",
            "organic": "Organic compost",
            "chemical": "Standard fungicide",
            "prevention": "General crop hygiene"
        }
    except Exception as e:
        print(f"[-] Fertilizer Engine Error: {e}")
        return None

if __name__ == "__main__":
    # Test cases
    print(get_fertilizer_advice("Tomato___Early_blight"))
    print(get_fertilizer_advice("Potato___Healthy"))
