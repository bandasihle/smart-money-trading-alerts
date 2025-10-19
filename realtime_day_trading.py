#!/usr/bin/env python3
"""
Real-Time Day Trading Signal Generator
Continuous monitoring and signal generation for intraday trading
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from day_trading_optimizer import DayTradingPatternDetector, DayTradingRiskManager, get_intraday_data
from index import get_real_market_data
import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
import json

class RealTimeDayTradingSystem:
    """Real-time day trading signal generator and monitor"""
    
    def __init__(self, pairs=None, update_interval=300):  # 5-minute updates
        self.pairs = pairs or {
            'EURUSD': 'EURUSD=X',
            'GBPJPY': 'GBPJPY=X', 
            'USDJPY': 'USDJPY=X',
            'USDCAD': 'USDCAD=X',
            'US30': '^DJI'
        }
        self.update_interval = update_interval  # seconds
        self.detector = DayTradingPatternDetector()
        self.risk_manager = DayTradingRiskManager()
        self.active_signals = {}
        self.account_balance = 10000
        
    def get_trading_session(self):
        """Determine current trading session"""
        now = datetime.now()
        hour = now.hour
        
        if 2 <= hour < 12:
            return "LONDON"
        elif 13 <= hour < 22:
            return "NEW_YORK"
        elif 22 <= hour or hour < 2:
            return "ASIA"
        else:
            return "OVERLAP"  # London-NY overlap (most volatile)
    
    def is_high_impact_time(self):
        """Check if current time is high-impact for trading"""
        now = datetime.now()
        hour, minute = now.hour, now.minute
        
        # Market open times (high volatility)
        high_impact_times = [
            (8, 30),   # London open
            (14, 30),  # NY open
            (21, 0),   # Asian session
        ]
        
        for impact_hour, impact_min in high_impact_times:
            if abs(hour - impact_hour) <= 1:  # Within 1 hour of major session
                return True
        
        return False
    
    def scan_for_signals(self):
        """Scan all pairs for real-time trading signals"""
        session = self.get_trading_session()
        high_impact = self.is_high_impact_time()
        
        print(f"\n🕐 {datetime.now().strftime('%H:%M:%S')} - {session} SESSION {'(HIGH IMPACT)' if high_impact else ''}")
        print("=" * 60)
        
        new_signals = {}
        
        for pair_name, symbol in self.pairs.items():
            try:
                # Get fresh intraday data
                if high_impact:
                    data = get_intraday_data(symbol, period="1d", interval="5m")  # 5-min for high impact
                else:
                    data = get_intraday_data(symbol, period="2d", interval="15m")  # 15-min for normal
                
                if len(data) >= 20:
                    # Detect patterns
                    signals = self.detector.analyze_intraday_patterns(data)
                    
                    if signals:
                        # Get current live price
                        current_price = data['Close'].iloc[-1]
                        
                        # Filter signals by session preference
                        session_filtered = self.filter_signals_by_session(signals, session)
                        
                        if session_filtered:
                            best_signal = session_filtered[0]  # Highest confidence
                            
                            # Calculate position sizing
                            trade_setup = self.risk_manager.calculate_day_trading_position_size(
                                best_signal, current_price, self.account_balance
                            )
                            
                            if trade_setup['position_size'] > 0:
                                signal_data = {
                                    'pair': pair_name,
                                    'signal': best_signal,
                                    'trade_setup': trade_setup,
                                    'current_price': current_price,
                                    'session': session,
                                    'timestamp': datetime.now(),
                                    'high_impact': high_impact
                                }
                                
                                new_signals[pair_name] = signal_data
                                
                                print(f"🎯 {pair_name} - NEW SIGNAL!")
                                print(f"   Pattern: {best_signal['pattern']} ({best_signal['pattern_type']})")
                                print(f"   Direction: {best_signal['direction']}")
                                print(f"   Confidence: {best_signal['confidence']:.1f}%")
                                print(f"   Entry: {trade_setup['entry_price']:.4f}")
                                print(f"   Stop: {trade_setup['stop_loss']:.4f}")
                                print(f"   Target: {trade_setup['take_profit']:.4f}")
                                print(f"   Size: {trade_setup['position_size']:.2f}")
                                print(f"   R:R: 1:{trade_setup['risk_reward_ratio']:.1f}")
                            else:
                                print(f"{pair_name} - Signal found but risk limits exceeded")
                        else:
                            print(f"{pair_name} - Signals filtered by session preference")
                    else:
                        print(f"{pair_name} - No patterns detected")
                else:
                    print(f"{pair_name} - Insufficient data")
                    
            except Exception as e:
                print(f"{pair_name} - Error: {e}")
            
            time.sleep(0.5)  # Avoid rate limits
        
        self.active_signals = new_signals
        return new_signals
    
    def filter_signals_by_session(self, signals, session):
        """Filter signals based on trading session preferences"""
        session_preferences = {
            'LONDON': ['momentum', 'reversal'],      # European session
            'NEW_YORK': ['scalping', 'momentum'],    # US session  
            'ASIA': ['reversal', 'gap_fill'],        # Asian session
            'OVERLAP': ['scalping', 'momentum']      # High volatility overlap
        }
        
        preferred_types = session_preferences.get(session, ['momentum'])
        
        filtered = []
        for signal in signals:
            if signal.get('pattern_type') in preferred_types:
                filtered.append(signal)
        
        return filtered or signals  # Return all if none match session preference
    
    def generate_alert(self, signal_data):
        """Generate trading alert for a signal"""
        alert = {
            'timestamp': signal_data['timestamp'].strftime('%H:%M:%S'),
            'pair': signal_data['pair'],
            'action': f"{signal_data['signal']['direction']} {signal_data['pair']}",
            'entry': signal_data['trade_setup']['entry_price'],
            'stop': signal_data['trade_setup']['stop_loss'],
            'target': signal_data['trade_setup']['take_profit'],
            'confidence': signal_data['signal']['confidence'],
            'pattern': signal_data['signal']['pattern'],
            'session': signal_data['session'],
            'high_impact': signal_data['high_impact']
        }
        return alert
    
    def run_continuous_monitoring(self, duration_minutes=60):
        """Run continuous signal monitoring for specified duration"""
        print("STARTING REAL-TIME DAY TRADING MONITOR")
        print(f"Duration: {duration_minutes} minutes")
        print(f"Update interval: {self.update_interval} seconds")
        print("=" * 60)
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        all_alerts = []
        
        while datetime.now() < end_time:
            try:
                # Scan for new signals
                signals = self.scan_for_signals()
                
                # Generate alerts for new signals
                for pair, signal_data in signals.items():
                    alert = self.generate_alert(signal_data)
                    all_alerts.append(alert)
                    
                    print(f"\n🚨 TRADING ALERT:")
                    print(f"   {alert['action']} @ {alert['entry']:.4f}")
                    print(f"   Stop: {alert['stop']:.4f} | Target: {alert['target']:.4f}")
                    print(f"   Confidence: {alert['confidence']:.1f}% | Pattern: {alert['pattern']}")
                
                if not signals:
                    print("No trading opportunities at this time")
                
                print(f"\n⏰ Next scan in {self.update_interval} seconds...")
                time.sleep(self.update_interval)
                
            except KeyboardInterrupt:
                print(f"\n⏹️ Monitoring stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Error during monitoring: {e}")
                time.sleep(30)  # Wait before retrying
        
        # Summary
        print("\n" + "=" * 60)
        print("MONITORING SESSION COMPLETE")
        print(f"⏰ Duration: {(datetime.now() - start_time).total_seconds() / 60:.1f} minutes")
        print(f"🎯 Total alerts generated: {len(all_alerts)}")
        
        if all_alerts:
            print(f"\n📋 ALERT SUMMARY:")
            for alert in all_alerts[-5:]:  # Last 5 alerts
                print(f"   {alert['timestamp']} - {alert['action']} ({alert['confidence']:.1f}%)")
        
        return all_alerts

def run_day_trading_scanner():
    """Run the day trading signal scanner"""
    scanner = RealTimeDayTradingSystem()
    
    print("🎯 DAY TRADING SIGNAL SCANNER")
    print("Choose monitoring duration:")
    print("1. Quick scan (1 minute)")
    print("2. Short session (15 minutes)")
    print("3. Full session (60 minutes)")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        durations = {'1': 1, '2': 15, '3': 60}
        duration = durations.get(choice, 1)
        
        alerts = scanner.run_continuous_monitoring(duration_minutes=duration)
        
        print(f"\n🎉 Scanning complete! Found {len(alerts)} trading opportunities")
        
    except KeyboardInterrupt:
        print(f"\n👋 Scanner stopped by user")

if __name__ == "__main__":
    run_day_trading_scanner()