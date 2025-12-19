# 📈 Bursa Stock Tracker - Backend API

FastAPI backend for monitoring Malaysian stock prices (Bursa Malaysia) with real-time alerts via Email and Telegram.

## ✨ Features

- **REST API**: Full-featured API for frontend connectivity
- **Real-time Monitoring**: Background task tracks multiple Malaysian stocks
- **Dual Notifications**: Email (HTML) and Telegram alerts
- **Smart Alerts**: Configurable cooldown periods
- **Data Persistence**: Historical price data in CSV
- **API Documentation**: Auto-generated Swagger UI at `/docs`

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.template .env
# Edit .env with your credentials
```

### 4. Configure Stock Thresholds

Edit `thresholds.json`:
```json
{
  "5285.KL": {"up": 10.50, "down": 9.80},
  "5335.KL": {"up": 5.00, "down": 4.50}
}
```

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Get All Stocks
```
GET /api/stocks
```
Returns all monitored stocks with current prices and thresholds.

### Get Specific Stock
```
GET /api/stocks/{symbol}
```
Example: `GET /api/stocks/5285.KL`

### Get Price History
```
GET /api/history?limit=100
```

### Get Recent Alerts
```
GET /api/alerts
```

### Get Thresholds
```
GET /api/thresholds
```

### Update Threshold (In-Memory)
```
PUT /api/thresholds/{symbol}
Body: {"up": 10.50, "down": 9.80}
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── logger.py        # Logging
│   ├── services/
│   │   ├── stock_monitor.py # Stock monitoring
│   │   └── notifications.py # Email/Telegram
│   ├── utils/
│   │   └── helpers.py       # Utility functions
│   └── main.py              # FastAPI app
├── data/                    # CSV and JSON data
├── logs/                    # Log files
├── .venv/                   # Virtual environment
├── .env                     # Environment variables
├── thresholds.json          # Stock thresholds
└── requirements.txt         # Dependencies
```

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_SERVER` | Email SMTP server | smtp.gmail.com |
| `SMTP_PORT` | SMTP port | 587 |
| `EMAIL_ADDRESS` | Your email address | - |
| `EMAIL_PASSWORD` | Email app password | - |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | - |
| `TELEGRAM_CHAT_ID` | Telegram chat ID | - |
| `CHECK_INTERVAL_MINUTES` | Monitoring interval | 5 |
| `ALERT_COOLDOWN_HOURS` | Alert cooldown | 1 |
| `MAX_CSV_SIZE_MB` | Max CSV size | 10 |

## 🔧 Development

### Run with Auto-Reload
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run in Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 CORS Configuration

CORS is enabled for all origins by default. For production, update `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Notes

- Background monitoring runs automatically when the server starts
- Stock prices are fetched from Yahoo Finance API
- Price history is saved to `data/history.csv`
- Alert tracking is saved to `data/last_alerts.json`
- Logs are saved to `logs/bursa_tracker_YYYYMMDD.log`

## 🔗 Frontend Integration

The backend is ready to connect with any frontend framework. Use the API endpoints to:
1. Fetch current stock prices
2. Display price history
3. Show recent alerts
4. Update thresholds

Example fetch from frontend:
```javascript
const response = await fetch('http://localhost:8000/api/stocks');
const stocks = await response.json();
```
