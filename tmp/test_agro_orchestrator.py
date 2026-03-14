"""
Verification script for ai_engine/agro_analysis.py.
Mocks all underlying modules to verify orchestration and data mapping.
"""
from unittest.mock import patch, MagicMock
from ai_engine.agro_analysis import get_full_agro_analysis

def test_full_orchestration():
    print("=== Verifying Agro Intelligence Orchestrator ===\n")
    
    # Mock data
    mock_prediction = {
        "disease": "Tomato___Late_blight",
        "confidence": 0.95,
        "heatmap_path": "outputs/heatmaps/heatmap_sample.jpg"
    }
    mock_soil = {
        "NPK_ratio": "10-26-26",
        "fertilizers": ["DAP"],
        "soil_condition": "High phosphorus needed"
    }
    mock_rotation = {
        "recommended_crop": "Maize",
        "reason": "Family break"
    }
    mock_weather = {
        "disease_risk_level": "High",
        "description": "Fungal window active"
    }
    mock_groq = {
        "preventive_measures": "Avoid overhead irrigation, remove infected plants."
    }

    # Patching all dependencies
    with patch('ai_engine.agro_analysis.analyze_crop', return_value=mock_prediction):
        with patch('ai_engine.agro_analysis.get_soil_analysis', return_value=mock_soil):
            with patch('ai_engine.agro_analysis.get_rotation_recommendation', return_value=mock_rotation):
                with patch('ai_engine.agro_analysis.get_weather_analysis', return_value=mock_weather):
                    with patch('ai_engine.agro_analysis.get_agricultural_advice', return_value=mock_groq):
                        
                        print("[*] Calling get_full_agro_analysis...")
                        result = get_full_agro_analysis("dummy.jpg", "London")
                        
                        # Verify Orchestration Results
                        print(f"[+] Disease: {result['disease']}")
                        assert result["disease"] == "Tomato___Late_blight"
                        assert result["confidence"] == 0.95
                        assert result["npk_ratio"] == "10-26-26"
                        assert result["next_crop"] == "Maize"
                        assert result["weather_risk"] == "High"
                        assert "overhead irrigation" in result["prevention"]
                        
    print("\n[SUCCESS] Agro Intelligence Orchestrator verified!")

if __name__ == "__main__":
    try:
        test_full_orchestration()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
