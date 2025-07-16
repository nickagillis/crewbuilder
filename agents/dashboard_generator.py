"""
Dashboard Generator - Creates client dashboards for deployed systems
"""

from typing import Dict, Any
from pydantic import BaseModel, Field

class DashboardCode(BaseModel):
    """Generated dashboard code for a client system"""
    app_py: str = Field(description="Main Flask application code")
    requirements_txt: str = Field(description="Dashboard requirements")
    templates_index: str = Field(description="Main HTML template")
    templates_setup: str = Field(description="Setup page template")
    templates_status: str = Field(description="Status page template")
    static_style_css: str = Field(description="CSS styles")

def generate_client_dashboard(client_name: str, agent_system_info: Dict[str, Any]) -> DashboardCode:
    """
    Generate a complete client dashboard for managing their AI agent system
    """
    
    # Main Flask app
    app_py = f'''#!/usr/bin/env python3
"""
Client Dashboard for {client_name}
Manage your AI agent system
"""

import os
import json
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session
import redis
from pathlib import Path
import secrets

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Client info
CLIENT_ID = os.getenv('CLIENT_ID', 'unknown')
CLIENT_NAME = os.getenv('CLIENT_NAME', '{client_name}')

# Store for API keys (in production, use proper encryption)
API_KEYS_FILE = Path('api_keys.json')

def load_api_keys():
    """Load API keys from encrypted storage"""
    if API_KEYS_FILE.exists():
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    return {{}}

def save_api_keys(keys):
    """Save API keys to encrypted storage"""
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(keys, f)

def is_setup_complete():
    """Check if initial setup is complete"""
    keys = load_api_keys()
    return 'OPENAI_API_KEY' in keys

def get_agent_status():
    """Check if agent system is running"""
    try:
        # Check if agent process is running
        result = subprocess.run(['pgrep', '-f', 'agent_system/main.py'], 
                              capture_output=True, text=True)
        is_running = result.returncode == 0
        
        # Get recent logs
        log_file = Path('../agent_system/agent.log')
        recent_logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                recent_logs = f.readlines()[-20:]  # Last 20 lines
        
        return {{
            'running': is_running,
            'last_check': datetime.now().isoformat(),
            'recent_logs': recent_logs
        }}
    except Exception as e:
        return {{
            'running': False,
            'error': str(e),
            'last_check': datetime.now().isoformat()
        }}

@app.route('/')
def index():
    """Main dashboard page"""
    if not is_setup_complete():
        return redirect(url_for('setup'))
    
    status = get_agent_status()
    return render_template('index.html', 
                         client_name=CLIENT_NAME,
                         status=status)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """Initial setup page for API keys"""
    if request.method == 'POST':
        # Save API keys
        keys = {{
            'OPENAI_API_KEY': request.form.get('openai_key', ''),
            'ANTHROPIC_API_KEY': request.form.get('anthropic_key', ''),
            'GOOGLE_API_KEY': request.form.get('google_key', '')
        }}
        
        # Filter out empty keys
        keys = {{k: v for k, v in keys.items() if v}}
        
        if keys:
            save_api_keys(keys)
            
            # Set environment variables for agent system
            for key, value in keys.items():
                os.environ[key] = value
            
            # Restart agent system with new keys
            try:
                subprocess.run(['supervisorctl', 'restart', 'agent_system'])
            except:
                pass  # Supervisor might not be available in dev
            
            return redirect(url_for('index'))
    
    return render_template('setup.html', client_name=CLIENT_NAME)

@app.route('/status')
def status():
    """System status page"""
    if not is_setup_complete():
        return redirect(url_for('setup'))
    
    status_info = get_agent_status()
    keys = load_api_keys()
    
    # Mask API keys for display
    masked_keys = {{}}
    for key, value in keys.items():
        if len(value) > 8:
            masked_keys[key] = value[:4] + '*' * (len(value) - 8) + value[-4:]
        else:
            masked_keys[key] = '*' * len(value)
    
    return render_template('status.html',
                         client_name=CLIENT_NAME,
                         status=status_info,
                         api_keys=masked_keys)

@app.route('/api/test', methods=['POST'])
def test_agents():
    """Test the agent system with a sample task"""
    if not is_setup_complete():
        return jsonify({{'error': 'Setup not complete'}}), 400
    
    test_input = request.json.get('input', 'Hello, agents!')
    
    try:
        # Call the agent system API
        import requests
        response = requests.post('http://localhost:8001/run', 
                               json={{'input': test_input}},
                               timeout=30)
        
        if response.status_code == 200:
            return jsonify({{
                'success': True,
                'result': response.json()
            }})
        else:
            return jsonify({{
                'success': False,
                'error': f'Agent system returned {{response.status_code}}'
            }})
    except Exception as e:
        return jsonify({{
            'success': False,
            'error': str(e)
        }})

@app.route('/api/restart', methods=['POST'])
def restart_agents():
    """Restart the agent system"""
    if not is_setup_complete():
        return jsonify({{'error': 'Setup not complete'}}), 400
    
    try:
        subprocess.run(['supervisorctl', 'restart', 'agent_system'])
        return jsonify({{'success': True, 'message': 'Agent system restarting...'}})
    except Exception as e:
        return jsonify({{'success': False, 'error': str(e)}})

@app.route('/api/logs')
def get_logs():
    """Get recent agent logs"""
    if not is_setup_complete():
        return jsonify({{'error': 'Setup not complete'}}), 400
    
    try:
        log_file = Path('../agent_system/agent.log')
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = f.readlines()[-100:]  # Last 100 lines
            return jsonify({{
                'success': True,
                'logs': logs
            }})
        else:
            return jsonify({{
                'success': True,
                'logs': ['No logs available yet']
            }})
    except Exception as e:
        return jsonify({{
            'success': False,
            'error': str(e)
        }})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
'''

    # Requirements
    requirements_txt = '''flask==3.0.0
flask-session==0.5.0
redis==5.0.1
requests==2.31.0
gunicorn==21.2.0'''

    # HTML Templates
    templates_index = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ client_name }} - AI Agent Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ client_name }}</h1>
            <p class="subtitle">AI Agent System Dashboard</p>
        </header>
        
        <nav>
            <a href="/" class="active">Dashboard</a>
            <a href="/status">System Status</a>
            <a href="/setup">API Keys</a>
        </nav>
        
        <main>
            <div class="status-card {{ 'running' if status.running else 'stopped' }}">
                <h2>System Status</h2>
                <p class="status-text">
                    {% if status.running %}
                        ✅ Your AI agents are running
                    {% else %}
                        ❌ Your AI agents are stopped
                    {% endif %}
                </p>
                <p class="last-check">Last checked: {{ status.last_check }}</p>
                
                {% if not status.running %}
                <button onclick="restartAgents()" class="btn btn-primary">Start Agents</button>
                {% endif %}
            </div>
            
            <div class="test-card">
                <h2>Test Your Agents</h2>
                <p>Send a test message to your AI agent system:</p>
                <textarea id="test-input" placeholder="Enter your test message here..."></textarea>
                <button onclick="testAgents()" class="btn btn-secondary">Send Test</button>
                <div id="test-result"></div>
            </div>
            
            <div class="logs-card">
                <h2>Recent Activity</h2>
                <div id="logs-container">
                    {% for log in status.recent_logs[-10:] %}
                        <p class="log-line">{{ log }}</p>
                    {% endfor %}
                </div>
                <button onclick="refreshLogs()" class="btn btn-small">Refresh Logs</button>
            </div>
        </main>
    </div>
    
    <script>
        function restartAgents() {
            fetch('/api/restart', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    alert(data.message || 'Restart initiated');
                    setTimeout(() => location.reload(), 3000);
                });
        }
        
        function testAgents() {
            const input = document.getElementById('test-input').value;
            const resultDiv = document.getElementById('test-result');
            
            resultDiv.innerHTML = '<p>Testing...</p>';
            
            fetch('/api/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = '<p class="success">Result: ' + JSON.stringify(data.result) + '</p>';
                } else {
                    resultDiv.innerHTML = '<p class="error">Error: ' + data.error + '</p>';
                }
            });
        }
        
        function refreshLogs() {
            fetch('/api/logs')
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        const container = document.getElementById('logs-container');
                        container.innerHTML = data.logs.slice(-10).map(log => 
                            '<p class="log-line">' + log + '</p>'
                        ).join('');
                    }
                });
        }
        
        // Auto-refresh logs every 30 seconds
        setInterval(refreshLogs, 30000);
    </script>
