#!/usr/bin/env python3
"""
Install dependencies for CrewBuilder FastAPI integration
"""

import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    
    dependencies = [
        "fastapi",
        "uvicorn[standard]", 
        "pydantic"
    ]
    
    print("CrewBuilder FastAPI Integration Setup")
    print("=" * 40)
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], capture_output=True, text=True, check=True)
            
            print(f"✅ {dep} installed successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}")
            print(f"Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Error installing {dep}: {e}")
            return False
    
    print("\n✅ All dependencies installed successfully!")
    return True

def test_imports():
    """Test that we can import the dependencies"""
    
    print("\nTesting imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} imported")
    except ImportError:
        print("❌ FastAPI import failed")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__} imported")
    except ImportError:
        print("❌ Uvicorn import failed")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__} imported")
    except ImportError:
        print("❌ Pydantic import failed")
        return False
    
    return True

def test_basic_pipeline():
    """Test the basic pipeline without FastAPI"""
    
    print("\nTesting basic CrewBuilder pipeline...")
    
    try:
        # Add the project root to Python path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # Test basic imports first
        from agents.requirements_analyst import TechnicalSpecification
        from agents.system_architect import AgentSpecification, TaskSpecification, CrewWorkflow, CrewArchitecture
        
        print("✅ CrewBuilder agent imports successful")
        
        # Test fallback classes
        from api_server_fallback import FallbackRequirementsAnalyst, FallbackSystemArchitect
        
        print("✅ Fallback classes imported")
        
        # Test pipeline
        analyst = FallbackRequirementsAnalyst()
        architect = FallbackSystemArchitect()
        
        test_requirement = "I need to automate content creation for my digital marketing agency"
        
        # Test requirements analysis
        tech_spec = analyst.analyze_requirements(test_requirement)
        print(f"✅ Requirements analysis: {tech_spec.complexity_estimate} complexity")
        print(f"✅ Estimated agents: {tech_spec.estimated_agents}")
        
        # Test architecture design
        crew_arch = architect.design_crew_architecture(tech_spec)
        print(f"✅ Architecture design: {crew_arch.crew_name}")
        print(f"✅ Agents designed: {len(crew_arch.agents)}")
        print(f"✅ Tasks defined: {len(crew_arch.tasks)}")
        
        print("\n🎉 Basic pipeline test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main setup and test function"""
    
    print("🚀 CrewBuilder FastAPI Setup & Test")
    print("=" * 50)
    
    # Step 1: Install dependencies
    print("\n📦 STEP 1: Installing dependencies...")
    if not install_dependencies():
        print("❌ Dependency installation failed")
        return False
    
    # Step 2: Test imports
    print("\n🧪 STEP 2: Testing imports...")
    if not test_imports():
        print("❌ Import test failed")
        return False
    
    # Step 3: Test basic pipeline
    print("\n🔄 STEP 3: Testing basic pipeline...")
    if not test_basic_pipeline():
        print("❌ Pipeline test failed")
        return False
    
    # Success!
    print("\n" + "=" * 50)
    print("🎉 SUCCESS: CrewBuilder FastAPI setup complete!")
    print("=" * 50)
    
    print("\n🚀 NEXT STEPS:")
    print("1. Start API server: python api_server_fallback.py")
    print("2. Start web interface: cd web && npm run dev")
    print("3. Test integration: http://localhost:3000")
    
    print("\n📝 NOTE:")
    print("- API server runs on http://localhost:8000")
    print("- Web interface runs on http://localhost:3000") 
    print("- API docs available at http://localhost:8000/docs")
    print("- Currently using fallback mode (no OpenAI API keys required)")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed - check errors above")
        sys.exit(1)
    else:
        print("\n✅ Setup complete - ready to run CrewBuilder!")
        sys.exit(0)
