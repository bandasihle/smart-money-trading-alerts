# Real Trading System Classes
# Extracted from model.ipynb for Flask app integration

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, time
import random
from typing import Dict, List, Optional
import pytz

class InstitutionalPatternDetector:
    def __init__(self):
        self.liquidity_levels = []
        
    def detect_liquidity_sweeps(self, data, lookback=20):
        """Detect liquidity sweeps (stop loss hunting)"""
        sweeps = []
        
        if len(data) < lookback:
            return sweeps
            
        for i in range(lookback, len(data)):
            current = data.iloc[i]
            recent_data = data.iloc[i-lookback:i]
            
            # Check for sweep above recent highs
            recent_high = recent_data['high'].max()
            if current['high'] > recent_high * 1.001:  # 0.1% above
                # Check for quick reversal
                if current['close'] < current['high'] * 0.998:  # Closed below high
                    sweeps.append({
                        'type': 'BULLISH_SWEEP',
                        'index': i,
                        'sweep_high': current['high'],
                        'reversal_strength': (current['high'] - current['close']) / current['close'] * 100
                    })
            
            # Check for sweep below recent lows
            recent_low = recent_data['low'].min()
            if current['low'] < recent_low * 0.999:  # 0.1% below
                # Check for quick reversal
                if current['close'] > current['low'] * 1.002:  # Closed above low
                    sweeps.append({
                        'type': 'BEARISH_SWEEP',
                        'index': i,
                        'sweep_low': current['low'],
                        'reversal_strength': (current['close'] - current['low']) / current['low'] * 100
                    })
        
        return sweeps
    
    def detect_order_blocks(self, data):
        """Detect institutional order blocks"""
        order_blocks = []
        
        for i in range(3, len(data)):
            current = data.iloc[i]
            prev = data.iloc[i-1]
            
            # Bullish order block: strong green candle after rejection
            if (current['close'] > current['open'] and 
                current['close'] > prev['high'] and
                (current['close'] - current['open']) / current['open'] > 0.005):  # 0.5% move
                
                order_blocks.append({
                    'type': 'BULLISH_OB',
                    'top': current['high'],
                    'bottom': current['low'],
                    'strength': (current['close'] - current['open']) / current['open'] * 100,
                    'index': i
                })
            
            # Bearish order block: strong red candle after rejection
            elif (current['close'] < current['open'] and 
                  current['close'] < prev['low'] and
                  (current['open'] - current['close']) / current['close'] > 0.005):
                
                order_blocks.append({
                    'type': 'BEARISH_OB',
                    'top': current['high'],
                    'bottom': current['low'],
                    'strength': (current['open'] - current['close']) / current['close'] * 100,
                    'index': i
                })
        
        return order_blocks
    
    def calculate_liquidity_confluence(self, price, tolerance=0.02):
        """Calculate liquidity confluence at a price level"""
        confluence = 0
        for level in self.liquidity_levels:
            distance = abs(price - level) / price
            if distance < tolerance:
                confluence += 1
        return confluence

