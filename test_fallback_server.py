#!/usr/bin/env python3
"""
Test the FastAPI fallback server
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_fallback_server():
    """Test the fallback API server"""
    try:
        print("Testing fallback API server...")
        
        # Import the fallback server
        import api_server_fallback
        
        print("SUCCESS: Fallback server imported")
        
        # Test the pipeline directly
        test_requirement = "I need to automate content creation for my digital marketing agency"
        
        result = api_server_fallback.run_fallback_pipeline(test_requirement)
        
        print("SUCCESS: Fallback pipeline executed")
        print(f"System Name: {result['systemName']}")
        print(f"Complexity: {result['complexity']}")
        print(f"Agents: {result['agents']}")
        print(f"Estimated Time: {result['estimatedTime']}")
        print(f"Pipeline Stages: {len(result['pipeline_stages'])}")
        
        # Test crew architecture
        if 'architecture' in result:
            arch = result['architecture']
            print(f"Crew Name: {arch['crew_name']}")
            print(f"Agents Designed: {len(arch['agents'])}")
            print(f"Tasks Defined: {len(arch['tasks'])}")
        
        print("\nSUCCESS: All fallback tests passed!")
        return True
        
    except Exception as e:
        print(f"ERROR: Fallback server test failed - {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("CrewBuilder Fallback API Test")
    print("=" * 35)
    
    if test_fallback_server():
        print("\nREADY TO START:")
        print("1. Run: python api_server_fallback.py")
        print("2. In another terminal: cd web && npm run dev")
        print("3. Visit: http://localhost:3000")
        print("4. Test the complete web integration!")
    else:
        print("\nFailed - check errors above")
