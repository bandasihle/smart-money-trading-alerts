"""
Constants and magic numbers for the trading system.

This module centralizes all constants to make the codebase
more maintainable and self-documenting.
"""

from typing import Dict, List, Tuple


# =====================================================
# Trading Pair Symbols
# =====================================================

FOREX_SYMBOLS: Dict[str, str] = {
    'EURUSD': 'EURUSD=X',
    'GBPJPY': 'GBPJPY=X',
    'USDJPY': 'USDJPY=X',
    'USDCAD': 'USDCAD=X',
    'EURCAD': 'EURCAD=X',
    'CADCHF': 'CADCHF=X',
    'GBPUSD': 'GBPUSD=X',
    'AUDUSD': 'AUDUSD=X',
    'NZDUSD': 'NZDUSD=X',
}

INDEX_SYMBOLS: Dict[str, str] = {
    'US30': '^DJI',
    'NAS100': '^IXIC',
    'SPX500': '^GSPC',
}

ALL_SYMBOLS: Dict[str, str] = {**FOREX_SYMBOLS, **INDEX_SYMBOLS}


class PatternThresholds:
    MIN_PATTERN_CONFIDENCE: float = 70.0
    HIGH_CONFIDENCE_THRESHOLD: float = 85.0
    MIN_PATTERN_STRENGTH: float = 65.0
    STRONG_PATTERN_STRENGTH: float = 80.0
    MIN_QUALITY_SCORE: float = 0.7
    HIGH_QUALITY_SCORE: float = 0.85
    SWEEP_THRESHOLD_PCT: float = 0.001
    SWEEP_REVERSAL_PCT: float = 0.002
    ORDER_BLOCK_MIN_MOVE_PCT: float = 0.005
    FVG_MIN_GAP_PCT: float = 0.001
    RSI_OVERSOLD: float = 30.0
    RSI_OVERBOUGHT: float = 70.0
    RSI_PERIOD: int = 14
    ATR_PERIOD: int = 14
    VOLUME_SPIKE_MULTIPLIER: float = 1.5


class RiskParameters:
    MAX_DAILY_RISK_PCT: float = 0.02
    MAX_POSITION_RISK_PCT: float = 0.005
    MAX_DRAWDOWN_PCT: float = 0.10
    MAX_TRADES_PER_DAY: int = 5
    MAX_CONCURRENT_POSITIONS: int = 3
    MIN_RISK_REWARD_RATIO: float = 2.0
    TARGET_RISK_REWARD_RATIO: float = 3.0


class TradingSessions:
    SYDNEY: Dict[str, int] = {'start': 21, 'end': 6}
    TOKYO: Dict[str, int] = {'start': 0, 'end': 9}
    LONDON: Dict[str, int] = {'start': 8, 'end': 17}
    NEW_YORK: Dict[str, int] = {'start': 13, 'end': 22}
    LONDON_NY_OVERLAP: Tuple[int, int] = (13, 17)


class SignalTypes:
    BUY: str = "BUY"
    SELL: str = "SELL"
    MOMENTUM: str = "momentum"
    REVERSAL: str = "reversal"
    SCALPING: str = "scalping"
    GAP_FILL: str = "gap_fill"
    HIGH_CONFIDENCE: str = "HIGH"
    MEDIUM_CONFIDENCE: str = "MEDIUM"
    LOW_CONFIDENCE: str = "LOW"
