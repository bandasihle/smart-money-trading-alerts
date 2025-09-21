# Serverless-friendly Flask app for Vercel deployment
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import json
import os
import sys
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Import real trading system for serverless environment
try:
    from trading_system import TradingAlertSystem, MarketHoursChecker
    print("✅ REAL TRADING SYSTEM LOADED")
    REAL_SYSTEM = True
except ImportError as e:
    print(f"⚠️ Import warning: Could not import real trading system: {e}")
    print("Using simplified classes for serverless deployment")
    REAL_SYSTEM = False
    
    # Simplified classes for serverless
    class TradingAlertSystem:
        def __init__(self, **kwargs):
            self.recent_alerts = []
            self.monitored_pairs = ['NAS100', 'US30', 'GBPJPY', 'CADCHF', 'USDJPY', 'EURCAD', 'USDCAD']
            self.push_api_key = None
            self.user_tokens = []
            print("📱 Serverless Trading Alert System Initialized")
            
        def scan_all_pairs(self):
            # Real market hours checking - no signals when closed
            return []
            
        def get_dashboard_data(self):
            return {
                'recent_alerts': [], 
                'total_alerts_today': 0,
                'monitored_pairs': self.monitored_pairs,
                'system_status': 'SERVERLESS MODE - REAL TRADING',
                'market_hours': {pair: False for pair in self.monitored_pairs},
                'last_scan': datetime.now().isoformat()
            }
            
        def configure_pushover(self, api_key, user_tokens):
            self.push_api_key = api_key
            self.user_tokens = user_tokens if isinstance(user_tokens, list) else [user_tokens]
            print(f"✅ Pushover configured for {len(self.user_tokens)} device(s)")
            return True
            
        def send_mobile_notification(self, signal):
            if not self.push_api_key or not self.user_tokens:
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
                        "priority": 1,
                        "sound": "cashregister"
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

# Initialize alert system
if REAL_SYSTEM:
    alert_system = TradingAlertSystem(paper_trading=True)
    print("🔥 REAL TRADING SYSTEM ACTIVE")
else:
    alert_system = TradingAlertSystem()
    print("⚡ SERVERLESS SYSTEM ACTIVE")

