import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# cred = credentials.Certificate("credentials/firebase.json")
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))

# Check if already initialized to prevent error on re-runs/reloads
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_scan_result(scan_data, user_id="guest_user"):
    """
    Saves a complete crop analysis record to Firestore.
    """
    try:
        data = {
            "disease": scan_data.get("disease"),
            "confidence": scan_data.get("confidence"),
            "temperature": scan_data.get("temperature"),
            "humidity": scan_data.get("humidity"),
            "risk_level": scan_data.get("risk_level"),
            "treatment_plan": scan_data.get("treatment"),
            "user_id": user_id,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        doc_ref = db.collection("crop_scans").add(data)
        return doc_ref[1].id
    except Exception as e:
        print("Firebase save failed:", e)
        return None

def get_scan_history(user_id="guest_user"):
    """Fetches scan history for a user."""
    try:
        from google.cloud.firestore_v1.base_query import FieldFilter
        docs = db.collection("crop_scans").where(filter=FieldFilter("user_id", "==", user_id)).limit(10).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"[-] Firebase History Error: {e}")
        return []
