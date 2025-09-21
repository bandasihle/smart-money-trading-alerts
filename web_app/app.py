from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import json
import os
import sys
import random
from datetime import datetime

# Add parent directory to path to import our trading modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our trading alert system
try:
    # Import from local trading_system.py file
    from trading_system import TradingAlertSystem, MarketHoursChecker
    print("✅ REAL TRADING SYSTEM LOADED")
    REAL_SYSTEM = True
except ImportError as e:
    print(f"⚠️ Import warning: Could not import real trading system: {e}")
    print("Using mock classes for demonstration")
    REAL_SYSTEM = False
    
    # Mock classes for deployment when model not available
    class TradingAlertSystem:
        def __init__(self):
            self.recent_alerts = []
            self.monitored_pairs = ['NAS100', 'GBPJPY', 'CADCHF']
            print("📱 Mock Trading Alert System Initialized")
            
        def scan_all_pairs(self):
            # NO MOCK SIGNALS - market hours respected
            return []
            
        def get_dashboard_data(self):
            return {
                'recent_alerts': [], 
                'total_alerts_today': 0,
                'monitored_pairs': self.monitored_pairs,
                'system_status': 'MOCK MODE - NO SIGNALS',
                'market_hours': {pair: False for pair in self.monitored_pairs}
            }
            
        def send_mobile_notification(self, signal):
            print(f"📱 Mock notification: {signal['pair']} {signal['direction']}")
            return True

app = Flask(__name__)
CORS(app)

# Initialize alert system
if REAL_SYSTEM:
    alert_system = TradingAlertSystem(paper_trading=True)
    print("🔥 REAL TRADING SYSTEM ACTIVE")
else:
    alert_system = TradingAlertSystem()
    print("⚠️ MOCK SYSTEM ACTIVE")

@app.route('/')
def dashboard():
    """Serve the main dashboard"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, 'index.html')
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
        <head><title>Trading Alert System</title></head>
        <body>
            <h1>🚀 Trading Alert System</h1>
            <p>✅ Flask backend is running!</p>
            <p>📍 HTML file not found, but API is working.</p>
            <p>🔗 Try: <a href="/api/dashboard">/api/dashboard</a></p>
            <p>🔗 Try: <a href="/health">/health</a></p>
        </body>
        </html>
        """

@app.route('/api/dashboard')
def get_dashboard_data():
    """API endpoint for dashboard data"""
    try:
        data = alert_system.get_dashboard_data()
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/scan')
def manual_scan():
    """Manual scan endpoint"""
    try:
        new_signals = alert_system.scan_all_pairs()
        return jsonify({
            'success': True,
            'signals_found': len(new_signals),
            'signals': new_signals,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/alerts/recent')
def get_recent_alerts():
    """Get recent alerts"""
    try:
        alerts = alert_system.recent_alerts[-10:]  # Last 10 alerts
        return jsonify({
            'success': True,
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/config/mobile', methods=['POST'])
def configure_mobile():
    """Configure mobile notifications"""
    try:
        from flask import request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No configuration data provided',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        api_key = data.get('api_key')
        user_token = data.get('user_token')
        
        if not api_key or not user_token:
            return jsonify({
                'success': False,
                'error': 'API key and user token are required',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Configure the alert system
        if hasattr(alert_system, 'configure_pushover'):
            alert_system.configure_pushover(api_key, [user_token])
            
            return jsonify({
                'success': True,
                'message': 'Mobile notifications configured successfully',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Mobile notifications not supported in current mode',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/test/notification', methods=['POST'])
def test_notification():
    """Test mobile notification"""
    try:
        test_signal = {
            'pair': 'TEST',
            'direction': 'BUY',
            'entry_price': 1.2345,
            'target_profit': 1.2500,
            'stop_loss': 1.2200,
            'confidence': '🔥 HIGH',
            'risk_level': '🟢 LOW',
            'timestamp': datetime.now()
        }
        
        success = alert_system.send_mobile_notification(test_signal)
        
        return jsonify({
            'success': success,
            'message': 'Test notification sent' if success else 'Failed to send test notification',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting Smart Money Trading Alert Web App")
    print("📱 Dashboard: http://localhost:5000")
    print("🔍 API Health: http://localhost:5000/health")
    print("📊 API Dashboard: http://localhost:5000/api/dashboard")
    
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)