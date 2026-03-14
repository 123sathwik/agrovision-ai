"""
Verification script for ai_engine/groq_analysis.py.
Mocks the Groq client to verify API integration and fallback logic.
"""
import json
from unittest.mock import patch, MagicMock
from ai_engine.groq_analysis import get_agricultural_advice

def test_groq_integration():
    print("=== Verifying Groq API Integration (7 Fields) ===\n")
    
    # 1. Mock API Response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "disease_explanation": "Test explanation.",
        "cause": "Test cause.",
        "fertilizer_recommendation": "Test fertilizer.",
        "npk_ratio": "0-0-0",
        "organic_treatment": "Test organic.",
        "chemical_treatment": "Test chemical.",
        "next_crop_suggestion": "Test rotation."
    })
    
    # 2. Mock Groq Client
    with patch('ai_engine.groq_analysis.Groq') as MockGroq:
        mock_client = MockGroq.return_value
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test Successful API Call
        with patch('ai_engine.groq_analysis.GROQ_API_KEY', 'fake_active_key'):
            print("[*] Testing successful Groq API call...")
            result = get_agricultural_advice("Tomato", "Test Disease")
            assert len(result) == 7
            assert "fertilizer_recommendation" in result
            assert result["npk_ratio"] == "0-0-0"
            print("[+] API Integration: OK")

    # 3. Test Fallback (Missing Key)
    with patch('ai_engine.groq_analysis.GROQ_API_KEY', None):
        print("[*] Testing fallback for missing API key...")
        result = get_agricultural_advice("Tomato", "Test Disease")
        assert len(result) == 7
        assert result["npk_ratio"] == "10-10-10"
        print("[+] Fallback Logic: OK")

    print("\n[SUCCESS] Groq API integration verified!")

if __name__ == "__main__":
    try:
        test_groq_integration()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
