import json
import requests
import time

# FTSE Bursa Malaysia Top 100 Constituents (KLCI + Mid 70)
# Sources: Bursa Malaysia, TradingView
STOCK_CODES = [
    # KLCI Top 30
    "5326", "1015", "6888", "6947", "1023", "5398", "3182", "4715", "5819", "1082", 
    "5225", "1961", "2445", "1155", "6012", "3816", "5296", "4707", "5183", "5681", 
    "6033", "4065", "8869", "1295", "7084", "1066", "5285", "4197", "5211", "4863", 
    "5347", "4677", "6742",
    # Mid 70 (Partial Selection)
    "5139", "5185", "2488", "1163", "6399", "5106", "5258", "5248", "4162", "5210", 
    "1818", "2852", "2836", "5273", "5301", "7204", "4456", "5141", "7277", "1619", 
    "7233", "7148", "5318", "8206", "5306", "5222", "3689", "0128", "5209", "0078", 
    "2291", "0021", "0208", "5102", "5168", "3255", "3301", "0041", "3336", "5208", 
    "7153", "5878", "6633", "5284", "3859", "5014", "1171", "3867", "1651", "5236", 
    "3069", "5286", "0138", "7052", "7160", "9822", "5288", "5031", "2089", "5246"
]

# Clean and format codes
FORMATTED_STOCKS = {}
for code in STOCK_CODES:
    # Ensure 4 digits for int-like strings (e.g. "128" -> "0128")
    # But some data sources strip leading zeros. I assume the list above is mixed.
    # I'll rely on the string provided, but append .KL
    # Wait, "128" is Frontken? Yes. "78" is GDEX.
    # yfinance often needs "0128.KL".
    # I'll try to pad them to 4 digits if length < 4.
    
    clean_code = code.strip()
    if len(clean_code) < 4:
        clean_code = clean_code.zfill(4)
        
    symbol = f"{clean_code}.KL"
    
    # Generic thresholds (Wide range to avoid immediate alerts)
    FORMATTED_STOCKS[symbol] = {"up": 9999.00, "down": 0.01}

def update_file():
    """Update thresholds.json file for persistence."""
    try:
        with open('thresholds.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Merge new stocks
    data.update(FORMATTED_STOCKS)

    with open('thresholds.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Updated thresholds.json with {len(FORMATTED_STOCKS)} new stocks.")

def hot_load_stocks():
    """Inject stocks into running backend via API."""
    base_url = "http://localhost:8000/api/thresholds"
    
    print(f"Hot-loading {len(FORMATTED_STOCKS)} stocks into running backend...")
    
    count = 0
    for symbol, thresholds in FORMATTED_STOCKS.items():
        try:
            # We don't want to spam requests too fast, backend might choke?
            # It's local, should be fast. But let's verify.
            response = requests.put(
                f"{base_url}/{symbol}",
                json=thresholds
            )
            if response.status_code == 200:
                print(f"  [+] Added {symbol}")
                count += 1
            else:
                print(f"  [-] Failed {symbol}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"  [-] Connection error for {symbol}")
        except Exception as e:
            print(f"  [-] Error {symbol}: {e}")
            
    print(f"Done. Successfully loaded {count} stocks.")

if __name__ == "__main__":
    update_file()
    hot_load_stocks()
