#!/usr/bin/env python3
"""
Fix agents to disable memory feature which might be causing issues
"""

import os
import re
from pathlib import Path

agents_dir = Path("agents")
agent_files = [
    "requirements_analyst.py",
    "system_architect.py",
    "code_generator.py", 
    "quality_assurance.py",
    "api_detective.py",
    "documentation_specialist.py",
    "infrastructure_analyst.py",
    "deployment_engineer.py",
    "hosting_assistant.py",
    "monitoring_engineer.py",
    "clarification_agent.py"
]

def fix_agent_memory(filepath):
    """Add memory=False to agent initialization"""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find Agent( initialization and add memory=False if not present
    agent_pattern = r"(Agent\([^)]+)"
    
    def add_memory_false(match):
        agent_init = match.group(1)
        # Check if memory is already specified
        if "memory=" in agent_init:
            return match.group(0)
        # Add memory=False before the closing parenthesis
        return agent_init + ",\n        memory=False  # Disable memory to avoid connection issues"
    
    content = re.sub(agent_pattern + r"\)", add_memory_false, content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {filepath.name}")

# Fix all agents
for agent_file in agent_files:
    filepath = agents_dir / agent_file
    if filepath.exists():
        try:
            fix_agent_memory(filepath)
        except Exception as e:
            print(f"❌ Error fixing {agent_file}: {e}")
    else:
        print(f"⚠️  {agent_file} not found")

print("\n✅ All agents updated to disable memory!")