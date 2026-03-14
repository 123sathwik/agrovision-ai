"""
AgroVision AI: Soil NPK Recommendation Engine.
Infers likely nutrient deficiencies based on visual crop symptoms associated with diseases or poor health.
"""

def analyze_soil_npk(disease_name):
    """
    Suggests NPK ratios and fertilizer types based on inferred deficiencies from symptoms.
    
    :param disease_name: The classified disease or crop condition.
    :return: A dictionary containing the suggested NPK ratio and fertilizer recommendation.
    """
    
    disease = disease_name.lower()
    
    # 1. Nitrogen (N) Deficiency -> Leaf yellowing (chlorosis), older leaves affected first
    if "yellow" in disease or "chlorosis" in disease or "blight" in disease:
        return {
            "npk_ratio": "12-6-6",
            "fertilizer": "Urea + compost mixture (High Nitrogen focus)"
        }
        
    # 2. Potassium (K) Deficiency -> Brown spots, leaf edge curling, poor drought resistance
    elif "spot" in disease or "brown" in disease or "curl" in disease or "rust" in disease:
        return {
            "npk_ratio": "5-10-15",
            "fertilizer": "Potash + wood ash (High Potassium focus)"
        }
        
    # 3. Phosphorus (P) Deficiency -> Stunted growth, dark green/purple older leaves, poor root growth
    elif "stunt" in disease or "dwarf" in disease or "purple" in disease or "mold" in disease:
        return {
            "npk_ratio": "5-15-5",
            "fertilizer": "Bone meal + superphosphate (High Phosphorus focus)"
        }
        
    # Balanced Default for common maintenance or unrecognized specific symptoms
    else:
        return {
            "npk_ratio": "10-10-10",
            "fertilizer": "Balanced NPK granular + organic matter"
        }

if __name__ == "__main__":
    # Internal Test
    test_cases = [
        "Tomato Yellow Leaf Curl Virus",
        "Pepper Bacterial spot",
        "Leaf Mold",
        "Healthy"
    ]
    print("=== AgroVision AI: Soil NPK Engine Test ===")
    for tc in test_cases:
        print(f"[{tc}]: {analyze_soil_npk(tc)}")

