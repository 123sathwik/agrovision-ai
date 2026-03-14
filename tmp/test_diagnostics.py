import requests

print("Testing backend analysis...")
try:
    with open(__file__, "rb") as f:
        res = requests.post("http://127.0.0.1:8000/analyze-crop", files={"image": ("dummy.jpg", f, "image/jpeg")})
    print("Analyze Crop Status Code:", res.status_code)
    import json
    print("Analyze Crop Response:", json.dumps(res.json(), indent=2))
except Exception as e:
    print("Analysis test failed:", e)
