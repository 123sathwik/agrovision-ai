import cv2
import numpy as np
import os

def calculate_severity(heatmap_path):
    """
    Estimates disease severity using heatmap pixel intensity.
    
    :param heatmap_path: Path to the generated AI heatmap image.
    :return: Dictionary containing severity level and infected area percentage.
    """
    if not heatmap_path or not os.path.exists(heatmap_path):
        return {
            "severity": "Unknown",
            "infected_area": 0.0
        }

    try:
        img = cv2.imread(heatmap_path)
        if img is None:
             raise ValueError(f"Could not read image at {heatmap_path}")
             
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Count pixels above an intensity threshold (150 represents "hot" activation areas)
        infected_pixels = np.sum(gray > 150)
        total_pixels = gray.size

        severity_ratio = infected_pixels / total_pixels

        if severity_ratio < 0.15:
            level = "Mild Infection"
        elif severity_ratio < 0.40:
            level = "Moderate Infection"
        else:
            level = "Severe Infection"

        return {
            "severity": level,
            "infected_area": round(severity_ratio * 100, 2)
        }
        
    except Exception as e:
        print(f"[!] Error calculating disease severity: {e}")
        return {
            "severity": "Unknown",
            "infected_area": 0.0
        }

if __name__ == "__main__":
    # Internal Test - Needs a real heatmap path to test fully
    print("=== AgroVision AI: Disease Severity Test ===")
    res = calculate_severity("non_existent.jpg")
    print(f"Fallback Test: {res}")
