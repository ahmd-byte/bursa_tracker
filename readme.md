# 📈 Bursa Stock Tracker

A full-stack application for monitoring Malaysian stock prices (Bursa Malaysia) with real-time alerts via Email and Telegram.

## 🏗️ Project Structure

```
bursa_tracker/
├── backend/          # FastAPI backend with stock monitoring
│   ├── app/         # Application code
│   ├── data/        # CSV and JSON data files
│   ├── logs/        # Log files
│   ├── .venv/       # Python virtual environment
│   └── README.md    # Backend documentation
├── frontend/        # Frontend application (to be implemented)
└── README.md        # This file
```

## ✨ Features

### Backend
- **REST API**: FastAPI with auto-generated Swagger documentation
- **Real-time Monitoring**: Background task tracks multiple Malaysian stocks
- **Dual Notifications**: Email (HTML formatted) and Telegram alerts
- **Smart Alert Management**: Configurable cooldown periods
- **Data Persistence**: Historical price data saved to CSV
- **Robust Error Handling**: Retry logic with exponential backoff
- **Comprehensive Logging**: File and console logging with daily rotation

### Frontend (Coming Soon)
- Modern web interface for stock monitoring
- Real-time price updates
- Interactive charts and analytics
- Alert management dashboard

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend folder**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.template .env
   # Edit .env with your credentials
   ```

5. **Configure stock thresholds**
   Edit `thresholds.json`:
   ```json
   {
     "5285.KL": {"up": 10.50, "down": 9.80},
     "5335.KL": {"up": 5.00, "down": 4.50}
   }
   ```

6. **Run the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```

   Access the API at:
   - **API**: http://localhost:8000
   - **Swagger Docs**: http://localhost:8000/docs
   - **API Health**: http://localhost:8000/api/health

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/stocks` | GET | Get all monitored stocks |
| `/api/stocks/{symbol}` | GET | Get specific stock details |
| `/api/history` | GET | Get price history |
| `/api/alerts` | GET | Get recent alerts |
| `/api/thresholds` | GET | Get all thresholds |
| `/api/thresholds/{symbol}` | PUT | Update threshold |

See [backend/README.md](backend/README.md) for detailed API documentation.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend` folder:

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

### Stock Thresholds

Edit `backend/thresholds.json`:
- **Stock Symbol Format**: `[4-digit-code].KL` (e.g., `5285.KL`)
- **up**: Upper threshold - alert when price >= this value
- **down**: Lower threshold - alert when price <= this value

## 📧 Setting Up Notifications

### Gmail Setup
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Select "2-Step Verification"
   - Scroll to "App passwords"
   - Generate a new app password for "Mail"
3. Use this 16-character password in your `.env` file

### Telegram Setup
1. **Create a Telegram Bot**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy the Bot Token

2. **Get Your Chat ID**:
   - Message [@userinfobot](https://t.me/userinfobot)
   - Copy your Chat ID

3. **Add credentials to `.env`**

## 🛡️ Security Best Practices

- ✅ Never commit `.env` to version control
- ✅ Use environment variables for sensitive data
- ✅ Enable Gmail App Passwords instead of account password
- ✅ Regularly rotate your API tokens and passwords
- ✅ Review `.gitignore` to ensure sensitive files are excluded

## 🔧 Development

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
Coming soon...

## 📊 Data Management

### CSV History
- Price data is saved to `backend/data/history.csv`
- Automatic rotation when file exceeds `MAX_CSV_SIZE_MB`
- Backup files created with timestamp

### Alert Tracking
- Last alert times stored in `backend/data/last_alerts.json`
- Prevents duplicate alerts within cooldown period

### Logging
- Logs saved to `backend/logs/bursa_tracker_YYYYMMDD.log`
- Both file and console output
- Daily rotation

## 🐛 Troubleshooting

### Backend not starting
- Verify all dependencies are installed
- Check `.env` file exists and is configured
- Ensure `thresholds.json` exists

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

## 🚧 Roadmap

- [x] Backend API with FastAPI
- [x] Stock monitoring service
- [x] Email and Telegram notifications
- [x] REST API endpoints
- [ ] Frontend web application
- [ ] Real-time WebSocket updates
- [ ] User authentication
- [ ] Database integration
- [ ] Advanced charting and analytics

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Made with ❤️ for Bursa Malaysia traders**
