#!/usr/bin/env python3
"""
Test each stage of the pipeline to identify where it fails
"""

import os
import sys

# Set up environment
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')

if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: OPENAI_API_KEY not set!")
    sys.exit(1)

# Import agents
try:
    from agents import (
        create_requirements_analyst,
        create_system_architect,
        create_code_generator
    )
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test requirement
test_requirement = """
I need to set up an agent that will take in a list of content ideas, 
research the topics using OpenAI, generate a short 2-3 minute script, 
then generate videos using HeyGen with a certain avatar ID I've created, 
and then send them to people in my CRM GoHighLevel.
"""

print("\n🧪 Testing Stage 1: Requirements Analysis")
try:
    analyst = create_requirements_analyst()
    tech_spec = analyst.analyze_requirements(test_requirement)
    print(f"✅ Requirements Analysis successful!")
    print(f"   Complexity: {tech_spec.complexity_estimate}")
    print(f"   Agents needed: {tech_spec.estimated_agents}")
    print(f"   Agent roles: {len(tech_spec.agent_roles_needed)}")
except Exception as e:
    print(f"❌ Stage 1 failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🧪 Testing Stage 2: System Architecture")
try:
    architect = create_system_architect()
    crew_architecture = architect.design_crew_architecture(tech_spec)
    print(f"✅ System Architecture successful!")
    print(f"   Crew name: {crew_architecture.crew_name}")
    print(f"   Agents designed: {len(crew_architecture.agents)}")
    print(f"   Tasks defined: {len(crew_architecture.tasks)}")
except Exception as e:
    print(f"❌ Stage 2 failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🧪 Testing Stage 3: Code Generation")
try:
    generator = create_code_generator()
    generated_code = generator.generate_crew_code(crew_architecture)
    print(f"✅ Code Generation successful!")
    print(f"   Main code length: {len(generated_code.main_code)} chars")
    print(f"   Requirements: {len(generated_code.requirements_txt.splitlines())} packages")
except Exception as e:
    print(f"❌ Stage 3 failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All stages completed successfully!")