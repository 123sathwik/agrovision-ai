"""
AgroVision AI: Soil Analysis Service.
Provides rule-based soil nutrient estimations and conditioning advice.
Used to suggest specific recovery strategies for infected crops.
"""

def get_soil_analysis(crop_name, disease_name):
    """
    Estimates soil nutrient requirements based on the detected crop and disease.
    
    :param crop_name: Name of the crop (e.g., Tomato).
    :param disease_name: Name of the detected disease (e.g., Early Blight).
    :return: Dictionary containing soil analysis data.
    """
    # Normalize logger: lowercase, strip, and replace underscores with spaces
    crop = crop_name.lower().strip().replace("_", " ")
    disease = disease_name.lower().strip().replace("_", " ")
    
    # Rule-Based Knowledge Base
    # Format: {(crop, disease_keyword): {NPK_ratio, fertilizers, soil_condition}}
    knowledge_base = {
        # Tomato Rules
        ("tomato", "late blight"): {
            "NPK_ratio": "10-26-26",
            "fertilizers": ["DAP", "Sulfate of Potash"],
            "soil_condition": "High phosphorus required for recovery; possible nitrogen leaching."
        },
        ("tomato", "early blight"): {
            "NPK_ratio": "5-10-10",
            "fertilizers": ["Bone Meal", "Kelp Meal"],
            "soil_condition": "Potassium deficiency; soil may be compacted."
        },
        ("tomato", "healthy"): {
            "NPK_ratio": "10-10-10",
            "fertilizers": ["Balanced Garden Fertilizer", "Organic Compost"],
            "soil_condition": "Soil nutrients appear balanced. Maintain organic matter."
        },
        
        # Potato Rules
        ("potato", "late blight"): {
            "NPK_ratio": "5-10-10",
            "fertilizers": ["Rock Phosphate", "Muriate of Potash"],
            "soil_condition": "Excessive moisture; potential calcium deficiency in tubers."
        },
        ("potato", "early blight"): {
            "NPK_ratio": "10-15-15",
            "fertilizers": ["Blood Meal", "Fish Emulsion"],
            "soil_condition": "Nitrogen and Phosphorus levels need enrichment."
        },
        ("potato", "healthy"): {
            "NPK_ratio": "15-15-15",
            "fertilizers": ["Balanced slow-release fertilizer"],
            "soil_condition": "Optimal for tuber development. Keep soil slightly acidic."
        },

        # Corn Rules
        ("corn", "common rust"): {
            "NPK_ratio": "20-10-10",
            "fertilizers": ["Urea", "Ammonium Sulfate"],
            "soil_condition": "Nitrogen deficiency often exacerbates rust symptoms."
        },
        
        # Grape Rules
        ("grape", "black rot"): {
            "NPK_ratio": "10-20-20",
            "fertilizers": ["Potassium Sulfate", "Phosphate Rock"],
            "soil_condition": "Potassium-heavy feeding required; improve soil drainage."
        }
    }

    # 1. Exact Match Search
    # Try searching for specific disease name in the crop context
    for (k_crop, k_disease), advice in knowledge_base.items():
        if k_crop == crop and k_disease in disease:
            return advice

    # 2. Generic Fallback (by disease type)
    if "late blight" in disease:
        return {
            "NPK_ratio": "5-15-15",
            "fertilizers": ["Super Phosphate", "Potash"],
            "soil_condition": "Blight recovery requires high Phosphorus and Potassium."
        }
    if "bacterial spot" in disease:
        return {
            "NPK_ratio": "10-10-10",
            "fertilizers": ["Micro-nutrient enriched NPK"],
            "soil_condition": "Ensure soil pH is between 6.0 and 6.5; copper-supplemented fertilization."
        }
    if "healthy" in disease:
        return {
            "NPK_ratio": "10-10-10",
            "fertilizers": ["Organic Compost", "General Purpose NPK"],
            "soil_condition": "Nutrient levels seem adequate. Focus on maintenance."
        }

    # 3. Default Fallback
    return {
        "NPK_ratio": "10-10-10",
        "fertilizers": ["General Purpose Fertilizer"],
        "soil_condition": "Standard nutrient maintenance recommended. Consult local soil test for specifics."
    }

if __name__ == "__main__":
    # Internal Dry Run
    print("Testing Soil Analysis Service...")
    print(f"Tomato Late Blight: {get_soil_analysis('Tomato', 'Late Blight')}")
    print(f"Random Disease: {get_soil_analysis('Apple', 'Scab')}")
