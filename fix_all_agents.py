#!/usr/bin/env python3
"""
Fix all agents to use explicit LLM configuration
"""

import os
import re
from pathlib import Path

agents_dir = Path("agents")
agent_files = [
    "system_architect.py",
    "code_generator.py", 
    "quality_assurance.py",
    "api_detective.py",
    "documentation_specialist.py",
    "infrastructure_analyst.py",
    "deployment_engineer.py",
    "hosting_assistant.py",
    "monitoring_engineer.py"
]

def fix_agent_file(filepath):
    """Fix an agent file to use explicit LLM configuration"""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already fixed
    if "from .llm_config import get_configured_llm" in content:
        print(f"✓ {filepath.name} already fixed")
        return
    
    # Add import
    import_pattern = r"(from crewai import .*\n)"
    import_replacement = r"\1from .llm_config import get_configured_llm\n"
    content = re.sub(import_pattern, import_replacement, content, count=1)
    
    # Fix Agent initialization - find the pattern
    agent_pattern = r"(\s+)self\.agent = Agent\(([\s\S]*?)\n(\s+)\)"
    
    def replace_agent(match):
        indent = match.group(1)
        agent_content = match.group(2)
        closing_indent = match.group(3)
        
        # Check if llm is already specified
        if "llm=" in agent_content:
            return match.group(0)
        
        # Add LLM configuration before Agent creation
        llm_init = f"{indent}# Get configured LLM\n{indent}llm = get_configured_llm(temperature=0.7)\n{indent}\n"
        
        # Add llm parameter to Agent
        new_agent = f"{indent}self.agent = Agent({agent_content},\n{closing_indent}    llm=llm  # Pass the LLM explicitly\n{closing_indent})"
        
        return llm_init + new_agent
    
    content = re.sub(agent_pattern, replace_agent, content)
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed {filepath.name}")

# Fix all agents
for agent_file in agent_files:
    filepath = agents_dir / agent_file
    if filepath.exists():
        try:
            fix_agent_file(filepath)
        except Exception as e:
            print(f"❌ Error fixing {agent_file}: {e}")
    else:
        print(f"⚠️  {agent_file} not found")

print("\n✅ All agents updated!")