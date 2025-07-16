#!/usr/bin/env python3
"""
Test script for CrewBuilder API
Allows testing the backend directly without the frontend
"""

import requests
import json
import sys
from datetime import datetime

# API URL - can be local or production
API_URL = "https://web-production-bd955.up.railway.app"  # Production Railway URL
# API_URL = "http://localhost:8000"  # For local testing

def test_health():
    """Test if the API is running"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy!")
            print(f"   Agents ready: {data.get('agents_initialized', 0)}")
            print(f"   Agents: {', '.join(data.get('agents_ready', []))}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False
    return True

def test_clarification(requirement):
    """Test the clarification endpoint"""
    print(f"\n💬 Testing clarification for: {requirement[:50]}...")
    try:
        response = requests.post(
            f"{API_URL}/api/clarify",
            json={"requirement": requirement}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Clarification successful!")
                print(f"   Session ID: {data['session_id']}")
                print(f"   Questions generated: {len(data.get('questions', []))}")
                for i, q in enumerate(data.get('questions', [])[:3]):
                    print(f"   Q{i+1}: {q['question']}")
                return data['session_id'], data['questions']
            else:
                print(f"❌ Clarification failed: {data.get('error')}")
        else:
            print(f"❌ Clarification request failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Clarification error: {e}")
    return None, None

def test_generation(requirement, skip_clarification=False):
    """Test the generation endpoint"""
    print(f"\n🚀 Testing generation for: {requirement[:50]}...")
    print("This will run the full 11-agent pipeline, please wait...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/generate",
            json={
                "requirement": requirement,
                "skip_clarification": skip_clarification
            },
            timeout=300  # 5 minute timeout
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Generation successful!")
                system_data = data.get('data', {})
                print(f"   System name: {system_data.get('systemName', 'Unknown')}")
                print(f"   Agents: {system_data.get('agents', 0)}")
                print(f"   Complexity: {system_data.get('complexity', 'Unknown')}")
                print(f"   Estimated time: {system_data.get('estimatedTime', 'Unknown')}")
                print(f"   Estimated cost: {system_data.get('estimatedCost', 'Unknown')}")
                
                # Show pipeline stages
                stages = system_data.get('pipeline_stages', [])
                print(f"\n   Pipeline stages completed: {len(stages)}")
                for stage in stages:
                    status_icon = "✅" if stage['status'] == 'completed' else "❌"
                    print(f"   {status_icon} {stage['stage']}")
                
                # Check if code was generated
                if 'generated_code' in system_data:
                    print(f"\n   Generated code length: {len(system_data['generated_code'])} characters")
                
                return system_data
            else:
                print(f"❌ Generation failed: {data.get('error')}")
        else:
            print(f"❌ Generation request failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', error_data.get('error', 'Unknown error'))}")
            except:
                print(f"   Response: {response.text[:500]}")
    except requests.exceptions.Timeout:
        print("❌ Generation timed out (>5 minutes)")
    except Exception as e:
        print(f"❌ Generation error: {e}")
    return None

def test_deployment(requirement, api_keys=None):
    """Test the deployment endpoint"""
    print(f"\n🚂 Testing deployment for: {requirement[:50]}...")
    
    if not api_keys:
        api_keys = {"OPENAI_API_KEY": "test-key-123"}
        print("   ⚠️  Using test API keys")
    
    try:
        response = requests.post(
            f"{API_URL}/api/deploy",
            json={
                "requirement": requirement,
                "api_keys": api_keys,
                "deploy_to_railway": True
            },
            timeout=600  # 10 minute timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Deployment successful!")
                print(f"   Deployment URL: {data.get('deployment_url', 'Unknown')}")
                print(f"   Dashboard URL: {data.get('dashboard_url', 'Unknown')}")
                print(f"   Project ID: {data.get('project_id', 'Unknown')}")
                return data
            else:
                print(f"❌ Deployment failed: {data.get('error')}")
        else:
            print(f"❌ Deployment request failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
    except Exception as e:
        print(f"❌ Deployment error: {e}")
    return None

def main():
    """Run tests based on command line arguments"""
    
    print("🔧 CrewBuilder API Test Suite")
    print(f"   API URL: {API_URL}")
    print(f"   Time: {datetime.now().isoformat()}\n")
    
    # Test health first
    if not test_health():
        print("\n❌ API is not running. Start it with: python api_server.py")
        sys.exit(1)
    
    # Default test requirement
    requirement = "Build an AI system that monitors social media for brand mentions and automatically responds"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "clarify":
            # Test clarification
            session_id, questions = test_clarification(requirement)
        elif sys.argv[1] == "generate":
            # Test generation
            if len(sys.argv) > 2:
                requirement = " ".join(sys.argv[2:])
            test_generation(requirement)
        elif sys.argv[1] == "deploy":
            # Test deployment
            if len(sys.argv) > 2:
                requirement = " ".join(sys.argv[2:])
            test_deployment(requirement)
        elif sys.argv[1] == "full":
            # Test full pipeline
            print("Running full pipeline test...")
            
            # 1. Clarification
            session_id, questions = test_clarification(requirement)
            
            # 2. Generation
            system = test_generation(requirement, skip_clarification=True)
            
            # 3. Deployment (only if generation succeeded)
            if system:
                test_deployment(requirement)
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("\nUsage:")
            print("  python test_api.py clarify     - Test clarification")
            print("  python test_api.py generate [requirement]  - Test generation")
            print("  python test_api.py deploy [requirement]    - Test deployment")
            print("  python test_api.py full        - Test full pipeline")
    else:
        # Default: test generation with the video content requirement
        requirement = """I need set up an agent that will take in a list of content ideas. 
        Research the topics and news using open ai deep research or something similar. 
        generate a short 2-3 minute script then generate videos using hey gen with a 
        certain avatar id that I've created and then send them to people in my crm gohighlevel."""
        
        print(f"Testing with your requirement:\n{requirement}\n")
        test_generation(requirement)

if __name__ == "__main__":
    main()