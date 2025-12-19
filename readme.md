# 📈 Bursa Stock Tracker

A robust Python application that monitors Malaysian stock prices (Bursa Malaysia) and sends real-time alerts via Email and Telegram when price thresholds are breached.

## ✨ Features

- **Real-time Monitoring**: Tracks multiple Malaysian stocks simultaneously
- **Dual Notification System**: Alerts via Email (HTML formatted) and Telegram
- **Smart Alert Management**: Configurable cooldown periods to prevent alert spam
- **Data Persistence**: Historical price data saved to CSV with automatic rotation
- **Robust Error Handling**: Retry logic with exponential backoff for network operations
- **Flexible Configuration**: Environment variables and JSON-based configuration
- **Comprehensive Logging**: File and console logging with daily rotation

## 📋 Prerequisites

- Python 3.8 or higher
- Gmail account (for email notifications) with App Password enabled
- Telegram Bot Token and Chat ID (for Telegram notifications)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bursa_tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### 1. Environment Variables (Recommended)

Create a `.env` file in the project root:

```bash
cp .env.template .env
```

Edit `.env` with your credentials:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password_here

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Monitor Settings
CHECK_INTERVAL_MINUTES=5
ALERT_COOLDOWN_HOURS=1
MAX_CSV_SIZE_MB=10
```

### 2. Stock Thresholds

Edit `thresholds.json` to configure which stocks to monitor:

```json
{
  "5285.KL": {"up": 10.50, "down": 9.80},
  "5335.KL": {"up": 5.00, "down": 4.50},
  "1155.KL": {"up": 3.20, "down": 2.90}
}
```

- **Stock Symbol Format**: `[4-digit-code].KL` (e.g., `5285.KL`)
- **up**: Upper threshold - alert when price >= this value
- **down**: Lower threshold - alert when price <= this value

## 🎯 Usage

### Run the Stock Tracker

```bash
python main.py
```

The application will:
1. Load configuration and validate settings
2. Perform an initial stock price check
3. Continue monitoring at configured intervals
4. Send alerts when thresholds are breached
5. Log all activities to `logs/` directory

### Stop the Application

Press `Ctrl+C` to gracefully shutdown

## 📁 Project Structure

```
bursa_tracker/
├── main.py                 # Main application entry point
├── config_manager.py       # Configuration management
├── logger.py              # Logging setup
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── thresholds.json        # Stock price thresholds
├── .env                   # Environment variables (create from template)
├── .env.template          # Environment variables template
├── history.csv            # Price history (auto-generated)
├── last_alerts.json       # Alert tracking (auto-generated)
└── logs/                  # Log files (auto-generated)
```

## 🔧 Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `CHECK_INTERVAL_MINUTES` | 5 | How often to check stock prices |
| `ALERT_COOLDOWN_HOURS` | 1 | Minimum time between duplicate alerts |
| `MAX_CSV_SIZE_MB` | 10 | Max CSV size before rotation |

## 📧 Setting Up Email Notifications

### Gmail Setup

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Select "2-Step Verification"
   - Scroll to "App passwords"
   - Generate a new app password for "Mail"
3. Use this 16-character password in your `.env` file

## 🤖 Setting Up Telegram Notifications

1. **Create a Telegram Bot**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy the Bot Token

2. **Get Your Chat ID**:
   - Message [@userinfobot](https://t.me/userinfobot)
   - Copy your Chat ID

3. **Add credentials to `.env`**

## 📊 Data Management

### CSV History

- Price data is saved to `history.csv`
- Automatic rotation when file exceeds `MAX_CSV_SIZE_MB`
- Backup files created with timestamp: `history_backup_YYYYMMDD_HHMMSS.csv`

### Alert Tracking

- Last alert times stored in `last_alerts.json`
- Prevents duplicate alerts within cooldown period
- Automatically managed by the application

## 🔍 Logging

Logs are saved to `logs/bursa_tracker_YYYYMMDD.log` with:
- Timestamp for each event
- Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Detailed error messages with stack traces
- Both file and console output

## 🛡️ Security Best Practices

- ✅ Never commit `.env` to version control
- ✅ Use environment variables for sensitive data
- ✅ Enable Gmail App Passwords instead of account password
- ✅ Regularly rotate your API tokens and passwords
- ✅ Review `.gitignore` to ensure sensitive files are excluded

## 🐛 Troubleshooting

### Email not sending
- Verify Gmail App Password is correct
- Check if 2FA is enabled on Google account
- Review logs for specific error messages

### Telegram not working
- Verify Bot Token and Chat ID are correct
- Ensure you've started a conversation with your bot
- Check network connectivity

### Stock data not updating
- Verify stock symbols are in correct format (`XXXX.KL`)
- Check internet connection
- Review logs for API errors from yfinance

### Configuration errors
- Run `python main.py` and check error messages
- Validate JSON syntax in `thresholds.json`
- Ensure all required environment variables are set

## 🚧 Upcoming Features (FastAPI Backend)

The next phase will include:
- RESTful API with FastAPI
- Web-based dashboard
- User authentication
- Real-time WebSocket updates
- Database integration (PostgreSQL/SQLite)
- API documentation with Swagger UI


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Made with ❤️ for Bursa Malaysia traders**
