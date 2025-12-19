"""
Notification services for Bursa Stock Tracker.
Handles email and Telegram notifications.
"""
import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime

from app.core.config import config
from app.core.logger import setup_logger
from app.utils.helpers import format_price

logger = setup_logger()


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
        message = (f"🚨 {alert['stock']} {alert['alert_type']} Alert!\\n"
                  f"Current: RM {format_price(alert['price'])}\\n"
                  f"Threshold: RM {format_price(alert['threshold'])}")
        send_telegram(message)
