"""
Dry run verification for train_model.py.
Mocks a small training cycle to ensure logic is sound.
"""
import torch
from ai_engine.train_model import main
from unittest.mock import patch, MagicMock

def test_training_flow():
    print("=== Verifying Model Training Logic ===\n")
    
    # We will patch the actual get_dataset_loaders to return small dummy data
    # and limit epochs to 1 for a quick dry run check.
    
    mock_train_loader = MagicMock()
    mock_val_loader = MagicMock()
    
    # Simulate 2 batches
    dummy_input = torch.randn(2, 3, 224, 224)
    dummy_label = torch.LongTensor([0, 1])
    mock_train_loader.__iter__.return_value = [(dummy_input, dummy_label), (dummy_input, dummy_label)]
    mock_train_loader.__len__.return_value = 2
    
    mock_val_loader.__iter__.return_value = [(dummy_input, dummy_label)]
    mock_val_loader.__len__.return_value = 1
    
    with patch('ai_engine.train_model.get_dataset_loaders', return_value=(mock_train_loader, mock_val_loader, ['class1', 'class2'])):
        print("[*] Running 1-epoch dry run...")
        main(epochs=1)
    
    print("\n[SUCCESS] Training orchestrator logic verified!")

if __name__ == "__main__":
    test_training_flow()
