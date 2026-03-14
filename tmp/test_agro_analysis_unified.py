"""
Verification script for ai_engine/agro_analysis.py.
Mocks all input services to verify the unified data construction.
"""
import json
from unittest.mock import patch, MagicMock
from ai_engine.agro_analysis import get_full_agro_analysis

def test_agro_analysis_unified():
    print("=== Verifying Unified Agro Analysis Orchestrator ===\n")
    
    # 1. Mock Analyze Crop
    mock_prediction = {
        "disease": "Potato___Early_blight",
        "confidence": 0.95,
        "heatmap_path": "outputs/heatmaps/test.png"
    }
    
    # 2. Mock Weather Analysis
    mock_weather = {
        "disease_risk": "High",
        "recommendation": "Spray fungicide."
    }
    
    # 3. Mock Groq Advice
    mock_groq = {
        "npk_ratio": "5-10-15",
        "fertilizer_recommendation": "Potassium-rich fertilizer",
        "organic_treatment": "Neem oil",
        "chemical_treatment": "Chlorothalonil",
        "next_crop_suggestion": "Beans"
    }

    with patch('ai_engine.agro_analysis.analyze_crop', return_value=mock_prediction):
        with patch('ai_engine.agro_analysis.get_weather_analysis', return_value=mock_weather):
            with patch('ai_engine.agro_analysis.get_agricultural_advice', return_value=mock_groq):
                
                print("[*] Testing unified report construction...")
                report = get_full_agro_analysis("test_image.jpg", "London")
                
                # Verify 7 fields
                expected_keys = ["disease", "confidence", "npk_ratio", "fertilizers", "next_crop", "weather_risk", "prevention"]
                for key in expected_keys:
                    assert key in report, f"Missing key: {key}"
                
                assert report["npk_ratio"] == "5-10-15"
                assert report["weather_risk"] == "High"
                assert "Neem oil" in report["prevention"]
                assert "Spray fungicide" in report["prevention"]
                
                print("[+] Report Data Construction: OK")

    print("\n[SUCCESS] Unified Agro Analysis logic verified!")

if __name__ == "__main__":
    try:
        test_agro_analysis_unified()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
