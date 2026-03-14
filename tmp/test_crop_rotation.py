"""
Verification script for services/crop_rotation.py.
Tests plant family logic and disease-breaking recommendations.
"""
from services.crop_rotation import get_rotation_recommendation

def test_crop_rotation_logic():
    print("=== Verifying Crop Rotation Service Logic ===\n")
    
    # 1. Test Fungal Break (Tomato -> Maize)
    print("[*] Testing Tomato Late Blight...")
    tomato_blight = get_rotation_recommendation("Tomato", "Tomato___Late_blight")
    assert tomato_blight["recommended_crop"] == "Maize (Corn)"
    assert "Breaks" in tomato_blight["reason"]
    print("[+] Tomato Late Blight -> Maize: OK")

    # 2. Test Legume Shift (Corn -> Soybeans/Beans)
    print("[*] Testing Corn Rust...")
    corn_rust = get_rotation_recommendation("Corn", "Corn___Common_rust")
    assert "Bean" in corn_rust["recommended_crop"]
    print("[+] Corn Rust -> Beans: OK")

    # 3. Test Cereal Shift (Soybeans -> Wheat/Corn)
    print("[*] Testing Beans Healthy...")
    beans_healthy = get_rotation_recommendation("Beans", "Healthy")
    assert "Corn" in beans_healthy["recommended_crop"]
    print("[+] Beans Healthy -> Corn: OK")

    # 4. Test Fallback
    print("[*] Testing Unknown Crop (Healthy)...")
    unknown = get_rotation_recommendation("Dragonfruit", "Healthy")
    # Logic 2 triggers for "Healthy", recommending Green Beans
    assert "Bean" in unknown["recommended_crop"]
    print("[+] Unknown Crop (Healthy) -> Green Beans: OK")

    # 5. Test Pure Fallback (No logic 1 or 2 trigger)
    print("[*] Testing Unknown Crop (Unknown Disease)...")
    pure_fallback = get_rotation_recommendation("Dragonfruit", "Unknown Problem")
    assert pure_fallback["recommended_crop"] == "Clover"
    print("[+] Unknown Crop (Unknown Disease) -> Clover: OK")

    print("\n[SUCCESS] Crop Rotation Service verified!")

if __name__ == "__main__":
    try:
        test_crop_rotation_logic()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
