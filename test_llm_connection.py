#!/usr/bin/env python3
"""
Test LLM connection to debug CrewAI issues
"""

import os
import sys

# Test 1: Check environment
print("=== Environment Check ===")
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    print(f"✓ OPENAI_API_KEY found: {openai_key[:20]}...")
else:
    print("✗ OPENAI_API_KEY not found!")

# Test 2: Try OpenAI directly
print("\n=== OpenAI Direct Test ===")
try:
    import openai
    print(f"✓ OpenAI module version: {openai.__version__}")
    
    # Set the API key
    openai.api_key = openai_key
    
    # Try a simple completion
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello from CrewBuilder!'"}],
        max_tokens=50
    )
    print(f"✓ OpenAI API works: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"✗ OpenAI test failed: {e}")

# Test 3: Try LangChain
print("\n=== LangChain Test ===")
try:
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=openai_key
    )
    
    result = llm.invoke("Say 'Hello from LangChain!'")
    print(f"✓ LangChain works: {result.content}")
    
except Exception as e:
    print(f"✗ LangChain test failed: {e}")

# Test 4: Try CrewAI
print("\n=== CrewAI Test ===")
try:
    from crewai import Agent, Task, Crew
    
    # Create a simple agent
    test_agent = Agent(
        role="Test Agent",
        goal="Test if CrewAI can use the LLM",
        backstory="You are a test agent.",
        verbose=True
    )
    
    # Create a simple task
    test_task = Task(
        description="Say 'Hello from CrewAI!'",
        agent=test_agent,
        expected_output="A greeting message"
    )
    
    # Create and run crew
    crew = Crew(
        agents=[test_agent],
        tasks=[test_task],
        verbose=True
    )
    
    result = crew.kickoff()
    print(f"✓ CrewAI works: {result}")
    
except Exception as e:
    print(f"✗ CrewAI test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")