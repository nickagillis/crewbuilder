#!/usr/bin/env python3
"""
Simple CrewAI test to isolate the connection issue
"""

import os
import sys

# Set environment variables
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

if not os.getenv('OPENAI_API_KEY'):
    print("ERROR: OPENAI_API_KEY not set!")
    sys.exit(1)

print(f"✅ OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')[:20]}...")

# Test 1: Direct OpenAI
print("\n1️⃣ Testing direct OpenAI connection:")
try:
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print(f"✅ Direct OpenAI works: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Direct OpenAI failed: {e}")

# Test 2: LangChain
print("\n2️⃣ Testing LangChain:")
try:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    result = llm.invoke("Say hello")
    print(f"✅ LangChain works: {result.content}")
except Exception as e:
    print(f"❌ LangChain failed: {e}")

# Test 3: CrewAI with explicit LLM
print("\n3️⃣ Testing CrewAI with explicit LLM:")
try:
    from crewai import Agent, Task, Crew
    from langchain_openai import ChatOpenAI
    
    # Create LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # Create agent with LLM
    agent = Agent(
        role="Test Agent",
        goal="Test the connection",
        backstory="A simple test agent",
        llm=llm,
        verbose=True
    )
    
    # Create task
    task = Task(
        description="Say 'Hello from CrewAI with explicit LLM'",
        agent=agent,
        expected_output="A greeting"
    )
    
    # Run crew
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    print(f"✅ CrewAI with explicit LLM works: {result}")
    
except Exception as e:
    print(f"❌ CrewAI with explicit LLM failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: CrewAI default (no explicit LLM)
print("\n4️⃣ Testing CrewAI with default LLM:")
try:
    from crewai import Agent, Task, Crew
    
    # Create agent without LLM
    agent = Agent(
        role="Test Agent",
        goal="Test the connection",
        backstory="A simple test agent",
        verbose=True
    )
    
    # Create task
    task = Task(
        description="Say 'Hello from CrewAI default'",
        agent=agent,
        expected_output="A greeting"
    )
    
    # Run crew
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    print(f"✅ CrewAI default works: {result}")
    
except Exception as e:
    print(f"❌ CrewAI default failed: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Tests complete!")