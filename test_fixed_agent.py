#!/usr/bin/env python3
"""
Test if the fixed agent configuration works
"""

import os
import sys

# Ensure we have the API key
if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: OPENAI_API_KEY environment variable not set!")
    print("Please set it with: export OPENAI_API_KEY='your-key-here'")
    sys.exit(1)

print(f"✓ OPENAI_API_KEY found: {os.getenv('OPENAI_API_KEY')[:20]}...")

# Test the fixed agent
try:
    from agents.requirements_analyst import create_requirements_analyst
    
    print("\n=== Testing Fixed Requirements Analyst ===")
    analyst = create_requirements_analyst()
    
    test_input = """
    I need to set up an agent that will take in a list of content ideas, 
    research the topics using OpenAI, generate a short 2-3 minute script, 
    then generate videos using HeyGen with a certain avatar ID I've created, 
    and then send them to people in my CRM GoHighLevel.
    """
    
    print(f"\nAnalyzing requirement: {test_input[:100]}...")
    
    result = analyst.analyze_requirements(test_input)
    
    print(f"\n✓ Analysis successful!")
    print(f"Complexity: {result.complexity_estimate}")
    print(f"Estimated Agents: {result.estimated_agents}")
    print(f"Agent Roles: {len(result.agent_roles_needed)}")
    for role in result.agent_roles_needed:
        print(f"  - {role['role']}: {role['responsibility']}")
    
except Exception as e:
    print(f"\n✗ Test failed: {e}")
    import traceback
    traceback.print_exc()