"""
Verification script for services/firebase_service.py.
Mocks the Firebase Admin SDK to verify initialization and CRUD logic.
"""
import json
from unittest.mock import patch, MagicMock
from services.firebase_service import save_scan_result, get_scan_history

def test_firebase_service():
    print("=== Verifying Firebase Service Integration ===\n")
    
    # 1. Mock Firestore Client
    mock_db = MagicMock()
    mock_collection = mock_db.collection.return_value
    mock_doc = mock_collection.document.return_value
    mock_doc.id = "mock_doc_id_999"

    # 2. Patch the global 'db' instance in the service
    with patch('services.firebase_service.db', mock_db):
        print("[*] Testing save_scan_result...")
        test_data = {
            "user_id": "user_456",
            "disease": "Late Blight",
            "confidence": 0.98
        }
        doc_id = save_scan_result(test_data)
        
        assert doc_id == "mock_doc_id_999"
        mock_doc.set.assert_called_once()
        print("[+] save_scan_result: OK")

        print("[*] Testing get_scan_history...")
        # Mocking stream result
        mock_doc_snapshot = MagicMock()
        mock_doc_snapshot.to_dict.return_value = {"disease": "Healthy", "user_id": "user_456"}
        mock_collection.where.return_value.order_by.return_value.limit.return_value.stream.return_value = [mock_doc_snapshot]

        history = get_scan_history("user_456")
        assert len(history) == 1
        assert history[0]["disease"] == "Healthy"
        print("[+] get_scan_history: OK")

    print("\n[SUCCESS] Firebase service logic verified!")

if __name__ == "__main__":
    try:
        test_firebase_service()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
