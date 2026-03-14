"""
Verification script for Dashboard Scan History.
Mocks Firebase and API calls to ensure data flows from Backend to Frontend.
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
import json

client = TestClient(app)

def test_history_api_integration():
    print("=== Verifying Dashboard Scan History API ===\n")
    
    mock_history_data = [
        {
            "disease": "Tomato___Late_blight",
            "confidence": "95.00%",
            "timestamp": "2024-03-14T10:00:00",
            "user_id": "guest_user",
            "weather_risk": "High"
        },
        {
            "disease": "Potato___Healthy",
            "confidence": "99.00%",
            "timestamp": "2024-03-14T09:00:00",
            "user_id": "guest_user",
            "weather_risk": "Low"
        }
    ]

    with patch('app.main.get_scan_history', return_value=mock_history_data):
        print("[*] Testing GET /scan-history...")
        response = client.get("/scan-history?user_id=guest_user")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["disease"] == "Tomato___Late_blight"
        print("[+] History Retrieval API: OK")

def test_analyze_saves_to_history():
    print("\n[*] Testing persistence during analysis...")
    
    mock_agro_report = {
        "disease": "Corn___Rust",
        "confidence": 0.88,
        "prevention": "Test advice"
    }

    with patch('app.main.get_full_agro_analysis', return_value=mock_agro_report):
        with patch('app.main.save_scan_result') as mock_save:
            file_content = b"fake-image"
            file = {"image": ("test.jpg", file_content, "image/jpeg")}
            
            response = client.post("/analyze-crop", files=file)
            
            assert response.status_code == 200
            # Ensure save_scan_result was called
            assert mock_save.called
            print("[+] Scan Persistence Trigger: OK")

    print("\n[SUCCESS] Dashboard Scan History integration verified!")

if __name__ == "__main__":
    try:
        test_history_api_integration()
        test_analyze_saves_to_history()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
