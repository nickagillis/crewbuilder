#!/usr/bin/env python3
"""
Test the clarification flow to see if it's working
"""

import requests
import json
import time

API_URL = "https://web-production-bd955.up.railway.app"

def test_clarification():
    """Test the clarification endpoint"""
    print("Testing Clarification Agent...")
    
    requirement = """I need set up an agent that will take in a list of content ideas. 
    Research the topics and news using open ai deep research or something similar. 
    generate a short 2-3 minute script then generate videos using hey gen with a 
    certain avatar id that I've created and then send them to people in my crm gohighlevel."""
    
    # Test clarification
    response = requests.post(
        f"{API_URL}/api/clarify",
        json={"requirement": requirement},
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Session ID: {data.get('session_id')}")
        print(f"Questions: {json.dumps(data.get('questions', []), indent=2)}")
        return data
    else:
        print(f"Error: {response.text}")
        return None

def test_generation():
    """Test the generate endpoint directly"""
    print("\nTesting Direct Generation...")
    
    requirement = """I need set up an agent that will take in a list of content ideas. 
    Research the topics and news using open ai deep research or something similar. 
    generate a short 2-3 minute script then generate videos using hey gen with a 
    certain avatar id that I've created and then send them to people in my crm gohighlevel."""
    
    start_time = time.time()
    response = requests.post(
        f"{API_URL}/api/generate",
        json={"requirement": requirement},
        timeout=300
    )
    end_time = time.time()
    
    print(f"Status: {response.status_code}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if response.ok:
        data = response.json()
        if data.get('success'):
            result = data.get('data', {})
            print(f"Agents designed: {result.get('agents', 0)}")
            print(f"Complexity: {result.get('complexity', 'unknown')}")
            print(f"Pipeline stages: {len(result.get('pipeline_stages', []))}")
            
            # Check if we got actual code
            if 'generated_code' in result:
                print(f"Generated code length: {len(result['generated_code'])} chars")
            else:
                print("No generated code found!")
        else:
            print(f"Generation failed: {data.get('error')}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("=== CrewBuilder Clarification Flow Test ===\n")
    
    # Test clarification first
    clarification_result = test_clarification()
    
    # Test generation
    test_generation()