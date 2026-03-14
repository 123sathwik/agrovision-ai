"""
Service to provide crop rotation and suitability recommendations based on the current crop and its health status.
"""

# Simple Crop Rotation Rules
# Key: Current Crop, Value: List of ideal next crops
ROTATION_RULES = {
    "Tomato": ["Beans", "Peas", "Cucumbers", "Garlic"],
    "Potato": ["Corn", "Beans", "Peas", "Cabbage"],
    "Pepper": ["Onions", "Carrots", "Beets", "Cabbage"],
    "Corn": ["Beans", "Soybeans", "Clover", "Alfalfa"],
    "Apple": ["Cover crops like Clover", "Grasses"],
    "Grape": ["Cover crops", "Mustard (for soil bio-fumigation)"]
}

def suggest_next_crop(crop_name, current_disease="Healthy"):
    """
    Suggests the best next crop for rotation based on the current situation.
    :param crop_name: Name of the current crop.
    :param current_disease: Name of the detected disease.
    :return: String recommendation.
    """
    base_crop = crop_name.split()[0] if crop_name else "Unknown"
    
    # If the crop is heavily diseased (Blight or Rot), prioritize break crops
    if "Blight" in current_disease or "Rot" in current_disease:
        return f"Due to {current_disease}, a minimum 3-year break from Solanaceous crops (Tomato, Potato, Pepper) is recommended. Plant Nitrogen-fixers like Beans or Peas to restore soil health."
    
    # Standard rotation
    if base_crop in ROTATION_RULES:
        suggestions = ROTATION_RULES[base_crop]
        return f"Ideal next crops for rotation: {', '.join(suggestions)}. These will help balance soil nutrients and break disease cycles."
    
    return "Plant legumes (Beans/Peas) or cover crops (Clover) to enrich the soil before the next main season."

if __name__ == "__main__":
    print(suggest_next_crop("Tomato", "Tomato___Early_blight"))
    print(suggest_next_crop("Potato", "Healthy"))
