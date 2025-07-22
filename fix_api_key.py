#!/usr/bin/env python3
"""
Fix API key that has newlines in it
"""

import os

# Get the current API key
api_key = os.getenv('OPENAI_API_KEY', '')

print(f"Original API key length: {len(api_key)}")
print(f"Contains newline: {'\\n' in api_key}")
print(f"First 50 chars: {repr(api_key[:50])}")
print(f"Last 50 chars: {repr(api_key[-50:])}")

# Clean the API key
cleaned_key = api_key.replace('\n', '').replace('\r', '').strip()
cleaned_key = ' '.join(cleaned_key.split())  # Remove extra spaces

print(f"\nCleaned API key length: {len(cleaned_key)}")
print(f"Cleaned first 50: {repr(cleaned_key[:50])}")

# Set the cleaned key
os.environ['OPENAI_API_KEY'] = cleaned_key

# Test it
print("\nTesting cleaned key:")
try:
    from openai import OpenAI
    client = OpenAI(api_key=cleaned_key)
    models = client.models.list()
    print(f"✅ Success! Found {len(models.data)} models")
    print(f"   First model: {models.data[0].id}")
except Exception as e:
    print(f"❌ Still failed: {e}")