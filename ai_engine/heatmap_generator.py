"""
Generates GradCAM heatmaps for visual explainability of crop disease predictions.
Uses the pytorch-grad-cam library for high-quality activation mapping.
Delegates to the disease_detector model to ensure class count always matches.
"""
import os
import cv2
import torch
import numpy as np
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

def generate_heatmap(image_path, class_index, output_dir="outputs/heatmaps"):
    """
    Generates and saves a Grad-CAM heatmap for an image.
    Re-uses the loaded disease_detector model to avoid class mismatch.

    :param image_path: Path to the input image.
    :param class_index: The winning class index from predict_disease.
    :param output_dir: Directory where the heatmap will be saved.
    :return: Dict with 'heatmap_path' key.
    """
    try:
        from ai_engine.disease_detector import model, device, transform

        # Re-enable gradients for GradCAM backward pass
        for param in model.parameters():
            param.requires_grad_(True)

        image_pil = Image.open(image_path).convert("RGB")
        image_tensor = transform(image_pil).unsqueeze(0).to(device)

        target_layer = model.features[-1]
        cam = GradCAM(model=model, target_layers=[target_layer])

        print(f"[*] Generating Grad-CAM for class {class_index}...")
        grayscale_cam = cam(input_tensor=image_tensor)

        if grayscale_cam is None or len(grayscale_cam) == 0:
            print("[!] Warning: Grad-CAM returned empty result.")
            return {"heatmap_path": image_path}

        grayscale_cam = grayscale_cam[0]
        print(f"[*] Grad-CAM map shape: {grayscale_cam.shape}")

        # Overlay on original image
        image_np = np.array(image_pil.resize((224, 224))).astype(np.float32)
        visualization = show_cam_on_image(image_np / 255.0, grayscale_cam, use_rgb=True)

        os.makedirs(output_dir, exist_ok=True)
        import time
        output_path = os.path.join(output_dir, f"heatmap_{int(time.time())}.png")
        cv2.imwrite(output_path, cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))

        return {"heatmap_path": output_path}

    except Exception as e:
        print("Heatmap generation failed:", e)
        return {"heatmap_path": image_path}


def create_heatmap(image_path, class_index):
    """
    Wrapper for backward compatibility with analyze_crop.py.
    """
    try:
        result = generate_heatmap(image_path, class_index)
        return result["heatmap_path"]
    except Exception as e:
        print("Heatmap generation failed:", e)
        return image_path


if __name__ == "__main__":
    print("=== AgroVision AI: Heatmap Generator (GradCAM) ===")
