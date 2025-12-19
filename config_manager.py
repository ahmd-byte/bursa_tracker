"""
Configuration management for Bursa Stock Tracker.
Loads settings from environment variables and JSON files.
"""
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration with environment variable support."""
    
    def __init__(self):
        self.email = self._load_email_config()
        self.telegram = self._load_telegram_config()
        self.monitor = self._load_monitor_config()
        self.thresholds = self._load_thresholds()
    
    def _load_email_config(self) -> Dict[str, Any]:
        """Load email configuration from environment or config.json."""
        return {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
            'email_address': os.getenv('EMAIL_ADDRESS', self._get_from_json('email', 'email_address')),
            'password': os.getenv('EMAIL_PASSWORD', self._get_from_json('email', 'password'))
        }
    
    def _load_telegram_config(self) -> Dict[str, Any]:
        """Load Telegram configuration from environment or config.json."""
        return {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', self._get_from_json('telegram', 'bot_token')),
            'chat_id': os.getenv('TELEGRAM_CHAT_ID', self._get_from_json('telegram', 'chat_id'))
        }
    
    def _load_monitor_config(self) -> Dict[str, Any]:
        """Load monitoring settings from environment variables."""
        return {
            'check_interval_minutes': int(os.getenv('CHECK_INTERVAL_MINUTES', 5)),
            'alert_cooldown_hours': int(os.getenv('ALERT_COOLDOWN_HOURS', 1)),
            'max_csv_size_mb': int(os.getenv('MAX_CSV_SIZE_MB', 10))
        }
    
    def _load_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Load stock thresholds from thresholds.json."""
        try:
            with open('thresholds.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("thresholds.json not found. Please create it with stock thresholds.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in thresholds.json: {e}")
    
    def _get_from_json(self, section: str, key: str) -> str:
        """Fallback to config.json if environment variable not set."""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                return config.get(section, {}).get(key, '')
        except (FileNotFoundError, json.JSONDecodeError):
            return ''
    
    def validate(self) -> None:
        """Validate that all required configuration is present."""
        errors = []
        
        if not self.email['email_address']:
            errors.append("Email address not configured")
        if not self.email['password']:
            errors.append("Email password not configured")
        if not self.telegram['bot_token']:
            errors.append("Telegram bot token not configured")
        if not self.telegram['chat_id']:
            errors.append("Telegram chat ID not configured")
        if not self.thresholds:
            errors.append("No stock thresholds configured")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
