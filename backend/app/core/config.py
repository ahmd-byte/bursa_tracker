"""
Configuration management for Bursa Stock Tracker.
Loads settings from environment variables (.env file).
"""
import os
import json
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Get the backend directory path
BACKEND_DIR = Path(__file__).parent.parent.parent
ENV_PATH = BACKEND_DIR / '.env'

# Load environment variables from .env file
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    """Application configuration loaded from environment variables."""
    
    def __init__(self):
        self.email = self._load_email_config()
        self.telegram = self._load_telegram_config()
        self.monitor = self._load_monitor_config()
        self.thresholds = self._load_thresholds()
    
    def _load_email_config(self) -> Dict[str, Any]:
        """Load email configuration from environment variables."""
        return {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'email_address': os.getenv('EMAIL_ADDRESS', ''),
            'password': os.getenv('EMAIL_PASSWORD', '')
        }
    
    def _load_telegram_config(self) -> Dict[str, Any]:
        """Load Telegram configuration from environment variables."""
        return {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
            'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
        }
    
    def _load_monitor_config(self) -> Dict[str, Any]:
        """Load monitoring settings from environment variables."""
        return {
            'check_interval_minutes': int(os.getenv('CHECK_INTERVAL_MINUTES', '5')),
            'alert_cooldown_hours': int(os.getenv('ALERT_COOLDOWN_HOURS', '1')),
            'max_csv_size_mb': int(os.getenv('MAX_CSV_SIZE_MB', '10'))
        }
    
    def _load_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Load stock thresholds from thresholds.json."""
        thresholds_path = BACKEND_DIR / 'thresholds.json'
        try:
            with open(thresholds_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"thresholds.json not found at {thresholds_path}. Please create it with stock thresholds."
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in thresholds.json: {e}")
    
    def validate(self) -> None:
        """Validate that all required configuration is present."""
        errors = []
        
        if not self.email['email_address']:
            errors.append("EMAIL_ADDRESS not set in .env file")
        if not self.email['password']:
            errors.append("EMAIL_PASSWORD not set in .env file")
        if not self.telegram['bot_token']:
            errors.append("TELEGRAM_BOT_TOKEN not set in .env file")
        if not self.telegram['chat_id']:
            errors.append("TELEGRAM_CHAT_ID not set in .env file")
        if not self.thresholds:
            errors.append("No stock thresholds configured in thresholds.json")
        
        if errors:
            error_msg = "Configuration errors:\\n  - " + "\\n  - ".join(errors)
            error_msg += "\\n\\nPlease create a .env file from .env.template and fill in your credentials."
            raise ValueError(error_msg)


# Global config instance
config = Config()
