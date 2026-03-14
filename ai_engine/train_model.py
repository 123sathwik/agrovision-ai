import sys
import os

# Ensure project root is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"""
Orchestrates the training and validation loops for the crop disease classifier.
Integrates dataset loading, model initialization, optimization, and checkpointing.
"""
import torch
import torch.nn as nn
import torch.optim as optim
import os
import time
from tqdm import tqdm
from ai_engine.dataset_loader import get_dataset_loaders
from ai_engine.model import create_model

def main(epochs=10, batch_size=32, learning_rate=0.001):
    """
    Main training function to orchestrate the learning process.
    """
    print("=== AgroVision AI: Model Training Orchestrator ===\n")
    
    # 1. Setup Device
    device = torch.device("mps" if torch.backends.mps.is_available() else 
                          "cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Training on device: {device}")

    # 2. Load Dataset
    print("[*] Stage 1: Loading DataLoaders...")
    train_loader, val_loader, class_names = get_dataset_loaders(batch_size=batch_size)
    num_classes = len(class_names)

    # 3. Initialize Model
    print("[*] Stage 2: Initializing Architecture...")
    model = create_model(num_classes).to(device)

    # 4. Setup Loss and Optimizer
    criterion = nn.CrossEntropyLoss()
    # Only optimizing the classifier head (transfer learning)
    optimizer = optim.Adam(model.classifier.parameters(), lr=learning_rate)

    # 5. Training Loop
    print(f"\n[*] Stage 3: Starting Training Loop ({epochs} Epochs)...")
    checkpoint_dir = "models/checkpoints"
    final_dir = "models/final"
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(final_dir, exist_ok=True)

    for epoch in range(1, epochs + 1):
        print(f"\n--- Epoch {epoch}/{epochs} ---")
        
        # --- Training Phase ---
        model.train()
        running_loss = 0.0
        train_bar = tqdm(train_loader, desc=f"Epoch {epoch} [Train]", unit="batch")
        
        for inputs, labels in train_bar:
            inputs, labels = inputs.to(device), labels.to(device)
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            train_bar.set_postfix(loss=f"{loss.item():.4f}")

        avg_train_loss = running_loss / len(train_loader)

        # --- Validation Phase ---
        model.eval()
        correct = 0
        total = 0
        val_bar = tqdm(val_loader, desc=f"Epoch {epoch} [Val]", unit="batch")
        
        with torch.no_grad():
            for inputs, labels in val_bar:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_accuracy = 100 * correct / total
        print(f"\n[Summary] Train Loss: {avg_train_loss:.4f} | Val Accuracy: {val_accuracy:.2f}%")

        # --- Checkpointing ---
        checkpoint_path = os.path.join(checkpoint_dir, f"epoch_{epoch}.pth")
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': avg_train_loss,
            'accuracy': val_accuracy
        }, checkpoint_path)
        print(f"[*] Checkpoint saved: {checkpoint_path}")

    # 6. Save Final Model
    final_path = os.path.join(final_dir, "crop_disease_model.pth")
    torch.save(model.state_dict(), final_path)
    print(f"\n[SUCCESS] Final model saved: {final_path}")
    print("=== Training sequence complete! ===")

if __name__ == "__main__":
    main()
