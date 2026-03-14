"""
Configuration settings for AgroVision AI.
Loads environmental variables from the .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_env_variable(name):
    """
    Retrieves an environment variable or raises a detailed ValueError if not found.
    """
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}. "
                         f"Please ensure it is set in your .env file.")
    return value

# AI & LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Firebase Configuration
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

# Weather Service Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Global Paths
DISEASE_MODEL_PATH = os.path.join("models", "final", "crop_disease_model.pth")
HEATMAP_OUTPUT_DIR = "outputs/heatmaps"
TEMP_UPLOAD_DIR = "temp_uploads"
