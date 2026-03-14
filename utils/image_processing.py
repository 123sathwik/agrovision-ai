"""
Utilities for loading, resizing, normalizing, and converting crop images.
Prepares images for the disease detection model.
"""
import cv2
import numpy as np
import torch

def load_image(path):
    """
    Loads an image from the specified path using OpenCV.
    :param path: Path to the image file.
    :return: Image array in RGB format.
    """
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Could not load image at {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def resize_image(image, target_size=(224, 224)):
    """
    Resizes the image to the target dimensions.
    :param image: Input image array.
    :param target_size: Tuple (width, height).
    :return: Resized image array.
    """
    return cv2.resize(image, target_size)

def normalize_image(image):
    """
    Normalizes pixel values to the range [0, 1].
    :param image: Input image array.
    :return: Normalized image array.
    """
    return image.astype(np.float32) / 255.0

def convert_to_tensor(image):
    """
    Converts a NumPy image array to a PyTorch tensor.
    Rearranges dimensions from (H, W, C) to (C, H, W).
    :param image: Input image array.
    :return: PyTorch tensor.
    """
    # Transpose dimensions: (H, W, C) -> (C, H, W)
    image = np.transpose(image, (2, 0, 1))
    return torch.from_numpy(image).float()
