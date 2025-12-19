"""
Utility functions for Bursa Stock Tracker.
"""
import os
import re
from typing import List, Optional
from datetime import datetime
from pathlib import Path


def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate Malaysian stock symbol format (e.g., 5285.KL).
    
    Args:
        symbol: Stock symbol to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^\d{4}\.KL$'
    return bool(re.match(pattern, symbol))


def validate_threshold(threshold: dict) -> bool:
    """
    Validate threshold configuration.
    
    Args:
        threshold: Dictionary with 'up' and 'down' keys
    
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(threshold, dict):
        return False
    
    if 'up' not in threshold or 'down' not in threshold:
        return False
    
    try:
        up = float(threshold['up'])
        down = float(threshold['down'])
        return up > down > 0
    except (ValueError, TypeError):
        return False


def get_file_size_mb(filepath: Path) -> float:
    """
    Get file size in megabytes.
    
    Args:
        filepath: Path to file
    
    Returns:
        File size in MB, or 0 if file doesn't exist
    """
    if not filepath.exists():
        return 0.0
    return filepath.stat().st_size / (1024 * 1024)


def rotate_csv_file(filepath: Path, max_size_mb: int = 10) -> None:
    """
    Rotate CSV file if it exceeds max size.
    Creates a backup with timestamp and starts fresh file.
    
    Args:
        filepath: Path to CSV file
        max_size_mb: Maximum file size in MB before rotation
    """
    if get_file_size_mb(filepath) > max_size_mb:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = filepath.parent / f'{filepath.stem}_backup_{timestamp}{filepath.suffix}'
        
        if filepath.exists():
            filepath.rename(backup_path)
            print(f"CSV file rotated: {backup_path}")


def format_price(price: float) -> str:
    """
    Format price with 2 decimal places.
    
    Args:
        price: Price value
    
    Returns:
        Formatted price string
    """
    return f"{price:.2f}"


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text
    
    Returns:
        Sanitized text
    """
    # Remove potentially dangerous characters
    return re.sub(r'[^\w\s\-\.]', '', text)
