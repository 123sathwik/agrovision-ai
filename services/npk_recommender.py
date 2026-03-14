"""
AgroVision AI: NPK Recommender Service
Provides specific NPK (Nitrogen, Phosphorus, Potassium) ratios and fertilizer types 
based on the identified crop disease.
"""

def recommend_npk(disease):
    """
    Returns a structured NPK recommendation based on the disease name.
    
    :param disease: The identified crop disease name.
    :return: A dictionary containing ratio, fertilizer, and reason.
    """
    if not disease:
        disease = "general"

    disease = disease.lower()

    if "blight" in disease:
        return {
            "ratio": "12-6-6",
            "fertilizer": "Urea fertilizer",
            "reason": "Nitrogen recovery for damaged leaves"
        }

    return {
        "ratio": "10-10-10",
        "fertilizer": "Balanced fertilizer",
        "reason": "General plant recovery"
    }

if __name__ == "__main__":
    # Internal Test
    test_cases = ["Tomato Early Blight", "Apple Cedar Rust", "Pepper Bell Bacterial Spot"]
    print("=== AgroVision AI: NPK Recommender Test ===")
    for case in test_cases:
        print(f"Disease: {case}\nRec: {recommend_npk(case)}\n")
