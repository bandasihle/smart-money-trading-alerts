"""
Constants and magic numbers for the trading system.

This module contains all constant values used throughout the application,
making it easy to modify parameters without searching through code.
"""

from typing import Dict, List, Tuple

# =====================================================
# Trading Pair Symbols
# =====================================================

FOREX_PAIRS: Dict[str, str] = {
    'EURUSD': 'EURUSD=X',
    'GBPJPY': 'GBPJPY=X',
    'USDJPY': 'USDJPY=X',
    'USDCAD': 'USDCAD=X',
    'EURCAD': 'EURCAD=X',
    'CADCHF': 'CADCHF=X',
    'GBPUSD': 'GBPUSD=X',
    'AUDUSD': 'AUDUSD=X',
    'NZDUSD': 'NZDUSD=X',
    'EURJPY': 'EURJPY=X',
    'AUDJPY': 'AUDJPY=X',
}

INDEX_PAIRS: Dict[str, str] = {
    'NAS100': '^IXIC',
    'US30': '^DJI',
    'SPX500': '^GSPC',
}

ALL_PAIRS: Dict[str, str] = {**FOREX_PAIRS, **INDEX_PAIRS}

# Default monitored pairs
DEFAULT_MONITORED_PAIRS: List[str] = [
    'NAS100', 'US30', 'GBPJPY', 'CADCHF', 'USDJPY', 'EURCAD', 'USDCAD'
]


# =====================================================
# Pattern Detection Thresholds
# =====================================================

class PatternThresholds:
    """Thresholds for pattern detection algorithms."""
    
    # Minimum confidence levels
    MIN_CONFIDENCE_HIGH: float = 80.0
    MIN_CONFIDENCE_MEDIUM: float = 70.0
    MIN_CONFIDENCE_LOW: float = 60.0
    
    # Pattern strength thresholds
    MIN_PATTERN_STRENGTH: float = 65.0
    HIGH_PATTERN_STRENGTH: float = 85.0
    
    # Quality score thresholds
    MIN_QUALITY_SCORE: float = 0.7
    HIGH_QUALITY_SCORE: float = 0.85
    
    # Liquidity sweep detection
    SWEEP_THRESHOLD_PCT: float = 0.001  # 0.1%
    REVERSAL_THRESHOLD_PCT: float = 0.002  # 0.2%
    
    # Order block detection
    ORDER_BLOCK_MIN_MOVE_PCT: float = 0.005  # 0.5%
    
    # Fair value gap detection
    FVG_MIN_GAP_PCT: float = 0.001  # 0.1%
    
    # Volume thresholds
    VOLUME_SPIKE_MULTIPLIER: float = 1.5
    HIGH_VOLUME_MULTIPLIER: float = 2.0


# =====================================================
# Risk Management Parameters
# =====================================================

class RiskParameters:
    """Risk management constants."""
    
    # Daily risk limits
    MAX_DAILY_RISK_PCT: float = 0.02  # 2%
    MAX_DAILY_RISK_AGGRESSIVE: float = 0.03  # 3%
    MAX_DAILY_RISK_CONSERVATIVE: float = 0.01  # 1%
    
    # Per-trade risk limits
    MAX_POSITION_RISK_PCT: float = 0.005  # 0.5%
    MAX_POSITION_RISK_AGGRESSIVE: float = 0.01  # 1%
    MAX_POSITION_RISK_CONSERVATIVE: float = 0.003  # 0.3%
    
    # Trade frequency limits
    MAX_TRADES_PER_DAY: int = 5
    MAX_TRADES_PER_SESSION: int = 3
    MAX_CONCURRENT_POSITIONS: int = 3
    
    # Stop loss and take profit defaults (as percentage)
    DEFAULT_STOP_LOSS_PCT: float = 0.008  # 0.8%
    DEFAULT_TAKE_PROFIT_PCT: float = 0.016  # 1.6%
    
    # Risk/reward ratios
    MIN_RISK_REWARD_RATIO: float = 1.5
    TARGET_RISK_REWARD_RATIO: float = 2.0
    OPTIMAL_RISK_REWARD_RATIO: float = 3.0
    
    # Drawdown limits
    MAX_DRAWDOWN_PCT: float = 0.10  # 10%
    DRAWDOWN_WARNING_PCT: float = 0.05  # 5%


# =====================================================
# Session Time Definitions (UTC)
# =====================================================

