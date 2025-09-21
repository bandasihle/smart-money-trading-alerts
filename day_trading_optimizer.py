#!/usr/bin/env python3
"""
Day Trading Optimized Pattern Detection System
High-frequency pattern detection for intraday trading with real market data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from typing import List, Dict, Optional

class DayTradingPatternDetector:
    """Optimized pattern detection for day trading with faster signals"""
    
    def __init__(self):
        self.min_pattern_strength = 60  # Lower threshold for faster signals
        self.lookback_periods = 20  # Shorter lookback for responsiveness
        
    def detect_liquidity_sweep(self, data: pd.DataFrame) -> List[Dict]:
        """Detect liquidity sweeps - key day trading pattern"""
        signals = []
        
        if len(data) < 20:
            return signals
            
        # Calculate recent highs and lows
        recent_high = data['High'].rolling(10).max()
        recent_low = data['Low'].rolling(10).min()
        
        for i in range(15, len(data)):
            current = data.iloc[i]
            prev_bars = data.iloc[i-10:i]
            
            # Bullish liquidity sweep (sweep lows then reverse up)
            if (current['Low'] < recent_low.iloc[i-1] and  # Sweep recent low
                current['Close'] > current['Open'] and      # Bullish close
                current['Close'] > prev_bars['High'].max() * 0.999):  # Break structure
                
                strength = min(95, 70 + abs(current['Close'] - current['Low']) / current['Close'] * 1000)
                
                signals.append({
                    'timestamp': current.name,
                    'pattern': 'liquidity_sweep',
                    'direction': 'BUY',
                    'confidence': strength,
                    'entry_price': current['Close'],
                    'pattern_type': 'scalping',
                    'timeframe': 'intraday'
                })
            
            # Bearish liquidity sweep (sweep highs then reverse down)
            elif (current['High'] > recent_high.iloc[i-1] and  # Sweep recent high
                  current['Close'] < current['Open'] and        # Bearish close
                  current['Close'] < prev_bars['Low'].min() * 1.001):  # Break structure
                
                strength = min(95, 70 + abs(current['High'] - current['Close']) / current['Close'] * 1000)
                
                signals.append({
                    'timestamp': current.name,
                    'pattern': 'liquidity_sweep',
                    'direction': 'SELL',
                    'confidence': strength,
                    'entry_price': current['Close'],
                    'pattern_type': 'scalping',
                    'timeframe': 'intraday'
                })
        
        return signals
    
    def detect_order_blocks(self, data: pd.DataFrame) -> List[Dict]:
        """Detect order blocks - institutional supply/demand zones"""
        signals = []
        
        if len(data) < 15:
            return signals
        
        # Look for strong moves that create order blocks
        data['price_change'] = data['Close'].pct_change()
        data['volume_surge'] = data['Volume'] > data['Volume'].rolling(10).mean() * 1.5
        
        for i in range(10, len(data)):
            current = data.iloc[i]
            
            # Strong bullish move creating supply zone
            if (current['price_change'] > 0.005 and  # 0.5% move
                data.iloc[i-1:i+1]['volume_surge'].any()):
                
                # Look for retest of this level
                future_data = data.iloc[i:min(i+5, len(data))]
                retest = False
                
                for j, future_bar in future_data.iterrows():
                    if abs(future_bar['Close'] - current['Close']) / current['Close'] < 0.002:  # Within 0.2%
                        retest = True
                        break
                
                if retest:
                    signals.append({
                        'timestamp': current.name,
                        'pattern': 'order_block',
                        'direction': 'BUY',
                        'confidence': 75,
                        'entry_price': current['Close'],
                        'pattern_type': 'momentum',
                        'timeframe': 'intraday'
                    })
            
            # Strong bearish move creating demand zone
            elif (current['price_change'] < -0.005 and  # -0.5% move
                  data.iloc[i-1:i+1]['volume_surge'].any()):
                
                future_data = data.iloc[i:min(i+5, len(data))]
                retest = False
                
                for j, future_bar in future_data.iterrows():
                    if abs(future_bar['Close'] - current['Close']) / current['Close'] < 0.002:
                        retest = True
                        break
                
                if retest:
                    signals.append({
                        'timestamp': current.name,
                        'pattern': 'order_block',
                        'direction': 'SELL',
                        'confidence': 75,
                        'entry_price': current['Close'],
                        'pattern_type': 'momentum',
                        'timeframe': 'intraday'
                    })
        
        return signals
    
    def detect_breaker_blocks(self, data: pd.DataFrame) -> List[Dict]:
        """Detect breaker blocks - failed support/resistance becoming opposite"""
        signals = []
        
        if len(data) < 20:
            return signals
        
        # Identify key support/resistance levels
        data['support'] = data['Low'].rolling(5).min()
        data['resistance'] = data['High'].rolling(5).max()
        
        for i in range(15, len(data)):
            current = data.iloc[i]
            prev_data = data.iloc[i-10:i]
            
            # Support becomes resistance (bearish breaker)
            support_level = prev_data['support'].iloc[-1]
            if (current['Close'] < support_level and  # Break support
                prev_data['Close'].iloc[-1] > support_level):  # Was above support
                
                signals.append({
                    'timestamp': current.name,
                    'pattern': 'breaker_block',
                    'direction': 'SELL',
                    'confidence': 80,
                    'entry_price': current['Close'],
                    'pattern_type': 'reversal',
                    'timeframe': 'intraday'
                })
            
            # Resistance becomes support (bullish breaker)
            resistance_level = prev_data['resistance'].iloc[-1]
            if (current['Close'] > resistance_level and  # Break resistance
                prev_data['Close'].iloc[-1] < resistance_level):  # Was below resistance
                
                signals.append({
                    'timestamp': current.name,
                    'pattern': 'breaker_block',
                    'direction': 'BUY',
                    'confidence': 80,
                    'entry_price': current['Close'],
                    'pattern_type': 'reversal',
                    'timeframe': 'intraday'
                })
        
        return signals
    
    def detect_fair_value_gaps_fast(self, data: pd.DataFrame) -> List[Dict]:
        """Fast fair value gap detection for day trading"""
        signals = []
        
        if len(data) < 10:
            return signals
        
        for i in range(3, len(data)):
            bar1 = data.iloc[i-2]  # First bar
            bar2 = data.iloc[i-1]  # Gap bar  
            bar3 = data.iloc[i]    # Current bar
            
            # Bullish FVG (gap up that gets filled)
            if (bar1['High'] < bar3['Low'] and  # Gap exists
                bar2['Close'] > bar2['Open'] and  # Bullish gap bar
                bar3['Close'] > bar1['High']):    # Gap holding
                
                gap_size = (bar3['Low'] - bar1['High']) / bar1['High']
                
                if gap_size > 0.001:  # Minimum 0.1% gap for day trading
                    strength = min(90, 60 + gap_size * 10000)
                    
                    signals.append({
                        'timestamp': bar3.name,
                        'pattern': 'fair_value_gap_fast',
                        'direction': 'BUY',
                        'confidence': strength,
                        'entry_price': bar3['Close'],
                        'pattern_type': 'gap_fill',
                        'timeframe': 'intraday'
                    })
            
            # Bearish FVG (gap down that gets filled)
            elif (bar1['Low'] > bar3['High'] and  # Gap exists
                  bar2['Close'] < bar2['Open'] and  # Bearish gap bar
                  bar3['Close'] < bar1['Low']):     # Gap holding
                
                gap_size = (bar1['Low'] - bar3['High']) / bar3['High']
                
                if gap_size > 0.001:  # Minimum 0.1% gap
                    strength = min(90, 60 + gap_size * 10000)
                    
                    signals.append({
                        'timestamp': bar3.name,
                        'pattern': 'fair_value_gap_fast',
                        'direction': 'SELL',
                        'confidence': strength,
                        'entry_price': bar3['Close'],
                        'pattern_type': 'gap_fill',
                        'timeframe': 'intraday'
                    })
        
        return signals
    
    def analyze_intraday_patterns(self, data: pd.DataFrame) -> List[Dict]:
        """Comprehensive intraday pattern analysis"""
        all_signals = []
        
        # Run all pattern detection methods
        all_signals.extend(self.detect_liquidity_sweep(data))
        all_signals.extend(self.detect_order_blocks(data))
        all_signals.extend(self.detect_breaker_blocks(data))
        all_signals.extend(self.detect_fair_value_gaps_fast(data))
        
        # Sort by confidence and timestamp
        all_signals.sort(key=lambda x: (x['confidence'], x['timestamp']), reverse=True)
        
        # Filter for day trading quality signals
        day_trading_signals = []
        for signal in all_signals:
            if signal['confidence'] >= self.min_pattern_strength:
                day_trading_signals.append(signal)
        
        return day_trading_signals[:5]  # Top 5 signals for focus

class DayTradingRiskManager:
    """Specialized risk management for day trading"""
    
    def __init__(self, max_daily_risk=0.02, max_position_risk=0.005):
        self.max_daily_risk = max_daily_risk  # 2% max daily risk
        self.max_position_risk = max_position_risk  # 0.5% per trade
        self.daily_pnl = 0
        self.trades_today = []
        
    def calculate_day_trading_position_size(self, signal: Dict, current_price: float, account_balance: float) -> Dict:
        """Calculate position size for day trading with tight risk control"""
        
        # Tighter stops for day trading
        if signal['pattern_type'] == 'scalping':
            stop_distance_pct = 0.003  # 0.3% stop for scalping
            profit_target_pct = 0.006  # 0.6% target (1:2 R:R)
        elif signal['pattern_type'] == 'momentum':
            stop_distance_pct = 0.005  # 0.5% stop for momentum
            profit_target_pct = 0.01   # 1% target (1:2 R:R)
        else:  # reversal patterns
            stop_distance_pct = 0.004  # 0.4% stop
            profit_target_pct = 0.008  # 0.8% target (1:2 R:R)
        
        # Calculate levels
        if signal['direction'] == 'BUY':
            stop_loss = current_price * (1 - stop_distance_pct)
            take_profit = current_price * (1 + profit_target_pct)
        else:
            stop_loss = current_price * (1 + stop_distance_pct)
            take_profit = current_price * (1 - profit_target_pct)
        
        # Position sizing based on risk per trade
        risk_amount = account_balance * self.max_position_risk
        stop_distance = abs(current_price - stop_loss)
        
        if stop_distance > 0:
            position_size = risk_amount / stop_distance
        else:
            position_size = 0
        
        # Check daily risk limits
        if abs(self.daily_pnl) >= account_balance * self.max_daily_risk:
            position_size = 0  # Stop trading for the day
        
        return {
            'position_size': position_size,
            'entry_price': current_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk_amount': risk_amount,
            'risk_reward_ratio': abs(take_profit - current_price) / abs(current_price - stop_loss),
            'pattern_type': signal['pattern_type']
        }

def get_intraday_data(symbol: str, period: str = "1d", interval: str = "15m") -> pd.DataFrame:
    """Get high-frequency intraday data for day trading"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval=interval)
        
        if len(data) > 0:
            print(f"✅ {symbol}: {len(data)} bars of {interval} data")
            return data
        else:
            print(f"❌ {symbol}: No intraday data")
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ {symbol}: Error getting intraday data - {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Test day trading optimization
    print("🚀 DAY TRADING PATTERN DETECTION TEST")
    print("=" * 50)
    
    detector = DayTradingPatternDetector()
    risk_manager = DayTradingRiskManager()
    
    # Test on EURUSD with 15-minute data
    symbol = "EURUSD=X"
    data = get_intraday_data(symbol, period="5d", interval="15m")
    
    if len(data) > 0:
        signals = detector.analyze_intraday_patterns(data)
        
        print(f"📊 Found {len(signals)} day trading signals:")
        
        for i, signal in enumerate(signals[:3]):
            print(f"\n🎯 Signal {i+1}:")
            print(f"   Pattern: {signal['pattern']}")
            print(f"   Direction: {signal['direction']}")
            print(f"   Confidence: {signal['confidence']:.1f}%")
            print(f"   Type: {signal['pattern_type']}")
            
            # Calculate position sizing
            trade_setup = risk_manager.calculate_day_trading_position_size(
                signal, signal['entry_price'], 10000
            )
            
            print(f"   💰 Position Size: {trade_setup['position_size']:.2f}")
            print(f"   📊 Stop Loss: {trade_setup['stop_loss']:.4f}")
            print(f"   📊 Take Profit: {trade_setup['take_profit']:.4f}")
            print(f"   📊 R:R Ratio: 1:{trade_setup['risk_reward_ratio']:.1f}")
    
    print(f"\n✅ Day trading optimization complete!")