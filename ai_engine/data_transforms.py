"""
Standardized image transformation and augmentation pipelines for AgroVision AI.
Uses torchvision.transforms to prepare crop images for model training and validation.
"""
from torchvision import transforms

def get_train_transforms():
    """
    Returns the transformation pipeline for training data.
    Includes augmentations to improve model generalization.
    """
    return transforms.Compose([
        # 1. Resize images to standard input size for most CNNs
        transforms.Resize((224, 224)),
        
        # 2. Random augmentations for robustness
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2),
        
        # 3. Convert to PyTorch Tensor
        transforms.ToTensor(),
        
        # 4. Normalize using ImageNet statistics
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def get_validation_transforms():
    """
    Returns the transformation pipeline for validation/inference data.
    No randomness, just resizing and normalization.
    """
    return transforms.Compose([
        # 1. Resize to same size as training
        transforms.Resize((224, 224)),
        
        # 2. Convert to Tensor
        transforms.ToTensor(),
        
        # 3. Normalize using same stats as training
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