class MarketHoursChecker:
    """Check if markets are open for different instruments"""
    
    def __init__(self):
        # Market hours in UTC
        self.market_hours = {
            'NAS100': {'open': 14, 'close': 21},  # NYSE/NASDAQ: 9:30 AM - 4:00 PM EST
            'US30': {'open': 14, 'close': 21},    # Same as NAS100
            'GBPJPY': {'open': 0, 'close': 23},   # Forex: Sunday 5 PM EST - Friday 5 PM EST
            'CADCHF': {'open': 0, 'close': 23}    # Forex: Same as GBPJPY
        }
    
    def is_market_open(self, pair_name: str) -> bool:
        """Check if market is currently open for a specific pair"""
        now_utc = datetime.now(pytz.UTC)
        current_hour = now_utc.hour
        current_weekday = now_utc.weekday()  # 0=Monday, 6=Sunday
        
        # Check if it's weekend
        if current_weekday >= 5:  # Saturday or Sunday
            if pair_name in ['NAS100', 'US30']:
                return False  # Stock markets closed on weekends
            elif current_weekday == 6:  # Sunday
                return current_hour >= 22  # Forex opens Sunday 5 PM EST (22 UTC)
            else:  # Saturday
                return False
        
        # Weekday hours
        hours = self.market_hours.get(pair_name, {'open': 0, 'close': 23})
        return hours['open'] <= current_hour <= hours['close']
    
    def get_next_open_time(self, pair_name: str) -> str:
        """Get next market open time"""
        if self.is_market_open(pair_name):
            return "Market is currently open"
        
        now_utc = datetime.now(pytz.UTC)
        
        if pair_name in ['NAS100', 'US30']:
            # Next weekday at 14:00 UTC (9:30 AM EST)
            days_ahead = 0
            while True:
                next_day = now_utc + pd.Timedelta(days=days_ahead)
                if next_day.weekday() < 5:  # Monday to Friday
                    next_open = next_day.replace(hour=14, minute=30, second=0, microsecond=0)
                    if next_open > now_utc:
                        return next_open.strftime("%Y-%m-%d %H:%M UTC")
                days_ahead += 1
                if days_ahead > 7:
                    break
        
        else:  # Forex
            # Next Sunday 22:00 UTC (5 PM EST)
            days_ahead = (6 - now_utc.weekday()) % 7
            next_open = now_utc + pd.Timedelta(days=days_ahead)
            next_open = next_open.replace(hour=22, minute=0, second=0, microsecond=0)
            return next_open.strftime("%Y-%m-%d %H:%M UTC")

