#!/usr/bin/env python3
"""
Trading Session Optimizer
Session-specific strategies and market timing for optimal day trading
"""

from datetime import datetime, timezone
import pytz
from typing import Dict, List

class TradingSessionOptimizer:
    """Optimize trading strategies based on market sessions and timing"""
    
    def __init__(self):
        self.sessions = {
            'SYDNEY': {'start': 21, 'end': 6, 'timezone': 'Australia/Sydney'},
            'TOKYO': {'start': 0, 'end': 9, 'timezone': 'Asia/Tokyo'}, 
            'LONDON': {'start': 8, 'end': 17, 'timezone': 'Europe/London'},
            'NEW_YORK': {'start': 13, 'end': 22, 'timezone': 'America/New_York'}
        }
        
        # Session characteristics for strategy optimization
        self.session_profiles = {
            'SYDNEY': {
                'volatility': 'LOW',
                'preferred_pairs': ['AUDUSD', 'NZDUSD', 'AUDJPY'],
                'strategies': ['reversal', 'range_trading'],
                'risk_multiplier': 0.8
            },
            'TOKYO': {
                'volatility': 'MEDIUM',
                'preferred_pairs': ['USDJPY', 'EURJPY', 'GBPJPY'],
                'strategies': ['momentum', 'reversal'],
                'risk_multiplier': 1.0
            },
            'LONDON': {
                'volatility': 'HIGH',
                'preferred_pairs': ['EURUSD', 'GBPUSD', 'EURGBP'],
                'strategies': ['momentum', 'breakout'],
                'risk_multiplier': 1.2
            },
            'NEW_YORK': {
                'volatility': 'HIGH',
                'preferred_pairs': ['EURUSD', 'GBPUSD', 'USDCAD', 'US30'],
                'strategies': ['scalping', 'momentum'],
                'risk_multiplier': 1.3
            },
            'LONDON_NY_OVERLAP': {
                'volatility': 'VERY_HIGH',
                'preferred_pairs': ['EURUSD', 'GBPUSD', 'USDCAD'],
                'strategies': ['scalping', 'momentum', 'breakout'],
                'risk_multiplier': 1.5
            }
        }
    
    def get_current_session(self, utc_time=None):
        """Determine the current dominant trading session"""
        if utc_time is None:
            utc_time = datetime.now(timezone.utc)
        
        hour = utc_time.hour
        
        # Check for session overlaps (most important)
        if 13 <= hour < 17:  # London-NY overlap (13:00-17:00 UTC)
            return 'LONDON_NY_OVERLAP'
        elif 8 <= hour < 17:   # London session (08:00-17:00 UTC)
            return 'LONDON'
        elif 13 <= hour < 22:  # New York session (13:00-22:00 UTC)
            return 'NEW_YORK'
        elif 0 <= hour < 9:    # Tokyo session (00:00-09:00 UTC)
            return 'TOKYO'
        else:                  # Sydney/Asian session
            return 'SYDNEY'
    
    def get_session_strategy(self, pair: str, current_session: str = None):
        """Get optimized strategy for pair and session"""
        if current_session is None:
            current_session = self.get_current_session()
        
        session_profile = self.session_profiles.get(current_session, self.session_profiles['LONDON'])
        
        # Check if pair is preferred for this session
        pair_preference = 'HIGH' if pair in session_profile['preferred_pairs'] else 'MEDIUM'
        
        return {
            'session': current_session,
            'volatility': session_profile['volatility'],
            'preferred_strategies': session_profile['strategies'],
            'risk_multiplier': session_profile['risk_multiplier'],
            'pair_preference': pair_preference
        }
    
    def optimize_signal_for_session(self, signal: Dict, pair: str):
        """Optimize trading signal based on current session"""
        session_info = self.get_session_strategy(pair)
        
        # Adjust confidence based on session preference
        confidence_multiplier = 1.0
        if session_info['pair_preference'] == 'HIGH':
            confidence_multiplier = 1.2
        elif session_info['volatility'] == 'VERY_HIGH':
            confidence_multiplier = 1.1
        
        # Adjust signal parameters
        optimized_signal = signal.copy()
        optimized_signal['confidence'] = min(95, signal['confidence'] * confidence_multiplier)
        optimized_signal['session_info'] = session_info
        
        # Session-specific pattern preferences
        pattern_type = signal.get('pattern_type', 'momentum')
        if pattern_type in session_info['preferred_strategies']:
            optimized_signal['session_match'] = True
            optimized_signal['confidence'] = min(95, optimized_signal['confidence'] * 1.1)
        else:
            optimized_signal['session_match'] = False
        
        return optimized_signal
    
    def get_session_risk_parameters(self, current_session: str = None):
        """Get session-specific risk management parameters"""
        if current_session is None:
            current_session = self.get_current_session()
        
        session_profile = self.session_profiles.get(current_session, self.session_profiles['LONDON'])
        
        base_risk = 0.005  # 0.5% base risk per trade
        
        return {
            'risk_per_trade': base_risk * session_profile['risk_multiplier'],
            'max_positions': self._get_max_positions(session_profile['volatility']),
            'stop_loss_multiplier': self._get_stop_multiplier(session_profile['volatility']),
            'take_profit_multiplier': self._get_profit_multiplier(session_profile['volatility'])
        }
    
    def _get_max_positions(self, volatility: str) -> int:
        """Get maximum concurrent positions based on volatility"""
        volatility_map = {
            'LOW': 3,
            'MEDIUM': 2, 
            'HIGH': 2,
            'VERY_HIGH': 1  # Focus on fewer trades during high volatility
        }
        return volatility_map.get(volatility, 2)
    
    def _get_stop_multiplier(self, volatility: str) -> float:
        """Get stop loss multiplier based on session volatility"""
        volatility_map = {
            'LOW': 0.8,      # Tighter stops in low volatility
            'MEDIUM': 1.0,
            'HIGH': 1.2,     # Wider stops in high volatility
            'VERY_HIGH': 1.4
        }
        return volatility_map.get(volatility, 1.0)
    
    def _get_profit_multiplier(self, volatility: str) -> float:
        """Get take profit multiplier based on session volatility"""
        volatility_map = {
            'LOW': 1.5,      # Lower targets in low volatility
            'MEDIUM': 2.0,
            'HIGH': 2.5,     # Higher targets in high volatility
            'VERY_HIGH': 3.0
        }
        return volatility_map.get(volatility, 2.0)
    
    def is_high_impact_news_time(self, utc_time=None):
        """Check if current time coincides with high-impact news releases"""
        if utc_time is None:
            utc_time = datetime.now(timezone.utc)
        
        hour, minute = utc_time.hour, utc_time.minute
        
        # Common high-impact news times (UTC)
        high_impact_times = [
            (8, 30),   # London open
            (12, 30),  # ECB announcements
            (13, 30),  # US market open
            (14, 30),  # US data releases
            (18, 0),   # FOMC, etc.
        ]
        
        for impact_hour, impact_min in high_impact_times:
            if hour == impact_hour and abs(minute - impact_min) <= 30:
                return True
        
        return False
    
    def get_session_summary(self):
        """Get summary of current session characteristics"""
        current_session = self.get_current_session()
        session_profile = self.session_profiles.get(current_session)
        risk_params = self.get_session_risk_parameters(current_session)
        high_impact = self.is_high_impact_news_time()
        
        return {
            'session': current_session,
            'volatility': session_profile['volatility'],
            'preferred_pairs': session_profile['preferred_pairs'],
            'strategies': session_profile['strategies'],
            'risk_per_trade': risk_params['risk_per_trade'],
            'max_positions': risk_params['max_positions'],
            'high_impact_news': high_impact,
            'utc_time': datetime.now(timezone.utc).strftime('%H:%M UTC')
        }

