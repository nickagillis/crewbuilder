"""Code Generator Agent - Converts crew architectures into runnable CrewAI Python code"""

from dataclasses import dataclass
from typing import List, Dict, Any
import json
import re

from crewai import Agent, Task, Crew
from .llm_config import get_configured_llm
from .system_architect import CrewArchitecture, GeneratedCode


class CodeGenerator:
    """
    AI-powered code generation agent that converts crew architectures 
    into complete, runnable CrewAI Python code packages.
    
    Transforms CrewArchitecture specifications into production-ready code
    with proper error handling, documentation, and configuration management.
    """
    
    def __init__(self):
        """Initialize the Code Generator agent"""
        # Get configured LLM

        llm = get_configured_llm(temperature=0.7)

        

        self.agent = Agent(
            role="Code Generation Specialist",
            goal="Convert crew architectures into clean, runnable CrewAI Python code",
            backstory="""You are an expert Python developer specializing in CrewAI framework.
            Your expertise lies in translating architectural specifications into clean, 
            well-documented, production-ready code. You understand CrewAI patterns, 
            best practices, and proper error handling. You generate code that is not only 
            functional but also maintainable and following Python conventions.""",
            verbose=True,
            max_iter=3,
            memory=True,
            allow_delegation=False,
            llm=llm  # Pass the LLM explicitly
        )
    
    def generate_crew_code(self, crew_architecture: CrewArchitecture) -> GeneratedCode:
        """
        Main method: Generate complete CrewAI code from architecture specification
        
        Args:
            crew_architecture: Complete crew architecture from SystemArchitect
            
        Returns:
            GeneratedCode: Complete code package ready for deployment
        """
        print(f"🔧 Generating code for: {crew_architecture.crew_name}")
        print(f"   📊 Agents: {len(crew_architecture.agents)}")
        print(f"   📋 Tasks: {len(crew_architecture.tasks)}")
        
        # Create code generation task
        generation_task = Task(
            description=f"""Generate complete, runnable CrewAI Python code for the following crew architecture:

CREW SPECIFICATION:
- Name: {crew_architecture.crew_name}
- Description: {crew_architecture.crew_description}
- Estimated Runtime: {crew_architecture.estimated_runtime}

AGENTS TO IMPLEMENT:
{self._format_agents_for_prompt(crew_architecture.agents)}

TASKS TO IMPLEMENT:
{self._format_tasks_for_prompt(crew_architecture.tasks)}

WORKFLOW:
- Name: {crew_architecture.workflow.name}
- Description: {crew_architecture.workflow.description}
- Task Sequence: {' -> '.join(crew_architecture.workflow.task_sequence)}

DEPENDENCIES: {', '.join(crew_architecture.dependencies)}

REQUIREMENTS:
1. Generate complete Python code using CrewAI framework
2. Include proper imports and dependencies
3. Create Agent instances with all specified properties
4. Create Task instances with proper agent assignments
5. Create Crew instance with proper orchestration
6. Add comprehensive error handling and logging
7. Include clear documentation and docstrings
8. Add configuration management for API keys
9. Include usage examples and setup instructions

OUTPUT FORMAT:
Return a structured response with these sections:
MAIN_CODE: [Complete Python code]
REQUIREMENTS: [Dependencies list for requirements.txt]
CONFIG: [Environment configuration template]
SETUP: [Step-by-step setup instructions]
USAGE: [Example usage code]
TESTS: [Basic validation tests]
COST: [Estimated API costs and usage]
PERFORMANCE: [Runtime and resource notes]""",
            expected_output="Complete CrewAI code package with all required components",
            agent=self.agent
        )
        
        # Execute the generation task
        crew = Crew([self.agent], [generation_task], verbose=True)
        result = crew.kickoff()
        
        # Parse the AI-generated response
        try:
            generated_code = self._parse_code_generation(str(result))
            print("✅ Code generation completed successfully!")
            return generated_code
        except Exception as e:
            print(f"⚠️  AI parsing failed, using fallback: {e}")
            return self._create_fallback_code(crew_architecture)
    
    def _format_agents_for_prompt(self, agents) -> str:
        """Format agent specifications for the AI prompt"""
        formatted = []
        for agent in agents:
            formatted.append(f"""
Agent: {agent.name}
- Role: {agent.role}
- Goal: {agent.goal}
- Backstory: {agent.backstory}
- Tools: {', '.join(agent.tools)}
- Max Iterations: {agent.max_iter}
- Memory: {agent.memory}
- Verbose: {agent.verbose}
- Allow Delegation: {agent.allow_delegation}""")
        return '\n'.join(formatted)
    
    def _format_tasks_for_prompt(self, tasks) -> str:
        """Format task specifications for the AI prompt"""
        formatted = []
        for task in tasks:
            formatted.append(f"""
Task: {task.name}
- Description: {task.description}
- Assigned Agent: {task.agent_name}
- Expected Output: {task.expected_output}
- Output Format: {task.output_format}
- Dependencies: {', '.join(task.depends_on) if task.depends_on else 'None'}""")
        return '\n'.join(formatted)
    
    def _parse_code_generation(self, ai_response: str) -> GeneratedCode:
        """Parse the AI-generated code response into structured format"""
        
        # Extract sections using regex patterns
        sections = {
            'MAIN_CODE': self._extract_section(ai_response, 'MAIN_CODE'),
            'REQUIREMENTS': self._extract_section(ai_response, 'REQUIREMENTS'),
            'CONFIG': self._extract_section(ai_response, 'CONFIG'),
            'SETUP': self._extract_section(ai_response, 'SETUP'),
            'USAGE': self._extract_section(ai_response, 'USAGE'),
            'TESTS': self._extract_section(ai_response, 'TESTS'),
            'COST': self._extract_section(ai_response, 'COST'),
            'PERFORMANCE': self._extract_section(ai_response, 'PERFORMANCE')
        }
        
        return GeneratedCode(
            main_code=sections['MAIN_CODE'] or "# Code generation failed",
            requirements_txt=sections['REQUIREMENTS'] or "crewai>=0.1.0",
            config_template=sections['CONFIG'] or "# Add your API keys here",
            setup_instructions=sections['SETUP'] or "1. Install dependencies\n2. Configure API keys",
            usage_example=sections['USAGE'] or "# Run the generated crew",
            validation_tests=sections['TESTS'] or "# Add tests here",
            estimated_cost=sections['COST'] or "Estimate not available",
            performance_notes=sections['PERFORMANCE'] or "Performance analysis pending"
        )
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from the AI response"""
        pattern = rf"{section_name}:\s*(.*?)(?=\n[A-Z_]+:|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        
        if match:
            content = match.group(1).strip()
            # Clean up common formatting artifacts
            content = re.sub(r'^\[|\]$', '', content)  # Remove brackets
            content = re.sub(r'^```python\n|```$', '', content, flags=re.MULTILINE)  # Remove code blocks
            return content.strip()
        
        return ""
    
    def _create_fallback_code(self, crew_architecture: CrewArchitecture) -> GeneratedCode:
        """Create basic code when AI generation fails"""
        
        # Generate basic CrewAI code using templates
        agents_code = self._generate_agents_code(crew_architecture.agents)
        tasks_code = self._generate_tasks_code(crew_architecture.tasks)
        crew_code = self._generate_crew_code(crew_architecture)
        
        main_code = f'''"""
{crew_architecture.crew_name}
{crew_architecture.crew_description}

