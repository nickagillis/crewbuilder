#!/usr/bin/env python3
"""
Test if Railway can connect to OpenAI directly
This will help determine if it's a CrewAI issue or Railway network issue
"""

import os
import sys
import time

# Test requirements:
# 1. Direct OpenAI connection
# 2. Through LangChain (used by CrewAI)
# 3. Simple CrewAI agent

print("🔍 Railway OpenAI Connection Test\n")

# Check environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY not set!")
    sys.exit(1)

print(f"✅ API Key found: {api_key[:20]}...\n")

# Test 1: Direct OpenAI
print("1️⃣ Testing direct OpenAI connection...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the same model as configured
        messages=[{"role": "user", "content": "Say 'Hello from Railway'"}],
        max_tokens=50
    )
    print(f"✅ Success: {response.choices[0].message.content}\n")
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}\n")

# Test 2: Through LangChain (what CrewAI uses)
print("2️⃣ Testing LangChain OpenAI...")
try:
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key,
        max_retries=2,
        timeout=30
    )
    
    result = llm.invoke("Say 'Hello from LangChain'")
    print(f"✅ Success: {result.content}\n")
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}\n")

# Test 3: Minimal CrewAI
print("3️⃣ Testing minimal CrewAI agent...")
try:
    from crewai import Agent, Task, Crew
    
    # Create the simplest possible agent
    agent = Agent(
        role="Tester",
        goal="Test connection",
        backstory="Testing"
    )
    
    task = Task(
        description="Say 'Hello from CrewAI'",
        agent=agent
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    
    result = crew.kickoff()
    print(f"✅ Success: {result}\n")
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}\n")
    import traceback
    traceback.print_exc()

print("\n✅ Test complete!")