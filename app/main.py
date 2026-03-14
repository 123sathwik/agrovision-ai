import os
import shutil
import uuid
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from app.config import DISEASE_MODEL_PATH

# Import the unified intelligence orchestrator and firebase services
from ai_engine.agro_analysis import get_full_agro_analysis
from services.firebase_service import save_scan_result, get_scan_history

app = FastAPI(title="AgroVision AI")

# Ensure temporary storage exists
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to AgroVision AI API"}

@app.get("/scan-history")
async def scan_history_endpoint(user_id: str = Query("guest_user")):
    """
    Retrieves the scan history for a user from Firebase.
    """
    try:
        history = get_scan_history(user_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-crop")
async def analyze_crop_endpoint(
    image: UploadFile = File(...),
    location: str = Query("Unknown", description="Location for weather analysis (City or lat,lon)"),
    user_id: str = Query("guest_user", description="User ID for history tracking")
):
    """
    Endpoint to analyze a crop image for diseases and provide agro intelligence.
    Returns a unified report including AI detection, weather risk, and Groq advice.
    """
    temp_file_path = None
    try:
        # 1. Upload leaf image (temporarily saved onto disk)
        file_extension = os.path.splitext(image.filename)[1]
        temp_file_name = f"{uuid.uuid4()}{file_extension}"
        temp_file_path = os.path.join(TEMP_DIR, temp_file_name)
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # 2-7. Orchestrator executes analysis steps internally
        agro_result = get_full_agro_analysis(temp_file_path, location=location)
        
        if "error" in agro_result:
            raise HTTPException(status_code=500, detail=agro_result["error"])

        # 8. Save result to Firebase
        save_scan_result(
            agro_result,
            user_id
        )

        # confidence is already a float percentage like 66.62 from predict_disease
        # Format as display string: '66.62%'
        raw_conf = agro_result.get("confidence", 0)
        if isinstance(raw_conf, (float, int)):
            agro_result["confidence"] = f"{raw_conf:.2f}%"

        # 10. Return result to dashboard
        return agro_result

    except Exception as e:
        print("ERROR during crop analysis:", str(e))
        raise HTTPException(status_code=500, detail=f"Crop analysis failed: {str(e)}")
    finally:
        image.file.close()
        # Clean up temp file to prevent disk bloat
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"[!] Warning: Could not remove temp file {temp_file_path}: {e}")
