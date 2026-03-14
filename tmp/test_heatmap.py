"""
Verification script for heatmap_generator.py.
Mocks model and verification of file output.
"""
import torch
import os
import numpy as np
from PIL import Image
from unittest.mock import patch, MagicMock
from ai_engine.heatmap_generator import create_heatmap

def test_heatmap_generation():
    print("=== Verifying GradCAM Heatmap Logic ===\n")
    
    # 1. Setup Mock Data
    dummy_img_path = "tmp/dummy_leaf.jpg"
    os.makedirs("tmp", exist_ok=True)
    dummy_img = Image.new('RGB', (224, 224), color='green')
    dummy_img.save(dummy_img_path)
    
    # 2. Mock Model and Generator
    mock_model = MagicMock()
    # Simulate a forward pass output (batch=1, classes=16)
    mock_model.return_value = torch.randn(1, 16)
    mock_model.features = [MagicMock()] * 10 # Simulate features list
    
    # Mock GradCAM internal hooks and generate
    with patch('ai_engine.heatmap_generator.get_heatmap_generator') as mock_get_gen:
        mock_gen = MagicMock()
        # Simulate a 7x7 CAM activation map
        mock_gen.generate.return_value = np.random.rand(7, 7)
        mock_get_gen.return_value = (mock_gen, torch.device('cpu'))
        
        with patch('ai_engine.disease_detector.CLASS_NAMES', ['class']*16):
            print("[*] Generating verification heatmap...")
            output_path = create_heatmap(dummy_img_path, 0, output_dir="tmp/heatmaps")
            
            print(f"[+] Output generated at: {output_path}")
            
            # 3. Verify
            if os.path.exists(output_path):
                print("[SUCCESS] Heatmap file created.")
                img = Image.open(output_path)
                print(f"[*] Final image size: {img.size}")
                assert img.size == (224, 224), "Output size mismatch"
            else:
                print("[-] Error: Heatmap file not found.")
                exit(1)

    print("\n[FINISH] Heatmap generation logic verified!")

if __name__ == "__main__":
    test_heatmap_generation()