class DayTradingSmartMoney:
    """Real day trading smart money system"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.trades = []
        self.max_drawdown = 0
        self.peak_capital = initial_capital
        self.detector = InstitutionalPatternDetector()
        
    def detect_day_trading_signal(self, data, index):
        """Detect day trading signals with relaxed restrictions"""
        if index < 20:
            return None
            
        current = data.iloc[index]
        recent_data = data.iloc[index-20:index+1]
        
        # Detect institutional patterns
        liquidity_sweeps = self.detector.detect_liquidity_sweeps(recent_data, lookback=10)
        order_blocks = self.detector.detect_order_blocks(recent_data)
        
        # Bias determination
        recent_12h = data.iloc[index-12:index] if index >= 12 else data.iloc[:index]
        if len(recent_12h) == 0:
            return None
            
        daily_high = recent_12h['high'].max()
        daily_low = recent_12h['low'].min()
        daily_range = daily_high - daily_low
        
        if daily_range == 0:
            return None
            
        price_position = (current['close'] - daily_low) / daily_range
        
        # Determine bias
        bias = None
        bias_strength = 0
        
        # Check for liquidity sweeps
        recent_sweeps = [s for s in liquidity_sweeps if s['index'] >= len(recent_data) - 10]
        
        if recent_sweeps:
            latest_sweep = recent_sweeps[-1]
            if latest_sweep['type'] == 'BULLISH_SWEEP' and price_position > 0.2:
                bias = 'BULLISH'
                bias_strength = latest_sweep['reversal_strength']
            elif latest_sweep['type'] == 'BEARISH_SWEEP' and price_position < 0.8:
                bias = 'BEARISH'
                bias_strength = latest_sweep['reversal_strength']
        
        # Fallback bias
        if not bias:
            if price_position > 0.6:
                bias = 'BULLISH'
                bias_strength = price_position * 4
            elif price_position < 0.4:
                bias = 'BEARISH'
                bias_strength = (1 - price_position) * 4
                
        if not bias:
            return None
            
        # FVG detection
        fvg_detected = False
        fvg_strength = 0
        
        if index >= 2:
            # Check for gaps
            if (current['low'] > data.iloc[index-1]['high'] and bias == 'BULLISH'):
                gap_size = current['low'] - data.iloc[index-1]['high']
                fvg_strength = (gap_size / current['close']) * 10000
                fvg_direction = 'BUY'
                fvg_detected = True
                
            elif (current['high'] < data.iloc[index-1]['low'] and bias == 'BEARISH'):
                gap_size = data.iloc[index-1]['low'] - current['high']
                fvg_strength = (gap_size / current['close']) * 10000
                fvg_direction = 'SELL'
                fvg_detected = True
        
        # Accept momentum signals if no FVG
        if not fvg_detected:
            if bias == 'BULLISH' and current['close'] > current['open']:
                fvg_direction = 'BUY'
                fvg_strength = (current['close'] - current['open']) / current['open'] * 10000
                fvg_detected = True
            elif bias == 'BEARISH' and current['close'] < current['open']:
                fvg_direction = 'SELL'
                fvg_strength = (current['open'] - current['close']) / current['open'] * 10000
                fvg_detected = True
        
        if not fvg_detected:
            return None
            
        # Order block confluence
        current_price = current['close']
        nearby_obs = []
        
        for ob in order_blocks:
            ob_mid = (ob['top'] + ob['bottom']) / 2
            distance = abs(current_price - ob_mid) / current_price
            
            if distance < 0.05:  # 5% tolerance
                nearby_obs.append(ob)
        
        ob_confluence = len(nearby_obs) > 0
        ob_strength = max([ob['strength'] for ob in nearby_obs]) if nearby_obs else 0
        
        # Session timing check
        current_hour = datetime.now().hour
        if not (2 <= current_hour <= 21):  # Trading hours
            return None
            
        # Session multipliers
        if 13 <= current_hour <= 16:
            session_multiplier = 1.5
        elif 8 <= current_hour <= 17:
            session_multiplier = 1.3
        elif 2 <= current_hour <= 6:
            session_multiplier = 1.1
        else:
            session_multiplier = 1.0
        
        # Volume check
        avg_volume = recent_12h['volume'].mean()
        volume_ratio = current['volume'] / avg_volume
        
        # Liquidity confluence
        liquidity_confluence = self.detector.calculate_liquidity_confluence(
            current_price, tolerance=0.03
        )
        
        # Signal scoring
        signal_score = (
            bias_strength * 0.25 +
            min(fvg_strength, 10) * 0.25 +
            ob_strength * 0.1 +
            liquidity_confluence * 0.1 +
            volume_ratio * 1.5 * 0.15 +
            session_multiplier * 2 * 0.15
        )
        
        # Threshold for day trading
        if signal_score < 4:
            return None
            
        return {
            'symbol': 'DAY_TRADE',
            'direction': fvg_direction,
            'strength': min(signal_score, 15),
            'entry': current['close'],
            'timestamp': datetime.now(),
            'liquidity_sweep': recent_sweeps[-1] if recent_sweeps else None,
            'order_block_confluence': ob_confluence,
            'session_multiplier': session_multiplier,
            'bias_strength': bias_strength
        }

class TradingAlertSystem:
    """Real trading alert system with market hours checking"""
    
    def __init__(self, initial_capital=10000, paper_trading=True):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.paper_trading = paper_trading
        self.trades = []
        self.positions = {}
        self.running = False
        
        # Focus on profitable pairs from backtesting
        self.monitored_pairs = {
            'NAS100': '^IXIC',  # Best return: 5.2%
            'GBPJPY': 'GBPJPY=X',  # Best win rate: 66.7%
            'CADCHF': 'CADCHF=X'   # Solid performer: 1.5%
        }
        
        self.detector = InstitutionalPatternDetector()
        self.day_trader = DayTradingSmartMoney(initial_capital)
        self.market_checker = MarketHoursChecker()
        
        # Alert storage
        self.recent_alerts = []
        self.last_check_time = {}
        
        # Mobile notification settings
        self.push_service_url = None
        self.push_api_key = None
        self.user_tokens = []
        
        print("📱 REAL TRADING ALERT SYSTEM INITIALIZED")
        print(f"Monitoring: {list(self.monitored_pairs.keys())}")
        print("✅ Market hours checking enabled")
        print("✅ Real smart money patterns")
        
    def get_live_data(self, pair_name: str) -> Optional[pd.DataFrame]:
        """Get real-time data for a trading pair"""
        try:
            yahoo_symbol = self.monitored_pairs[pair_name]
            ticker = yf.Ticker(yahoo_symbol)
            
            # Get recent 5-minute data
            data = ticker.history(period="1d", interval="5m")
            
            if len(data) < 20:
                return None
                
            # Ensure volume column
            if 'Volume' not in data.columns or data['Volume'].sum() == 0:
                if pair_name in ['GBPJPY', 'CADCHF']:
                    data['Volume'] = (data['High'] - data['Low']) * 1000000
                else:
                    data['Volume'] = 100000
                    
            data.columns = [col.lower() for col in data.columns]
            return data
            
        except Exception as e:
            print(f"❌ Error fetching {pair_name}: {e}")
            return None
    
    def check_trading_signal(self, pair_name: str) -> Optional[Dict]:
        """Check for trading signal with market hours validation"""
        
        # FIRST: Check if market is open
        if not self.market_checker.is_market_open(pair_name):
            next_open = self.market_checker.get_next_open_time(pair_name)
            print(f"🕒 {pair_name} market closed. Next open: {next_open}")
            return None
        
        data = self.get_live_data(pair_name)
        if data is None or len(data) < 20:
            return None
        
        # Use real day trading signal detection
        signal = self.day_trader.detect_day_trading_signal(data, len(data) - 1)
        
        if signal:
            current_price = data['close'].iloc[-1]
            timestamp = datetime.now()
            
            # Enhanced signal info
            enhanced_signal = {
                'pair': pair_name,
                'direction': signal['direction'],
                'entry_price': current_price,
                'strength': signal['strength'],
                'timestamp': timestamp,
                'session': signal.get('session_multiplier', 1.0),
                'confidence': self.calculate_confidence(signal),
                'risk_level': self.assess_risk_level(pair_name, signal),
                'target_profit': self.calculate_target(current_price, signal),
                'stop_loss': self.calculate_stop_loss(current_price, signal),
                'market_status': 'OPEN'
            }
            
            return enhanced_signal
        
        return None
    
    def calculate_confidence(self, signal: Dict) -> str:
        """Calculate signal confidence based on strength"""
        strength = signal.get('strength', 0)
        
        if strength >= 10:
            return "🔥 HIGH"
        elif strength >= 7:
            return "📈 MEDIUM"
        else:
            return "⚠️ LOW"
    
    def assess_risk_level(self, pair_name: str, signal: Dict) -> str:
        """Assess risk level based on backtesting results"""
        risk_profiles = {
            'NAS100': '🟡 MEDIUM',  # 50% win rate
            'GBPJPY': '🟢 LOW',     # 66.7% win rate
            'CADCHF': '🟡 MEDIUM'   # 50% win rate
        }
        
        return risk_profiles.get(pair_name, '🔴 HIGH')
    
    def calculate_target(self, entry_price: float, signal: Dict) -> float:
        """Calculate profit target"""
        direction = signal['direction']
        strength = signal.get('strength', 5)
        
        target_multiplier = 1.5 + (strength / 20)
        
        if direction == 'BUY':
            return entry_price * (1 + 0.01 * target_multiplier)
        else:
            return entry_price * (1 - 0.01 * target_multiplier)
    
    def calculate_stop_loss(self, entry_price: float, signal: Dict) -> float:
        """Calculate stop loss"""
        direction = signal['direction']
        stop_multiplier = 0.8
        
        if direction == 'BUY':
            return entry_price * (1 - 0.01 * stop_multiplier)
        else:
            return entry_price * (1 + 0.01 * stop_multiplier)
    
    def scan_all_pairs(self) -> List[Dict]:
        """Scan all monitored pairs for signals with market hours check"""
        current_time = datetime.now()
        new_signals = []
        
        print(f"🔍 Scanning pairs at {current_time.strftime('%H:%M:%S')}...")
        
        for pair_name in self.monitored_pairs.keys():
            # Rate limiting
            last_check = self.last_check_time.get(pair_name)
            if last_check and (current_time - last_check).seconds < 60:
                continue
            
            print(f"📊 Checking {pair_name}...")
            
            signal = self.check_trading_signal(pair_name)
            if signal:
                print(f"🚨 REAL SIGNAL DETECTED: {pair_name} {signal['direction']}")
                
                # Store alert
                self.store_alert(signal)
                new_signals.append(signal)
            else:
                market_open = self.market_checker.is_market_open(pair_name)
                if market_open:
                    print(f"✅ {pair_name}: Market open, no signal")
                else:
                    print(f"🕒 {pair_name}: Market closed")
            
            self.last_check_time[pair_name] = current_time
        
        return new_signals
    
    def store_alert(self, signal: Dict):
        """Store alert for web dashboard"""
        alert_data = {
            **signal,
            'id': len(self.recent_alerts) + 1,
            'timestamp': signal['timestamp'].isoformat(),
            'status': 'ACTIVE'
        }
        
        self.recent_alerts.append(alert_data)
        
        # Keep only last 50 alerts
        if len(self.recent_alerts) > 50:
            self.recent_alerts = self.recent_alerts[-50:]
        
        print(f"💾 Real alert stored: {signal['pair']} {signal['direction']} at {signal['entry_price']:.4f}")
    
    def get_dashboard_data(self) -> Dict:
        """Get data for web dashboard"""
        return {
            'monitored_pairs': list(self.monitored_pairs.keys()),
            'recent_alerts': self.recent_alerts[-10:],
            'system_status': 'REAL TRADING MODE',
            'last_scan': max(self.last_check_time.values()).isoformat() if self.last_check_time else None,
            'total_alerts_today': len([a for a in self.recent_alerts 
                                     if datetime.fromisoformat(a['timestamp']).date() == datetime.now().date()]),
            'market_hours': {pair: self.market_checker.is_market_open(pair) for pair in self.monitored_pairs.keys()}
        }
    
    def send_mobile_notification(self, signal: Dict) -> bool:
        """Send push notification to mobile devices via Pushover"""
        if not self.push_api_key or not self.user_tokens:
            print(f"📱 Alert ready: {signal['pair']} {signal['direction']} - Configure Pushover for mobile notifications")
            return False
            
        try:
            import requests
            
            message = f"🚨 {signal['pair']} {signal['direction']}\n"
            message += f"💰 Entry: {signal['entry_price']:.4f}\n"
            message += f"🎯 Target: {signal['target_profit']:.4f}\n"
            message += f"🛡️ Stop: {signal['stop_loss']:.4f}\n"
            message += f"📊 Confidence: {signal['confidence']}\n"
            message += f"⚠️ Risk: {signal['risk_level']}"
            
            for user_token in self.user_tokens:
                response = requests.post("https://api.pushover.net/1/messages.json", data={
                    "token": self.push_api_key,
                    "user": user_token,
                    "title": f"Trading Alert: {signal['pair']}",
                    "message": message,
                    "priority": 1,  # High priority
                    "sound": "cashregister"  # Trading sound
                })
                
                if response.status_code == 200:
                    print(f"📱 Mobile notification sent: {signal['pair']} {signal['direction']}")
                    return True
                else:
                    print(f"❌ Failed to send notification: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Notification error: {e}")
            return False
    
    def configure_pushover(self, api_key: str, user_tokens: List[str]):
        """Configure Pushover settings"""
        self.push_api_key = api_key
        self.user_tokens = user_tokens if isinstance(user_tokens, list) else [user_tokens]
        print(f"✅ Pushover configured for {len(self.user_tokens)} device(s)")
        return True