#!/usr/bin/env python3
"""
Test the new CrewAI Orchestrator
"""

import asyncio
from crewbuilder_orchestrator import get_orchestrator

def test_orchestrator():
    """Test the orchestrator with a sample requirement"""
    
    print("🧪 Testing CrewBuilder Orchestrator...")
    
    # Sample requirement
    requirement = """
    I need set up an agent that will take in a list of content ideas. 
    Research the topics and news using open ai deep research or something similar. 
    generate a short 2-3 minute script then generate videos using hey gen with a 
    certain avatar id that I've created and then send them to people in my crm gohighlevel.
    """
    
    try:
        # Get orchestrator instance
        orchestrator = get_orchestrator()
        print("✅ Orchestrator initialized")
        
        # Test clarification first
        print("\n📝 Testing clarification...")
        clarification_result = orchestrator.run_clarification(requirement)
        
        if clarification_result['success']:
            print(f"✅ Got {len(clarification_result['questions'])} clarification questions")
            for i, q in enumerate(clarification_result['questions'], 1):
                print(f"   {i}. {q['question']}")
        else:
            print(f"❌ Clarification failed: {clarification_result.get('error')}")
        
        # Test the full crew orchestration
        print("\n🚀 Testing full crew orchestration...")
        print("This will run all 10 agents in a coordinated crew...")
        
        # Mock clarified requirements
        clarified_requirements = {
            "volume": "10-20 videos per week",
            "target_audience": "business professionals",
            "integration_apis": ["OpenAI", "HeyGen", "GoHighLevel"],
            "budget": "$500/month",
            "technical_level": "intermediate"
        }
        
        # Run the orchestrated crew
        result = orchestrator.build_crew_system(requirement, clarified_requirements)
        
        # Display results
        print(f"\n✅ Crew execution completed in {result['execution_time']:.1f} seconds")
        print(f"📊 Tasks completed: {result['tasks_completed']}")
        
        print("\n📋 Task Results:")
        for task_name, output in result['task_outputs'].items():
            status = "✅" if output['completed'] else "❌"
            print(f"   {status} {task_name}: {output['agent']}")
            if not output['completed'] and 'error' in output:
                print(f"      Error: {output['error']}")
        
        # Check for generated code
        if 'generated_code' in result:
            print(f"\n💻 Generated code length: {len(result['generated_code'])} characters")
        
        if 'requirements_txt' in result:
            print(f"\n📦 Dependencies generated: {len(result['requirements_txt'].splitlines())} packages")
        
        print("\n✅ Orchestrator test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Orchestrator test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_orchestrator()