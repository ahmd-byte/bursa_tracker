"""
FastAPI application for Bursa Stock Tracker.
Provides REST API for frontend connectivity and runs background stock monitoring.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import schedule
import time

from app.api.routes import router
from app.core.config import config
from app.core.logger import setup_logger
from app.services.stock_monitor import check_stocks

logger = setup_logger()

# Background task flag
monitoring_task = None
should_monitor = True


async def run_monitoring():
    """Background task to run stock monitoring."""
    global should_monitor
    
    # Schedule periodic checks
    interval = config.monitor['check_interval_minutes']
    schedule.every(interval).minutes.do(check_stocks)
    
    # Initial check
    check_stocks()
    
    logger.info(f"Stock monitoring started (interval: {interval} minutes)")
    
    # Run scheduled tasks
    while should_monitor:
        schedule.run_pending()
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    global monitoring_task, should_monitor
    
    # Startup
    logger.info("=" * 60)
    logger.info("Bursa Stock Tracker API Starting")
    logger.info("=" * 60)
    logger.info(f"Monitoring {len(config.thresholds)} stocks")
    logger.info(f"Check interval: {config.monitor['check_interval_minutes']} minutes")
    logger.info(f"Alert cooldown: {config.monitor['alert_cooldown_hours']} hour(s)")
    logger.info("=" * 60)
    
    # Start background monitoring
    should_monitor = True
    monitoring_task = asyncio.create_task(run_monitoring())
    
    yield
    
    # Shutdown
    logger.info("Shutting down stock monitoring...")
    should_monitor = False
    if monitoring_task:
        monitoring_task.cancel()
        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass
    logger.info("Bursa Stock Tracker API stopped")


# Create FastAPI app
app = FastAPI(
    title="Bursa Stock Tracker API",
    description="REST API for monitoring Malaysian stock prices with real-time alerts",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Bursa Stock Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
