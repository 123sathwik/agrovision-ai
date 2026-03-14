"""
Verification script for GradCAM++ heatmap generation.
Mocks the library calls to verify the implementation logic.
"""
import os
import numpy as np
from unittest.mock import patch, MagicMock
from ai_engine.heatmap_generator import generate_heatmap

def test_gradcam_plus_plus():
    print("=== Verifying GradCAM++ Implementation ===\n")
    
    dummy_img_path = "tmp/sample_leaf.jpg"
    os.makedirs("tmp", exist_ok=True)
    # Create a dummy image if it doesn't exist
    from PIL import Image
    if not os.path.exists(dummy_img_path):
        Image.new('RGB', (224, 224), color='green').save(dummy_img_path)
    
    # Mocking GradCAMPlusPlus compute logic
    mock_cam_instance = MagicMock()
    # grayscale_cam should be a 2D numpy array
    mock_cam_instance.return_value = np.zeros((1, 224, 224), dtype=np.float32)
    
    with patch('ai_engine.heatmap_generator.GradCAMPlusPlus', return_value=mock_cam_instance):
        with patch('ai_engine.heatmap_generator.create_model', return_value=MagicMock()):
            with patch('cv2.imwrite') as mock_write:
                
                print("[*] Calling generate_heatmap...")
                result = generate_heatmap(dummy_img_path, 3)
                
                # Check result
                print(f"[+] Heatmap path: {result['heatmap_path']}")
                assert "heatmap_path" in result
                # Use normpath to ensure separators match
                normalized_path = os.path.normpath(result["heatmap_path"])
                expected_part = os.path.normpath("outputs/heatmaps/heatmap_")
                assert expected_part in normalized_path
                
                # Verify library usage
                mock_cam_instance.assert_called_once()
                mock_write.assert_called_once()

    print("\n[SUCCESS] GradCAM++ implementation logic verified!")

if __name__ == "__main__":
    try:
        test_gradcam_plus_plus()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
