"""
Test script for dataset_loader.py.
Verifies batch loading, tensor shapes, and class mapping.
"""
import torch
from ai_engine.dataset_loader import get_dataset_loaders

def test_loader():
    print("=== Testing AgroVision AI Dataset Loader ===\n")
    
    try:
        # Load with small batch size for quick verification
        train_loader, val_loader, class_names = get_dataset_loaders(batch_size=4, num_workers=0)
        
        print(f"\n[*] Class Names Example: {class_names[:3]}...")
        assert len(class_names) > 0, "No classes found"
        
        # Test pulling a training batch
        print("[*] Verifying Training DataLoader...")
        train_images, train_labels = next(iter(train_loader))
        print(f"  - Batch Image Shape:  {train_images.shape}")
        print(f"  - Batch Label Shape:  {train_labels.shape}")
        assert train_images.shape == (4, 3, 224, 224), "Training batch shape mismatch"
        
        # Test pulling a validation batch
        print("[*] Verifying Validation DataLoader...")
        val_images, val_labels = next(iter(val_loader))
        print(f"  - Batch Image Shape:  {val_images.shape}")
        assert val_images.shape == (4, 3, 224, 224), "Validation batch shape mismatch"
        
        print("\n[SUCCESS] Dataset Loader verified correctly!")
        
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    test_loader()
