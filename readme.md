# 📈 Bursa Stock Tracker

<div align="center">

![Bursa Stock Tracker](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)

**A modern, full-stack application for monitoring Malaysian stock prices (Bursa Malaysia) with real-time alerts via Email and Telegram.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [API Documentation](#-api-endpoints) • [Screenshots](#-screenshots)

</div>

---

## 🏗️ Project Structure

```
bursa_tracker/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # REST API routes
│   │   ├── core/           # Configuration & logging
│   │   ├── services/       # Business logic (monitoring, notifications)
│   │   └── utils/          # Helper functions
│   ├── data/               # CSV and JSON data files
│   ├── logs/               # Application logs
│   ├── .venv/              # Python virtual environment
│   ├── requirements.txt    # Python dependencies
│   └── thresholds.json     # Stock price thresholds
│
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   │   ├── ui/        # shadcn/ui base components
│   │   │   ├── StockCard.jsx
│   │   │   ├── StatsCard.jsx
│   │   │   └── LoadingSkeleton.jsx
│   │   ├── pages/         # Page components
│   │   │   └── Dashboard.jsx
│   │   ├── services/      # API service layer
│   │   │   └── api.js
│   │   ├── lib/           # Utilities
│   │   │   └── utils.js
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── public/            # Static assets
│   └── package.json       # Node dependencies
│
└── README.md              # This file
```

## ✨ Features

### Backend
- **REST API**: FastAPI with auto-generated Swagger documentation
- **Real-time Monitoring**: Background task tracks multiple Malaysian stocks
- **Dual Notifications**: Email (HTML formatted) and Telegram alerts
- **Smart Alert Management**: Configurable cooldown periods to prevent spam
- **Data Persistence**: Historical price data saved to CSV with automatic rotation
- **Robust Error Handling**: Retry logic with exponential backoff
- **Comprehensive Logging**: File and console logging with daily rotation

### Frontend
- **Modern UI**: Gen Z-friendly design with glassmorphism and soft gradients
- **Real-time Updates**: Auto-refresh every 5 minutes with manual refresh option
- **Interactive Cards**: Stock cards with hover effects and Framer Motion animations
- **Toast Notifications**: User feedback for all actions (loading, success, error)
- **Responsive Design**: Mobile-first approach, works on all devices
- **Loading States**: Skeleton loaders for smooth UX
- **Empty States**: Friendly messages when no data is available

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **FastAPI** | Modern web framework |
| **Uvicorn** | ASGI server |
| **yfinance** | Stock price data |
| **aiosmtplib** | Async email sending |
| **python-telegram-bot** | Telegram notifications |
| **Pydantic** | Data validation |
| **Schedule** | Task scheduling |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI library |
| **Vite** | Build tool & dev server |
| **Tailwind CSS** | Utility-first styling |
| **shadcn/ui** | Component library |
| **Framer Motion** | Animations |
| **react-hot-toast** | Toast notifications |
| **Axios** | HTTP client |
| **Lucide React** | Icon library |

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed
- **Node.js 18+** and npm installed
- Gmail account with App Password (for email alerts)
- Telegram Bot Token (for Telegram alerts)

### Backend Setup

1. **Navigate to backend folder**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.template .env
   # Edit .env with your credentials (see Configuration section)
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

   The API will be available at:
   - **API**: http://localhost:8000
   - **Swagger Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/api/health

### Frontend Setup

1. **Navigate to frontend folder**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment** (optional)
   
   Create `.env` file:
   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

   The frontend will be available at:
   - **App**: http://localhost:5173

### Access the Application

1. Start the backend server (port 8000)
2. Start the frontend dev server (port 5173)
3. Open http://localhost:5173 in your browser
4. View real-time stock prices and alerts!

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/stocks` | GET | Get all monitored stocks with current prices |
| `/api/stocks/{symbol}` | GET | Get specific stock details |
| `/api/history?limit=100` | GET | Get price history (default: 100 records) |
| `/api/alerts` | GET | Get recent alerts |
| `/api/thresholds` | GET | Get all thresholds |
| `/api/thresholds/{symbol}` | PUT | Update threshold (in-memory only) |

### Example API Response

**GET /api/stocks**
```json
[
  {
    "symbol": "5285.KL",
    "current_price": 10.25,
    "threshold_up": 10.50,
    "threshold_down": 9.80
  }
]
```

See [backend/README.md](backend/README.md) for detailed API documentation.

## ⚙️ Configuration

### Environment Variables (Backend)

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

## 🎨 Design Philosophy

The frontend follows modern Gen Z design principles:

- **Soft Gradients**: Slate → Indigo → Purple background
- **Glassmorphism**: Cards with backdrop blur and transparency
- **Rounded Corners**: 2xl-3xl border radius for softness
- **Micro-interactions**: Hover effects, smooth transitions, animations
- **Toast Notifications**: Every action provides user feedback
- **Responsive**: Mobile-first, desktop-polished

## 🛡️ Security Best Practices

- ✅ Never commit `.env` to version control
- ✅ Use environment variables for sensitive data
- ✅ Enable Gmail App Passwords instead of account password
- ✅ Regularly rotate your API tokens and passwords
- ✅ Review `.gitignore` to ensure sensitive files are excluded

##  Data Management

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
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check `.env` file exists and is configured
- Ensure `thresholds.json` exists

### Frontend not loading
- Verify Node.js 18+ is installed: `node --version`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if backend is running on port 8000

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
- [x] Frontend web application with React
- [x] Real-time price updates
- [x] Responsive design
- [ ] User authentication & authorization
- [ ] Database integration (PostgreSQL)
- [ ] WebSocket for real-time updates
- [ ] Advanced charting with historical data
- [ ] Portfolio management
- [ ] Custom alert rules engine
- [ ] Mobile app (React Native)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

For questions or support, please open an issue in the repository.

---

<div align="center">

**Made with ❤️ for Bursa Malaysia traders**

⭐ Star this repo if you find it helpful!

</div>
