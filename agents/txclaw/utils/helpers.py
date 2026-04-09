"""Utility helpers for TXclaw"""

import re
from typing import List, Dict, Any
from datetime import datetime

def format_tx_hash(tx_hash: str) -> str:
    """Format a transaction hash for display"""
    if len(tx_hash) > 20:
        return f"{tx_hash[:10]}...{tx_hash[-8:]}"
    return tx_hash

def is_valid_tx_hash(tx_hash: str) -> bool:
    """Validate TX blockchain transaction hash format"""
    pattern = r'^[A-Fa-f0-9]{64}$'
    return bool(re.match(pattern, tx_hash))

def is_valid_address(address: str) -> bool:
    """Validate TX blockchain address format"""
    pattern = r'^tx[0-9a-zA-Z]{39}$'
    return bool(re.match(pattern, address))

def parse_amount(amount_str: str) -> float:
    """Parse amount string to float"""
    try:
        return float(amount_str)
    except ValueError:
        return 0.0

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_divide(a: float, b: float) -> float:
    """Safe division returning 0 if denominator is 0"""
    return a / b if b != 0 else 0.0

def build_explorer_url(tx_hash: str) -> str:
    """Build TX.org explorer URL for transaction"""
    return f"https://explorer.tx.org/tx/{tx_hash}"

def build_api_url(endpoint: str) -> str:
    """Build TX.org API URL"""
    return f"https://api.tx.org/{endpoint.lstrip('/')}"
