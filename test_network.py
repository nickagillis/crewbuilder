#!/usr/bin/env python3
"""
Test network connectivity to OpenAI from Railway
"""

import os
import socket
import urllib.request
import ssl

print("=== Network Connectivity Test ===\n")

# Test 1: DNS Resolution
print("1. Testing DNS resolution for api.openai.com...")
try:
    ip = socket.gethostbyname('api.openai.com')
    print(f"✓ Resolved to: {ip}")
except Exception as e:
    print(f"✗ DNS failed: {e}")

# Test 2: Port connectivity
print("\n2. Testing port 443 connectivity...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex(('api.openai.com', 443))
    sock.close()
    if result == 0:
        print("✓ Port 443 is open")
    else:
        print(f"✗ Port 443 connection failed: {result}")
except Exception as e:
    print(f"✗ Socket test failed: {e}")

# Test 3: HTTPS request
print("\n3. Testing HTTPS request to OpenAI...")
try:
    context = ssl.create_default_context()
    with urllib.request.urlopen('https://api.openai.com/v1/models', context=context) as response:
        print(f"✓ HTTPS request successful: {response.status}")
except Exception as e:
    print(f"✗ HTTPS request failed: {e}")

# Test 4: Check for proxy settings
print("\n4. Checking proxy settings...")
proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'no_proxy']
proxy_found = False
for var in proxy_vars:
    value = os.getenv(var)
    if value:
        print(f"Found {var}: {value}")
        proxy_found = True
if not proxy_found:
    print("No proxy settings found")

# Test 5: Try with requests library
print("\n5. Testing with requests library...")
try:
    import requests
    response = requests.get('https://api.openai.com/v1/models', timeout=5)
    print(f"✓ Requests library works: {response.status_code}")
except Exception as e:
    print(f"✗ Requests failed: {e}")

print("\n=== Test Complete ===")