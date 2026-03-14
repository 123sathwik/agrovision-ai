"""
Utilities for loading and splitting the PlantVillage dataset for training and validation.
Uses PyTorch's ImageFolder and DataLoader with standardized transforms.
"""
import os
import torch
from torchvision import datasets
from torch.utils.data import DataLoader, Subset, random_split
from ai_engine.data_transforms import get_train_transforms, get_validation_transforms

def get_dataset_loaders(data_path="data/crop_disease_dataset", batch_size=32, num_workers=4):
    """
    Creates training and validation DataLoaders with an 80/20 split.
    :param data_path: Root directory of the dataset.
    :param batch_size: Number of images per batch.
    :param num_workers: Number of subprocesses for data loading.
    :return: (train_loader, val_loader, class_names)
    """
    print(f"[*] Initializing Dataset Loader from: {data_path}")
    
    # 1. Resolve actual dataset path (handling nested PlantVillage folder)
    target_path = data_path
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"[-] Error: Path '{target_path}' not found.")
    
    nested_pv = os.path.join(target_path, "PlantVillage")
    if os.path.exists(nested_pv) and os.path.isdir(nested_pv):
        target_path = nested_pv
        print(f"[*] Using resolved path: {target_path}")

    # 2. Create two ImageFolder instances for different transforms
    # This prevents training augmentations from leaking into validation
    full_train_dataset = datasets.ImageFolder(root=target_path, transform=get_train_transforms())
    full_val_dataset = datasets.ImageFolder(root=target_path, transform=get_validation_transforms())
    
    class_names = full_train_dataset.classes
    dataset_size = len(full_train_dataset)
    
    # 3. Calculate split indices
    train_size = int(0.8 * dataset_size)
    val_size = dataset_size - train_size
    
    # Use torch.random.manual_seed for reproducibility of the split if needed
    indices = torch.randperm(dataset_size).tolist()
    train_indices = indices[:train_size]
    val_indices = indices[train_size:]
    
    # Create Subsets from the correctly transformed master datasets
    train_dataset = Subset(full_train_dataset, train_indices)
    val_dataset = Subset(full_val_dataset, val_indices)
    
    print(f"[+] Dataset Split Summary:")
    print(f"    - Total Images:      {dataset_size}")
    print(f"    - Training Set:      {len(train_dataset)}")
    print(f"    - Validation Set:    {len(val_dataset)}")
    print(f"    - Number of Classes: {len(class_names)}")

    # 4. Create PyTorch DataLoaders
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=num_workers,
        pin_memory=True if torch.cuda.is_available() else False
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=num_workers,
        pin_memory=True if torch.cuda.is_available() else False
    )
    
    return train_loader, val_loader, class_names

if __name__ == "__main__":
    # Internal test/preview
    try:
        t_loader, v_loader, names = get_dataset_loaders()
        print(f"\n[SUCCESS] Loaded {len(t_loader)} training batches and {len(v_loader)} validation batches.")
    except Exception as e:
        print(f"\n[-] Loader initialization failed: {e}")
