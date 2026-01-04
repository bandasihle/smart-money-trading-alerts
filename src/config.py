"""
Centralized configuration management for the trading system.

This module provides a single source of truth for all configuration
parameters, loading from environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class TradingConfig:
    """Trading-related configuration parameters."""
    
    # Risk Management
    max_daily_risk: float = 0.02  # 2% max daily risk
    max_position_risk: float = 0.005  # 0.5% per trade
    max_trades_per_day: int = 5
    
    # Pattern Detection
    min_pattern_confidence: float = 70.0
    min_pattern_strength: float = 65.0
    quality_score_threshold: float = 0.7
    
    # Position Sizing
    default_stop_loss_pct: float = 0.008  # 0.8%
    default_take_profit_pct: float = 0.016  # 1.6%
    min_risk_reward_ratio: float = 2.0
    
    # Timeframes
    default_period: str = "2d"
    default_interval: str = "15m"
    high_volatility_interval: str = "5m"


@dataclass
class MarketConfig:
    """Market and session configuration."""
    
    # Trading pairs with their Yahoo Finance symbols
    monitored_pairs: Dict[str, str] = field(default_factory=lambda: {
        'NAS100': '^IXIC',
        'US30': '^DJI',
        'GBPJPY': 'GBPJPY=X',
        'CADCHF': 'CADCHF=X',
        'USDJPY': 'USDJPY=X',
        'EURCAD': 'EURCAD=X',
        'USDCAD': 'USDCAD=X',
        'EURUSD': 'EURUSD=X'
    })
    
    # Market hours in UTC
    market_hours: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        'NAS100': {'open': 14, 'close': 21},
        'US30': {'open': 14, 'close': 21},
        'GBPJPY': {'open': 0, 'close': 23},
        'CADCHF': {'open': 0, 'close': 23},
        'USDJPY': {'open': 0, 'close': 23},
        'EURCAD': {'open': 0, 'close': 23},
        'USDCAD': {'open': 0, 'close': 23},
        'EURUSD': {'open': 0, 'close': 23}
    })


@dataclass
class SessionConfig:
    """Trading session configuration."""
    
    sessions: Dict[str, Dict] = field(default_factory=lambda: {
        'SYDNEY': {'start': 21, 'end': 6, 'timezone': 'Australia/Sydney'},
        'TOKYO': {'start': 0, 'end': 9, 'timezone': 'Asia/Tokyo'},
        'LONDON': {'start': 8, 'end': 17, 'timezone': 'Europe/London'},
        'NEW_YORK': {'start': 13, 'end': 22, 'timezone': 'America/New_York'}
    })
    
    session_volatility: Dict[str, str] = field(default_factory=lambda: {
        'SYDNEY': 'LOW',
        'TOKYO': 'MEDIUM',
        'LONDON': 'HIGH',
        'NEW_YORK': 'HIGH',
        'LONDON_NY_OVERLAP': 'VERY_HIGH'
    })


@dataclass
class AppConfig:
    """Application configuration."""
    
    # Flask settings
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 5000
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache settings
    cache_ttl_seconds: int = 300  # 5 minutes
    
    # Rate limiting
    api_rate_limit: int = 60  # requests per minute


class Config:
    """Main configuration class that combines all config sections."""
    
    def __init__(self):
        self.trading = TradingConfig(
            max_daily_risk=float(os.getenv("MAX_DAILY_RISK", "0.02")),
            max_position_risk=float(os.getenv("MAX_POSITION_RISK", "0.005")),
            max_trades_per_day=int(os.getenv("MAX_TRADES_PER_DAY", "5")),
            min_pattern_confidence=float(os.getenv("MIN_PATTERN_CONFIDENCE", "70.0")),
            min_pattern_strength=float(os.getenv("MIN_PATTERN_STRENGTH", "65.0")),
            quality_score_threshold=float(os.getenv("QUALITY_SCORE_THRESHOLD", "0.7")),
        )
        self.market = MarketConfig()
        self.session = SessionConfig()
        self.app = AppConfig(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls()


# Global configuration instance
config = Config.from_env()
