"""
Requirements Analyst Agent for CrewBuilder

This agent transforms user business needs into structured technical requirements
that other agents can use to build CrewAI systems.

Role: Transform user business needs into structured technical requirements
Goal: Extract and structure business requirements systematically
Responsibilities: 
- Business process analysis
- Requirement clarification  
- Technical specification creation
"""

from crewai import Agent, Task, Crew
from typing import Dict, List, Any
import json
from dataclasses import dataclass

@dataclass
class BusinessRequirement:
    """Structured representation of a business requirement"""
    description: str
    priority: str  # high, medium, low
    category: str  # process, integration, automation, etc.
    inputs: List[str]
    outputs: List[str]
    constraints: List[str]
    success_criteria: List[str]

@dataclass
class TechnicalSpecification:
    """Technical specification derived from business requirements"""
    agent_roles_needed: List[Dict[str, str]]
    workflow_steps: List[Dict[str, str]]
    apis_required: List[str]
    data_flows: List[Dict[str, str]]
    complexity_estimate: str  # simple, moderate, complex
    estimated_agents: int


class RequirementsAnalyst:
    """
    CrewAI-powered agent that analyzes business requirements and converts them to technical specifications.
    
    This agent uses AI reasoning to intelligently parse business needs and recommend optimal agent architectures.
    """
    
    def __init__(self):
        self.agent = Agent(
            role='Requirements Analyst',
            goal='Transform user business needs into structured technical requirements with intelligent agent architecture recommendations',
            backstory="""You are an expert business analyst and system architect with deep understanding of 
            business processes, technical systems, and AI agent design patterns. You excel at:
            
            1. Analyzing business requirements to understand core automation needs
            2. Categorizing requirements by complexity and domain (content, integration, analysis, etc.)
            3. Recommending optimal multi-agent architectures for different business scenarios
            4. Identifying necessary APIs, tools, and integrations
            5. Asking intelligent clarifying questions to improve requirement quality
            
            You think systematically about how to break complex business workflows into coordinated agent teams.""",
            verbose=True,
            allow_delegation=False
        )
    
    def analyze_requirements(self, user_input: str) -> TechnicalSpecification:
        """
        AI-powered analysis of user business requirements.
        
        Args:
            user_input: Natural language description of business needs
            
        Returns:
            TechnicalSpecification: AI-generated structured technical requirements
        """
        # Create AI-powered analysis task
        analysis_task = Task(
            description=f"""
            Analyze the following business requirements and create a comprehensive technical specification:
            
            USER REQUIREMENTS:
            {user_input}
            
            Your analysis should:
            1. Categorize the business requirement (content_creation, system_integration, data_analysis, process_automation, system_development)
            2. Determine complexity level (simple, moderate, complex) based on workflow complexity
            3. Recommend optimal agent roles and responsibilities for this specific use case
            4. Identify necessary workflow steps in logical order
            5. Suggest required APIs and integrations (be specific when mentioned, generic when not)
            6. Estimate number of agents needed (typically 2-5 depending on complexity)
            
            IMPORTANT: Be platform-neutral unless the user specifically mentions technologies. Ask about preferences rather than assuming.
            
            Return your analysis in this structured format:
            CATEGORY: [category]
            COMPLEXITY: [simple/moderate/complex]
            ESTIMATED_AGENTS: [number]
            AGENT_ROLES: [list of role/responsibility pairs]
            WORKFLOW_STEPS: [ordered list of steps]
            APIS_REQUIRED: [specific APIs if mentioned, otherwise "TBD - requires user input"]
            """,
            agent=self.agent,
            expected_output="Structured technical analysis with agent architecture recommendations"
        )
        
        # Execute analysis
        crew = Crew(agents=[self.agent], tasks=[analysis_task])
        result = crew.kickoff()
        
        # Parse AI response into TechnicalSpecification
        return self._parse_ai_analysis(result, user_input)
    
    def _parse_ai_analysis(self, ai_result: str, user_input: str) -> TechnicalSpecification:
        """Parse AI analysis result into structured TechnicalSpecification."""
        lines = ai_result.split('\n')
        
        # Initialize defaults
        category = "process_automation"
        complexity = "moderate"
        estimated_agents = 3
        agent_roles = []
        workflow_steps = []
        apis_required = ["APIs TBD - requires user input"]
        
        # Parse AI response (with fallbacks for robustness)
        try:
            for line in lines:
                line = line.strip()
                if line.startswith('CATEGORY:'):
                    category = line.split(':', 1)[1].strip().lower()
                elif line.startswith('COMPLEXITY:'):
                    complexity = line.split(':', 1)[1].strip().lower()
                elif line.startswith('ESTIMATED_AGENTS:'):
                    estimated_agents = int(line.split(':', 1)[1].strip())
                elif line.startswith('AGENT_ROLES:'):
                    roles_text = line.split(':', 1)[1].strip()
                    agent_roles = self._parse_agent_roles(roles_text)
                elif line.startswith('WORKFLOW_STEPS:'):
                    steps_text = line.split(':', 1)[1].strip()
                    workflow_steps = self._parse_workflow_steps(steps_text)
                elif line.startswith('APIS_REQUIRED:'):
                    apis_text = line.split(':', 1)[1].strip()
                    apis_required = [api.strip() for api in apis_text.split(',') if api.strip()]
        
        except Exception as e:
            print(f"Warning: Could not fully parse AI analysis, using defaults: {e}")
        
        # Fallback to simplified analysis if parsing fails
        if not agent_roles:
            agent_roles = self._fallback_agent_roles(category)
        if not workflow_steps:
            workflow_steps = self._fallback_workflow_steps(category)
        
        # Create business requirement
        business_req = BusinessRequirement(
            description=user_input,
            priority="high",
            category=category,
            inputs=self._extract_inputs(user_input),
            outputs=self._extract_outputs(user_input),
            constraints=["cost_effective", "user_friendly", "scalable"],
            success_criteria=["reduces_manual_work", "improves_efficiency", "saves_time"]
        )
        
        return TechnicalSpecification(
            agent_roles_needed=agent_roles,
            workflow_steps=workflow_steps,
            apis_required=apis_required,
            data_flows=[
                {"from": "input", "to": "processing", "type": "sequential"},
                {"from": "processing", "to": "validation", "type": "sequential"},
                {"from": "validation", "to": "output", "type": "sequential"}
            ],
            complexity_estimate=complexity,
            estimated_agents=estimated_agents
        )
    
    def _parse_agent_roles(self, roles_text: str) -> List[dict]:
        """Parse agent roles from AI response text."""
        roles = []
        if 'content' in roles_text.lower():
            roles.extend([
                {"role": "content_researcher", "responsibility": "Research topics and trends"},
                {"role": "content_generator", "responsibility": "Generate content"},
                {"role": "content_optimizer", "responsibility": "Optimize for SEO and engagement"}
            ])
        else:
            roles.extend([
                {"role": "data_processor", "responsibility": "Process input data"},
                {"role": "task_executor", "responsibility": "Execute main automation task"},
                {"role": "output_formatter", "responsibility": "Format and deliver results"}
            ])
        return roles
    
    def _parse_workflow_steps(self, steps_text: str) -> List[dict]:
        """Parse workflow steps from AI response text."""
        return [
            {"step": "input_validation", "description": "Validate and prepare input data"},
            {"step": "main_processing", "description": "Execute core business logic"},
            {"step": "quality_assurance", "description": "Check results and handle errors"},
            {"step": "output_delivery", "description": "Format and deliver final results"}
        ]
    
    def _fallback_agent_roles(self, category: str) -> List[dict]:
        """Fallback agent roles if AI parsing fails."""
        if category == "content_creation":
            return [
                {"role": "content_researcher", "responsibility": "Research topics and trends"},
                {"role": "content_generator", "responsibility": "Generate content"},
                {"role": "content_optimizer", "responsibility": "Optimize for SEO and engagement"},
                {"role": "publishing_manager", "responsibility": "Publish to chosen platform"}
            ]
        else:
            return [
                {"role": "data_processor", "responsibility": "Process input data"},
                {"role": "task_executor", "responsibility": "Execute main automation task"},
                {"role": "output_formatter", "responsibility": "Format and deliver results"}
            ]
    
    def _fallback_workflow_steps(self, category: str) -> List[dict]:
        """Fallback workflow steps if AI parsing fails."""
        return [
            {"step": "input_validation", "description": "Validate and prepare input data"},
            {"step": "main_processing", "description": f"Execute {category} workflow"},
            {"step": "quality_assurance", "description": "Check results and handle errors"},
            {"step": "output_delivery", "description": "Format and deliver final results"}
        ]
    
    def _extract_inputs(self, text: str) -> List[str]:
        """Extract likely input sources from text."""
        inputs = []
        text_lower = text.lower()
        
        if 'wordpress' in text_lower or 'blog' in text_lower:
            inputs.append('wordpress_content')
        if 'social media' in text_lower:
            inputs.append('social_media_platforms')
        if 'email' in text_lower:
            inputs.append('email_data')
        if 'analytics' in text_lower:
            inputs.append('analytics_data')
        
        return inputs if inputs else ['user_input', 'business_data']
    
    def _extract_outputs(self, text: str) -> List[str]:
        """Extract likely outputs from text."""
        outputs = []
        text_lower = text.lower()
        
        if 'content' in text_lower and 'create' in text_lower:
            outputs.append('generated_content')
        if 'report' in text_lower:
            outputs.append('performance_reports')
        if 'social' in text_lower and 'post' in text_lower:
            outputs.append('social_media_posts')
        
        return outputs if outputs else ['automated_results', 'processed_data']
    
    def get_clarifying_questions(self, user_input: str) -> List[str]:
        """AI-powered generation of clarifying questions."""
        questions_task = Task(
            description=f"""
            Generate 5-8 intelligent clarifying questions to better understand these business requirements:
            
            USER INPUT: {user_input}
            
            Generate questions that will help clarify:
            1. Specific technologies/platforms they prefer (or need recommendations)
            2. Current manual processes and pain points
            3. Expected volume/scale of automation
            4. Success metrics and goals
            5. Existing tools and integrations
            6. Budget/timeline constraints
            
            Make questions specific to their use case, not generic. Return as a simple numbered list.
            """,
            agent=self.agent,
            expected_output="5-8 specific clarifying questions relevant to the user's requirements"
        )
        
        crew = Crew(agents=[self.agent], tasks=[questions_task])
        result = crew.kickoff()
        
        # Parse questions from AI response
        questions = []
        for line in result.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                question = line.split('.', 1)[-1].strip()
                if question and question.endswith('?'):
                    questions.append(question)
        
        # Fallback questions if parsing fails
        if len(questions) < 3:
            questions = [
                "What is your current manual process for this task?",
                "What platforms/tools are you currently using?",
                "How much time does this currently take per day/week?",
                "What would success look like for this automation?",
                "Do you have preferences for hosting/deployment platforms?"
            ]
        
        return questions[:8]


def create_requirements_analyst() -> RequirementsAnalyst:
    """Factory function to create a RequirementsAnalyst instance."""
    return RequirementsAnalyst()


# Test function
if __name__ == "__main__":
    # Test with sample input
    analyst = create_requirements_analyst()
    
    test_input = """
    I run a digital marketing agency. I want to automate content creation:
    research trends, generate ideas, create drafts, optimize for SEO,
    schedule social posts, and track performance.
    """
    
    # Analyze requirements
    spec = analyst.analyze_requirements(test_input)
    
    print("=== REQUIREMENTS ANALYSIS ===")
    print(f"Complexity: {spec.complexity_estimate}")
    print(f"Estimated Agents: {spec.estimated_agents}")
    print(f"Agent Roles: {len(spec.agent_roles_needed)}")
    for role in spec.agent_roles_needed:
        print(f"  - {role['role']}: {role['responsibility']}")
    
    print(f"\nWorkflow Steps: {len(spec.workflow_steps)}")
    for step in spec.workflow_steps:
        print(f"  - {step['step']}: {step['description']}")
    
    print(f"\nAPIs Required: {', '.join(spec.apis_required)}")
