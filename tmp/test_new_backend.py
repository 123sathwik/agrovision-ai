import requests

print("Testing backend health...")
try:
    res = requests.get("http://127.0.0.1:8000/")
    print("Health Status Code:", res.status_code)
    print("Health Response:", res.json())
except Exception as e:
    print("Health check failed:", e)

print("\nTesting /analyze-crop fallback...")
try:
    # Send a dummy image to see if it gracefully fails inside with a fallback config
    with open(__file__, "rb") as f:
        res = requests.post("http://127.0.0.1:8000/analyze-crop", files={"image": ("dummy.jpg", f, "image/jpeg")})
    print("Analyze Crop Status Code:", res.status_code)
    import json
    print("Analyze Crop Response:", json.dumps(res.json(), indent=2))
except Exception as e:
    print("Fallback test failed:", e)
