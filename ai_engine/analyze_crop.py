"""
Orchestrates the full crop analysis pipeline.
Combines disease detection with visual explainability (GradCAM heatmaps).
"""
import os
import sys

# Ensure project root is in Python path for direct execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_engine.disease_detector import predict_disease
from ai_engine.heatmap_generator import create_heatmap

def analyze_crop(image_path):
    """
    Runs the complete analysis for a given crop image.
    1. Predicts disease and confidence (heatmap generated inside predict_disease).
    2. Falls back to create_heatmap if heatmap_path is missing.

    :param image_path: Path to the image file.
    :return: Dictionary containing analysis results.
    """
    print(f"[*] Starting analysis for: {image_path}")

    # 1. Disease Prediction (includes integrated heatmap generation)
    try:
        prediction = predict_disease(image_path)
    except Exception as e:
        print(f"[-] Error during disease prediction: {e}")
        return {
            "disease": "Unknown Disease",
            "confidence": 0,
            "class_index": 0,
            "raw_class": "Unknown Disease",
            "heatmap_path": None
        }

    # 2. Heatmap — use from predict_disease if available, else fallback
    heatmap_path = prediction.get("heatmap_path")
    if not heatmap_path:
        try:
            heatmap_path = create_heatmap(image_path, prediction["class_index"])
        except Exception as e:
            print(f"[-] Heatmap fallback also failed: {e}")
            heatmap_path = None

    result = {
        "disease": prediction["disease"],
        "confidence": prediction["confidence"],
        "class_index": prediction["class_index"],
        "raw_class": prediction["raw_class"],
        "heatmap_path": heatmap_path
    }

    print(f"[+] Analysis complete: {result['disease']} ({result['confidence']}%)")
    return result

if __name__ == "__main__":
    # CLI Usage: python ai_engine/analyze_crop.py <path_to_image>
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        if os.path.exists(img_path):
            analyze_crop(img_path)
        else:
            print(f"[-] Error: File not found at {img_path}")
    else:
        print("Usage: python ai_engine/analyze_crop.py <path_to_image>")
