import os
import shutil
import uuid
import sys
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# Add the current directory (project root) to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the unified intelligence orchestrator and firebase services
from ai_engine.agro_analysis import get_full_agro_analysis
from services.firebase_service import save_scan_result, get_scan_history

app = FastAPI(title="AgroVision AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure temporary storage exists
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "AgroVision backend running"}

@app.get("/scan-history")
async def scan_history_endpoint(user_id: str = Query("guest_user")):
    try:
        history = get_scan_history(user_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-crop")
async def analyze_crop(
    image: UploadFile = File(...),
    location: str = Query("Unknown", description="Location for weather analysis (City or lat,lon)"),
    user_id: str = Query("guest_user", description="User ID for history tracking")
):
    temp_file_path = None
    try:
        print("Starting crop analysis for location:", location)
        
        file_extension = os.path.splitext(image.filename)[1]
        temp_file_name = f"{uuid.uuid4()}{file_extension}"
        temp_file_path = os.path.join(TEMP_DIR, temp_file_name)
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # Call Orchestrator
        agro_result = get_full_agro_analysis(temp_file_path, location=location)
        
        # Save result to Firebase
        try:
            save_scan_result(agro_result, user_id)
        except Exception as e:
            print("FIREBASE ERROR:", str(e))
            
        # confidence is already a float percentage like 66.62 from predict_disease
        # Format as display string: '66.62%'
        raw_conf = agro_result.get("confidence", 0)
        if isinstance(raw_conf, (float, int)):
            agro_result["confidence"] = f"{raw_conf:.2f}%"

        return agro_result

    except Exception as e:
        print("ANALYSIS ERROR:", str(e))
        traceback.print_exc()

        return {
            "error": "AI analysis failed",
            "details": str(e),
            "disease": "Error Detected",
            "confidence": 0,
            "temperature": 0,
            "humidity": 0,
            "risk_level": "Unknown",
            "npk": {},
            "severity": {"severity": "Unknown", "infected_area": 0.0},
            "spread_prediction": {},
            "farmer_advice": "Service temporarily unavailable.",
            "next_crop": "Unknown",
            "treatment": "Service temporarily unavailable. Please try again later.",
            "heatmap_path": None
        }
    finally:
        image.file.close()
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"[!] Warning: Could not remove temp file {temp_file_path}: {e}")
