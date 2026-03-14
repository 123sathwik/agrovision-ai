"""
Verification script for app/main.py.
Verifies that the /analyze-crop endpoint returns the full 7-field report.
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
import io

client = TestClient(app)

def test_analyze_crop_full_report():
    print("=== Verifying Final Agro Intelligence API ===\n")
    
    # Mock return value from agro_analysis orchestrator
    mock_agro_report = {
        "disease": "Tomato___Early_blight",
        "confidence": 0.985,
        "npk_ratio": "10-10-10",
        "fertilizers": "Nitrogen-rich fertilizer",
        "next_crop": "Corn",
        "weather_risk": "Moderate",
        "prevention": "Keep leaves dry. Apply fungicide if rain persists."
    }

    with patch('app.main.get_full_agro_analysis', return_value=mock_agro_report):
        print("[*] Testing POST /analyze-crop with location query...")
        
        # Create a dummy image file
        file_content = b"fake-image-binary-content"
        file = {"image": ("test_leaf.jpg", file_content, "image/jpeg")}
        
        response = client.post("/analyze-crop?location=Chicago", files=file)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all 7 required fields are present
        required_fields = ["disease", "confidence", "npk_ratio", "fertilizers", "next_crop", "weather_risk", "prevention"]
        for field in required_fields:
            assert field in data, f"Missing field in API response: {field}"
        
        # Verify confidence formatting
        assert data["confidence"] == "98.50%"
        assert data["weather_risk"] == "Moderate"
        
        print("[+] API Multi-Service Integration: OK")
        print("[+] 7-Field Report Schema: OK")

    print("\n[SUCCESS] Final Agro Intelligence API verified!")

if __name__ == "__main__":
    try:
        test_analyze_crop_full_report()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