class SessionTimes:
    """Trading session times in UTC."""
    
    SYDNEY_START: int = 21
    SYDNEY_END: int = 6
    
    TOKYO_START: int = 0
    TOKYO_END: int = 9
    
    LONDON_START: int = 8
    LONDON_END: int = 17
    
    NEW_YORK_START: int = 13
    NEW_YORK_END: int = 22
    
    # Overlap periods (highest volatility)
    LONDON_NY_OVERLAP_START: int = 13
    LONDON_NY_OVERLAP_END: int = 17
    
    TOKYO_LONDON_OVERLAP_START: int = 8
    TOKYO_LONDON_OVERLAP_END: int = 9


# Session preferred pairs
SESSION_PREFERRED_PAIRS: Dict[str, List[str]] = {
    'SYDNEY': ['AUDUSD', 'NZDUSD', 'AUDJPY'],
    'TOKYO': ['USDJPY', 'EURJPY', 'GBPJPY'],
    'LONDON': ['EURUSD', 'GBPUSD', 'EURGBP'],
    'NEW_YORK': ['EURUSD', 'GBPUSD', 'USDCAD', 'US30'],
    'LONDON_NY_OVERLAP': ['EURUSD', 'GBPUSD', 'USDCAD'],
}

# Session volatility levels
SESSION_VOLATILITY: Dict[str, str] = {
    'SYDNEY': 'LOW',
    'TOKYO': 'MEDIUM',
    'LONDON': 'HIGH',
    'NEW_YORK': 'HIGH',
    'LONDON_NY_OVERLAP': 'VERY_HIGH',
}

# Session risk multipliers
SESSION_RISK_MULTIPLIERS: Dict[str, float] = {
    'SYDNEY': 0.8,
    'TOKYO': 1.0,
    'LONDON': 1.2,
    'NEW_YORK': 1.3,
    'LONDON_NY_OVERLAP': 1.5,
}


# =====================================================
# API and Rate Limiting
# =====================================================

class APIConstants:
    """API-related constants."""
    
    # Rate limiting
    DEFAULT_RATE_LIMIT: int = 60  # requests per minute
    YFINANCE_RATE_LIMIT: int = 30  # requests per minute
    PUSHOVER_RATE_LIMIT: int = 10  # requests per minute
    
    # Timeouts
    DEFAULT_TIMEOUT_SECONDS: int = 30
    YFINANCE_TIMEOUT_SECONDS: int = 15
    
    # Retry settings
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: float = 1.0
    RETRY_BACKOFF_MULTIPLIER: float = 2.0
    
    # Cache settings
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    CACHE_TTL_SHORT: int = 60  # 1 minute
    CACHE_TTL_LONG: int = 900  # 15 minutes


# =====================================================
# Timeframe Constants
# =====================================================

VALID_PERIODS: List[str] = ['1d', '2d', '5d', '1mo', '3mo', '6mo', '1y']
VALID_INTERVALS: List[str] = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d']

DEFAULT_PERIOD: str = '2d'
DEFAULT_INTERVAL: str = '15m'
HIGH_VOLATILITY_INTERVAL: str = '5m'
SCALPING_INTERVAL: str = '1m'


# =====================================================
# Signal and Alert Constants
# =====================================================

class SignalConstants:
    """Constants for trading signals."""
    
    # Signal directions
    DIRECTION_BUY: str = 'BUY'
    DIRECTION_SELL: str = 'SELL'
    
    # Confidence levels
    CONFIDENCE_HIGH: str = 'HIGH'
    CONFIDENCE_MEDIUM: str = 'MEDIUM'
    CONFIDENCE_LOW: str = 'LOW'
    
    # Risk levels
    RISK_LOW: str = 'LOW'
    RISK_MEDIUM: str = 'MEDIUM'
    RISK_HIGH: str = 'HIGH'
    
    # Pattern types
    PATTERN_MOMENTUM: str = 'momentum'
    PATTERN_REVERSAL: str = 'reversal'
    PATTERN_SCALPING: str = 'scalping'
    PATTERN_GAP_FILL: str = 'gap_fill'
    PATTERN_BREAKOUT: str = 'breakout'
    
    # Alert statuses
    STATUS_ACTIVE: str = 'ACTIVE'
    STATUS_TRIGGERED: str = 'TRIGGERED'
    STATUS_EXPIRED: str = 'EXPIRED'
    STATUS_CANCELLED: str = 'CANCELLED'


# =====================================================
# Fallback Values
# =====================================================

FALLBACK_PRICES: Dict[str, float] = {
    'EURUSD': 1.1745,
    'GBPJPY': 199.295,
    'USDJPY': 147.912,
    'USDCAD': 1.378,
    'EURCAD': 1.6181,
    'CADCHF': 0.5766,
    'US30': 46315.27,
    'NAS100': 18500.00,
}
