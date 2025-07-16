#!/usr/bin/env python3
"""
Test CrewBuilder FastAPI Server
Quick test to verify the API server integration
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_agent_imports():
    """Test that all agents can be imported successfully"""
    try:
        print("Testing agent imports...")
        
        from agents import (
            create_requirements_analyst,
            create_system_architect,
            create_code_generator,
            create_quality_assurance,
            create_api_detective,
            create_documentation_specialist,
            create_infrastructure_analyst,
            create_deployment_engineer,
            create_hosting_assistant,
            create_monitoring_engineer
        )
        
        print("✅ All agent imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Agent import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi_dependencies():
    """Test that FastAPI dependencies are available"""
    try:
        print("🧪 Testing FastAPI dependencies...")
        
        import fastapi
        import uvicorn
        import pydantic
        
        print(f"✅ FastAPI {fastapi.__version__} available")
        print(f"✅ Uvicorn {uvicorn.__version__} available") 
        print(f"✅ Pydantic {pydantic.__version__} available")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📝 To install: pip install fastapi uvicorn[standard] pydantic")
        return False

def test_single_agent():
    """Test creating a single agent to verify functionality"""
    try:
        print("🧪 Testing single agent creation...")
        
        from agents import create_requirements_analyst
        
        analyst = create_requirements_analyst()
        print(f"✅ Requirements Analyst created: {type(analyst).__name__}")
        
        # Test a simple requirement analysis (using fallback)
        test_requirement = "I need to automate content creation for my blog"
        
        # This should use the fallback logic which doesn't require API keys
        print("🧪 Testing requirement analysis...")
        result = analyst.analyze_requirements(test_requirement)
        
        print(f"✅ Analysis completed: {result.complexity_estimate} complexity")
        print(f"✅ Estimated agents: {result.estimated_agents}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_server_startup():
    """Test that the API server can start without errors"""
    try:
        print("🧪 Testing API server imports...")
        
        # Import the API server module
        import api_server
        
        print("✅ API server module imported successfully")
        
        # Test agent initialization
        print("🧪 Testing agent initialization...")
        success = api_server.initialize_agents()
        
        if success:
            print("✅ All 10 agents initialized successfully!")
            print(f"✅ Agent count: {len(api_server.agents)}")
            
            # List initialized agents
            for name in api_server.agents.keys():
                print(f"   • {name}")
                
        else:
            print("❌ Agent initialization failed")
            
        return success
        
    except Exception as e:
        print(f"❌ API server test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("CrewBuilder FastAPI Integration Test")
    print("=" * 50)
    
    tests = [
        ("Agent Imports", test_agent_imports),
        ("FastAPI Dependencies", test_fastapi_dependencies), 
        ("Single Agent", test_single_agent),
        ("API Server Startup", test_api_server_startup)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        print("-" * 30)
        
        success = test_func()
        results.append((test_name, success))
        
        if success:
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print("\n" + "=" * 50)
    print("🏆 TEST SUMMARY:")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"   {status:>4}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! FastAPI integration ready!")
        print("\n🚀 Next steps:")
        print("   1. Run: python api_server.py")
        print("   2. Run: cd web && npm run dev")
        print("   3. Visit: http://localhost:3000")
        print("   4. Test full integration!")
        return True
    else:
        print("⚠️ Some tests failed. Check errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
