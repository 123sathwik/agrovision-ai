"""
Verification script for disease_detector.py.
Mocks model inference and verifies the return structure.
"""
import torch
from unittest.mock import patch, MagicMock
from PIL import Image
from ai_engine.disease_detector import predict_disease

def test_inference_logic():
    print("=== Verifying Disease Detector Inference Logic ===\n")
    
    # Create a dummy image
    dummy_img = Image.new('RGB', (224, 224), color='green')
    
    # Mocking the predict_disease's internal model call
    with patch('ai_engine.disease_detector.model') as mock_model:
        # Simulate a prediction (2 classes for simplicity in mock)
        # Assuming the mock handles the actual class count in real usage
        mock_output = torch.FloatTensor([[10.0] + [0.0]*14]) # Class 0 has highest logit
        mock_model.return_value = mock_output
        
        print("[*] Running inference on dummy image...")
        result = predict_disease(dummy_img)
        
        print(f"[+] Result: {result}")
        
        # Verify structure
        assert "disease" in result, "Missing 'disease' key"
        assert "confidence" in result, "Missing 'confidence' key"
        assert "class_index" in result, "Missing 'class_index' key"
        
        # Verify types
        assert isinstance(result["disease"], str), "Disease should be a string"
        assert isinstance(result["confidence"], float), "Confidence should be a float"
        assert isinstance(result["class_index"], int), "Class index should be an int"
        
        print("\n[SUCCESS] Inference logic verified correctly!")

if __name__ == "__main__":
    try:
        test_inference_logic()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
