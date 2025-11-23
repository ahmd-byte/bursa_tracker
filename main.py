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

# --- Load thresholds ---
with open('thresholds.json', 'r') as f:
    thresholds = json.load(f)

# --- Load config ---
with open('config.json', 'r') as f:
    config = json.load(f)

# --- CSV File for price history ---
CSV_FILE = 'history.csv'
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['Timestamp', 'Stock', 'Price'])
    df.to_csv(CSV_FILE, index=False)

# --- JSON file to track last alerts ---
ALERT_FILE = 'last_alerts.json'
if not os.path.exists(ALERT_FILE):
    with open(ALERT_FILE, 'w') as f:
        json.dump({}, f)

# --- Notification Functions ---
def send_email(subject, html_content):
    email_conf = config['email']
    msg = MIMEMultipart()
    msg['From'] = email_conf['email_address']
    msg['To'] = email_conf['email_address']
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(email_conf['smtp_server'], email_conf['smtp_port'])
        server.starttls()
        server.login(email_conf['email_address'], email_conf['password'])
        server.send_message(msg)
        server.quit()
        print(f"[Email] Alert sent: {subject}")
    except Exception as e:
        print(f"[Email] Failed to send alert: {e}")

def send_telegram(message):
    telegram_conf = config['telegram']
    url = f"https://api.telegram.org/bot{telegram_conf['bot_token']}/sendMessage"
    payload = {'chat_id': telegram_conf['chat_id'], 'text': message}
    try:
        requests.post(url, data=payload)
        print(f"[Telegram] Alert sent: {message}")
    except Exception as e:
        print(f"[Telegram] Failed to send alert: {e}")

# --- Helper to load/save last alerts ---
def load_last_alerts():
    with open(ALERT_FILE, 'r') as f:
        return json.load(f)

def save_last_alerts(data):
    with open(ALERT_FILE, 'w') as f:
        json.dump(data, f)

# --- Monitoring Function ---
def check_stocks():
    last_alerts = load_last_alerts()
    triggered_alerts = []

    for stock, limits in thresholds.items():
        ticker = yf.Ticker(stock)
        try:
            price = ticker.history(period="1d")['Close'].iloc[-1]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} | {stock} price: {price}")

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

            # Check last alert time (avoid duplicates within 1 hour)
            if alert_type:
                last_time_str = last_alerts.get(stock, {}).get(alert_type)
                send_now = True
                if last_time_str:
                    last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S')
                    if datetime.now() - last_time < timedelta(hours=1):
                        send_now = False  # skip alert if sent within 1 hour

                if send_now:
                    triggered_alerts.append({
                        'stock': stock,
                        'price': price,
                        'alert_type': alert_type,
                        'threshold': threshold_value
                    })
                    last_alerts.setdefault(stock, {})[alert_type] = timestamp

        except Exception as e:
            print(f"Failed to fetch {stock} price: {e}")

    # Save updated last alerts
    save_last_alerts(last_alerts)

    # Send one combined HTML email
    if triggered_alerts:
        html = "<h2 style='color:#2E86C1;'>Bursa Stock Alerts</h2>"
        html += "<table border='1' cellpadding='5' cellspacing='0'>"
        html += "<tr><th>Stock</th><th>Price</th><th>Alert</th><th>Threshold</th></tr>"
        for alert in triggered_alerts:
            color = "green" if alert['alert_type']=="UP" else "red"
            html += f"<tr><td>{alert['stock']}</td><td>{alert['price']}</td><td style='color:{color}'>{alert['alert_type']}</td><td>{alert['threshold']}</td></tr>"
        html += "</table>"
        html += f"<p>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"

        send_email("Bursa Stock Alerts", html)

        # Send Telegram messages individually
        for alert in triggered_alerts:
            message = f"{alert['stock']} price {alert['alert_type']} alert! Current: {alert['price']}, Threshold: {alert['threshold']}"
            send_telegram(message)

# --- Scheduler ---
schedule.every(5).minutes.do(check_stocks)

print("Bursa Stock Tracker started...")
check_stocks()  # Initial check

while True:
    schedule.run_pending()
    time.sleep(1)