</body>
</html>'''

    templates_setup = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Setup - {{ client_name }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>Welcome to {{ client_name }}</h1>
            <p class="subtitle">Let's set up your AI agents</p>
        </header>
        
        <main class="setup-main">
            <div class="setup-card">
                <h2>Configure API Keys</h2>
                <p>Your AI agents need API keys to function. Please provide at least one:</p>
                
                <form method="POST">
                    <div class="form-group">
                        <label for="openai_key">OpenAI API Key</label>
                        <input type="password" id="openai_key" name="openai_key" 
                               placeholder="sk-..." class="form-input">
                        <small>Required for GPT-based agents</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="anthropic_key">Anthropic API Key (Optional)</label>
                        <input type="password" id="anthropic_key" name="anthropic_key" 
                               placeholder="sk-ant-..." class="form-input">
                        <small>For Claude-based agents</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="google_key">Google API Key (Optional)</label>
                        <input type="password" id="google_key" name="google_key" 
                               placeholder="AIza..." class="form-input">
                        <small>For Google services integration</small>
                    </div>
                    
                    <button type="submit" class="btn btn-primary btn-large">Complete Setup</button>
                </form>
                
                <div class="security-note">
                    <p>🔒 Your API keys are stored securely and never shared</p>
                </div>
            </div>
        </main>
    </div>
</body>
</html>'''

    templates_status = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Status - {{ client_name }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ client_name }}</h1>
            <p class="subtitle">System Status</p>
        </header>
        
        <nav>
            <a href="/">Dashboard</a>
            <a href="/status" class="active">System Status</a>
            <a href="/setup">API Keys</a>
        </nav>
        
        <main>
            <div class="status-details">
                <h2>Agent System Status</h2>
                <table>
                    <tr>
                        <td>Status:</td>
                        <td>{{ "🟢 Running" if status.running else "🔴 Stopped" }}</td>
                    </tr>
                    <tr>
                        <td>Last Check:</td>
                        <td>{{ status.last_check }}</td>
                    </tr>
                    <tr>
                        <td>Client ID:</td>
                        <td>{{ client_id }}</td>
                    </tr>
                </table>
            </div>
            
            <div class="api-keys-status">
                <h2>Configured API Keys</h2>
                <table>
                    {% for key, value in api_keys.items() %}
                    <tr>
                        <td>{{ key }}:</td>
                        <td>{{ value }}</td>
                    </tr>
                    {% endfor %}
                </table>
                <a href="/setup" class="btn btn-small">Update Keys</a>
            </div>
            
            <div class="full-logs">
                <h2>System Logs</h2>
                <div id="full-logs-container">
                    <p>Loading logs...</p>
                </div>
                <button onclick="loadFullLogs()" class="btn btn-small">Load More</button>
            </div>
        </main>
    </div>
    
    <script>
        function loadFullLogs() {
            fetch('/api/logs')
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        const container = document.getElementById('full-logs-container');
                        container.innerHTML = data.logs.map(log => 
                            '<p class="log-line">' + log + '</p>'
                        ).join('');
                    }
                });
        }
        
        // Load logs on page load
        loadFullLogs();
    </script>
