#!/usr/bin/env python3
"""
Simple CrewBuilder API Test
Test the FastAPI integration without Unicode issues
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_imports():
    """Test basic imports"""
    try:
        print("Testing basic imports...")
        
        from agents import create_requirements_analyst
        print("SUCCESS: Basic agent import works")
        return True
        
    except Exception as e:
        print(f"ERROR: Import failed - {e}")
        return False

def test_fastapi_available():
    """Test FastAPI availability"""
    try:
        print("Testing FastAPI availability...")
        
        import fastapi
        print(f"SUCCESS: FastAPI {fastapi.__version__} available")
        return True
        
    except ImportError:
        print("ERROR: FastAPI not installed. Run: pip install fastapi uvicorn pydantic")
        return False

def test_agent_creation():
    """Test agent creation"""
    try:
        print("Testing agent creation...")
        
        from agents import create_requirements_analyst
        
        agent = create_requirements_analyst()
        print(f"SUCCESS: Agent created - {type(agent).__name__}")
        return True
        
    except Exception as e:
        print(f"ERROR: Agent creation failed - {e}")
        return False

def test_simple_analysis():
    """Test simple requirement analysis"""
    try:
        print("Testing requirement analysis...")
        
        from agents import create_requirements_analyst
        
        agent = create_requirements_analyst()
        result = agent.analyze_requirements("I need to automate my blog content creation")
        
        print(f"SUCCESS: Analysis completed - {result.complexity_estimate} complexity")
        print(f"SUCCESS: Estimated {result.estimated_agents} agents needed")
        return True
        
    except Exception as e:
        print(f"ERROR: Analysis failed - {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run tests"""
    print("CrewBuilder FastAPI Integration Test")
    print("=" * 40)
    
    tests = [
        test_basic_imports,
        test_fastapi_available,
        test_agent_creation,
        test_simple_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n{test.__name__}:")
        print("-" * 25)
        
        if test():
            passed += 1
            print("RESULT: PASS")
        else:
            print("RESULT: FAIL")
    
    print("\n" + "=" * 40)
    print(f"SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed!")
        print("\nNext steps:")
        print("1. Run: python api_server.py")
        print("2. Run: cd web && npm run dev") 
        print("3. Test integration at http://localhost:3000")
        return True
    else:
        print("WARNING: Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\nTest result: {'SUCCESS' if success else 'FAILED'}")
