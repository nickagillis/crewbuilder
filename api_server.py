#!/usr/bin/env python3
"""
CrewBuilder FastAPI Server
Connects the beautiful Next.js frontend to the complete 10-agent backend
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List
import json
import traceback
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Ensure OpenAI key is available for CrewAI/LangChain
if os.getenv('OPENAI_API_KEY'):
    # Set it for langchain to find
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import all CrewBuilder agents
try:
    from agents import (
        create_clarification_agent,
        create_requirements_analyst,
        create_system_architect, 
        create_code_generator,
        create_quality_assurance,
        create_api_detective,
        create_documentation_specialist,
        create_infrastructure_analyst,
        create_deployment_engineer,
        create_hosting_assistant,
        create_monitoring_engineer,
        analyze_initial_requirement,
        create_clarification_session
    )
    CLARIFICATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Clarification agent not available: {e}")
    # Import core agents only
    from agents import (
        create_requirements_analyst,
        create_system_architect, 
        create_code_generator,
        create_quality_assurance,
        create_api_detective,
        create_documentation_specialist,
        create_infrastructure_analyst,
        create_deployment_engineer,
        create_hosting_assistant,
        create_monitoring_engineer
    )
    CLARIFICATION_AVAILABLE = False

# Create FastAPI app
app = FastAPI(
    title="CrewBuilder API",
    description="AI Agent Meta-System - Building AI agents that build AI agent systems",
    version="1.0.0"
)

# Configure CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://web-production-bd955.up.railway.app",
        "https://crewbuilder.vercel.app",  # Live frontend!
        "https://crewbuilder.app",  # Future custom domain
        "https://crewbuilder-*.vercel.app"  # Preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class GenerationRequest(BaseModel):
    requirement: str
    skip_clarification: bool = False  # For cases where clarification was already done

class GenerationResponse(BaseModel):
    success: bool
    data: Dict[str, Any] = None
    error: str = None

class DeploymentRequest(BaseModel):
    requirement: str
    api_keys: Dict[str, str]  # User's API keys (OpenAI, etc)
    deploy_to_railway: bool = True

class DeploymentResponse(BaseModel):
    success: bool
    deployment_url: str = None
    dashboard_url: str = None
    project_id: str = None
    error: str = None

class ClarificationRequest(BaseModel):
    requirement: str

class ClarificationResponse(BaseModel):
    success: bool
    questions: List[Dict[str, Any]] = None
    session_id: str = None
    error: str = None

class ClarificationAnswerRequest(BaseModel):
    session_id: str
    responses: Dict[str, str]

class ClarificationAnswerResponse(BaseModel):
    success: bool
    refined_requirement: str = None
    confidence_score: float = None
    error: str = None

# Global agent instances (initialized once for performance)
agents = {}

def initialize_agents():
    """Initialize all CrewBuilder agents"""
    global agents
    
    try:
        print(" Initializing CrewBuilder agents...")
        
        # Check if we have OpenAI API key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            print(" ERROR: OPENAI_API_KEY not found!")
            print(" Available environment variables:")
            for key in sorted(os.environ.keys()):
                if 'KEY' in key.upper() or 'TOKEN' in key.upper():
                    print(f"   {key}: ***hidden***")
                else:
                    print(f"   {key}: {os.environ[key][:30]}..." if len(os.environ[key]) > 30 else f"   {key}: {os.environ[key]}")
            print(" Agents will use fallback mode and won't generate real content")
            return False
        else:
            print(f" ✓ OPENAI_API_KEY found: {openai_key[:10]}...")  # Show first 10 chars
        
        if CLARIFICATION_AVAILABLE:
            try:
                agents['clarification_agent'] = create_clarification_agent()
                print(" Clarification Agent ready")
            except Exception as e:
                print(f" Warning: Could not initialize Clarification Agent: {e}")
        
        agents['requirements_analyst'] = create_requirements_analyst()
        print(" Requirements Analyst ready")
        
        agents['system_architect'] = create_system_architect()
        print(" System Architect ready")
        
        agents['code_generator'] = create_code_generator()
        print(" Code Generator ready")
        
        agents['quality_assurance'] = create_quality_assurance()
        print(" Quality Assurance ready")
        
        agents['api_detective'] = create_api_detective()
        print(" API Detective ready")
        
        agents['documentation_specialist'] = create_documentation_specialist()
        print(" Documentation Specialist ready")
        
        agents['infrastructure_analyst'] = create_infrastructure_analyst()
        print(" Infrastructure Analyst ready")
        
        agents['deployment_engineer'] = create_deployment_engineer()
        print(" Deployment Engineer ready")
        
        agents['hosting_assistant'] = create_hosting_assistant()
        print(" Hosting Assistant ready")
        
        agents['monitoring_engineer'] = create_monitoring_engineer()
        print(" Monitoring Engineer ready")
        
        agent_count = len(agents)
        print(f" {agent_count} CrewBuilder agents initialized and ready!")
        return True
        
    except Exception as e:
        print(f" Error initializing agents: {e}")
        traceback.print_exc()
        return False

def run_complete_pipeline(requirement: str, skip_clarification: bool = False) -> Dict[str, Any]:
    """
    Run the complete 11-agent CrewBuilder pipeline
    
    Pipeline: Clarification → Requirements → Architecture → Code → QA → APIs → Docs → Infrastructure → Deployment → Hosting → Monitoring
    """
    
    pipeline_results = {
        'systemName': 'Generated System',
        'agents': 0,
        'complexity': 'moderate',
        'estimatedTime': '15-30 minutes',
        'estimatedCost': '$50-100',
        'architecture': {},
        'deployment': {},
        'generatedAt': datetime.now().isoformat(),
        'complexity_score': 2,
        'pipeline_stages': []
    }
    
    try:
        # Stage 1: Requirements Analysis
        print(" Stage 1: Analyzing business requirements...")
        tech_spec = agents['requirements_analyst'].analyze_requirements(requirement)
        
        pipeline_results['complexity'] = tech_spec.complexity_estimate
        pipeline_results['agents'] = tech_spec.estimated_agents
        pipeline_results['systemName'] = extract_system_name(requirement)
        pipeline_results['complexity_score'] = get_complexity_score(tech_spec.complexity_estimate)
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Requirements Analysis',
            'status': 'completed',
            'output': {
                'complexity': tech_spec.complexity_estimate,
                'estimated_agents': tech_spec.estimated_agents,
                'agent_roles': tech_spec.agent_roles_needed[:3],  # First 3 for display
                'apis_required': tech_spec.apis_required[:3]
            }
        })
        
        # Stage 2: System Architecture
        print(" Stage 2: Designing crew architecture...")
        crew_architecture = agents['system_architect'].design_crew_architecture(tech_spec)
        
        pipeline_results['architecture'] = {
            'crew_name': crew_architecture.crew_name,
            'crew_description': crew_architecture.crew_description,
            'agents': [
                {
                    'name': agent.name,
                    'role': agent.role,
                    'goal': agent.goal[:60] + '...' if len(agent.goal) > 60 else agent.goal
                }
                for agent in crew_architecture.agents[:4]  # First 4 for display
            ],
            'tasks': [
                {
                    'name': task.name,
                    'description': task.description[:50] + '...' if len(task.description) > 50 else task.description,
                    'agent_name': task.agent_name
                }
                for task in crew_architecture.tasks[:4]  # First 4 for display
            ],
            'estimated_runtime': crew_architecture.estimated_runtime,
            'workflow_name': crew_architecture.workflow.name
        }
        
        pipeline_results['estimatedTime'] = crew_architecture.estimated_runtime
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'System Architecture',
            'status': 'completed',
            'output': {
                'crew_name': crew_architecture.crew_name,
                'agents_designed': len(crew_architecture.agents),
                'tasks_defined': len(crew_architecture.tasks),
                'workflow': crew_architecture.workflow.name
            }
        })
        
        # Stage 3: Code Generation
        print(" Stage 3: Generating production code...")
        generated_code = agents['code_generator'].generate_crew_code(crew_architecture)
        
        # Store generated code in results
        pipeline_results['generated_code'] = generated_code.main_code
        pipeline_results['requirements_txt'] = generated_code.requirements_txt
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Code Generation',
            'status': 'completed',
            'output': {
                'main_code_length': len(generated_code.main_code),
                'requirements_count': len(generated_code.requirements_txt.splitlines()),
                'estimated_cost': str(generated_code.estimated_cost),
                'performance_notes': str(generated_code.performance_notes)[:100] + '...' if len(str(generated_code.performance_notes)) > 100 else str(generated_code.performance_notes)
            }
        })
        
        # Stage 4: Quality Assurance
        print(" Stage 4: Quality validation...")
        qa_report = agents['quality_assurance'].validate_generated_system(generated_code, crew_architecture)
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Quality Assurance',
            'status': 'completed',
            'output': {
                'approval_status': qa_report.approval_status,
                'quality_score': qa_report.quality_score,
                'issues_found': len(qa_report.issues_found),
                'test_results': len(qa_report.test_results)
            }
        })
        
        # Stage 5: API Integration Planning
        print(" Stage 5: API integration analysis...")
        api_plan = agents['api_detective'].analyze_api_requirements(tech_spec, crew_architecture)
        
        pipeline_results['estimatedCost'] = str(api_plan.estimated_monthly_cost)
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'API Integration',
            'status': 'completed',
            'output': {
                'apis_recommended': len(api_plan.recommended_apis),
                'estimated_cost': api_plan.estimated_monthly_cost,
                'free_tier_available': any(api.free_tier_available for api in api_plan.recommended_apis),
                'setup_complexity': api_plan.overall_complexity
            }
        })
        
        # Stage 6: Documentation Generation
        print(" Stage 6: Documentation creation...")
        doc_plan = agents['documentation_specialist'].generate_documentation(
            generated_code, api_plan, qa_report
        )
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Documentation',
            'status': 'completed',
            'output': {
                'user_guide_sections': len(doc_plan.user_guide.sections),
                'technical_docs_length': len(doc_plan.technical_documentation.content),
                'deployment_steps': len(doc_plan.deployment_guide.steps),
                'estimated_reading_time': doc_plan.estimated_reading_time
            }
        })
        
        # Stage 7: Infrastructure Analysis
        print(" Stage 7: Infrastructure recommendations...")
        infra_recommendations = agents['infrastructure_analyst'].analyze_infrastructure_needs(
            crew_architecture, api_plan, doc_plan
        )
        
        pipeline_results['deployment'] = {
            'platform': infra_recommendations.recommended_platform.name,
            'estimatedSetupTime': infra_recommendations.estimated_setup_time,
            'monthlyRunningCost': infra_recommendations.cost_analysis.monthly_estimate,
            'security_score': infra_recommendations.security_assessment.overall_score,
            'scalability_rating': infra_recommendations.scalability_analysis.scalability_score
        }
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Infrastructure Analysis',
            'status': 'completed',
            'output': {
                'recommended_platform': infra_recommendations.recommended_platform.name,
                'setup_time': infra_recommendations.estimated_setup_time,
                'monthly_cost': str(infra_recommendations.cost_analysis.monthly_estimate),
                'security_score': infra_recommendations.security_assessment.overall_score
            }
        })
        
        # Stage 8: Deployment Engineering
        print(" Stage 8: Deployment automation...")
        deployment_plan = agents['deployment_engineer'].create_deployment_plan(
            crew_architecture, infra_recommendations, api_plan
        )
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Deployment Engineering',
            'status': 'completed',
            'output': {
                'deployment_type': deployment_plan.deployment_configuration.deployment_type,
                'cicd_pipeline': deployment_plan.cicd_pipeline.pipeline_type,
                'secrets_managed': len(deployment_plan.secrets_management.required_secrets),
                'estimated_deployment_time': deployment_plan.estimated_deployment_time
            }
        })
        
        # Stage 9: Hosting Assistance
        print(" Stage 9: Hosting guidance...")
        hosting_plan = agents['hosting_assistant'].create_hosting_assistance_plan(
            infra_recommendations, deployment_plan, crew_architecture
        )
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Hosting Assistance',
            'status': 'completed',
            'output': {
                'setup_guide_steps': len(hosting_plan.platform_setup_guide.steps),
                'configuration_items': len(hosting_plan.configuration_assistance.configuration_steps),
                'optimization_recommendations': len(hosting_plan.resource_optimization.recommendations),
                'support_level': hosting_plan.ongoing_support.support_level
            }
        })
        
        # Stage 10: Monitoring Engineering
        print(" Stage 10: Monitoring setup...")
        monitoring_plan = agents['monitoring_engineer'].generate_monitoring_plan(
            hosting_plan, deployment_plan, crew_architecture
        )
        
        pipeline_results['pipeline_stages'].append({
            'stage': 'Monitoring Engineering',
            'status': 'completed',
            'output': {
                'monitoring_stack': monitoring_plan.monitoring_stack.primary_platform,
                'alert_channels': len(monitoring_plan.alerting_system.notification_channels),
                'dashboard_count': len(monitoring_plan.dashboard_configuration.dashboards),
                'estimated_cost': monitoring_plan.estimated_cost,
                'implementation_timeline': monitoring_plan.implementation_timeline
            }
        })
        
        print(" Complete 10-agent pipeline finished successfully!")
        
        return pipeline_results
        
    except Exception as e:
        print(f" Pipeline error at stage {len(pipeline_results.get('pipeline_stages', []))}: {e}")
        print(f" Error type: {type(e).__name__}")
        print(f" Error details: {str(e)}")
        traceback.print_exc()
        
        # Return partial results with error info
        pipeline_results['pipeline_stages'].append({
            'stage': 'Error',
            'status': 'failed',
            'output': {
                'error': str(e),
                'error_type': type(e).__name__,
                'completed_stages': len([s for s in pipeline_results['pipeline_stages'] if s['status'] == 'completed'])
            }
        })
        
        return pipeline_results

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

def get_complexity_score(complexity: str) -> int:
    """Convert complexity to numeric score"""
    mapping = {'simple': 1, 'moderate': 2, 'complex': 3}
    return mapping.get(complexity, 2)

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "CrewBuilder API - Building AI agents that build AI agent systems",
        "version": "1.0.0",
        "status": "operational",
        "agents_ready": len(agents) >= 10  # At least 10 core agents
    }

@app.get("/")
def root():
    """Root endpoint - welcome message"""
    return {
        "message": "🚀 CrewBuilder API is Running!",
        "status": "active",
        "version": "1.0.0",
        "description": "AI-powered system that generates and deploys AI agent teams",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "clarify": "/api/clarify",
            "clarify_answer": "/api/clarify/answer",
            "generate": "/api/generate",
            "deploy": "/api/deploy",
            "feedback": "/api/feedback"
        },
        "frontend": "Deploy frontend separately or visit /docs for API testing",
        "agents": len(agents) if agents else "Initializing..."
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "agents_initialized": len(agents),
        "agents_ready": [name for name in agents.keys()],
        "timestamp": datetime.now().isoformat()
    }

# Global storage for clarification sessions (in production, use a database)
clarification_sessions = {}

@app.post("/api/clarify", response_model=ClarificationResponse)
async def clarify_requirement(request: ClarificationRequest):
    """
    Start a clarification session for a requirement
    
    This endpoint analyzes the initial requirement and returns questions
    to help clarify and refine what the user needs.
    """
    
    try:
        if not request.requirement or not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Valid requirement string is required")
        
        print(f"💬 Clarification request received: {request.requirement[:100]}...")
        
        # Check if clarification is available
        if not CLARIFICATION_AVAILABLE:
            raise HTTPException(status_code=501, detail="Clarification agent not available in this deployment")
            
        # Check if agents are initialized
        if 'clarification_agent' not in agents:
            print(" Agents not initialized, initializing now...")
            if not initialize_agents():
                raise HTTPException(status_code=500, detail="Failed to initialize agents")
        
        # Generate clarification questions
        questions = analyze_initial_requirement(
            agents['clarification_agent'], 
            request.requirement
        )
        
        # Create session
        session_id = f"clarify_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(request.requirement) % 10000}"
        
        # Store session data
        clarification_sessions[session_id] = {
            "requirement": request.requirement,
            "questions": questions,
            "created_at": datetime.now().isoformat()
        }
        
        # Convert questions to dict format for API response
        questions_dict = [
            {
                "question": q.question,
                "context": q.context,
                "options": q.options,
                "type": q.question_type
            }
            for q in questions
        ]
        
        print(f"✅ Generated {len(questions)} clarification questions")
        
        return ClarificationResponse(
            success=True,
            questions=questions_dict,
            session_id=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Clarification error: {e}")
        traceback.print_exc()
        
        return ClarificationResponse(
            success=False,
            error=f"Clarification failed: {str(e)}"
        )

@app.post("/api/clarify/answer", response_model=ClarificationAnswerResponse)
async def answer_clarification(request: ClarificationAnswerRequest):
    """
    Submit answers to clarification questions and get refined requirements
    """
    
    try:
        # Validate session
        if request.session_id not in clarification_sessions:
            raise HTTPException(status_code=404, detail="Invalid or expired session ID")
        
        session_data = clarification_sessions[request.session_id]
        
        print(f"📝 Processing clarification answers for session: {request.session_id}")
        
        # Create full clarification session
        session = create_clarification_session(
            agents['clarification_agent'],
            session_data['requirement'],
            request.responses
        )
        
        # Store the refined requirements
        session_data['refined_requirements'] = session.refined_requirements
        session_data['confidence_score'] = session.confidence_score
        
        print(f"✅ Requirements refined with confidence: {session.confidence_score:.2f}")
        
        return ClarificationAnswerResponse(
            success=True,
            refined_requirement=session.refined_requirements.refined_requirement,
            confidence_score=session.confidence_score
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Answer processing error: {e}")
        traceback.print_exc()
        
        return ClarificationAnswerResponse(
            success=False,
            error=f"Failed to process answers: {str(e)}"
        )

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_system(request: GenerationRequest):
    """
    Generate a complete AI agent system from business requirements
    
    This endpoint runs the complete 10-agent CrewBuilder pipeline:
    Requirements → Architecture → Code → QA → APIs → Docs → Infrastructure → Deployment → Hosting → Monitoring
    """
    
    try:
        if not request.requirement or not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Valid requirement string is required")
        
        print(f" Generation request received: {request.requirement[:100]}...")
        
        # Check if agents are initialized
        if len(agents) < 10:
            print(" Agents not initialized, initializing now...")
            if not initialize_agents():
                raise HTTPException(
                    status_code=503, 
                    detail="CrewBuilder agents require OPENAI_API_KEY to function. Please ensure the API key is set in Railway environment variables."
                )
        
        # Check if this requirement was clarified
        refined_requirement = request.requirement
        for session_id, session_data in clarification_sessions.items():
            if 'refined_requirements' in session_data:
                if session_data['requirement'] == request.requirement:
                    refined_requirement = session_data['refined_requirements'].refined_requirement
                    print(f"🎯 Using refined requirement from session: {session_id}")
                    break
        
        # Run the complete pipeline
        result = run_complete_pipeline(refined_requirement, skip_clarification=request.skip_clarification)
        
        print(f" Generation completed successfully!")
        
        # Ensure the result is JSON serializable
        try:
            # Test serialization
            import json
            json.dumps(result)
        except TypeError as e:
            print(f" Warning: Result contains non-serializable data: {e}")
            # Remove non-serializable fields
            if 'generated_code' in result and hasattr(result['generated_code'], '__dict__'):
                result['generated_code'] = str(result['generated_code'])
            if 'requirements_txt' in result and hasattr(result['requirements_txt'], '__dict__'):
                result['requirements_txt'] = str(result['requirements_txt'])
        
        return GenerationResponse(
            success=True,
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f" Generation error: {e}")
        traceback.print_exc()
        
        return GenerationResponse(
            success=False,
            error=f"Generation failed: {str(e)}"
        )

@app.post("/api/feedback")
async def collect_feedback(feedback_data: Dict[str, Any]):
    """Collect user feedback for learning improvements"""
    try:
        print(f"📝 Feedback received: {feedback_data}")
        
        # Store feedback for future learning (placeholder)
        # In production, this would go to a database
        
        return {
            "success": True,
            "message": "Feedback collected successfully"
        }
        
    except Exception as e:
        print(f" Feedback error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/deploy", response_model=DeploymentResponse)
async def deploy_system(request: DeploymentRequest):
    """
    Generate AND deploy a complete AI agent system to Railway
    
    This endpoint:
    1. Runs the complete 10-agent pipeline to generate the system
    2. Deploys the generated code directly to Railway
    3. Returns live URLs for the deployed system
    """
    
    try:
        if not request.requirement or not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Valid requirement string is required")
        
        if not request.api_keys or 'OPENAI_API_KEY' not in request.api_keys:
            raise HTTPException(status_code=400, detail="OpenAI API key is required for deployment")
        
        print(f"🚀 Deployment request received: {request.requirement[:100]}...")
        
        # Step 1: Generate the system using existing pipeline
        print("📦 Step 1/3: Generating system code...")
        generation_result = await generate_system(GenerationRequest(requirement=request.requirement))
        
        if not generation_result.success:
            raise HTTPException(status_code=500, detail=f"System generation failed: {generation_result.error}")
        
        # Step 2: Deploy to Railway if requested
        if request.deploy_to_railway:
            try:
                print("🚂 Step 2/3: Initiating Railway deployment...")
                from deployment.railway_deployer import RailwayDeploymentManager
                
                deployment_manager = RailwayDeploymentManager()
                
                # Create a unique user ID (in production, this would come from auth)
                user_id = f"user_{hash(request.requirement)}"[:10]
                
                # Deploy the generated system
                print(f"🔧 Creating deployment for user: {user_id}")
                print("📤 Step 3/3: Deploying to Railway infrastructure...")
                deployment = deployment_manager.create_deployment(
                    user_id=user_id,
                    generated_system={
                        'code': generation_result.data.get('generated_code', ''),
                        'requirements': generation_result.data.get('requirements_txt', ''),
                        'original_requirements': request.requirement
                    },
                    api_keys=request.api_keys
                )
                
                if deployment['success']:
                    print(f"✅ Deployment successful: {deployment['deployment_url']}")
                    
                    return DeploymentResponse(
                        success=True,
                        deployment_url=deployment['deployment_url'],
                        dashboard_url=deployment['dashboard_url'],
                        project_id=deployment['project_id']
                    )
                else:
                    error_msg = deployment.get('error', 'Unknown error')
                    error_type = deployment.get('error_type', 'UnknownError')
                    print(f"❌ Deployment failed at step 3: {error_type} - {error_msg}")
                    raise Exception(f"Deployment failed: {error_msg}")
                    
            except ImportError:
                print("❌ ImportError: Railway deployment module not available")
                raise HTTPException(status_code=501, detail="Railway deployment not configured. Please set RAILWAY_TOKEN.")
            except Exception as e:
                print(f"❌ Deployment error: {type(e).__name__} - {str(e)}")
                raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")
        
        # If not deploying, just return the generated code info
        return DeploymentResponse(
            success=True,
            deployment_url="Not deployed - code generated only",
            dashboard_url="N/A",
            project_id="N/A"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        traceback.print_exc()
        
        return DeploymentResponse(
            success=False,
            error=f"Deployment failed: {str(e)}"
        )

# Initialize agents on startup
@app.on_event("startup")
async def startup_event():
    """Initialize all agents when the server starts"""
    print("\n=== CrewBuilder API Server Starting ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    
    # Check environment variables
    print("\nEnvironment Check:")
    print(f"  OPENAI_API_KEY: {'✓ Present' if os.getenv('OPENAI_API_KEY') else '✗ Missing'}")
    print(f"  ANTHROPIC_API_KEY: {'✓ Present' if os.getenv('ANTHROPIC_API_KEY') else '✗ Missing (optional)'}")
    print(f"  RAILWAY_TOKEN: {'✓ Present' if os.getenv('RAILWAY_TOKEN') else '✗ Missing'}")
    print(f"  PORT: {os.getenv('PORT', 'Not set (will use 8000)')}")
    
    # Test critical imports
    print("\nTesting imports:")
    critical_modules = {
        'crewai': True,  # Required
        'openai': True,  # Required
        'pydantic': True,  # Required
        'fastapi': True,  # Required
        'langchain': False,  # Optional
        'anthropic': False  # Optional
    }
    
    import_errors = []
    for module_name, required in critical_modules.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"  {module_name}: ✓ {version}")
        except ImportError as e:
            if required:
                import_errors.append(f"{module_name}: {e}")
                print(f"  {module_name}: ✗ ERROR - {e}")
            else:
                print(f"  {module_name}: ✗ Not installed (optional)")
    
    if import_errors:
        print(f"\n✗ CRITICAL: Required modules missing! This will cause crashes.")
        print("  Install with: pip install -r requirements.txt")
        for error in import_errors:
            print(f"  - {error}")
    
    # Initialize agents with detailed error handling
    print("\nInitializing agents:")
    try:
        success = initialize_agents()
        if success:
            print(f"\n✓ CrewBuilder API ready! Initialized {len(agents)} agents.")
        else:
            print("\n✗ Warning: Some agents failed to initialize")
    except Exception as e:
        print(f"\n✗ ERROR during agent initialization: {e}")
        import traceback
        traceback.print_exc()
        print("\nThis error is likely causing the Railway crash!")
    
    print("=== Startup Complete ===\n")

if __name__ == "__main__":
    import uvicorn
    
    print(" Starting CrewBuilder FastAPI Server...")
    print("Frontend: http://localhost:3000")
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
