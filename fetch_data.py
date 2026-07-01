import os
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. Setup session with retry logic
def get_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    return session

# 2. Fetch function
def fetch_and_save(session, filename, url):
    print(f"Fetching {filename}...")
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        
        filepath = os.path.join("sample_data", filename)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(response.json(), file, indent=4)
        print(f"  ✅ Saved: {filepath}")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {filename} | Error: {e}")
        return False

# 3. Execution
if __name__ == "__main__":
    os.makedirs("sample_data", exist_ok=True)
    session = get_session()

    # The 3 APIs used in our project
    apis = {
        "sample_earthquake.json": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
        "sample_weather.json": "https://api.open-meteo.com/v1/forecast?latitude=26.91&longitude=75.79&current=temperature_2m,wind_speed_10m",
        "sample_products.json": "https://dummyjson.com/products?limit=5"
    }

    print("=" * 60)
    print("Fetching Project-Specific Datasets")
    print("=" * 60)

    for filename, url in apis.items():
        success = fetch_and_save(session, filename, url)
        
        # Fallback for Earthquake if USGS blocks the connection
        if not success and "earthquake" in filename:
            print("  ⚠️ Using local mock data fallback for Earthquake pipeline.")
            with open(os.path.join("sample_data", filename), "w") as f:
                json.dump({"features": [{"id": "mock-001", "properties": {"mag": 5.0, "place": "Jaipur"}}]}, f)

    print("\nExtraction Complete! Files are ready in the 'sample_data' folder.")