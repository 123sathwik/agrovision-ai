"""
Verification script for services/soil_analysis.py.
Tests rule-based logic and fallback behaviors.
"""
from services.soil_analysis import get_soil_analysis

def test_soil_analysis_logic():
    print("=== Verifying Soil Analysis Service Logic ===\n")
    
    # 1. Test Exact Match
    print("[*] Testing Tomato Late Blight...")
    tomato_blight = get_soil_analysis("Tomato", "Tomato___Late_blight")
    assert tomato_blight["NPK_ratio"] == "10-26-26"
    assert "DAP" in tomato_blight["fertilizers"]
    print("[+] Tomato Late Blight: OK")

    # 2. Test Tuber/Specific Match
    print("[*] Testing Potato Healthy...")
    potato_healthy = get_soil_analysis("Potato", "Potato___healthy")
    assert potato_healthy["NPK_ratio"] == "15-15-15"
    print("[+] Potato Healthy: OK")

    # 3. Test Generic Fallback
    print("[*] Testing Generic Blight (Apple)...")
    apple_blight = get_soil_analysis("Apple", "Apple___Late_blight")
    assert apple_blight["NPK_ratio"] == "5-15-15"
    print("[+] Generic Blight (Apple): OK")

    # 4. Test Default Fallback
    print("[*] Testing Unknown Pair (Watermelon Frost)...")
    unknown = get_soil_analysis("Watermelon", "Frost")
    assert unknown["NPK_ratio"] == "10-10-10"
    print("[+] Unknown Pair: OK")

    print("\n[SUCCESS] Soil Analysis Service verified!")

if __name__ == "__main__":
    try:
        test_soil_analysis_logic()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
