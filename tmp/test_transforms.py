"""
Test script for data_transforms.py.
Verifies transform output shapes and types.
"""
import torch
from ai_engine.data_transforms import get_train_transforms, get_validation_transforms
from PIL import Image
import numpy as np

def test_transforms():
    print("=== Testing AgroVision AI Data Transforms ===\n")
    
    # Create a dummy RGB image
    dummy_img = Image.fromarray(np.uint8(np.random.rand(300, 300, 3) * 255))
    
    train_tf = get_train_transforms()
    val_tf = get_validation_transforms()
    
    print("[*] Applying Training Transforms...")
    train_out = train_tf(dummy_img)
    print(f"  - Output Shape: {train_out.shape}")
    print(f"  - Output Type:  {type(train_out)}")
    assert train_out.shape == (3, 224, 224), "Training transform output shape mismatch"
    
    print("[*] Applying Validation Transforms...")
    val_out = val_tf(dummy_img)
    print(f"  - Output Shape: {val_out.shape}")
    print(f"  - Output Type:  {type(val_out)}")
    assert val_out.shape == (3, 224, 224), "Validation transform output shape mismatch"
    
    print("\n[SUCCESS] All transforms verified correctly!")

if __name__ == "__main__":
    try:
        test_transforms()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        exit(1)
