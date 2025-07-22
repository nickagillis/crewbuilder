#!/usr/bin/env python3
"""
Detailed network diagnostics for Railway OpenAI connection issues
"""

import os
import socket
import subprocess
import requests
import ssl
import certifi

print("🔍 Detailed Network Diagnostics\n")

# Test 1: DNS Resolution
print("1️⃣ DNS Resolution Test:")
try:
    import socket
    ips = socket.gethostbyname_ex('api.openai.com')
    print(f"✅ api.openai.com resolves to: {ips}")
except Exception as e:
    print(f"❌ DNS failed: {e}")

# Test 2: Basic HTTPS connectivity
print("\n2️⃣ HTTPS Connectivity Test:")
try:
    response = requests.get('https://api.openai.com', timeout=10)
    print(f"✅ HTTPS connection successful: {response.status_code}")
except Exception as e:
    print(f"❌ HTTPS failed: {type(e).__name__}: {e}")

# Test 3: SSL Certificate
print("\n3️⃣ SSL Certificate Test:")
try:
    context = ssl.create_default_context(cafile=certifi.where())
    with socket.create_connection(('api.openai.com', 443), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname='api.openai.com') as ssock:
            print(f"✅ SSL handshake successful")
            print(f"   Protocol: {ssock.version()}")
            print(f"   Cipher: {ssock.cipher()}")
except Exception as e:
    print(f"❌ SSL failed: {type(e).__name__}: {e}")

# Test 4: Environment Variables
print("\n4️⃣ Environment Check:")
env_vars = ['OPENAI_API_KEY', 'HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY']
for var in env_vars:
    value = os.getenv(var)
    if value:
        if 'KEY' in var:
            print(f"   {var}: {value[:20]}...")
        else:
            print(f"   {var}: {value}")
    else:
        print(f"   {var}: Not set")

# Test 5: Network interfaces
print("\n5️⃣ Network Configuration:")
try:
    result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    for line in lines:
        if 'inet ' in line:
            print(f"   {line.strip()}")
except Exception as e:
    print(f"   Failed to get network info: {e}")

# Test 6: Test with curl
print("\n6️⃣ Curl Test:")
try:
    result = subprocess.run(
        ['curl', '-v', '--max-time', '10', 'https://api.openai.com/v1/models'],
        capture_output=True,
        text=True
    )
    print(f"   Exit code: {result.returncode}")
    if result.stderr:
        for line in result.stderr.split('\n')[:10]:
            if line.strip():
                print(f"   {line}")
except Exception as e:
    print(f"   Curl failed: {e}")

print("\n✅ Diagnostics complete!")