"""
Logic for running crop disease inference using the trained EfficientNet-B0 model.
Integrates with standardized preprocessing and provides metadata for GradCAM.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms
from torchvision.models import efficientnet_b0

# Paths
MODEL_PATH = "models/final/crop_disease_model.pth"

def load_class_names():
    """
    Returns the fixed set of 16 classes matching the trained model.
    """
    return [
        "Apple_scab",
        "Apple_black_rot",
        "Apple_cedar_rust",
        "Apple_healthy",
        "Corn_gray_leaf_spot",
        "Corn_common_rust",
        "Corn_northern_leaf_blight",
        "Corn_healthy",
        "Potato_early_blight",
        "Potato_late_blight",
        "Potato_healthy",
        "Tomato_bacterial_spot",
        "Tomato_early_blight",
        "Tomato_late_blight",
        "Tomato_leaf_mold",
        "Tomato_healthy"
    ]

# Global class names — always 16
CLASS_NAMES = load_class_names()

def load_inference_model():
    """
    Initializes EfficientNet-B0 with the correct number of output classes
    and loads trained weights. Returns model and device.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    classes = load_class_names()
    num_classes = len(classes)
    print("Initializing EfficientNet for", num_classes, "classes")

    model = efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(1280, num_classes)

    if os.path.exists(MODEL_PATH):
        print(f"[*] Loading weights from: {MODEL_PATH}")
        try:
            checkpoint = torch.load(MODEL_PATH, map_location=device)
            # Support both raw state_dict and wrapped checkpoints
            if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
                checkpoint = checkpoint["state_dict"]
            model.load_state_dict(checkpoint, strict=False)
            print("[+] Weights loaded successfully.")
        except Exception as e:
            print(f"[!] Warning: Could not load weights: {e}")
    else:
        print(f"[!] Warning: Model file not found at {MODEL_PATH}. Using random weights.")

    model.to(device)
    model.eval()
    return model, device

# Global model and device loaded once at startup
model, device = load_inference_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def preprocess_image(path_or_img):
    """Load and preprocess image to tensor."""
    if isinstance(path_or_img, str):
        img = Image.open(path_or_img).convert("RGB")
    else:
        img = path_or_img.convert("RGB")
    tensor = transform(img).unsqueeze(0)
    return tensor, img

def predict_disease(image_input):
    """
    Runs inference and returns structured output with disease, confidence and heatmap.
    Always returns a valid dict; never raises.
    """
    print("Starting disease detection...")

    # Defaults for safe fallback
    disease = "Unknown Disease"
    confidence = 0.0
    pred_index = 0
    heatmap_path = None

    try:
        classes = load_class_names()
        print("Dataset classes:", classes)
        print("Model classes:", len(classes))

        # 1. Preprocess
        image_tensor, image_pil = preprocess_image(image_input)
        image_tensor = image_tensor.to(device)
        print("Image tensor shape:", image_tensor.shape)

        # 2. Forward pass
        with torch.no_grad():
            outputs = model(image_tensor)

        print("Model output shape:", outputs.shape)

        # 3. Softmax confidence (correct percentages)
        probs = F.softmax(outputs, dim=1)
        confidence_tensor, pred_index_tensor = torch.max(probs, 1)
        confidence = round(confidence_tensor.item() * 100, 2)
        pred_index = pred_index_tensor.item()

        print("Prediction index:", pred_index)

        try:
            disease = classes[pred_index]
        except IndexError:
            print(f"[!] pred_index {pred_index} out of range for {len(classes)} classes. Using fallback.")
            disease = "Unknown Disease"

        print("Predicted disease:", disease)
        print(f"Confidence: {confidence}%")

        # 4. Generate GradCAM heatmap
        try:
            from pytorch_grad_cam import GradCAM
            from pytorch_grad_cam.utils.image import show_cam_on_image

            # Re-enable gradients for GradCAM
            for param in model.parameters():
                param.requires_grad_(True)

            target_layer = model.features[-1]
            cam = GradCAM(model=model, target_layers=[target_layer])

            grayscale_cam = cam(input_tensor=image_tensor)[0]

            image_np = np.array(image_pil.resize((224, 224))).astype(np.float32)

            heatmap_vis = show_cam_on_image(
                image_np / 255.0,
                grayscale_cam,
                use_rgb=True
            )

            os.makedirs("temp_uploads", exist_ok=True)
            heatmap_path = "temp_uploads/heatmap.jpg"
            cv2.imwrite(heatmap_path, cv2.cvtColor(heatmap_vis, cv2.COLOR_RGB2BGR))
            print("[+] Heatmap saved to:", heatmap_path)

        except Exception as e:
            print("Heatmap generation failed:", e)
            heatmap_path = None

    except Exception as e:
        print("Prediction error:", e)
        disease = "Unknown Disease"
        confidence = 0.0
        pred_index = 0
        heatmap_path = None

    return {
        "disease": disease,
        "confidence": confidence,
        "class_index": pred_index,
        "raw_class": disease,
        "heatmap_path": heatmap_path
    }

if __name__ == "__main__":
    print("\n=== Disease Detector: Inference Test ===")
    dummy_img = Image.new("RGB", (224, 224), color="green")
    result = predict_disease(dummy_img)
    print(f"[Result] Disease: {result['disease']} | Confidence: {result['confidence']}%")
