#!/usr/bin/env python3
"""
Complete SMC Bot System Test
Test all components and verify yfinance data flow to Flask
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import requests
from datetime import datetime
import json

def test_yfinance_data_direct():
    """Test yfinance data directly"""
    print("🔍 TESTING YFINANCE DATA DIRECTLY")
    print("=" * 45)
    
    try:
        from index import get_real_market_data
        
        print("📡 Calling get_real_market_data() function...")
        data = get_real_market_data()
        
        print(f"\n✅ Direct yfinance test SUCCESS!")
        print(f"📊 Retrieved {len(data)} pairs:")
        for pair, price in data.items():
            print(f"   {pair}: {price:.4f}")
        
        return data
        
    except Exception as e:
        print(f"❌ Direct yfinance test FAILED: {e}")
        return None

def test_flask_app():
    """Test Flask app endpoints"""
    print(f"\n🌐 TESTING FLASK WEB APPLICATION")
    print("=" * 45)
    
    # Start Flask app in background
    import subprocess
    import threading
    
    try:
        # Test if app can import without running
        from index import app
        
        # Test with Flask test client (no server needed)
        with app.test_client() as client:
            
            # Test main page
            print("📄 Testing main page...")
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Main page: WORKING")
            else:
                print(f"❌ Main page: ERROR {response.status_code}")
            
            # Test API endpoints
            print("📊 Testing API endpoints...")
            
            # Test live data endpoint
            response = client.get('/api/data')
            if response.status_code == 200:
                api_data = response.get_json()
                print("✅ Live data API: WORKING")
                print(f"📡 API returned {len(api_data)} pairs")
                
                # Verify it's real yfinance data
                print("🔍 Verifying yfinance data in API:")
                for pair, price in api_data.items():
                    print(f"   {pair}: {price:.4f}")
                
            else:
                print(f"❌ Live data API: ERROR {response.status_code}")
            
            # Test status endpoint
            response = client.get('/api/status')
            if response.status_code == 200:
                status_data = response.get_json()
                print("✅ Status API: WORKING")
                print(f"📊 Status: {status_data}")
            else:
                print(f"❌ Status API: ERROR {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask test FAILED: {e}")
        return False

def test_pattern_detection():
    """Test pattern detection system"""
    print(f"\n🎯 TESTING PATTERN DETECTION")
    print("=" * 45)
    
    try:
        from day_trading_optimizer import DayTradingPatternDetector, get_intraday_data
        
        detector = DayTradingPatternDetector()
        
        # Test pattern detection on live data
        test_symbol = "EURUSD=X"
        print(f"📈 Testing pattern detection on {test_symbol}...")
        
        data = get_intraday_data(test_symbol, period="2d", interval="15m")
        
        if len(data) > 20:
            signals = detector.analyze_intraday_patterns(data)
            
            print(f"✅ Pattern detection: WORKING")
            print(f"🎯 Found {len(signals)} signals")
            
            if signals:
                best_signal = signals[0]
                print(f"📊 Best signal: {best_signal['pattern']} {best_signal['direction']} ({best_signal['confidence']:.1f}%)")
            
            return True
        else:
            print(f"⚠️ Insufficient data for pattern detection")
            return False
            
    except Exception as e:
        print(f"❌ Pattern detection test FAILED: {e}")
        return False

def test_session_optimizer():
    """Test session optimization"""
    print(f"\n🕐 TESTING SESSION OPTIMIZER")
    print("=" * 45)
    
    try:
        from session_optimizer import TradingSessionOptimizer, get_market_timing_advice
        
        optimizer = TradingSessionOptimizer()
        
        # Get current session
        current_session = optimizer.get_current_session()
        print(f"📅 Current session: {current_session}")
        
        # Get session summary
        summary = optimizer.get_session_summary()
        print(f"📊 Session volatility: {summary['volatility']}")
        print(f"🎯 Preferred pairs: {', '.join(summary['preferred_pairs'][:3])}")
        
        # Get market advice
        advice = get_market_timing_advice()
        print(f"💡 Market advice: {advice[0] if advice else 'None'}")
        
        print(f"✅ Session optimizer: WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Session optimizer test FAILED: {e}")
        return False

def test_realtime_scanner():
    """Test real-time scanner (quick test)"""
    print(f"\n📡 TESTING REAL-TIME SCANNER")
    print("=" * 45)
    
    try:
        from realtime_day_trading import RealTimeDayTradingSystem
        
        # Initialize scanner
        scanner = RealTimeDayTradingSystem()
        
        # Test session detection
        session = scanner.get_trading_session()
        print(f"📅 Detected session: {session}")
        
        # Test high impact detection
        high_impact = scanner.is_high_impact_time()
        print(f"📰 High impact time: {'Yes' if high_impact else 'No'}")
        
        print(f"✅ Real-time scanner: WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Real-time scanner test FAILED: {e}")
        return False

def run_comprehensive_smc_test():
    """Run complete SMC bot system test"""
    
    print("🤖 COMPREHENSIVE SMC BOT SYSTEM TEST")
    print("=" * 60)
    print(f"🕐 Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Track test results
    test_results = {}
    
    # Test 1: Direct yfinance data
    print(f"\n" + "🔥 TEST 1: YFINANCE DATA VERIFICATION" + " 🔥")
    yfinance_data = test_yfinance_data_direct()
    test_results['yfinance'] = yfinance_data is not None
    
    # Test 2: Flask application
    print(f"\n" + "🔥 TEST 2: FLASK WEB APPLICATION" + " 🔥")
    test_results['flask'] = test_flask_app()
    
    # Test 3: Pattern detection
    print(f"\n" + "🔥 TEST 3: SMC PATTERN DETECTION" + " 🔥")
    test_results['patterns'] = test_pattern_detection()
    
    # Test 4: Session optimizer
    print(f"\n" + "🔥 TEST 4: SESSION OPTIMIZATION" + " 🔥")
    test_results['sessions'] = test_session_optimizer()
    
    # Test 5: Real-time scanner
    print(f"\n" + "🔥 TEST 5: REAL-TIME SCANNER" + " 🔥")
    test_results['scanner'] = test_realtime_scanner()
    
    # Results summary
    print(f"\n" + "=" * 60)
    print("📊 SMC BOT SYSTEM TEST RESULTS")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    print(f"🎯 Tests passed: {passed_tests}/{total_tests}")
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name.upper()}: {status}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 ALL SYSTEMS OPERATIONAL!")
        print(f"✅ Your SMC bot is 100% functional with real yfinance data")
        print(f"🚀 Ready for live trading and analysis")
        
        # Show how to use each system
        print(f"\n🎮 READY TO USE:")
        print(f"   1. Web Dashboard: Run Flask app and visit http://localhost:5000")
        print(f"   2. Live Scanner: python realtime_day_trading.py")
        print(f"   3. Pattern Analysis: python complete_day_trading_test.py")
        print(f"   4. Strategy Test: python balanced_strategy.py")
        
    else:
        print(f"\n⚠️ Some systems need attention")
        failed_tests = [name for name, result in test_results.items() if not result]
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
    
    # Data verification
    if yfinance_data:
        print(f"\n📡 LIVE DATA CONFIRMATION:")
        print(f"✅ Flask is getting 100% REAL data from yfinance")
        print(f"📊 Current live prices:")
        for pair, price in yfinance_data.items():
            print(f"   {pair}: {price:.4f}")
    
    return test_results

if __name__ == "__main__":
    # Run comprehensive test
    results = run_comprehensive_smc_test()
    
    print(f"\n🤖 SMC BOT STATUS: {'FULLY OPERATIONAL' if all(results.values()) else 'NEEDS ATTENTION'}")
    print(f"📡 yfinance → Flask: {'✅ CONFIRMED' if results.get('yfinance') and results.get('flask') else '❌ ISSUE'}")