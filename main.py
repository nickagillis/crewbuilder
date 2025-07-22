#!/usr/bin/env python3
"""
CrewBuilder V2 - Build AI Agent Systems the Right Way
Using proper CrewAI patterns: Simple agents, smart tasks, hierarchical orchestration
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point - start the API server"""
    print("\n" + "="*60)
    print("🚀 CrewBuilder V2 - AI Agent Meta-System")
    print("="*60)
    
    print("\n📋 ARCHITECTURE:")
    print("   ✅ 8 Specialist Agents (not 11 complex ones)")
    print("   ✅ Simple agents with role/goal/backstory only")
    print("   ✅ Tasks contain the actual logic (80/20 rule)")
    print("   ✅ Hierarchical orchestration with manager")
    print("   ✅ Proper CrewAI patterns throughout")
    
    print("\n🎯 AGENTS:")
    print("   1. Clarification Specialist - Requirements refinement")
    print("   2. API Analyst - Integration verification")
    print("   3. Crew Architect - System design")
    print("   4. Task Designer - Workflow creation")
    print("   5. Code Writer - Implementation")
    print("   6. Quality Reviewer - Validation")
    print("   7. Deployment Specialist - Infrastructure")
    print("   8. Documentation Writer - User guides")
    
    print("\n🚀 STARTING OPTIONS:")
    print("   1. Web Interface: http://localhost:8000")
    print("   2. API Docs: http://localhost:8000/docs")
    print("   3. Test Script: python test_crewbuilder_v2.py")
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  WARNING: OPENAI_API_KEY not set!")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
        return
    
    print("\n" + "="*60)
    print("Starting API server...")
    print("="*60 + "\n")
    
    # Start the FastAPI server
    import uvicorn
    from api_server import app
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()