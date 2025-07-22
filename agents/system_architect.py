"""
System Architect Agent for CrewBuilder

Takes technical specifications and designs optimal CrewAI crew architectures.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from crewai import Agent, Task, Crew
from .llm_config import get_configured_llm
from .requirements_analyst import TechnicalSpecification


@dataclass
class AgentSpecification:
    """Detailed specification for a single CrewAI agent"""
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str]
    max_iter: int = 5
    memory: bool = True
    verbose: bool = True
    allow_delegation: bool = False


@dataclass
class TaskSpecification:
    """Detailed specification for a CrewAI task"""
    name: str
    description: str
    agent_name: str
    expected_output: str
    depends_on: List[str]  # List of task names this depends on
    output_format: str = "text"  # text, json, file, etc.


@dataclass
class CrewWorkflow:
    """High-level workflow orchestration"""
    name: str
    description: str
    task_sequence: List[str]  # Ordered list of task names
    parallel_tasks: List[List[str]]  # Groups of tasks that can run in parallel
    decision_points: List[Dict[str, str]]  # Conditional logic points


@dataclass
class CrewArchitecture:
    """Complete crew architecture specification"""
    crew_name: str
    crew_description: str
    agents: List[AgentSpecification]
    tasks: List[TaskSpecification]
    workflow: CrewWorkflow
    estimated_runtime: str  # e.g., "15-30 minutes"
    resource_requirements: Dict[str, str]
    success_metrics: List[str]
    dependencies: List[str]  # Required packages/APIs


@dataclass
class GeneratedCode:
    """Complete generated CrewAI code package"""
    main_code: str              # Complete Python code for the crew
    requirements_txt: str       # Dependencies list
    config_template: str        # Environment configuration template
    setup_instructions: str     # Human-readable setup guide
    usage_example: str          # Example of how to run the generated crew
    validation_tests: str       # Basic tests for the generated code
    estimated_cost: str         # Estimated API costs for running the crew
    performance_notes: str      # Expected runtime and resource usage


class SystemArchitect:
    """
    CrewAI-powered agent that designs optimal crew architectures from technical specifications.
    
    This agent uses AI reasoning to create detailed agent specifications, task workflows,
    and crew orchestration patterns optimized for specific business requirements.
    """
    
    def __init__(self):
        # Get configured LLM

        llm = get_configured_llm(temperature=0.7)

        

        self.agent = Agent(
            role='System Architect',
            goal='Design optimal multi-agent crew architectures that efficiently solve complex business problems',
            backstory="""You are a world-class system architect and CrewAI expert with deep understanding of:
            
            1. Multi-agent system design patterns and best practices
            2. CrewAI framework capabilities, limitations, and optimal usage patterns
            3. Business process decomposition into coordinated agent workflows
            4. Task interdependency analysis and parallel execution optimization
            5. Agent specialization and role definition for maximum efficiency
            6. Tool selection and integration patterns for different business domains
            
            You excel at taking technical specifications and designing elegant, efficient crew architectures
            that leverage the strengths of specialized agents working in coordinated workflows. You consider
            factors like task complexity, data flow, error handling, and scalability in your designs.
            
            Your architectures are practical, well-documented, and optimized for real-world business value.""",
            verbose=True,
            allow_delegation=False,
            llm=llm  # Pass the LLM explicitly
        )
    
    def design_crew_architecture(self, tech_spec: TechnicalSpecification) -> CrewArchitecture:
        """
        AI-powered design of optimal crew architecture from technical specifications.
        
        Args:
            tech_spec: TechnicalSpecification from Requirements Analyst
            
        Returns:
            CrewArchitecture: Detailed crew design ready for code generation
        """
        # Create AI-powered architecture design task
        design_task = Task(
            description=f"""
            Design an optimal CrewAI crew architecture based on these technical specifications:
            
            TECHNICAL SPECIFICATIONS:
            - Complexity: {tech_spec.complexity_estimate}
            - Estimated Agents: {tech_spec.estimated_agents}
            - Required Agent Roles: {tech_spec.agent_roles_needed}
            - Workflow Steps: {tech_spec.workflow_steps}
            - APIs Required: {tech_spec.apis_required}
            - Data Flows: {tech_spec.data_flows}
            
            Design a complete crew architecture including:
            
            1. AGENT SPECIFICATIONS: For each agent role, define:
               - Specific role name and responsibilities
               - Clear goal statement
               - Detailed backstory with relevant expertise
               - Required tools and capabilities
               - Configuration parameters (max_iter, memory, etc.)
            
            2. TASK SPECIFICATIONS: For each major workflow step, define:
               - Task name and detailed description
               - Which agent should execute it
               - Expected output format and content
               - Dependencies on other tasks
               - Success criteria
            
            3. WORKFLOW ORCHESTRATION: Design:
               - Sequential task execution order
               - Opportunities for parallel execution
               - Decision points and conditional logic
               - Error handling and fallback strategies
            
            4. SYSTEM REQUIREMENTS: Specify:
               - Required external APIs and tools
               - Estimated runtime and resource needs
               - Success metrics and KPIs
               - Package dependencies
            
            Focus on creating a design that is:
            - Efficient: Minimizes redundancy and maximizes parallel execution
            - Robust: Includes error handling and quality checks
            - Scalable: Can handle varying input volumes and complexity
            - Maintainable: Clear separation of concerns and well-defined interfaces
            
            Return your design in this structured format:
            CREW_NAME: [descriptive name]
            CREW_DESCRIPTION: [1-2 sentence description]
            
            AGENTS:
            [For each agent: NAME, ROLE, GOAL, BACKSTORY, TOOLS]
            
            TASKS:
            [For each task: NAME, DESCRIPTION, AGENT, OUTPUT, DEPENDENCIES]
            
            WORKFLOW:
            [Sequential order, parallel opportunities, decision points]
            
            REQUIREMENTS:
            [Runtime estimate, resources, metrics, dependencies]
            """,
            agent=self.agent,
            expected_output="Complete crew architecture design with agents, tasks, workflow, and requirements"
        )
        
        # Execute architecture design
        crew = Crew(agents=[self.agent], tasks=[design_task])
        result = crew.kickoff()
        
        # Parse AI response into CrewArchitecture
        return self._parse_architecture_design(result, tech_spec)
    
    def _parse_architecture_design(self, ai_result: str, tech_spec: TechnicalSpecification) -> CrewArchitecture:
        """Parse AI architecture design result into structured CrewArchitecture."""
        lines = ai_result.split('\n')
        
        # Initialize defaults
        crew_name = f"{tech_spec.complexity_estimate}_automation_crew"
        crew_description = "AI-powered automation crew for business process optimization"
        agents = []
        tasks = []
        workflow = None
        estimated_runtime = "15-30 minutes"
        resource_requirements = {"memory": "2GB", "cpu": "2 cores"}
        success_metrics = ["task_completion_rate", "output_quality", "execution_time"]
        dependencies = ["crewai", "openai"]
        
        # Parse AI response (with robust fallbacks)
        try:
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('CREW_NAME:'):
                    crew_name = line.split(':', 1)[1].strip()
                elif line.startswith('CREW_DESCRIPTION:'):
                    crew_description = line.split(':', 1)[1].strip()
                elif line.startswith('AGENTS:'):
                    current_section = 'agents'
                elif line.startswith('TASKS:'):
                    current_section = 'tasks'
                elif line.startswith('WORKFLOW:'):
                    current_section = 'workflow'
                elif line.startswith('REQUIREMENTS:'):
                    current_section = 'requirements'
        
        except Exception as e:
            print(f"Warning: Could not fully parse AI architecture design, using fallbacks: {e}")
        
        # Create fallback architecture if parsing fails
        if not agents:
            agents = self._create_fallback_agents(tech_spec)
        if not tasks:
            tasks = self._create_fallback_tasks(tech_spec, agents)
        if not workflow:
            workflow = self._create_fallback_workflow(tech_spec, tasks)
        
        return CrewArchitecture(
            crew_name=crew_name,
            crew_description=crew_description,
            agents=agents,
            tasks=tasks,
            workflow=workflow,
            estimated_runtime=estimated_runtime,
            resource_requirements=resource_requirements,
            success_metrics=success_metrics,
            dependencies=dependencies
        )
    
    def _create_fallback_agents(self, tech_spec: TechnicalSpecification) -> List[AgentSpecification]:
        """Create fallback agent specifications based on tech spec."""
        agents = []
        
        # Create agents based on the required roles from tech spec
        for i, role_info in enumerate(tech_spec.agent_roles_needed[:tech_spec.estimated_agents]):
            role = role_info.get('role', f'agent_{i+1}')
            responsibility = role_info.get('responsibility', 'Execute assigned tasks')
            
            agent = AgentSpecification(
                name=f"{role}_agent",
                role=role.replace('_', ' ').title(),
                goal=f"Efficiently execute {responsibility.lower()} with high quality results",
                backstory=f"""You are a specialized AI agent expert in {role.replace('_', ' ')}.
                You have extensive experience in {responsibility.lower()} and work collaboratively
                with other agents to achieve optimal business outcomes. You focus on quality,
                efficiency, and clear communication with your team.""",
                tools=self._get_tools_for_role(role),
                max_iter=5,
                memory=True,
                verbose=True,
                allow_delegation=False
            )
            agents.append(agent)
        
        return agents
    
    def _create_fallback_tasks(self, tech_spec: TechnicalSpecification, 
                             agents: List[AgentSpecification]) -> List[TaskSpecification]:
        """Create fallback task specifications based on workflow steps."""
        tasks = []
        
        for i, step_info in enumerate(tech_spec.workflow_steps):
            step = step_info.get('step', f'task_{i+1}')
            description = step_info.get('description', 'Execute workflow step')
            
            # Assign to appropriate agent (rotate if needed)
            agent_name = agents[i % len(agents)].name if agents else 'default_agent'
            
            task = TaskSpecification(
                name=f"{step}_task",
                description=f"Execute {description}. Ensure high quality output and proper validation.",
                agent_name=agent_name,
                expected_output=f"Completed {step} with validated results and clear status report",
                depends_on=[tasks[i-1].name] if i > 0 and tasks else [],
                output_format="text"
            )
            tasks.append(task)
        
        return tasks
    
    def _create_fallback_workflow(self, tech_spec: TechnicalSpecification,
                                tasks: List[TaskSpecification]) -> CrewWorkflow:
        """Create fallback workflow based on task dependencies."""
        return CrewWorkflow(
            name=f"{tech_spec.complexity_estimate}_workflow",
            description=f"Workflow for {tech_spec.complexity_estimate} automation with {len(tasks)} tasks",
            task_sequence=[task.name for task in tasks],
            parallel_tasks=[],  # Sequential by default
            decision_points=[]  # Simple linear workflow
        )
    
    def _get_tools_for_role(self, role: str) -> List[str]:
        """Get appropriate tools for an agent role."""
        tool_mapping = {
            'content_researcher': ['web_search', 'file_reader'],
            'content_generator': ['text_generator', 'template_engine'],
            'content_optimizer': ['seo_analyzer', 'readability_checker'],
            'data_processor': ['csv_handler', 'json_parser'],
            'task_executor': ['api_client', 'scheduler'],
            'output_formatter': ['file_writer', 'email_sender']
        }
        
        return tool_mapping.get(role, ['basic_tools', 'file_handler'])


def create_system_architect() -> SystemArchitect:
    """Factory function to create a SystemArchitect instance."""
    return SystemArchitect()


# Test function
if __name__ == "__main__":
    from .requirements_analyst import create_requirements_analyst
    
    # Test with sample technical specification
    analyst = create_requirements_analyst()
    
    test_input = """
    I run a digital marketing agency. I want to automate content creation:
    research trends, generate ideas, create drafts, optimize for SEO,
    schedule social posts, and track performance.
    """
    
    # Get technical specification from Requirements Analyst
    tech_spec = analyst.analyze_requirements(test_input)
    
    # Design crew architecture
    architect = create_system_architect()
    crew_architecture = architect.design_crew_architecture(tech_spec)
    
    print("=== CREW ARCHITECTURE DESIGN ===")
    print(f"Crew Name: {crew_architecture.crew_name}")
    print(f"Description: {crew_architecture.crew_description}")
    print(f"\nAgents: {len(crew_architecture.agents)}")
    for agent in crew_architecture.agents:
        print(f"  - {agent.name}: {agent.role}")
    
    print(f"\nTasks: {len(crew_architecture.tasks)}")
    for task in crew_architecture.tasks:
        print(f"  - {task.name}: {task.agent_name}")
    
    print(f"\nWorkflow: {crew_architecture.workflow.name}")
    print(f"Task Sequence: {' -> '.join(crew_architecture.workflow.task_sequence)}")
    
    print(f"\nEstimated Runtime: {crew_architecture.estimated_runtime}")
    print(f"Dependencies: {', '.join(crew_architecture.dependencies)}")
