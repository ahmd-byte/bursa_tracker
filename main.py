"""
Bursa Stock Tracker - Enhanced Version
Monitors Malaysian stock prices and sends alerts via email and Telegram.
"""
import yfinance as yf
import schedule
import time
import pandas as pd
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional

# Import custom modules
from config_manager import Config
from logger import setup_logger
from utils import validate_stock_symbol, validate_threshold, rotate_csv_file, format_price

# Setup logger
logger = setup_logger()

# --- Constants ---
CSV_FILE = 'history.csv'
ALERT_FILE = 'last_alerts.json'

# --- Initialize Configuration ---
try:
    config = Config()
    config.validate()
    logger.info("Configuration loaded and validated successfully")
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise

# --- Initialize CSV File ---
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['Timestamp', 'Stock', 'Price'])
    df.to_csv(CSV_FILE, index=False)
    logger.info(f"Created new CSV file: {CSV_FILE}")

# --- Initialize Alert Tracking File ---
if not os.path.exists(ALERT_FILE):
    with open(ALERT_FILE, 'w') as f:
        json.dump({}, f)
    logger.info(f"Created new alert tracking file: {ALERT_FILE}")


# --- Notification Functions ---
def send_email(subject: str, html_content: str) -> bool:
    """
    Send email notification.
    
    Args:
        subject: Email subject
        html_content: HTML email body
    
    Returns:
        True if successful, False otherwise
    """
    email_conf = config.email
    msg = MIMEMultipart()
    msg['From'] = email_conf['email_address']
    msg['To'] = email_conf['email_address']
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    max_retries = 3
    for attempt in range(max_retries):
        try:
            server = smtplib.SMTP(email_conf['smtp_server'], email_conf['smtp_port'])
            server.starttls()
            server.login(email_conf['email_address'], email_conf['password'])
            server.send_message(msg)
            server.quit()
            logger.info(f"Email sent successfully: {subject}")
            return True
        except Exception as e:
            logger.warning(f"Email send attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to send email after {max_retries} attempts")
                return False


def send_telegram(message: str) -> bool:
    """
    Send Telegram notification.
    
    Args:
        message: Message text
    
    Returns:
        True if successful, False otherwise
    """
    telegram_conf = config.telegram
    url = f"https://api.telegram.org/bot{telegram_conf['bot_token']}/sendMessage"
    payload = {'chat_id': telegram_conf['chat_id'], 'text': message}
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Telegram message sent: {message[:50]}...")
            return True
        except Exception as e:
            logger.warning(f"Telegram send attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to send Telegram message after {max_retries} attempts")
                return False


# --- Helper Functions ---
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


# --- Main Monitoring Function ---
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
        
        ticker = yf.Ticker(stock)
        try:
            history = ticker.history(period="1d")
            if history.empty:
                logger.warning(f"No data available for {stock}")
                continue
            
            price = history['Close'].iloc[-1]
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


def send_notifications(triggered_alerts: List[Dict]) -> None:
    """
    Send email and Telegram notifications for triggered alerts.
    
    Args:
        triggered_alerts: List of alert dictionaries
    """
    # Build HTML email
    html = "<h2 style='color:#2E86C1;'>Bursa Stock Alerts</h2>"
    html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse;'>"
    html += "<tr style='background-color:#f0f0f0;'><th>Stock</th><th>Price</th><th>Alert</th><th>Threshold</th></tr>"
    
    for alert in triggered_alerts:
        color = "green" if alert['alert_type'] == "UP" else "red"
        html += f"<tr><td>{alert['stock']}</td><td>{format_price(alert['price'])}</td>"
        html += f"<td style='color:{color}; font-weight:bold;'>{alert['alert_type']}</td>"
        html += f"<td>{format_price(alert['threshold'])}</td></tr>"
    
    html += "</table>"
    html += f"<p style='color:#666; font-size:12px;'>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"

    # Send email
    send_email("Bursa Stock Alerts", html)

    # Send Telegram messages
    for alert in triggered_alerts:
        message = (f"🚨 {alert['stock']} {alert['alert_type']} Alert!\n"
                  f"Current: RM {format_price(alert['price'])}\n"
                  f"Threshold: RM {format_price(alert['threshold'])}")
        send_telegram(message)


# --- Scheduler Setup ---
def main():
    """Main application entry point."""
    logger.info("=" * 60)
    logger.info("Bursa Stock Tracker Started")
    logger.info("=" * 60)
    logger.info(f"Monitoring {len(config.thresholds)} stocks")
    logger.info(f"Check interval: {config.monitor['check_interval_minutes']} minutes")
    logger.info(f"Alert cooldown: {config.monitor['alert_cooldown_hours']} hour(s)")
    logger.info("=" * 60)
    
    # Schedule periodic checks
    interval = config.monitor['check_interval_minutes']
    schedule.every(interval).minutes.do(check_stocks)
    
    # Initial check
    check_stocks()
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
