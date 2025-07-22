#!/usr/bin/env python3
"""
Test the live API and parse the actual response structure
"""

import requests
import json

API_URL = "https://web-production-bd955.up.railway.app"

test_requirement = """
I need to set up an agent that will take in a list of content ideas, 
research the topics using OpenAI, generate a short 2-3 minute script, 
then generate videos using HeyGen with a certain avatar ID I've created, 
and then send them to people in my CRM GoHighLevel.
"""

print("🔍 Testing Live CrewBuilder API\n")

# Make the request
response = requests.post(
    f"{API_URL}/api/generate",
    json={
        "requirement": test_requirement,
        "skip_clarification": True
    },
    timeout=300
)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    data = response.json()
    
    # Pretty print the entire response
    print("Full Response Structure:")
    print(json.dumps(data, indent=2))
    
    # Check pipeline stages
    if 'data' in data and 'pipeline_stages' in data['data']:
        print("\n\nPipeline Stages Analysis:")
        for i, stage in enumerate(data['data']['pipeline_stages']):
            status = "✅" if stage.get('status') == 'completed' else "❌"
            print(f"{i+1}. {status} {stage.get('stage', 'Unknown')}")
            if 'output' in stage:
                print(f"   Output: {json.dumps(stage['output'], indent=6)}")
else:
    print(f"Error: {response.text}")