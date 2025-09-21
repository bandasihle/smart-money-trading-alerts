from flask import Flask, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def dashboard():
    """Serve a simple test page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Alert Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { text-align: center; color: #333; }
            .status { background: #4CAF50; color: white; padding: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Trading Alert System</h1>
            <div class="status">
                <h2>✅ System Running Successfully!</h2>
                <p>Flask backend is operational</p>
                <p>Time: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/test')
def test_api():
    """Test API endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'API is working!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting Trading Alert Test Server")
    print("📱 Visit: http://localhost:5000")
    print("🔍 API Test: http://localhost:5000/api/test")
    print("❤️ Health: http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)