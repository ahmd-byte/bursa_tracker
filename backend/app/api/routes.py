"""
API routes for Bursa Stock Tracker.
Provides REST API endpoints for frontend connectivity.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel

from app.core.config import config
from app.services.stock_monitor import (
    get_all_stock_prices,
    get_price_history,
    get_stock_price,
    load_last_alerts
)
from app.utils.helpers import validate_stock_symbol

router = APIRouter(prefix="/api", tags=["stocks"])


class StockThreshold(BaseModel):
    """Stock threshold model for API requests."""
    up: float
    down: float


class StockInfo(BaseModel):
    """Stock information response model."""
    symbol: str
    current_price: float
    threshold_up: float
    threshold_down: float


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Bursa Stock Tracker API"}


@router.get("/stocks", response_model=List[StockInfo])
async def get_stocks():
    """
    Get all monitored stocks with current prices and thresholds.
    
    Returns:
        List of stock information
    """
    try:
        prices = get_all_stock_prices()
        stocks = []
        
        for symbol, thresholds in config.thresholds.items():
            stock_info = {
                "symbol": symbol,
                "current_price": prices.get(symbol, 0.0),
                "threshold_up": thresholds['up'],
                "threshold_down": thresholds['down']
            }
            stocks.append(stock_info)
        
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stocks: {str(e)}")


@router.get("/stocks/{symbol}")
async def get_stock(symbol: str):
    """
    Get specific stock details.
    
    Args:
        symbol: Stock symbol (e.g., 5285.KL)
    
    Returns:
        Stock information
    """
    if not validate_stock_symbol(symbol):
        raise HTTPException(status_code=400, detail="Invalid stock symbol format")
    
    if symbol not in config.thresholds:
        raise HTTPException(status_code=404, detail="Stock not found in monitored list")
    
    try:
        price = get_stock_price(symbol)
        thresholds = config.thresholds[symbol]
        
        return {
            "symbol": symbol,
            "current_price": price,
            "threshold_up": thresholds['up'],
            "threshold_down": thresholds['down']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock: {str(e)}")


@router.get("/history")
async def get_history(limit: int = 100):
    """
    Get price history.
    
    Args:
        limit: Maximum number of records to return (default: 100)
    
    Returns:
        List of price history records
    """
    try:
        history = get_price_history(limit)
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@router.get("/alerts")
async def get_alerts():
    """
    Get recent alerts.
    
    Returns:
        Dictionary of last alert times per stock
    """
    try:
        alerts = load_last_alerts()
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching alerts: {str(e)}")


@router.get("/thresholds")
async def get_thresholds():
    """
    Get all stock thresholds.
    
    Returns:
        Dictionary of stock thresholds
    """
    return {"thresholds": config.thresholds}


@router.put("/thresholds/{symbol}")
async def update_threshold(symbol: str, threshold: StockThreshold):
    """
    Update stock threshold (Note: This updates in-memory only, not persisted to file).
    
    Args:
        symbol: Stock symbol
        threshold: New threshold values
    
    Returns:
        Updated threshold
    """
    if not validate_stock_symbol(symbol):
        raise HTTPException(status_code=400, detail="Invalid stock symbol format")
    
    if threshold.up <= threshold.down or threshold.down <= 0:
        raise HTTPException(status_code=400, detail="Invalid threshold values: up must be > down > 0")
    
    # Update in-memory config (Note: This won't persist to thresholds.json)
    config.thresholds[symbol] = {"up": threshold.up, "down": threshold.down}
    
    return {
        "symbol": symbol,
        "threshold_up": threshold.up,
        "threshold_down": threshold.down,
        "message": "Threshold updated (in-memory only)"
    }
