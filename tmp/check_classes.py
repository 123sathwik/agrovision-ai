
import os
import sys
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_engine.disease_detector import CLASS_NAMES, DATASET_PATH

print(f"DATASET_PATH: {DATASET_PATH}")
print(f"Dataset exists: {os.path.exists(DATASET_PATH)}")
print(f"Number of classes: {len(CLASS_NAMES)}")
print("Classes:")
for i, name in enumerate(CLASS_NAMES):
    print(f"  {i}: {name}")
