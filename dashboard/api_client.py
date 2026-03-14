import requests
import os

# Base URL for the FastAPI backend
BASE_URL = "http://127.0.0.1:8000"

def analyze_crop(image_path, location="Unknown"):
    """
    Sends a crop image file and location to the FastAPI backend for analysis.
    
    Args:
        image_path (str): The path to the image file.
        location (str): The location for weather analysis.
        
    Returns:
        dict: JSON response containing disease, confidence, heatmap, npk_ratio, 
              fertilizers, next_crop, and weather_risk.
    """
    url = f"{BASE_URL}/analyze-crop"
    params = {"location": location}
    
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}

    try:
        with open(image_path, "rb") as f:
            files = {"image": (os.path.basename(image_path), f, "image/jpeg")}
            response = requests.post(url, params=params, files=files, timeout=30)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}

def get_history(user_id="guest_user"):
    """
    Fetches the scan history for a user from the backend.
    """
    url = f"{BASE_URL}/scan-history"
    params = {"user_id": user_id}
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch history: {str(e)}"}
