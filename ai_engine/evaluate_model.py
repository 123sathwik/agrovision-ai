"""
Evaluates the performance of the trained crop disease classification model.
Calculates accuracy, precision, recall, and generates a confusion matrix using scikit-learn.
"""
import torch
import numpy as np
import os
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from ai_engine.dataset_loader import get_dataset_loaders
from ai_engine.model import create_model
from tqdm import tqdm

def evaluate_model(model_path="models/final/crop_disease_model.pth", batch_size=32):
    """
    Loads a trained model and evaluates it on the validation set.
    """
    print("=== AgroVision AI: Model Performance Evaluation ===\n")
    
    # 1. Setup Device
    device = torch.device("mps" if torch.backends.mps.is_available() else 
                          "cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Evaluating on device: {device}")

    # 2. Load DataLoaders
    print("[*] Loading validation data...")
    _, val_loader, class_names = get_dataset_loaders(batch_size=batch_size)
    num_classes = len(class_names)

    # 3. Initialize and Load Model
    if not os.path.exists(model_path):
        print(f"[-] Error: Final model file not found at {model_path}")
        print("    Please run 'python ai_engine/train_model.py' first.")
        return

    print(f"[*] Loading model from: {model_path}")
    model = create_model(num_classes).to(device)
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
    except Exception as e:
        print(f"[-] Error loading model state dict: {e}")
        return

    # 4. Inference Loop
    print("[*] Running inference on validation set...")
    y_true = []
    y_pred = []

    with torch.no_grad():
        for inputs, labels in tqdm(val_loader, desc="Evaluating", unit="batch"):
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            
            y_true.extend(labels.numpy())
            y_pred.extend(predicted.cpu().numpy())

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # 5. Calculate Metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
    
    # 6. Generate Reports
    print("\n" + "="*50)
    print("PERFORMANCE SUMMARY")
    print("="*50)
    print(f"Accuracy:  {accuracy * 100:.2f}%")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("="*50)
    
    print("\nCLASSIFICATION REPORT")
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    print("\nCONFUSION MATRIX")
    conf_mat = confusion_matrix(y_true, y_pred)
    print(conf_mat)
    
    print("\n[FINISH] Evaluation sequence completed.")

if __name__ == "__main__":
    evaluate_model()