Auto-generated by CrewBuilder
"""

from crewai import Agent, Task, Crew
import os
from typing import List

# Agent Definitions
{agents_code}

# Task Definitions  
{tasks_code}

# Crew Definition
{crew_code}

if __name__ == "__main__":
    print("🚀 Starting {crew_architecture.crew_name}")
    result = crew.kickoff()
    # Convert CrewOutput to string for proper handling
    result_text = str(result)
    print("✅ Crew execution completed!")
    print(f"Result: {{result_text}}")
'''

        requirements = """crewai>=0.1.0
python-dotenv>=1.0.0
openai>=1.0.0"""

        config = """# Environment Configuration
# Copy this to .env and add your API keys

OPENAI_API_KEY=your_openai_key_here
# Add other API keys as needed"""

        setup = f"""# Setup Instructions for {crew_architecture.crew_name}

1. Install dependencies:
   pip install -r requirements.txt

2. Configure environment:
   - Copy config template to .env file
   - Add your API keys

3. Run the crew:
   python main.py

Dependencies needed: {', '.join(crew_architecture.dependencies)}"""

        return GeneratedCode(
            main_code=main_code,
            requirements_txt=requirements,
            config_template=config,
            setup_instructions=setup,
            usage_example="python main.py",
            validation_tests="# Basic validation tests would go here",
            estimated_cost="Varies based on API usage",
            performance_notes=f"Estimated runtime: {crew_architecture.estimated_runtime}"
        )
    
    def _generate_agents_code(self, agents) -> str:
        """Generate CrewAI Agent code from specifications"""
        code_parts = []
        
        for agent in agents:
            tools_str = ', '.join([f'"# {tool}"' for tool in agent.tools]) if agent.tools else ""
            tools_list = f"[{tools_str}]" if agent.tools else "[]"
            
            code_parts.append(f'''{agent.name.lower().replace(" ", "_")} = Agent(
    role="{agent.role}",
    goal="{agent.goal}",
    backstory="""{agent.backstory}""",
    tools={tools_list},
    max_iter={agent.max_iter},
    memory={agent.memory},
    verbose={agent.verbose},
    allow_delegation={agent.allow_delegation}
)''')
        
        return '\n\n'.join(code_parts)
    
    def _generate_tasks_code(self, tasks) -> str:
        """Generate CrewAI Task code from specifications"""
        code_parts = []
        
        for task in tasks:
            agent_var = task.agent_name.lower().replace(" ", "_")
            
            code_parts.append(f'''{task.name.lower().replace(" ", "_")} = Task(
    description="""{task.description}""",
    expected_output="{task.expected_output}",
    agent={agent_var}
)''')
        
        return '\n\n'.join(code_parts)
    
    def _generate_crew_code(self, crew_architecture: CrewArchitecture) -> str:
        """Generate CrewAI Crew orchestration code"""
        
        agent_vars = [agent.name.lower().replace(" ", "_") for agent in crew_architecture.agents]
        task_vars = [task.name.lower().replace(" ", "_") for task in crew_architecture.tasks]
        
        return f'''crew = Crew(
    agents=[{', '.join(agent_vars)}],
    tasks=[{', '.join(task_vars)}],
    verbose=True,
    memory=True
)'''


def create_code_generator() -> CodeGenerator:
    """Factory function to create a CodeGenerator instance"""
    return CodeGenerator()


# Testing section for development
if __name__ == "__main__":
    # Quick test of the code generator
    generator = create_code_generator()
    print("🔧 Code Generator agent initialized successfully!")
    print(f"Agent role: {generator.agent.role}")
    print(f"Agent goal: {generator.agent.goal}")
