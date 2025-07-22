#!/usr/bin/env python3
"""
Debug OpenAI SDK connection issues on Railway
"""

import os
import httpx
from openai import OpenAI

print("🔍 OpenAI SDK Debug\n")

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key: {api_key[:20]}...\n")

# Test 1: Direct httpx request (what OpenAI SDK uses)
print("1️⃣ Testing httpx (OpenAI's HTTP library):")
try:
    with httpx.Client() as client:
        response = client.get("https://api.openai.com/v1/models", 
                             headers={"Authorization": f"Bearer {api_key}"},
                             timeout=10.0)
        print(f"✅ httpx works: {response.status_code}")
        print(f"   Models: {len(response.json().get('data', []))} available")
except Exception as e:
    print(f"❌ httpx failed: {type(e).__name__}: {e}")

# Test 2: OpenAI client with custom httpx client
print("\n2️⃣ Testing OpenAI with custom timeout:")
try:
    client = OpenAI(
        api_key=api_key,
        timeout=30.0,  # 30 second timeout
        max_retries=0  # No retries for clearer errors
    )
    
    models = client.models.list()
    print(f"✅ OpenAI client works!")
    print(f"   First model: {models.data[0].id if models.data else 'None'}")
except Exception as e:
    print(f"❌ OpenAI client failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Try with explicit base URL
print("\n3️⃣ Testing with explicit base URL:")
try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.openai.com/v1",
        timeout=30.0
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print(f"✅ Chat completion works: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Chat failed: {type(e).__name__}: {e}")

# Test 4: Check httpx SSL settings
print("\n4️⃣ Testing httpx SSL configuration:")
try:
    import ssl
    import certifi
    
    # Create custom httpx client with explicit SSL
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    with httpx.Client(verify=ssl_context) as client:
        response = client.get("https://api.openai.com/v1/models",
                             headers={"Authorization": f"Bearer {api_key}"},
                             timeout=10.0)
        print(f"✅ Custom SSL context works: {response.status_code}")
except Exception as e:
    print(f"❌ Custom SSL failed: {type(e).__name__}: {e}")

print("\n✅ Debug complete!")