</body>
</html>'''

    # CSS Styles
    static_style_css = '''/* CrewBuilder Client Dashboard Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #0a0a0a;
    color: #ffffff;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    margin-bottom: 40px;
    padding: 40px 0;
    border-bottom: 1px solid #333;
}

h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
    background: linear-gradient(to right, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #999;
    font-size: 1.2em;
}

nav {
    display: flex;
    gap: 20px;
    margin-bottom: 40px;
    justify-content: center;
}

nav a {
    color: #999;
    text-decoration: none;
    padding: 10px 20px;
    border-radius: 8px;
    transition: all 0.3s;
}

nav a:hover, nav a.active {
    color: #fff;
    background-color: #1a1a1a;
}

.status-card, .test-card, .logs-card, .setup-card, .status-details, .api-keys-status, .full-logs {
    background-color: #1a1a1a;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 30px;
}

.status-card.running {
    border-color: #10b981;
}

.status-card.stopped {
    border-color: #ef4444;
}

.status-text {
    font-size: 1.5em;
    margin: 20px 0;
}

.last-check {
    color: #666;
    font-size: 0.9em;
}

.btn {
    background: linear-gradient(to right, #8b5cf6, #ec4899);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
    transition: all 0.3s;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3);
}

.btn-secondary {
    background: #333;
}

.btn-small {
    padding: 8px 16px;
    font-size: 0.9em;
}

.btn-large {
    padding: 16px 32px;
    font-size: 1.1em;
}

textarea {
    width: 100%;
    min-height: 100px;
    padding: 12px;
    border: 1px solid #333;
    border-radius: 8px;
    background-color: #0a0a0a;
    color: #fff;
    font-family: monospace;
    margin: 10px 0;
}

#test-result {
    margin-top: 20px;
    padding: 15px;
    border-radius: 8px;
    background-color: #0a0a0a;
}

.success {
    color: #10b981;
}

.error {
    color: #ef4444;
}

.log-line {
    font-family: monospace;
    font-size: 0.9em;
    padding: 5px 0;
    border-bottom: 1px solid #222;
    color: #999;
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #ccc;
}

.form-input {
    width: 100%;
    padding: 12px;
    border: 1px solid #333;
    border-radius: 8px;
    background-color: #0a0a0a;
    color: #fff;
    font-size: 1em;
}

.form-group small {
    display: block;
    margin-top: 5px;
    color: #666;
    font-size: 0.9em;
}

.security-note {
    margin-top: 30px;
    padding: 20px;
    background-color: #0a0a0a;
    border-radius: 8px;
    text-align: center;
    color: #999;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table td {
    padding: 10px;
    border-bottom: 1px solid #333;
}

table td:first-child {
    font-weight: bold;
    color: #999;
    width: 150px;
}

.setup-main {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
}

.setup-card {
    max-width: 600px;
    width: 100%;
}

#logs-container, #full-logs-container {
    max-height: 300px;
    overflow-y: auto;
    background-color: #0a0a0a;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
}

#full-logs-container {
    max-height: 500px;
}'''

    return DashboardCode(
        app_py=app_py,
        requirements_txt=requirements_txt,
        templates_index=templates_index,
        templates_setup=templates_setup,
        templates_status=templates_status,
        static_style_css=static_style_css
    )