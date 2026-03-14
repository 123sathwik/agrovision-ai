"""
Defines the neural network architecture for crop disease classification.
Uses a pretrained EfficientNet-B0 backbone with a custom classification head.
"""
import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import EfficientNet_B0_Weights

def create_model(num_classes):
    """
    Initializes a transfer learning model based on EfficientNet-B0.
    Backbone layers are frozen, and the classifier is replaced for the target classes.
    :param num_classes: Number of disease categories.
    :return: Initialized PyTorch model.
    """
    print(f"[*] Initializing EfficientNet-B0 for {num_classes} classes...")
    
    # 1. Load pretrained EfficientNet-B0
    # Using the modern Weights Enum API
    model = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
    
    # 2. Freeze backbone layers
    # This ensures only the new classifier layers are trained initially
    for param in model.parameters():
        param.requires_grad = False
        
    # 3. Modify the classifier head
    # For EfficientNet-B0, the input to the classifier is 1280 features
    num_ftrs = model.classifier[1].in_features
    
    # Replace the existing classifier with a custom sequential block
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2, inplace=True),
        nn.Linear(in_features=num_ftrs, out_features=num_classes)
    )
    
    return model

if __name__ == "__main__":
    # Internal test: Verify architecture for a hypothetical 15-class dataset
    test_num_classes = 15
    model = create_model(test_num_classes)
    
    # Verify parameter freezing
    is_frozen = not any(p.requires_grad for p in model.features.parameters())
    print(f"[*] Backbone Frozen: {is_frozen}")
    
    # Verify final layer
    out_features = model.classifier[1].out_features
    print(f"[*] Classifier output features: {out_features}")
    
    # Verify forward pass
    print("[*] Running forward pass on dummy input...")
    dummy_input = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        output = model(dummy_input)
    print(f"[+] Output shape: {output.shape}")
    
    if output.shape == (1, test_num_classes):
        print("\n[SUCCESS] Model architecture verified!")
