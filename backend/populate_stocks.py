import json
import requests
import sys

# Popular Bursa Malaysia stocks
NEW_STOCKS = {
    "1155.KL": {"up": 10.00, "down": 8.50},   # Maybank
    "1023.KL": {"up": 6.00, "down": 5.00},    # CIMB
    "1295.KL": {"up": 4.50, "down": 3.80},    # Public Bank
    "5347.KL": {"up": 11.00, "down": 9.50},   # Tenaga
    "5183.KL": {"up": 7.50, "down": 6.80},    # Petronas Chem
    "5225.KL": {"up": 6.20, "down": 5.50},    # IHH Healthcare
    "6033.KL": {"up": 18.00, "down": 16.50},  # Petronas Gas
    "2445.KL": {"up": 22.00, "down": 20.00},  # KLK
    "4707.KL": {"up": 120.00, "down": 110.00},# Nestle (Expensive!)
    "7113.KL": {"up": 1.20, "down": 0.80}     # Top Glove (Penny stock example)
}

def update_file():
    """Update thresholds.json file for persistence."""
    try:
        with open('thresholds.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Merge new stocks
    data.update(NEW_STOCKS)

    with open('thresholds.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Updated thresholds.json with {len(NEW_STOCKS)} new stocks.")

def hot_load_stocks():
    """Inject stocks into running backend via API."""
    base_url = "http://localhost:8000/api/thresholds"
    
    print("Hot-loading stocks into running backend...")
    
    for symbol, thresholds in NEW_STOCKS.items():
        try:
            response = requests.put(
                f"{base_url}/{symbol}",
                json=thresholds
            )
            response.raise_for_status()
            print(f"  [+] Added {symbol}")
        except requests.exceptions.ConnectionError:
            print(f"  [-] Failed to connect to backend. Is it running?")
            return False
        except Exception as e:
            print(f"  [-] Failed to add {symbol}: {e}")
    
    print("Done hot-loading.")
    return True

if __name__ == "__main__":
    update_file()
    success = hot_load_stocks()
    if not success:
        print("\nNOTE: Backend seems down. Stocks will be loaded when you start it next time.")
