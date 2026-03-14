"""
Verification script for analyze_crop.py.
Mocks internal engine components to verify the orchestration logic.
"""
import os
from unittest.mock import patch, MagicMock
from ai_engine.analyze_crop import analyze_crop

def test_unified_analysis():
    print("=== Verifying Unified Crop Analysis Pipeline ===\n")
    
    dummy_path = "tmp/sample_leaf.jpg"
    
    # Mock return values
    mock_prediction = {
        "disease": "Tomato Late Blight",
        "confidence": 0.9578,
        "class_index": 5
    }
    mock_heatmap = "outputs/heatmaps/heatmap_sample_leaf.jpg"
    
    with patch('ai_engine.analyze_crop.predict_disease', return_value=mock_prediction) as mock_predict:
        with patch('ai_engine.analyze_crop.create_heatmap', return_value=mock_heatmap) as mock_heat:
            
            print("[*] Running analyze_crop('tmp/sample_leaf.jpg')...")
            result = analyze_crop(dummy_path)
            
            # Verify calls
            mock_predict.assert_called_once_with(dummy_path)
            mock_heat.assert_called_once_with(dummy_path, 5)
            
            print(f"[+] Result: {result}")
            
            # Verify result dictionary
            assert result["disease"] == "Tomato Late Blight"
            assert result["confidence"] == 0.9578
            assert result["heatmap_path"] == mock_heatmap
            
    print("\n[SUCCESS] Unified analysis orchestration verified!")

if __name__ == "__main__":
    try:
        test_unified_analysis()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
