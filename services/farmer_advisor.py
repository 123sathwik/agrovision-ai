"""
AgroVision AI: Farmer Advisor
Generates specific, immediate action plans based on the estimated severity of a crop disease.
"""

def generate_farmer_advice(disease_name, severity):
    """
    Provide immediate situational farming advice.
    
    :param disease_name: The classified disease name.
    :param severity: The estimated severity level (Mild, Moderate, Severe).
    :return: A dictionary containing recommended actions, monitoring, and prevention steps.
    """
    advice = {}

    if severity == "Mild Infection":
        advice["action"] = "Apply organic neem oil spray every 5 days. Remove immediately visible infected leaves to prevent spread."
    elif severity == "Moderate Infection":
        advice["action"] = "Apply copper fungicide. Carefully prune and burn infected foliage. Do not compost infected material."
    else:  # Severe Infection
        advice["action"] = "Immediate chemical treatment required. Isolate infected plants if possible to save surrounding crops. Consider culling if infection is widespread."

    advice["monitoring"] = "Inspect plants every 48 hours for new spots or discoloration."
    advice["prevention"] = "Improve air circulation through pruning. Reduce ambient humidity around plants and avoid watering foliage from above."

    return advice

if __name__ == "__main__":
    # Internal Test
    print("=== AgroVision AI: Farmer Advisor Test ===")
    res = generate_farmer_advice("Tomato Early Blight", "Moderate Infection")
    print(res)
