#!/usr/bin/env python3
"""
Detailed test of CrewBuilder API to diagnose issues
"""

import requests
import json
from datetime import datetime

API_URL = "https://web-production-bd955.up.railway.app"

def test_generation_detailed(requirement):
    """Test generation with detailed error reporting"""
    print(f"\n🚀 Testing generation endpoint...")
    print(f"   Requirement: {requirement[:80]}...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/generate",
            json={
                "requirement": requirement,
                "skip_clarification": True  # Skip for now to test core generation
            },
            timeout=300  # 5 minute timeout
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        # Get raw response for debugging
        raw_response = response.text
        print(f"\n📄 Raw Response (first 500 chars):")
        print(raw_response[:500])
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\n✅ Response parsed successfully!")
                print(f"   Success: {data.get('success', False)}")
                
                if data.get('error'):
                    print(f"\n❌ Error in response: {data['error']}")
                
                if data.get('data'):
                    system = data['data']
                    print(f"\n📊 System Details:")
                    print(f"   Name: {system.get('system_name', 'Unknown')}")
                    print(f"   Agents: {system.get('num_agents', 0)}")
                    print(f"   Complexity: {system.get('complexity', 'Unknown')}")
                    
                    # Check pipeline results
                    if 'pipeline_results' in system:
                        print(f"\n🔄 Pipeline Results:")
                        for stage, result in system['pipeline_results'].items():
                            status = "✅" if result.get('success') else "❌"
                            print(f"   {status} {stage}")
                            if result.get('error'):
                                print(f"      Error: {result['error']}")
                    
                    # Check code generation
                    if 'generated_code' in system:
                        print(f"\n💻 Code Generated: {len(system['generated_code'])} files")
                        for filename in list(system['generated_code'].keys())[:3]:
                            print(f"   - {filename}")
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ Failed to parse JSON: {e}")
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"\n⏱️ Request timed out after 5 minutes")
    except Exception as e:
        print(f"\n❌ Request error: {type(e).__name__}: {e}")

# Test requirement
test_requirement = """
I need to set up an agent that will take in a list of content ideas, 
research the topics using OpenAI, generate a short 2-3 minute script, 
then generate videos using HeyGen with a certain avatar ID I've created, 
and then send them to people in my CRM GoHighLevel.
"""

print("🔧 CrewBuilder Detailed API Test")
print(f"   API URL: {API_URL}")
print(f"   Time: {datetime.now().isoformat()}")

test_generation_detailed(test_requirement)