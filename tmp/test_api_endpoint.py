"""
Verification script for app/main.py endpoint /analyze-crop.
Mocks the unified agro_analysis orchestrator to verify the API logic.
"""
import io
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_analyze_crop_api_unified():
    print("=== Verifying Upgraded POST /analyze-crop Endpoint ===\n")
    
    # 1. Mock Unified Response
    mock_unified_result = {
        "disease": "Tomato___Late_blight",
        "confidence": 0.95,
        "heatmap": "outputs/heatmaps/heatmap_test.jpg",
        "npk_ratio": "10-26-26",
        "fertilizers": ["DAP", "Sulfate of Potash"],
        "next_crop": "Maize",
        "weather_risk": "High",
        "prevention": "Avoid overhead irrigation, remove infected plants."
    }
    
    # 2. Mock Orchestrator
    with patch('app.main.get_full_agro_analysis', return_value=mock_unified_result):
        
        # 3. Send Request with Location
        print("[*] Sending mock image upload with location parameter...")
        dummy_image = io.BytesIO(b"dummy_image_content")
        response = client.post(
            "/analyze-crop?location=London",
            files={"image": ("test.jpg", dummy_image, "image/jpeg")}
        )
        
        # 4. Verify
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Response: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["disease"] == "Tomato___Late_blight"
        assert data["confidence"] == "95.00%"
        assert data["npk_ratio"] == "10-26-26"
        assert data["next_crop"] == "Maize"
        assert data["weather_risk"] == "High"
        assert "overhead irrigation" in data["prevention"]

    print("\n[SUCCESS] Upgraded API endpoint orchestration verified!")

if __name__ == "__main__":
    try:
        test_analyze_crop_api_unified()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
