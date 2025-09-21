#!/usr/bin/env python3
"""
Complete Smart Money Trading System for Backtesting
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

class InstitutionalPatternDetector:
    """Detects smart money and institutional trading patterns"""
    
    def __init__(self):
        self.patterns = ['order_block', 'fair_value_gap', 'liquidity_sweep']
    
    def analyze_patterns(self, data):
        """Analyze price data for institutional patterns"""
        if len(data) < 20:
            return []
        
        signals = []
        
        # Smart money pattern detection (simplified)
        current_price = data['Close'].iloc[-1]
        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
        volatility = data['Close'].rolling(10).std().iloc[-1]
        
        # Order block detection - look for strong rejection levels
        recent_high = data['High'].rolling(5).max().iloc[-1]
        recent_low = data['Low'].rolling(5).min().iloc[-1]
        
        # Fair value gap - price inefficiency
        if abs(current_price - sma_20) > volatility * 0.5:
            direction = 'BUY' if current_price > sma_20 else 'SELL'
            confidence = min(95, 60 + abs(current_price - sma_20) / volatility * 10)
            
            signals.append({
                'pattern': 'fair_value_gap',
                'direction': direction,
                'confidence': confidence,
                'entry_price': current_price
            })
        
        # Liquidity sweep pattern
        if len(data) >= 30:
            prev_high = data['High'].rolling(20).max().iloc[-2]
            if current_price > prev_high * 1.001:  # Breaking previous high
                signals.append({
                    'pattern': 'liquidity_sweep', 
                    'direction': 'SELL',  # Often reverses after liquidity grab
                    'confidence': 70,
                    'entry_price': current_price
                })
        
        return signals

class DayTradingSmartMoney:
    """Smart money day trading system"""
    
    def __init__(self, initial_capital=10000):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.risk_per_trade = 0.02  # 2% risk per trade
        self.trades = []
    
    def calculate_position_size(self, entry_price, stop_loss):
        """Calculate position size based on risk management"""
        risk_amount = self.capital * self.risk_per_trade
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            return 0
        
        position_size = risk_amount / price_risk
        return position_size
    
    def execute_trade(self, signal, market_data):
        """Execute a trade based on signal"""
        entry_price = signal['entry_price']
        
        # Set stop loss and take profit
        if signal['direction'] == 'BUY':
            stop_loss = entry_price * 0.99    # 1% stop loss
            take_profit = entry_price * 1.02  # 2% take profit
        else:
            stop_loss = entry_price * 1.01    # 1% stop loss  
            take_profit = entry_price * 0.98  # 2% take profit
        
        position_size = self.calculate_position_size(entry_price, stop_loss)
        
        trade = {
            'direction': signal['direction'],
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'position_size': position_size,
            'confidence': signal['confidence']
        }
        
        self.trades.append(trade)
        return trade

class MarketHoursChecker:
    """Check if markets are open for trading"""
    
    def __init__(self):
        self.forex_hours = True  # Forex is 24/5
        self.index_hours = True  # Simplified for backtesting
    
    def is_market_open(self, pair, timestamp=None):
        """Check if market is open for the given pair"""
        # Simplified - assume markets are open during backtesting
        return True