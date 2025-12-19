"""
Stock monitoring service for Bursa Stock Tracker.
Handles stock price fetching, threshold checking, and alert triggering.
"""
import yfinance as yf
import pandas as pd
import json
from typing import Dict, List
from datetime import datetime, timedelta
from pathlib import Path

from app.core.config import config
from app.core.logger import setup_logger
from app.utils.helpers import validate_stock_symbol, validate_threshold, rotate_csv_file, format_price
from app.services.notifications import send_notifications

logger = setup_logger()

# File paths
BACKEND_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BACKEND_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

CSV_FILE = DATA_DIR / 'history.csv'
ALERT_FILE = DATA_DIR / 'last_alerts.json'

# Initialize files
if not CSV_FILE.exists():
    df = pd.DataFrame(columns=['Timestamp', 'Stock', 'Price'])
    df.to_csv(CSV_FILE, index=False)
    logger.info(f"Created new CSV file: {CSV_FILE}")

if not ALERT_FILE.exists():
    with open(ALERT_FILE, 'w') as f:
        json.dump({}, f)
    logger.info(f"Created new alert tracking file: {ALERT_FILE}")


def load_last_alerts() -> Dict:
    """Load last alert timestamps from file."""
    try:
        with open(ALERT_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading alerts file: {e}")
        return {}


def save_last_alerts(data: Dict) -> None:
    """Save last alert timestamps to file."""
    try:
        with open(ALERT_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving alerts file: {e}")


def should_send_alert(stock: str, alert_type: str, last_alerts: Dict) -> bool:
    """
    Check if alert should be sent based on cooldown period.
    
    Args:
        stock: Stock symbol
        alert_type: Alert type (UP or DOWN)
        last_alerts: Dictionary of last alert times
    
    Returns:
        True if alert should be sent, False otherwise
    """
    last_time_str = last_alerts.get(stock, {}).get(alert_type)
    if not last_time_str:
        return True
    
    try:
        last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
        cooldown_hours = config.monitor['alert_cooldown_hours']
        if datetime.now() - last_time < timedelta(hours=cooldown_hours):
            logger.debug(f"Alert for {stock} {alert_type} skipped (cooldown period)")
            return False
    except ValueError as e:
        logger.warning(f"Invalid timestamp format for {stock}: {e}")
    
    return True


def get_stock_price(stock: str) -> float:
    """
    Fetch current stock price from Yahoo Finance.
    
    Args:
        stock: Stock symbol
    
    Returns:
        Current stock price
    
    Raises:
        Exception: If unable to fetch price
    """
    ticker = yf.Ticker(stock)
    history = ticker.history(period="1d")
    if history.empty:
        raise ValueError(f"No data available for {stock}")
    return history['Close'].iloc[-1]


def get_all_stock_prices() -> Dict[str, float]:
    """
    Fetch current prices for all monitored stocks.
    
    Returns:
        Dictionary mapping stock symbols to current prices
    """
    prices = {}
    for stock in config.thresholds.keys():
        try:
            if validate_stock_symbol(stock):
                prices[stock] = get_stock_price(stock)
        except Exception as e:
            logger.error(f"Failed to fetch {stock} price: {e}")
    return prices


def get_price_history(limit: int = 100) -> List[Dict]:
    """
    Get price history from CSV file.
    
    Args:
        limit: Maximum number of records to return
    
    Returns:
        List of price history records
    """
    try:
        if CSV_FILE.exists():
            df = pd.read_csv(CSV_FILE)
            # Get last N records
            df = df.tail(limit)
            return df.to_dict('records')
        return []
    except Exception as e:
        logger.error(f"Error reading price history: {e}")
        return []


def check_stocks() -> None:
    """
    Check stock prices and send alerts if thresholds are breached.
    """
    logger.info("Starting stock price check...")
    
    # Rotate CSV if needed
    rotate_csv_file(CSV_FILE, config.monitor['max_csv_size_mb'])
    
    last_alerts = load_last_alerts()
    triggered_alerts = []

    for stock, limits in config.thresholds.items():
        # Validate stock symbol
        if not validate_stock_symbol(stock):
            logger.warning(f"Invalid stock symbol: {stock}")
            continue
        
        # Validate threshold
        if not validate_threshold(limits):
            logger.warning(f"Invalid threshold for {stock}: {limits}")
            continue
        
        try:
            price = get_stock_price(stock)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"{stock} price: {format_price(price)}")

            # Save to CSV
            df = pd.DataFrame([[timestamp, stock, price]], columns=['Timestamp', 'Stock', 'Price'])
            df.to_csv(CSV_FILE, mode='a', header=False, index=False)

            # Determine alert type
            alert_type = None
            threshold_value = None
            if price >= limits['up']:
                alert_type = "UP"
                threshold_value = limits['up']
            elif price <= limits['down']:
                alert_type = "DOWN"
                threshold_value = limits['down']

            # Check if alert should be sent
            if alert_type and should_send_alert(stock, alert_type, last_alerts):
                triggered_alerts.append({
                    'stock': stock,
                    'price': price,
                    'alert_type': alert_type,
                    'threshold': threshold_value
                })
                last_alerts.setdefault(stock, {})[alert_type] = timestamp
                logger.info(f"Alert triggered for {stock}: {alert_type} at {format_price(price)}")

        except Exception as e:
            logger.error(f"Failed to fetch {stock} price: {e}")

    # Save updated last alerts
    save_last_alerts(last_alerts)

    # Send notifications if there are triggered alerts
    if triggered_alerts:
        send_notifications(triggered_alerts)
    else:
        logger.info("No alerts triggered")
