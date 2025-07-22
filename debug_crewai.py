"""
Debug script to understand why CrewAI LLM is failing
"""

import os
import sys

# Check environment
print("=== Environment Check ===")
for key in ['OPENAI_API_KEY', 'OPENAI_MODEL_NAME', 'OPENAI_API_BASE', 'CREWAI_LLM_PROVIDER']:
    value = os.getenv(key)
    if value:
        if 'KEY' in key:
            print(f"{key}: {value[:20]}...")
        else:
            print(f"{key}: {value}")
    else:
        print(f"{key}: NOT SET")

print("\n=== Testing CrewAI ===")
try:
    from crewai import Agent, Task, Crew
    
    # Try to understand what LLM CrewAI is trying to use
    test_agent = Agent(
        role="Debug Agent",
        goal="Test LLM connection",
        backstory="A test agent"
    )
    
    # Check agent's LLM attribute
    print(f"Agent LLM: {getattr(test_agent, 'llm', 'No LLM attribute')}")
    print(f"Agent attributes: {dir(test_agent)}")
    
    # Try a simple task
    task = Task(
        description="Say hello",
        agent=test_agent,
        expected_output="A greeting"
    )
    
    crew = Crew(
        agents=[test_agent],
        tasks=[task],
        verbose=2  # Maximum verbosity
    )
    
    print("\n=== Running Crew ===")
    result = crew.kickoff()
    print(f"Result: {result}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check CrewAI's internal config
print("\n=== CrewAI Internals ===")
try:
    import crewai
    print(f"CrewAI version: {crewai.__version__}")
    
    # Try to find what LLM provider CrewAI is using
    from crewai.agent import Agent
    
    # Create a test agent and inspect it
    agent = Agent(role="test", goal="test", backstory="test")
    
    # Look for LLM configuration
    for attr in ['llm', '_llm', 'llm_config', '_llm_config']:
        if hasattr(agent, attr):
            print(f"Agent.{attr}: {getattr(agent, attr)}")
            
except Exception as e:
    print(f"Inspection error: {e}")