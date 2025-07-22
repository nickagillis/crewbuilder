"""
CrewBuilder V2 - Proper CrewAI Implementation
This follows CrewAI best practices with simple agents and smart tasks
"""

from crewai import Crew, Process
from typing import Dict, Any, Optional
import os
from datetime import datetime

# Import our simple agents
from agents.simple_agents import get_all_crewbuilder_agents
from agents.cost_optimizer import enforce_cost_limit

# Import our task creators
from tasks.crewbuilder_tasks import (
    create_clarification_task,
    create_api_verification_task,
    create_architecture_design_task,
    create_task_flow_design_task,
    create_code_generation_task,
    create_quality_review_task,
    create_deployment_config_task,
    create_documentation_task,
    create_final_package_task
)
from tasks.interface_tasks import (
    create_interface_generation_task,
    create_deployment_wrapper_task
)

class CrewBuilderV2:
    """
    CrewBuilder following CrewAI best practices
    - Simple agents (role/goal/backstory only)
    - Smart tasks (contain all the logic)
    - Proper orchestration (hierarchical process)
    """
    
    def __init__(self):
        """Initialize CrewBuilder with all agents"""
        print("🚀 Initializing CrewBuilder V2...")
        self.agents = get_all_crewbuilder_agents()
        print(f"✅ Loaded {len(self.agents)} specialized agents")
        
    def run_clarification_phase(self, requirement: str) -> Dict[str, Any]:
        """
        Phase 1: Clarification
        Uses a simple sequential crew for focused clarification
        """
        print("\n📝 Phase 1: Clarification")
        
        # Create clarification task
        clarify_task = create_clarification_task(requirement)
        clarify_task.agent = self.agents['clarification']
        
        # Create API verification task
        api_task = create_api_verification_task(requirement)
        api_task.agent = self.agents['api_analyst']
        api_task.context = [clarify_task]
        
        # Simple crew for clarification
        clarification_crew = Crew(
            agents=[
                self.agents['clarification'],
                self.agents['api_analyst']
            ],
            tasks=[clarify_task, api_task],
            process=Process.sequential,
            verbose=False,  # Reduce token usage
            memory=False    # No memory for clarification phase
        )
        
        try:
            result = clarification_crew.kickoff()
            return {
                'success': True,
                'clarification_questions': str(clarify_task.output),
                'api_report': str(api_task.output),
                'result': str(result)
            }
        except Exception as e:
            print(f"❌ Clarification failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def build_complete_system(self, 
                            requirement: str, 
                            clarification_responses: Optional[Dict[str, str]] = None,
                            api_report: Optional[str] = None) -> Dict[str, Any]:
        """
        Phase 2: Build Complete System
        Uses hierarchical process with manager coordination
        """
        print("\n🏗️ Phase 2: Building Complete System")
        
        # If we don't have an API report, we need to run verification first
        if not api_report:
            api_task = create_api_verification_task(requirement, clarification_responses)
            api_task.agent = self.agents['api_analyst']
            # Run just this task
            api_crew = Crew(
                agents=[self.agents['api_analyst']],
                tasks=[api_task],
                process=Process.sequential,
                verbose=True
            )
            api_result = api_crew.kickoff()
            api_report = str(api_result)
        
        # Create all building tasks with proper dependencies
        tasks = []
        
        # 1. Architecture Design
        arch_task = create_architecture_design_task(requirement, api_report)
        arch_task.agent = self.agents['architect']
        tasks.append(arch_task)
        
        # 2. Task Flow Design
        flow_task = create_task_flow_design_task("{architecture}")  # Will be filled by context
        flow_task.agent = self.agents['task_designer']
        flow_task.context = [arch_task]
        tasks.append(flow_task)
        
        # 3. Code Generation
        code_task = create_code_generation_task("{architecture}", "{task_flow}")
        code_task.agent = self.agents['code_writer']
        code_task.context = [arch_task, flow_task]
        tasks.append(code_task)
        
        # 4. Quality Review
        review_task = create_quality_review_task("{generated_code}", requirement)
        review_task.agent = self.agents['quality_reviewer']
        review_task.context = [code_task]
        tasks.append(review_task)
        
        # 5. Deployment Configuration
        deploy_task = create_deployment_config_task("{generated_code}")
        deploy_task.agent = self.agents['deployment']
        deploy_task.context = [code_task]
        tasks.append(deploy_task)
        
        # 6. Interface Generation - NEW!
        interface_task = create_interface_generation_task("{generated_code}", requirement)
        interface_task.agent = self.agents['interface_builder']
        interface_task.context = [code_task]
        tasks.append(interface_task)
        
        # 7. Deployment Wrapper - NEW!
        wrapper_task = create_deployment_wrapper_task("{interface_code}")
        wrapper_task.agent = self.agents['execution_wrapper']
        wrapper_task.context = [interface_task]
        tasks.append(wrapper_task)
        
        # 8. Documentation (updated to include interface docs)
        docs_task = create_documentation_task("{generated_code}", "{deployment_config}")
        docs_task.agent = self.agents['documentation']
        docs_task.context = [code_task, deploy_task, interface_task]
        tasks.append(docs_task)
        
        # 9. Final Package
        package_task = create_final_package_task()
        package_task.agent = self.agents['manager']  # Manager summarizes everything
        package_task.context = tasks[:-1]  # All previous tasks
        tasks.append(package_task)
        
        # Create the main building crew with hierarchical process
        building_crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.hierarchical,  # Manager coordinates everything
            manager_llm=self.agents['manager'].llm,
            verbose=False,  # Reduce token usage
            memory=False    # Disable memory to save tokens
        )
        
        # Apply cost controls
        enforce_cost_limit(building_crew, max_cost=2.0)
        
        print(f"📋 Created {len(tasks)} tasks for {len(self.agents)} agents")
        print("🎯 Starting hierarchical orchestration...")
        
        try:
            start_time = datetime.now()
            result = building_crew.kickoff()
            execution_time = (datetime.now() - start_time).total_seconds()
            
            print(f"\n✅ System built in {execution_time:.1f} seconds")
            
            # Extract outputs from tasks
            outputs = {}
            task_names = ['architecture', 'task_flow', 'code', 'review', 'deployment', 'interface', 'wrapper', 'documentation', 'package']
            
            for task, name in zip(tasks, task_names):
                try:
                    outputs[name] = str(task.output) if hasattr(task, 'output') else None
                except:
                    outputs[name] = None
            
            # Parse generated code from the code task output
            generated_code = outputs.get('code', '')
            
            # Extract main.py content if present
            main_py = ""
            if "```python" in generated_code and "main.py" in generated_code:
                # Extract main.py content
                start = generated_code.find("```python")
                end = generated_code.find("```", start + 1)
                if start != -1 and end != -1:
                    main_py = generated_code[start+9:end].strip()
            
            # Extract requirements.txt
            requirements = "crewai==0.148.0\ncrewai-tools\nopenai>=1.0.0"
            if "requirements.txt" in generated_code:
                start = generated_code.find("requirements.txt")
                # Look for content after requirements.txt
                content_start = generated_code.find("```", start)
                content_end = generated_code.find("```", content_start + 1)
                if content_start != -1 and content_end != -1:
                    requirements = generated_code[content_start+3:content_end].strip()
            
            return {
                'success': True,
                'execution_time': execution_time,
                'requirement': requirement,
                'architecture': outputs.get('architecture'),
                'generated_code': main_py or generated_code,
                'interface_code': outputs.get('interface'),
                'deployment_package': outputs.get('wrapper'),
                'requirements_txt': requirements,
                'deployment_config': outputs.get('deployment'),
                'documentation': outputs.get('documentation'),
                'quality_review': outputs.get('review'),
                'package_summary': outputs.get('package'),
                'final_result': str(result)
            }
            
        except Exception as e:
            print(f"❌ System building failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def build_from_requirement(self, requirement: str) -> Dict[str, Any]:
        """
        Complete end-to-end system building
        Combines clarification and building phases
        """
        print(f"\n🎯 Building system for: {requirement[:100]}...")
        
        # Phase 1: Clarification
        clarification_result = self.run_clarification_phase(requirement)
        
        if not clarification_result['success']:
            return clarification_result
        
        # Phase 2: Build System
        system_result = self.build_complete_system(
            requirement=requirement,
            api_report=clarification_result.get('api_report')
        )
        
        # Combine results
        return {
            **system_result,
            'clarification_questions': clarification_result.get('clarification_questions'),
            'api_report': clarification_result.get('api_report')
        }

# Singleton instance
_crewbuilder = None

def get_crewbuilder_v2() -> CrewBuilderV2:
    """Get or create CrewBuilder instance"""
    global _crewbuilder
    if _crewbuilder is None:
        _crewbuilder = CrewBuilderV2()
    return _crewbuilder

# Example usage
if __name__ == "__main__":
    # Test with the user's example
    test_requirement = """
    I need set up an agent that will take in a list of content ideas. 
    Research the topics and news using open ai deep research or something similar. 
    generate a short 2-3 minute script then generate videos using hey gen with a 
    certain avatar id that I've created and then send them to people in my crm gohighlevel.
    """
    
    crewbuilder = get_crewbuilder_v2()
    result = crewbuilder.build_from_requirement(test_requirement)
    
    if result['success']:
        print("\n✅ System built successfully!")
        print(f"📄 Generated {len(result.get('generated_code', ''))} characters of code")
        print(f"📋 Review: {result.get('quality_review', 'N/A')[:200]}...")
    else:
        print(f"\n❌ Build failed: {result.get('error')}")