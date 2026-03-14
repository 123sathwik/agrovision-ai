"""
Verification script for groq_analysis.py.
Mocks Groq client to verify advice generation and JSON parsing.
"""
import json
from unittest.mock import patch, MagicMock
from ai_engine.groq_analysis import get_agricultural_advice

def test_groq_advice_logic():
    print("=== Verifying Groq Agricultural Advice Logic ===\n")
    
    # 1. Setup Mock Response
    mock_advice = {
        "disease_explanation": "Test Explanation",
        "cause": "Test Cause",
        "recommended_fertilizers": "Test Fertilizer",
        "npk_ratio": "1-1-1",
        "organic_treatment": "Test Organic",
        "chemical_treatment": "Test Chemical",
        "preventive_measures": "Test Prevention",
        "crop_rotation_suggestion": "Test Rotation"
    }
    
    # Build a mock completion object that mimics Groq's structure
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = json.dumps(mock_advice)
    
    # 2. Mock get_groq_client
    with patch('ai_engine.groq_analysis.get_groq_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_completion
        mock_get_client.return_value = mock_client
        
        print("[*] Calling get_agricultural_advice...")
        result = get_agricultural_advice("Potato", "Late Blight")
            
        # 3. Verify
        print(f"[+] Result Keys: {list(result.keys())}")
        
        expected_keys = [
            "disease_explanation", "cause", "recommended_fertilizers", 
            "npk_ratio", "organic_treatment", "chemical_treatment", 
            "preventive_measures", "crop_rotation_suggestion"
        ]
        
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"
            
        assert result["disease_explanation"] == "Test Explanation"
        print("\n[SUCCESS] Groq advice engine logic and parsing verified!")

if __name__ == "__main__":
    try:
        test_groq_advice_logic()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
