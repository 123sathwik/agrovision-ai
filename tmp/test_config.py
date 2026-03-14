"""
Verification script for app/config.py.
Verifies that environment variables are loaded correctly (even if they are dummy values).
"""
import os
from unittest.mock import patch
from app.config import get_env_variable

def test_config_loading():
    print("=== Verifying Configuration Loading ===\n")
    
    # Mocking environment variables
    test_env = {
        "TEST_VAR": "LoadedSuccessfully"
    }
    
    with patch.dict(os.environ, test_env):
        print("[*] Testing get_env_variable...")
        assert get_env_variable("TEST_VAR") == "LoadedSuccessfully"
        print("[+] get_env_variable: OK")
        
        try:
            get_env_variable("MISSING_VAR")
        except ValueError as e:
            print(f"[+] Error raising for missing var: OK ({e})")
        else:
            raise AssertionError("Should have raised ValueError for missing variable")

    print("\n[SUCCESS] Configuration management logic verified!")

if __name__ == "__main__":
    try:
        test_config_loading()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        exit(1)
