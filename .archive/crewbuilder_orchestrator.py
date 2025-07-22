"""
CrewBuilder Orchestrator - Proper CrewAI Implementation
This module uses CrewAI's full capabilities to orchestrate all 11 agents
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any, List
from datetime import datetime
import os

# Import all our agents
from agents.clarification_agent import create_clarification_agent
from agents.requirements_analyst import create_requirements_analyst
from agents.system_architect import create_system_architect
from agents.code_generator import create_code_generator
from agents.quality_assurance import create_quality_assurance_agent
from agents.api_detective import create_api_detective
from agents.documentation_specialist import create_documentation_specialist
from agents.infrastructure_analyst import create_infrastructure_analyst
from agents.deployment_engineer import create_deployment_engineer
from agents.hosting_assistant import create_hosting_assistant
from agents.monitoring_engineer import create_monitoring_engineer
from agents.llm_config import get_configured_llm

class CrewBuilderOrchestrator:
    """Orchestrates all 11 agents using CrewAI's hierarchical process"""
    
    def __init__(self):
        """Initialize all agents and the orchestration manager"""
        print("🚀 Initializing CrewBuilder Orchestrator...")
        
        # Create the manager LLM for hierarchical orchestration
        self.manager_llm = get_configured_llm(model="gpt-4", temperature=0.7)
        
        # Initialize all agents
        self.agents = {
            'clarification': create_clarification_agent(),
            'requirements': create_requirements_analyst(),
            'architect': create_system_architect(),
            'code_generator': create_code_generator(),
            'qa': create_quality_assurance_agent(),
            'api_detective': create_api_detective(),
            'documentation': create_documentation_specialist(),
            'infrastructure': create_infrastructure_analyst(),
            'deployment': create_deployment_engineer(),
            'hosting': create_hosting_assistant(),
            'monitoring': create_monitoring_engineer()
        }
        
        print(f"✅ Initialized {len(self.agents)} agents")
    
    def create_generation_tasks(self, user_requirement: str, clarified_requirements: Dict[str, Any] = None) -> List[Task]:
        """Create all tasks with proper dependencies"""
        
        tasks = []
        
        # Task 1: Requirements Analysis
        requirements_task = Task(
            description=f"""
            Analyze this business requirement and create a detailed technical specification:
            
            Original requirement: {user_requirement}
            {f"Clarified details: {clarified_requirements}" if clarified_requirements else ""}
            
            Focus on:
            1. Understanding the core business problem
            2. Identifying all necessary agent roles
            3. Mapping out the workflow
            4. Listing required integrations
            5. Estimating complexity
            
            Be specific and thorough.
            """,
            agent=self.agents['requirements'],
            expected_output="Detailed technical specification with agent roles and workflow"
        )
        tasks.append(requirements_task)
        
        # Task 2: System Architecture (depends on requirements)
        architecture_task = Task(
            description="""
            Design the complete CrewAI architecture based on the requirements analysis.
            
            Create:
            1. Detailed agent definitions (name, role, goal, backstory, tools)
            2. Task definitions with clear dependencies
            3. Workflow structure (sequential or hierarchical)
            4. Integration points and data flow
            5. Error handling strategy
            
            Ensure the architecture is production-ready and scalable.
            """,
            agent=self.agents['architect'],
            expected_output="Complete CrewAI architecture with agents, tasks, and workflow",
            context=[requirements_task]  # Depends on requirements
        )
        tasks.append(architecture_task)
        
        # Task 3: API Discovery (can run parallel to architecture)
        api_task = Task(
            description="""
            Research and document all APIs needed for this system.
            
            For each integration mentioned:
            1. Find the official API documentation
            2. Identify authentication methods
            3. List relevant endpoints
            4. Note rate limits and costs
            5. Provide code examples
            
            If no API exists, suggest alternatives.
            """,
            agent=self.agents['api_detective'],
            expected_output="Comprehensive API integration guide with examples",
            context=[requirements_task]
        )
        tasks.append(api_task)
        
        # Task 4: Code Generation (depends on architecture and APIs)
        code_task = Task(
            description="""
            Generate production-ready CrewAI code based on the architecture.
            
            Include:
            1. Complete main.py with all agents and tasks
            2. Proper error handling and logging
            3. Configuration management
            4. Requirements.txt with versions
            5. Environment variable handling
            
            Code must be immediately runnable.
            """,
            agent=self.agents['code_generator'],
            expected_output="Complete, production-ready CrewAI implementation",
            context=[architecture_task, api_task]  # Depends on both
        )
        tasks.append(code_task)
        
        # Task 5: Quality Assurance (depends on code)
        qa_task = Task(
            description="""
            Validate the generated code for quality and completeness.
            
            Check:
            1. Code syntax and structure
            2. Error handling coverage
            3. Security best practices
            4. Performance considerations
            5. Test coverage recommendations
            
            Provide specific improvements if needed.
            """,
            agent=self.agents['qa'],
            expected_output="QA report with validation results and improvements",
            context=[code_task]
        )
        tasks.append(qa_task)
        
        # Task 6: Documentation (depends on code and QA)
        docs_task = Task(
            description="""
            Create comprehensive documentation for the system.
            
            Include:
            1. README with setup instructions
            2. API documentation
            3. Configuration guide
            4. Troubleshooting section
            5. Examples and use cases
            
            Make it user-friendly and complete.
            """,
            agent=self.agents['documentation'],
            expected_output="Complete documentation package",
            context=[code_task, qa_task]
        )
        tasks.append(docs_task)
        
        # Task 7: Infrastructure Analysis (can run parallel to docs)
        infra_task = Task(
            description="""
            Analyze infrastructure requirements and provide recommendations.
            
            Consider:
            1. Compute requirements
            2. Storage needs
            3. Networking configuration
            4. Security requirements
            5. Cost optimization
            
            Recommend specific services and configurations.
            """,
            agent=self.agents['infrastructure'],
            expected_output="Infrastructure recommendations with cost estimates",
            context=[architecture_task, code_task]
        )
        tasks.append(infra_task)
        
        # Task 8: Deployment Configuration (depends on infra)
        deploy_task = Task(
            description="""
            Create deployment configurations and automation.
            
            Provide:
            1. Dockerfile or deployment scripts
            2. CI/CD pipeline configuration
            3. Environment setup
            4. Secrets management
            5. Rollback procedures
            
            Focus on Railway deployment.
            """,
            agent=self.agents['deployment'],
            expected_output="Complete deployment configuration",
            context=[infra_task, code_task]
        )
        tasks.append(deploy_task)
        
        # Task 9: Hosting Setup (depends on deployment)
        hosting_task = Task(
            description="""
            Configure hosting and provide setup instructions.
            
            Include:
            1. Railway project setup
            2. Environment variable configuration
            3. Domain setup (if needed)
            4. SSL configuration
            5. Backup strategy
            
            Make it step-by-step clear.
            """,
            agent=self.agents['hosting'],
            expected_output="Hosting setup guide",
            context=[deploy_task]
        )
        tasks.append(hosting_task)
        
        # Task 10: Monitoring Setup (final task)
        monitoring_task = Task(
            description="""
            Set up monitoring and observability.
            
            Configure:
            1. Logging strategy
            2. Error tracking
            3. Performance monitoring
            4. Alerts and notifications
            5. Dashboard setup
            
            Ensure production readiness.
            """,
            agent=self.agents['monitoring'],
            expected_output="Monitoring configuration and setup guide",
            context=[deploy_task, hosting_task]
        )
        tasks.append(monitoring_task)
        
        return tasks
    
    def build_crew_system(self, user_requirement: str, clarified_requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main orchestration method - builds complete system using CrewAI
        """
        print("\n🎯 Starting CrewBuilder Orchestration")
        print(f"📋 Requirement: {user_requirement[:100]}...")
        
        # Create all tasks with dependencies
        tasks = self.create_generation_tasks(user_requirement, clarified_requirements)
        
        # Get all agents for the crew (excluding clarification as it runs separately)
        crew_agents = [
            self.agents['requirements'],
            self.agents['architect'],
            self.agents['api_detective'],
            self.agents['code_generator'],
            self.agents['qa'],
            self.agents['documentation'],
            self.agents['infrastructure'],
            self.agents['deployment'],
            self.agents['hosting'],
            self.agents['monitoring']
        ]
        
        # Create the crew with hierarchical process
        print("\n🏗️ Creating CrewAI Crew with hierarchical orchestration...")
        crew = Crew(
            agents=crew_agents,
            tasks=tasks,
            process=Process.hierarchical,  # Manager coordinates all agents
            manager_llm=self.manager_llm,   # GPT-4 manages the crew
            verbose=True,
            memory=True,  # Enable memory sharing between agents
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-ada-002"
                }
            }
        )
        
        # Execute the crew
        print("\n🚀 Executing CrewAI pipeline...")
        start_time = datetime.now()
        
        try:
            # Kickoff returns the final task's output
            result = crew.kickoff()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            print(f"\n✅ Pipeline completed in {execution_time:.1f} seconds")
            
            # Process results from all tasks
            return self._process_crew_results(result, tasks, execution_time)
            
        except Exception as e:
            print(f"\n❌ Crew execution failed: {str(e)}")
            raise
    
    def _process_crew_results(self, final_result: Any, tasks: List[Task], execution_time: float) -> Dict[str, Any]:
        """Process and structure the results from all crew tasks"""
        
        # CrewAI stores task outputs in task.output
        results = {
            'success': True,
            'execution_time': execution_time,
            'generated_at': datetime.now().isoformat(),
            'tasks_completed': len(tasks),
            'final_output': str(final_result),
            'task_outputs': {}
        }
        
        # Extract outputs from each task
        task_names = [
            'requirements_analysis',
            'system_architecture', 
            'api_discovery',
            'code_generation',
            'quality_assurance',
            'documentation',
            'infrastructure_analysis',
            'deployment_config',
            'hosting_setup',
            'monitoring_setup'
        ]
        
        for i, (task, name) in enumerate(zip(tasks, task_names)):
            try:
                # Get task output (CrewAI stores it in task.output after execution)
                output = getattr(task, 'output', None)
                results['task_outputs'][name] = {
                    'completed': output is not None,
                    'output': str(output) if output else None,
                    'agent': task.agent.role
                }
            except Exception as e:
                print(f"Warning: Could not extract output for {name}: {e}")
                results['task_outputs'][name] = {
                    'completed': False,
                    'error': str(e)
                }
        
        # Extract specific artifacts
        try:
            # Get generated code from code generation task
            code_output = results['task_outputs'].get('code_generation', {}).get('output', '')
            if 'main.py' in code_output or 'import' in code_output:
                results['generated_code'] = code_output
            
            # Get requirements.txt if present
            if 'requirements.txt' in code_output or 'pip install' in code_output:
                # Extract requirements section
                lines = code_output.split('\n')
                req_start = False
                requirements = []
                for line in lines:
                    if 'requirements' in line.lower():
                        req_start = True
                    elif req_start and line.strip() and not line.startswith('#'):
                        requirements.append(line.strip())
                results['requirements_txt'] = '\n'.join(requirements)
            
            # Get architecture summary
            arch_output = results['task_outputs'].get('system_architecture', {}).get('output', '')
            results['architecture_summary'] = arch_output[:500] if arch_output else None
            
            # Get deployment instructions
            deploy_output = results['task_outputs'].get('deployment_config', {}).get('output', '')
            results['deployment_instructions'] = deploy_output
            
        except Exception as e:
            print(f"Warning: Error extracting artifacts: {e}")
        
        return results
    
    def run_clarification(self, user_requirement: str) -> Dict[str, Any]:
        """Run just the clarification agent separately"""
        print("\n💬 Running Clarification Agent...")
        
        # Import the clarification functions
        from agents.clarification_agent import analyze_initial_requirement
        
        try:
            # Get clarification questions
            questions = analyze_initial_requirement(
                self.agents['clarification'],
                user_requirement
            )
            
            return {
                'success': True,
                'questions': [
                    {
                        'question': q.question,
                        'context': q.context,
                        'type': q.question_type,
                        'options': q.options
                    }
                    for q in questions
                ],
                'session_id': f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
        except Exception as e:
            print(f"❌ Clarification failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }


# Singleton instance
_orchestrator = None

def get_orchestrator() -> CrewBuilderOrchestrator:
    """Get or create the orchestrator singleton"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = CrewBuilderOrchestrator()
    return _orchestrator