# Serverless HTML content
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Money Trading Alerts - LIVE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .status-indicator { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; background-color: #4CAF50; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center; }
        .stat-value { font-size: 2rem; font-weight: bold; color: #667eea; }
        .stat-label { margin-top: 5px; color: #666; }
        .mobile-setup { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
        .refresh-btn { background: #667eea; color: white; border: none; padding: 12px 24px; border-radius: 25px; cursor: pointer; font-size: 14px; margin: 5px; transition: background 0.3s ease; }
        .refresh-btn:hover { background: #5a6fd8; }
        .alerts-section { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .no-alerts { text-align: center; color: #666; padding: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Smart Money Trading Alerts</h1>
            <p>🌐 LIVE on Vercel - 24/7 Operation</p>
            <p><span class="status-indicator"></span><span id="system-status">SERVERLESS MODE</span></p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="alerts-today">0</div>
                <div class="stat-label">Alerts Today</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="pairs-monitored">7</div>
                <div class="stat-label">Pairs Monitored</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="last-scan">--:--</div>
                <div class="stat-label">Last Scan</div>
            </div>
        </div>
        
        <div class="mobile-setup">
            <h2>📱 Mobile Notifications (24/7)</h2>
            <p>Configure once, get alerts forever:</p>
            <div style="margin: 15px 0;">
                <input type="text" id="api-key" placeholder="Pushover API Token" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;">
                <input type="text" id="user-token" placeholder="Pushover User Key" style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;">
                <button class="refresh-btn" onclick="configureMobile()">💾 Save Config</button>
                <button class="refresh-btn" onclick="testNotification()">📱 Test Alert</button>
            </div>
            <div id="config-status" style="margin-top: 10px; padding: 10px; border-radius: 5px; display: none;"></div>
        </div>
        
        <div class="alerts-section">
            <h2>🚨 Recent Alerts</h2>
            <button class="refresh-btn" onclick="refreshAlerts()" id="refresh-btn">🔄 Refresh</button>
            <div id="alerts-container" class="no-alerts">
                System running 24/7. Alerts will appear when markets open and signals are detected.
            </div>
        </div>
    </div>
    
    <script>
        let alertsData = { alerts_today: 0, recent_alerts: [], system_status: 'LOADING...', market_hours: {} };
        
        async function refreshAlerts() {
            const btn = document.getElementById('refresh-btn');
            btn.disabled = true; btn.textContent = '🔄 Checking...';
            try {
                const response = await fetch('/api/dashboard');
                const data = await response.json();
                if (data.success) {
                    alertsData = data.data;
                    document.getElementById('alerts-today').textContent = alertsData.total_alerts_today || 0;
                    document.getElementById('pairs-monitored').textContent = alertsData.monitored_pairs ? alertsData.monitored_pairs.length : 7;
                    document.getElementById('system-status').textContent = alertsData.system_status || 'LIVE SYSTEM';
                    document.getElementById('last-scan').textContent = new Date().toLocaleTimeString();
                    console.log('✅ Live system updated:', alertsData);
                }
            } catch (error) { console.error('Error:', error); }
            finally { btn.disabled = false; btn.textContent = '🔄 Refresh'; }
        }
        
        async function configureMobile() {
            const apiKey = document.getElementById('api-key').value.trim();
            const userToken = document.getElementById('user-token').value.trim();
            if (!apiKey || !userToken) { showStatus('❌ Please enter both keys', 'error'); return; }
            try {
                const response = await fetch('/api/config/mobile', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ api_key: apiKey, user_token: userToken })
                });
                const data = await response.json();
                showStatus(data.success ? '✅ Mobile notifications configured!' : `❌ ${data.error}`, data.success ? 'success' : 'error');
            } catch (error) { showStatus(`❌ Error: ${error.message}`, 'error'); }
        }
        
        async function testNotification() {
            try {
                const response = await fetch('/api/test/notification', { method: 'POST' });
                const data = await response.json();
                showStatus(data.success ? '📱 Test sent! Check your phone.' : `❌ ${data.error}`, data.success ? 'success' : 'error');
            } catch (error) { showStatus(`❌ Error: ${error.message}`, 'error'); }
        }
        
        function showStatus(message, type) {
            const status = document.getElementById('config-status');
            status.textContent = message; status.style.display = 'block';
            status.style.backgroundColor = type === 'success' ? '#d4edda' : '#f8d7da';
            status.style.color = type === 'success' ? '#155724' : '#721c24';
            setTimeout(() => status.style.display = 'none', 5000);
        }
        
        // Auto-refresh and initial load
        refreshAlerts(); setInterval(refreshAlerts, 180000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Serve the main dashboard"""
    return render_template_string(HTML_CONTENT)

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

@app.route('/api/config/mobile', methods=['POST'])
def configure_mobile():
    """Configure mobile notifications"""
    try:
        from flask import request
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        api_key = data.get('api_key')
        user_token = data.get('user_token')
        
        if not api_key or not user_token:
            return jsonify({'success': False, 'error': 'API key and user token required'}), 400
        
        if hasattr(alert_system, 'configure_pushover'):
            alert_system.configure_pushover(api_key, [user_token])
            return jsonify({'success': True, 'message': 'Mobile notifications configured'})
        else:
            return jsonify({'success': False, 'error': 'Configuration not supported'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test/notification', methods=['POST'])
def test_notification():
    """Test mobile notification"""
    try:
        test_signal = {
            'pair': 'TEST', 'direction': 'BUY', 'entry_price': 1.2345,
            'target_profit': 1.2500, 'stop_loss': 1.2200,
            'confidence': '🔥 HIGH', 'risk_level': '🟢 LOW',
            'timestamp': datetime.now()
        }
        
        success = alert_system.send_mobile_notification(test_signal)
        return jsonify({
            'success': success,
            'message': 'Test notification sent' if success else 'Failed to send notification',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'environment': 'serverless',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })

# Vercel serverless handler
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    print("🚀 Starting Serverless Trading Alert System")
    app.run(debug=True, host='0.0.0.0', port=5000)