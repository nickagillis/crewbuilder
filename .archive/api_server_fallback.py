#!/usr/bin/env python3
"""
CrewBuilder FastAPI Server - No API Keys Version
API server that works without OpenAI API keys using fallback logic
"""

import sys
from pathlib import Path
from typing import Dict, Any
import json
import traceback
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# CrewBuilder imports
from agents.requirements_analyst import TechnicalSpecification
from agents.system_architect import AgentSpecification, TaskSpecification, CrewWorkflow, CrewArchitecture

# Create FastAPI app
app = FastAPI(
    title="CrewBuilder API",
    description="AI Agent Meta-System - Building AI agents that build AI agent systems (Fallback Mode)",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class GenerationRequest(BaseModel):
    requirement: str

class GenerationResponse(BaseModel):
    success: bool
    data: Dict[str, Any] = None
    error: str = None

# No-API-Key Fallback Implementation
class FallbackRequirementsAnalyst:
    """Requirements analyst that works without API keys"""
    
    def analyze_requirements(self, user_input: str) -> TechnicalSpecification:
        """Analyze requirements using fallback logic only"""
        
        # Categorize based on keywords
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['content', 'blog', 'social', 'post', 'article']):
            category = "content_creation"
        elif any(word in user_lower for word in ['crm', 'sales', 'lead', 'customer']):
            category = "system_integration"
        elif any(word in user_lower for word in ['data', 'analytics', 'report', 'dashboard']):
            category = "data_analysis"
        elif any(word in user_lower for word in ['meta', 'crewbuilder', 'agent', 'ai system']):
            category = "system_development"
        else:
            category = "process_automation"
        
        # Determine complexity
        complexity_indicators = {
            'simple': ['simple', 'basic', 'one', 'single', 'automate'],
            'moderate': ['multiple', 'integrate', 'workflow', 'process', 'several'],
            'complex': ['enterprise', 'advanced', 'complex', 'machine learning', 'ai', 'scale', 'distributed', 'meta']
        }
        
        complexity_scores = {}
        for level, keywords in complexity_indicators.items():
            score = sum(1 for keyword in keywords if keyword in user_lower)
            complexity_scores[level] = score
        
        if len(user_input) > 500 or complexity_scores['complex'] > 0:
            complexity = "complex"
            estimated_agents = 5
        elif len(user_input) > 200 or complexity_scores['moderate'] > 1:
            complexity = "moderate"
            estimated_agents = 4
        else:
            complexity = "simple"
            estimated_agents = 3
        
        # Generate agent roles based on category
        agent_roles = self._get_fallback_agent_roles(category)
        workflow_steps = self._get_fallback_workflow_steps(category)
        apis_required = self._get_fallback_apis(user_input, category)
        
        return TechnicalSpecification(
            agent_roles_needed=agent_roles[:estimated_agents],
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
    
    def _get_fallback_agent_roles(self, category: str):
        """Get fallback agent roles based on category"""
        role_templates = {
            "content_creation": [
                {"role": "content_researcher", "responsibility": "Research topics and trends"},
                {"role": "content_generator", "responsibility": "Generate high-quality content"},
                {"role": "seo_optimizer", "responsibility": "Optimize content for search engines"},
                {"role": "publishing_manager", "responsibility": "Schedule and publish content"},
                {"role": "performance_tracker", "responsibility": "Track content performance"}
            ],
            "system_integration": [
                {"role": "integration_analyst", "responsibility": "Analyze system requirements"},
                {"role": "data_connector", "responsibility": "Connect and sync data sources"},
                {"role": "workflow_orchestrator", "responsibility": "Orchestrate business workflows"},
                {"role": "validation_specialist", "responsibility": "Validate data integrity"},
                {"role": "monitoring_agent", "responsibility": "Monitor system health"}
            ],
            "data_analysis": [
                {"role": "data_collector", "responsibility": "Collect and aggregate data"},
                {"role": "data_processor", "responsibility": "Process and clean data"},
                {"role": "analytics_engine", "responsibility": "Perform data analysis"},
                {"role": "report_generator", "responsibility": "Generate insights and reports"},
                {"role": "visualization_specialist", "responsibility": "Create data visualizations"}
            ],
            "system_development": [
                {"role": "requirements_analyst", "responsibility": "Analyze business requirements"},
                {"role": "system_architect", "responsibility": "Design system architecture"},
                {"role": "code_generator", "responsibility": "Generate production-ready code"},
                {"role": "quality_assurance", "responsibility": "Validate system quality"},
                {"role": "deployment_engineer", "responsibility": "Deploy and monitor system"}
            ]
        }
        
        return role_templates.get(category, [
            {"role": "data_processor", "responsibility": "Process input data"},
            {"role": "task_executor", "responsibility": "Execute automation tasks"},
            {"role": "output_formatter", "responsibility": "Format and deliver results"}
        ])
    
    def _get_fallback_workflow_steps(self, category: str):
        """Get fallback workflow steps based on category"""
        return [
            {"step": "input_validation", "description": "Validate and prepare input data"},
            {"step": "main_processing", "description": f"Execute {category.replace('_', ' ')} workflow"},
            {"step": "quality_assurance", "description": "Check results and handle errors"},
            {"step": "output_delivery", "description": "Format and deliver final results"}
        ]
    
    def _get_fallback_apis(self, user_input: str, category: str):
        """Suggest APIs based on input content"""
        apis = []
        user_lower = user_input.lower()
        
        # Common API suggestions based on keywords
        if 'email' in user_lower:
            apis.extend(['Gmail API', 'SendGrid API'])
        if 'social' in user_lower:
            apis.extend(['Twitter API', 'LinkedIn API', 'Facebook API'])
        if 'wordpress' in user_lower or 'blog' in user_lower:
            apis.extend(['WordPress API'])
        if 'analytics' in user_lower:
            apis.extend(['Google Analytics API'])
        if 'crm' in user_lower:
            apis.extend(['Salesforce API', 'HubSpot API'])
        if 'slack' in user_lower:
            apis.extend(['Slack API'])
        
        # Category-based defaults
        if not apis:
            category_apis = {
                "content_creation": ["OpenAI API", "WordPress API", "Social Media APIs"],
                "system_integration": ["REST APIs", "Database connectors", "Webhook APIs"],
                "data_analysis": ["Data APIs", "Analytics APIs", "Visualization APIs"],
                "system_development": ["OpenAI API", "GitHub API", "Cloud Platform APIs"]
            }
            apis = category_apis.get(category, ["REST APIs", "Webhook APIs"])
        
        return apis

class FallbackSystemArchitect:
    """System architect that works without API keys"""
    
    def design_crew_architecture(self, tech_spec: TechnicalSpecification) -> CrewArchitecture:
        """Design crew architecture using fallback logic"""
        
        # Generate agents
        agents = []
        for i, role_info in enumerate(tech_spec.agent_roles_needed):
            role = role_info['role']
            responsibility = role_info['responsibility']
            
            agent = AgentSpecification(
                name=f"{role}_agent",
                role=role.replace('_', ' ').title(),
                goal=f"Efficiently {responsibility.lower()} with high quality and reliability",
                backstory=f"You are a specialized AI agent expert in {role.replace('_', ' ')}. "
                         f"You have extensive experience in {responsibility.lower()} and work collaboratively "
                         f"with other agents to achieve optimal business outcomes.",
                tools=self._get_tools_for_role(role),
                max_iter=5,
                memory=True,
                verbose=True,
                allow_delegation=False
            )
            agents.append(agent)
        
        # Generate tasks
        tasks = []
        for i, step_info in enumerate(tech_spec.workflow_steps):
            step = step_info['step']
            description = step_info['description']
            agent_name = agents[i % len(agents)].name
            
            task = TaskSpecification(
                name=f"{step}_task",
                description=f"Execute {description}. Ensure high quality output and proper validation.",
                agent_name=agent_name,
                expected_output=f"Completed {step} with validated results and clear status report",
                depends_on=[tasks[i-1].name] if i > 0 else [],
                output_format="structured_data"
            )
            tasks.append(task)
        
        # Generate workflow
        workflow = CrewWorkflow(
            name=f"{tech_spec.complexity_estimate}_automation_workflow",
            description=f"Coordinated workflow for {tech_spec.complexity_estimate} business automation",
            task_sequence=[task.name for task in tasks],
            parallel_tasks=[],
            decision_points=[]
        )
        
        # Resource estimation
        resource_map = {
            "simple": {"runtime": "5-15 minutes", "memory": "1GB", "cpu": "1 core"},
            "moderate": {"runtime": "15-30 minutes", "memory": "2GB", "cpu": "2 cores"},
            "complex": {"runtime": "30-60 minutes", "memory": "4GB", "cpu": "4 cores"}
        }
        
        resources = resource_map[tech_spec.complexity_estimate]
        
        return CrewArchitecture(
            crew_name=f"{tech_spec.complexity_estimate}_automation_crew",
            crew_description=f"AI-powered {tech_spec.complexity_estimate} automation crew with {len(agents)} specialized agents",
            agents=agents,
            tasks=tasks,
            workflow=workflow,
            estimated_runtime=resources["runtime"],
            resource_requirements={"memory": resources["memory"], "cpu": resources["cpu"]},
            success_metrics=["task_completion_rate", "output_quality", "execution_time", "user_satisfaction"],
            dependencies=["crewai"] + tech_spec.apis_required
        )
    
    def _get_tools_for_role(self, role: str):
        """Get appropriate tools for each role"""
        tool_mapping = {
            'content_researcher': ['web_search', 'trend_analyzer', 'competitor_monitor'],
            'content_generator': ['text_generator', 'template_engine', 'content_formatter'],
            'seo_optimizer': ['keyword_analyzer', 'seo_checker', 'readability_analyzer'],
            'publishing_manager': ['social_scheduler', 'cms_publisher', 'analytics_tracker'],
            'requirements_analyst': ['requirement_parser', 'business_analyzer', 'specification_generator'],
            'system_architect': ['architecture_designer', 'workflow_optimizer', 'resource_estimator'],
            'code_generator': ['code_templates', 'syntax_validator', 'documentation_generator'],
            'quality_assurance': ['test_generator', 'code_validator', 'performance_monitor'],
            'deployment_engineer': ['deployment_automator', 'environment_manager', 'monitoring_setup']
        }
        return tool_mapping.get(role, ['basic_tools', 'file_handler', 'api_client'])

# Global instances
requirements_analyst = FallbackRequirementsAnalyst()
system_architect = FallbackSystemArchitect()

def run_fallback_pipeline(requirement: str) -> Dict[str, Any]:
    """Run a simplified pipeline using fallback logic only"""
    
    try:
        print(f"Running fallback pipeline for: {requirement[:100]}...")
        
        # Stage 1: Requirements Analysis
        print("Stage 1: Analyzing business requirements...")
        tech_spec = requirements_analyst.analyze_requirements(requirement)
        
        # Stage 2: System Architecture
        print("Stage 2: Designing crew architecture...")
        crew_architecture = system_architect.design_crew_architecture(tech_spec)
        
        # Build response
        result = {
            'systemName': extract_system_name(requirement),
            'agents': len(crew_architecture.agents),
            'complexity': tech_spec.complexity_estimate,
            'estimatedTime': crew_architecture.estimated_runtime,
            'estimatedCost': estimate_cost(tech_spec.complexity_estimate, len(crew_architecture.agents)),
            'architecture': {
                'crew_name': crew_architecture.crew_name,
                'crew_description': crew_architecture.crew_description,
                'agents': [
                    {
                        'name': agent.name,
                        'role': agent.role,
                        'goal': agent.goal[:60] + '...' if len(agent.goal) > 60 else agent.goal
                    }
                    for agent in crew_architecture.agents
                ],
                'tasks': [
                    {
                        'name': task.name,
                        'description': task.description[:50] + '...' if len(task.description) > 50 else task.description,
                        'agent_name': task.agent_name
                    }
                    for task in crew_architecture.tasks
                ],
                'estimated_runtime': crew_architecture.estimated_runtime,
                'workflow_name': crew_architecture.workflow.name
            },
            'deployment': {
                'platform': "Railway",
                'estimatedSetupTime': "15-30 minutes",
                'monthlyRunningCost': estimate_cost(tech_spec.complexity_estimate, len(crew_architecture.agents))
            },
            'generatedAt': datetime.now().isoformat(),
            'complexity_score': get_complexity_score(tech_spec.complexity_estimate),
            'pipeline_stages': [
                {
                    'stage': 'Requirements Analysis',
                    'status': 'completed',
                    'output': {
                        'complexity': tech_spec.complexity_estimate,
                        'estimated_agents': tech_spec.estimated_agents,
                        'agent_roles': tech_spec.agent_roles_needed[:3],
                        'apis_required': tech_spec.apis_required[:3]
                    }
                },
                {
                    'stage': 'System Architecture', 
                    'status': 'completed',
                    'output': {
                        'crew_name': crew_architecture.crew_name,
                        'agents_designed': len(crew_architecture.agents),
                        'tasks_defined': len(crew_architecture.tasks),
                        'workflow': crew_architecture.workflow.name
                    }
                },
                {
                    'stage': 'Fallback Mode',
                    'status': 'completed',
                    'output': {
                        'note': 'Running in fallback mode without OpenAI API keys',
                        'recommendation': 'Add OpenAI API key for enhanced AI-powered analysis'
                    }
                }
            ]
        }
        
        print(" Fallback pipeline completed successfully!")
        return result
        
    except Exception as e:
        print(f" Fallback pipeline error: {e}")
        traceback.print_exc()
        raise

def extract_system_name(requirement: str) -> str:
    """Extract a reasonable system name from the requirement"""
    keywords = ['automate', 'automation', 'system', 'platform', 'solution', 'tool', 'assistant', 'bot']
    domains = ['content', 'marketing', 'sales', 'customer', 'email', 'social', 'data', 'inventory', 'finance', 'hr']
    
    requirement_lower = requirement.lower()
    
    found_domain = None
    found_keyword = None
    
    for domain in domains:
        if domain in requirement_lower:
            found_domain = domain
            break
    
    for keyword in keywords:
        if keyword in requirement_lower:
            found_keyword = keyword
            break
    
    if found_domain and found_keyword:
        return f"{found_domain.title()} {found_keyword.title()}"
    elif found_domain:
        return f"{found_domain.title()} System"
    elif found_keyword:
        return f"Business {found_keyword.title()}"
    else:
        return "Business Automation System"

def estimate_cost(complexity: str, agent_count: int) -> str:
    """Estimate monthly cost"""
    base_costs = {'simple': 25, 'moderate': 50, 'complex': 100}
    base_cost = base_costs.get(complexity, 50)
    agent_cost = agent_count * 10
    total_cost = base_cost + agent_cost
    return f"${total_cost}-{total_cost + 50}"

def get_complexity_score(complexity: str) -> int:
    """Convert complexity to numeric score"""
    mapping = {'simple': 1, 'moderate': 2, 'complex': 3}
    return mapping.get(complexity, 2)

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "CrewBuilder API - Fallback Mode (No API Keys Required)",
        "version": "1.0.0",
        "status": "operational",
        "mode": "fallback"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "mode": "fallback",
        "api_keys_required": False,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_system(request: GenerationRequest):
    """Generate a system using fallback logic (no API keys required)"""
    
    try:
        if not request.requirement or not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Valid requirement string is required")
        
        print(f"Generation request received: {request.requirement[:100]}...")
        
        # Run the fallback pipeline
        result = run_fallback_pipeline(request.requirement)
        
        print(f" Generation completed successfully!")
        
        return GenerationResponse(
            success=True,
            data=result
        )
        
    except Exception as e:
        print(f" Generation error: {e}")
        traceback.print_exc()
        
        return GenerationResponse(
            success=False,
            error=f"Generation failed: {str(e)}"
        )

@app.post("/api/feedback")
async def collect_feedback(feedback_data: Dict[str, Any]):
    """Collect user feedback"""
    try:
        print(f"Feedback received: {feedback_data}")
        return {"success": True, "message": "Feedback collected successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    
    print(" Starting CrewBuilder FastAPI Server (Fallback Mode)...")
    print(" This version works WITHOUT OpenAI API keys!")
    print(" For enhanced AI features, add OPENAI_API_KEY environment variable")
    print()
    print(" Frontend: http://localhost:3000")
    print(" API: http://localhost:8000")
    print(" Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "api_server_fallback:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
