#!/usr/bin/env python3
"""
Test CrewBuilder V2 - Following CrewAI Best Practices
"""

import os
import sys
from crewbuilder_crew_v2 import get_crewbuilder_v2

def test_crewbuilder_v2():
    """Test the new CrewBuilder with proper CrewAI patterns"""
    
    print("🧪 Testing CrewBuilder V2...")
    print("=" * 60)
    
    # Test requirement (user's example)
    requirement = """
    I need set up an agent that will take in a list of content ideas. 
    Research the topics and news using open ai deep research or something similar. 
    generate a short 2-3 minute script then generate videos using hey gen with a 
    certain avatar id that I've created and then send them to people in my crm gohighlevel.
    """
    
    print(f"📝 Requirement: {requirement[:100]}...")
    print("=" * 60)
    
    try:
        # Get CrewBuilder instance
        crewbuilder = get_crewbuilder_v2()
        
        # Test Phase 1: Clarification only
        print("\n🔍 Testing Phase 1: Clarification")
        clarification_result = crewbuilder.run_clarification_phase(requirement)
        
        if clarification_result['success']:
            print("\n✅ Clarification Phase Success!")
            print("\n📋 Clarification Questions:")
            print(clarification_result.get('clarification_questions', 'No questions'))[:500]
            print("\n🔌 API Report:")
            print(clarification_result.get('api_report', 'No report'))[:500]
        else:
            print(f"\n❌ Clarification failed: {clarification_result.get('error')}")
            return
        
        # Test Phase 2: Full system build
        print("\n" + "=" * 60)
        print("🏗️ Testing Phase 2: Full System Build")
        print("This will use hierarchical orchestration with all agents...")
        
        full_result = crewbuilder.build_complete_system(
            requirement=requirement,
            api_report=clarification_result.get('api_report')
        )
        
        if full_result['success']:
            print("\n✅ System Build Success!")
            print(f"⏱️ Execution time: {full_result.get('execution_time', 0):.1f} seconds")
            
            print("\n📊 Results Summary:")
            print(f"- Architecture: {'✓' if full_result.get('architecture') else '✗'}")
            print(f"- Generated Code: {len(full_result.get('generated_code', ''))} characters")
            print(f"- Requirements.txt: {'✓' if full_result.get('requirements_txt') else '✗'}")
            print(f"- Documentation: {'✓' if full_result.get('documentation') else '✗'}")
            print(f"- Deployment Config: {'✓' if full_result.get('deployment_config') else '✗'}")
            print(f"- Quality Review: {'✓' if full_result.get('quality_review') else '✗'}")
            
            # Show a snippet of generated code
            if full_result.get('generated_code'):
                print("\n💻 Generated Code Preview:")
                print("-" * 40)
                print(full_result['generated_code'][:500] + "...")
                print("-" * 40)
            
            # Show quality review
            if full_result.get('quality_review'):
                print("\n🔍 Quality Review:")
                print(full_result['quality_review'][:300] + "...")
                
        else:
            print(f"\n❌ System build failed: {full_result.get('error')}")
            if full_result.get('traceback'):
                print("\n🐛 Traceback:")
                print(full_result['traceback'])
    
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🏁 Test Complete!")

if __name__ == "__main__":
    # Check environment
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ ERROR: OPENAI_API_KEY not set!")
        print("Please set: export OPENAI_API_KEY='your-key'")
        sys.exit(1)
    
    test_crewbuilder_v2()