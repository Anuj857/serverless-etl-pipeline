import os
import json
import requests

# Ensure the sample_data directory exists
os.makedirs("sample_data", exist_ok=True)

def fetch_and_save(api_name, url, filename):
    print(f"Fetching {api_name} data...")
    
    # We add this header to mimic a standard Google Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Pass the headers into the get request
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        data = response.json()
        
        filepath = os.path.join("sample_data", filename)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            
        print(f"  ✅ Successfully saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Failed to fetch {api_name} data. Error: {e}")

if __name__ == "__main__":
    print("--- Starting Data Extraction ---\n")
    
    # 1. Weather API (Open-Meteo)
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=26.9124&longitude=75.7873&current_weather=true"
    fetch_and_save("Weather", weather_url, "sample_weather.json")
    
    # 2. Earthquake API (USGS)
    earthquake_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    fetch_and_save("Earthquake", earthquake_url, "sample_earthquake.json")
    
    # 3. E-commerce Products API (DummyJSON)
    products_url = "https://dummyjson.com/products?limit=5"
    fetch_and_save("Products", products_url, "sample_products.json")
    
    print("\n--- Data Extraction Complete ---")