# Market timing utilities
def get_market_timing_advice():
    """Get current market timing advice"""
    optimizer = TradingSessionOptimizer()
    summary = optimizer.get_session_summary()
    
    advice = []
    
    # Session-specific advice
    if summary['session'] == 'LONDON_NY_OVERLAP':
        advice.append("🔥 PRIME TIME: London-NY overlap - highest volatility and volume")
        advice.append("💡 Focus on major pairs (EURUSD, GBPUSD) with scalping strategies")
    elif summary['session'] == 'LONDON':
        advice.append("🇬🇧 LONDON SESSION: Good momentum opportunities")
        advice.append("💡 European pairs are most active")
    elif summary['session'] == 'NEW_YORK':
        advice.append("🇺🇸 NEW YORK SESSION: USD pairs in focus")
        advice.append("💡 Good for momentum and trend following")
    elif summary['session'] == 'TOKYO':
        advice.append("🇯🇵 TOKYO SESSION: JPY pairs active")
        advice.append("💡 Look for range-bound strategies")
    else:
        advice.append("🌏 SYDNEY SESSION: Lower volatility")
        advice.append("💡 Consider range trading or wait for major sessions")
    
    # Risk advice
    if summary['volatility'] == 'VERY_HIGH':
        advice.append("⚠️ VERY HIGH volatility - reduce position sizes")
    elif summary['volatility'] == 'LOW':
        advice.append("📊 LOW volatility - consider tighter stops and targets")
    
    # News impact
    if summary['high_impact_news']:
        advice.append("📰 HIGH IMPACT NEWS TIME - exercise extra caution")
    
    return advice

if __name__ == "__main__":
    # Test session optimization
    optimizer = TradingSessionOptimizer()
    summary = optimizer.get_session_summary()
    advice = get_market_timing_advice()
    
    print("🕐 TRADING SESSION ANALYSIS")
    print("=" * 50)
    print(f"📅 Current Time: {summary['utc_time']}")
    print(f"🌍 Active Session: {summary['session']}")
    print(f"📊 Volatility: {summary['volatility']}")
    print(f"💰 Risk per Trade: {summary['risk_per_trade']:.1%}")
    print(f"📈 Max Positions: {summary['max_positions']}")
    print(f"🎯 Preferred Pairs: {', '.join(summary['preferred_pairs'])}")
    print(f"🔧 Strategies: {', '.join(summary['strategies'])}")
    
    print(f"\n💡 TRADING ADVICE:")
    for tip in advice:
        print(f"   {tip}")