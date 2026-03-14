"""
AgroVision AI: Crop Rotation Service.
Recommends the best successor crop to break disease cycles and restore soil health.
"""

# Mapping of crops to their botanical families
PLANT_FAMILIES = {
    "tomato": "Solanaceae",
    "potato": "Solanaceae",
    "pepper": "Solanaceae",
    "eggplant": "Solanaceae",
    "beans": "Fabaceae",
    "peas": "Fabaceae",
    "lentils": "Fabaceae",
    "soybeans": "Fabaceae",
    "corn": "Poaceae",
    "wheat": "Poaceae",
    "rice": "Poaceae",
    "barley": "Poaceae",
    "apple": "Rosaceae",
    "strawberry": "Rosaceae",
    "grape": "Vitaceae",
    "squash": "Cucurbitaceae",
    "cucumber": "Cucurbitaceae",
    "watermelon": "Cucurbitaceae"
}

# Successor recommendations based on family or disease type
FAMILY_SUCCESSORS = {
    "Solanaceae": ("Beans", "Breaks fungal cycle and restores nitrogen in Solanaceae plots."),
    "Fabaceae": ("Corn", "Utilizes fixed nitrogen and breaks legume-specific pathogen cycles."),
    "Poaceae": ("Peas", "Restores nitrogen levels after heavy-feeding cereals."),
    "Rosaceae": ("Cover Crops (Clover)", "Improves soil structure and organic matter for fruit trees."),
    "Vitaceae": ("Leguminous cover crops", "Restores soil vitality in vineyard alleys."),
    "Cucurbitaceae": ("Wheat", "Breaks cycles of soil-borne squash diseases.")
}

def get_rotation_recommendation(disease_name):
    """
    Standardized crop rotation service with disease-specific rules.
    """
    disease_norm = disease_name.lower().strip()
    
    # 1. Specialized Disease-Specific Rules
    if "tomato early blight" in disease_norm:
        next_crop = "Maize or Beans"
        cycle = "2–3 season rotation"
    elif "potato late blight" in disease_norm:
        next_crop = "Legumes"
        cycle = "2–3 season rotation"
    elif "leaf spot" in disease_norm:
        next_crop = "Cereals"
        cycle = "2–3 season rotation"
    
    # 2. General Crop-Level Fallbacks
    elif "tomato" in disease_norm:
        next_crop = "Maize, Beans, or Peas"
        cycle = "2–3 season rotation"
    elif "rice" in disease_norm:
        next_crop = "Legumes or Oilseeds"
        cycle = "2–3 season rotation"
    elif "potato" in disease_norm:
        next_crop = "Cereals or Grasses"
        cycle = "2–3 season rotation"
    elif "pepper" in disease_norm:
        next_crop = "Crucifers or Legumes"
        cycle = "2–3 season rotation"
    else:
        next_crop = "Broad-leaf cereals or legumes"
        cycle = "2–3 season rotation"

    return {
        "next_crop": next_crop,
        "cycle": cycle
    }

if __name__ == "__main__":
    # Internal Dry Run
    print("Testing Refined Crop Rotation Service...")
    print(f"Tomato Early blight: {get_rotation_recommendation('Tomato Early blight')}")
    print(f"Potato Late blight: {get_rotation_recommendation('Potato Late blight')}")
    print(f"Leaf Spot: {get_rotation_recommendation('Tomato Septoria leaf spot')}")
    print(f"Rice healthy: {get_rotation_recommendation('Rice healthy')}")
