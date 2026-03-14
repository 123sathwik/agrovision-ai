"""
Verification script for ai_engine/model.py.
Checks architecture, freezing status, and output shapes.
"""
import torch
from ai_engine.model import create_model

def test_model():
    print("=== Testing AgroVision AI Model Architecture ===\n")
    
    num_classes = 15
    model = create_model(num_classes)
    
    # 1. Check backbone freezing
    backbone_trainable = any(p.requires_grad for p in model.features.parameters())
    print(f"[*] Backbone trainable parameters: {backbone_trainable}")
    assert not backbone_trainable, "Backbone layers should be frozen"
    
    # 2. Check classifier head
    classifier_trainable = any(p.requires_grad for p in model.classifier.parameters())
    print(f"[*] Classifier head trainable:     {classifier_trainable}")
    assert classifier_trainable, "Classifier head should be trainable"
    
    # 3. Verify output features
    last_layer = model.classifier[1]
    print(f"[*] Last layer out_features:      {last_layer.out_features}")
    assert last_layer.out_features == num_classes, f"Expected {num_classes} output features"
    
    # 4. Perform forward pass
    dummy_tensor = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        output = model(dummy_tensor)
    print(f"[*] Forward pass output shape:    {output.shape}")
    assert output.shape == (1, num_classes), f"Expected (1, {num_classes}) output shape"
    
    print("\n[SUCCESS] Model architecture verified correctly!")

if __name__ == "__main__":
    try:
        test_model()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        exit(1)
