#!/usr/bin/env python3
"""
Test OpenAI connection directly to diagnose Railway connection issues
"""

import os
import openai
from openai import OpenAI
import socket
import time

print("🔍 OpenAI Connection Diagnostics\n")

# Check environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY not set!")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...\n")

# Test DNS resolution
print("📡 Testing DNS resolution:")
try:
    ip = socket.gethostbyname('api.openai.com')
    print(f"✅ api.openai.com resolves to: {ip}")
except Exception as e:
    print(f"❌ DNS resolution failed: {e}")

# Test direct OpenAI connection
print("\n🧪 Testing OpenAI API connection:")
client = OpenAI(api_key=api_key)

try:
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello from Railway!'"}],
        max_tokens=50,
        timeout=30
    )
    elapsed = time.time() - start_time
    
    print(f"✅ OpenAI API call successful!")
    print(f"   Response: {response.choices[0].message.content}")
    print(f"   Time taken: {elapsed:.2f} seconds")
    print(f"   Model: {response.model}")
    
except openai.APIConnectionError as e:
    print(f"❌ Connection error: {e}")
    print("   This suggests a network/firewall issue")
    
except openai.AuthenticationError as e:
    print(f"❌ Authentication error: {e}")
    print("   Check your API key")
    
except openai.RateLimitError as e:
    print(f"❌ Rate limit error: {e}")
    print("   You've exceeded your API quota")
    
except Exception as e:
    print(f"❌ Unexpected error: {type(e).__name__}: {e}")

# Test with retries
print("\n🔄 Testing with retries:")
for i in range(3):
    try:
        print(f"   Attempt {i+1}/3...", end="")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Attempt {i+1}"}],
            max_tokens=10,
            timeout=10
        )
        print(" ✅ Success!")
        break
    except Exception as e:
        print(f" ❌ Failed: {type(e).__name__}")
        if i < 2:
            time.sleep(2)

print("\n✅ Diagnostics complete!")