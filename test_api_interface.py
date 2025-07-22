"""
Test Interface Generation via API - Quick verification
"""

import requests
import json
import time

API_URL = "https://web-production-bd955.up.railway.app"

def test_interface_generation():
    """Test if the API generates interface code"""
    
    print("🧪 Testing Interface Generation via API")
    print("=" * 60)
    
    # Test requirement that needs an interface
    requirement = """
    I need a system to monitor my website uptime. It should check 
    https://example.com every 5 minutes and send me an email if it's down.
    """
    
    # Step 1: Test system generation
    print("\n📡 Calling /api/generate endpoint...")
    
    response = requests.post(
        f"{API_URL}/api/generate",
        json={"requirement": requirement},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            data = result.get("data", {})
            
            print(f"\n✅ Generation successful!")
            print(f"- System Name: {data.get('systemName', 'N/A')}")
            print(f"- Agents: {data.get('agents', 0)}")
            print(f"- Complexity: {data.get('complexity', 'N/A')}")
            
            # Check for interface code
            interface_code = data.get('interface_code', '')
            deployment_package = data.get('deployment_package', '')
            
            print(f"\n📊 Generated Components:")
            print(f"- Core Code: {'✅' if data.get('generated_code') else '❌'} ({len(data.get('generated_code', ''))} chars)")
            print(f"- Interface Code: {'✅' if interface_code else '❌'} ({len(interface_code)} chars)")
            print(f"- Deployment Package: {'✅' if deployment_package else '❌'} ({len(deployment_package)} chars)")
            
            if interface_code:
                print(f"\n🎉 SUCCESS: Interface code was generated!")
                print("\nInterface Preview:")
                print("-" * 40)
                print(interface_code[:500] + "..." if len(interface_code) > 500 else interface_code)
                print("-" * 40)
            else:
                print(f"\n❌ PROBLEM: No interface code generated!")
                print("Users won't be able to run this system!")
                
        else:
            print(f"\n❌ Generation failed: {result}")
    else:
        print(f"\n❌ API error: {response.status_code}")
        print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    test_interface_generation()