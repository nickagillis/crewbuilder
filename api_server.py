#!/usr/bin/env python3
"""
CrewBuilder API Server V2
Clean implementation using proper CrewAI patterns
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import traceback

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure CrewAI
import crewai_config

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import CrewBuilder V2
from crewbuilder_crew_v2 import get_crewbuilder_v2

# Create FastAPI app
app = FastAPI(
    title="CrewBuilder API V2",
    description="Build AI agent systems the right way with CrewAI",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://crewbuilder.vercel.app",
        "https://crewbuilder-*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ClarificationRequest(BaseModel):
    requirement: str

class ClarificationChatRequest(BaseModel):
    message: str
    history: list = []
    requirement: str

class GenerationRequest(BaseModel):
    requirement: str
    clarification_context: Optional[Dict[str, Any]] = None

class DeploymentRequest(BaseModel):
    requirement: str
    generated_code: str
    api_keys: Dict[str, str]

class FeedbackRequest(BaseModel):
    requirement: str
    feedback: str
    system_id: Optional[str] = None

# Health Check
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "🚀 CrewBuilder V2 API Running!",
        "status": "operational",
        "version": "2.0.0",
        "description": "AI-powered system that builds CrewAI systems properly",
        "endpoints": {
            "/health": "Detailed health check",
            "/api/clarify": "Start clarification phase",
            "/api/clarify/chat": "Conversational clarification",
            "/api/generate": "Generate complete system",
            "/api/deploy": "Deploy to Railway",
            "/api/feedback": "Submit feedback"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "openai_configured": bool(api_key),
            "crewai_version": "0.148.0",
            "python_version": sys.version.split()[0]
        },
        "crewbuilder": {
            "architecture": "V2 - Simple agents, smart tasks",
            "agents": 8,
            "process": "hierarchical"
        }
    }

# Clarification Endpoints
@app.post("/api/clarify")
async def clarify_requirement(request: ClarificationRequest):
    """
    Start clarification phase for a requirement
    Returns clarification questions and API verification
    """
    try:
        if not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Requirement cannot be empty")
        
        print(f"📝 Clarification request: {request.requirement[:100]}...")
        
        # Get CrewBuilder instance
        crewbuilder = get_crewbuilder_v2()
        
        # Run clarification phase
        result = crewbuilder.run_clarification_phase(request.requirement)
        
        if result['success']:
            return {
                "success": True,
                "questions": result.get('clarification_questions', ''),
                "api_report": result.get('api_report', ''),
                "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get('error', 'Clarification failed')
            )
            
    except Exception as e:
        print(f"❌ Clarification error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clarify/chat")
async def clarify_chat(request: ClarificationChatRequest):
    """
    Conversational clarification using simple clarification specialist
    """
    try:
        from agents.simple_agents import create_clarification_specialist
        from crewai import Task, Crew
        
        # Get the clarification specialist
        clarification_agent = create_clarification_specialist()
        
        # Build context
        context = f"Original requirement: {request.requirement}\n\n"
        context += "Conversation so far:\n"
        for msg in request.history[-5:]:
            context += f"{msg['role']}: {msg['content']}\n"
        context += f"User: {request.message}\n"
        
        # Count exchanges
        user_messages = len([m for m in request.history if m['role'] == 'user']) + 1
        
        # Create conversational task
        task = Task(
            description=f"""
            Have a natural conversation about their automation needs.
            
            {context}
            
            Requirements: "{request.requirement}"
            Latest message: "{request.message}"
            
            Exchange count: {user_messages}
            
            {f"After {user_messages} exchanges, if you have enough info, say you're ready to build." if user_messages >= 4 else "Ask ONE specific question about their use case."}
            
            Focus on their specific tools, volumes, pain points.
            """,
            agent=clarification_agent,
            expected_output="Natural response with follow-up question"
        )
        
        # Simple crew for conversation
        crew = Crew(
            agents=[clarification_agent],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        response_text = str(result)
        
        # Check if ready
        ready_indicators = ["ready to build", "let me get started", "everything i need"]
        ready = any(ind in response_text.lower() for ind in ready_indicators) or user_messages >= 5
        
        return {
            "response": response_text,
            "ready_to_build": ready
        }
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return {
            "response": "I'd love to understand more about your needs. Can you tell me about your current process?",
            "ready_to_build": False
        }

# Generation Endpoint
@app.post("/api/generate")
async def generate_system(request: GenerationRequest):
    """
    Generate complete CrewAI system using hierarchical orchestration
    """
    try:
        if not request.requirement.strip():
            raise HTTPException(status_code=400, detail="Requirement cannot be empty")
        
        print(f"🚀 Generation request: {request.requirement[:100]}...")
        
        # Get CrewBuilder instance
        crewbuilder = get_crewbuilder_v2()
        
        # Build complete system
        result = crewbuilder.build_from_requirement(request.requirement)
        
        if result['success']:
            # Format for frontend
            return {
                "success": True,
                "data": {
                    "systemName": extract_system_name(request.requirement),
                    "agents": count_agents_in_code(result.get('generated_code', '')),
                    "complexity": determine_complexity(result),
                    "estimatedTime": f"{result.get('execution_time', 0):.1f} seconds",
                    "estimatedCost": "$50-100/month",
                    "architecture": {
                        "summary": result.get('architecture', '')[:500]
                    },
                    "deployment": {
                        "config": result.get('deployment_config', '')
                    },
                    "generatedAt": datetime.now().isoformat(),
                    "complexity_score": 2,
                    "pipeline_stages": format_pipeline_stages(result),
                    "generated_code": result.get('generated_code', ''),
                    "requirements_txt": result.get('requirements_txt', ''),
                    "documentation": result.get('documentation', '')
                }
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get('error', 'Generation failed')
            )
            
    except Exception as e:
        print(f"❌ Generation error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Deployment Endpoint
@app.post("/api/deploy")
async def deploy_system(request: DeploymentRequest):
    """
    Deploy generated system to Railway
    """
    try:
        # Import deployment module
        from deployment.railway_deployer import deploy_to_railway
        
        # Prepare deployment package
        deployment_package = {
            "main.py": request.generated_code,
            "requirements.txt": "crewai==0.148.0\ncrewai-tools\nopenai>=1.0.0",
            ".env.example": generate_env_example(request.api_keys)
        }
        
        # Deploy to Railway
        result = await deploy_to_railway(
            deployment_package,
            request.requirement,
            request.api_keys
        )
        
        return {
            "success": result.get('success', False),
            "deployment_url": result.get('deployment_url'),
            "dashboard_url": result.get('dashboard_url'),
            "project_id": result.get('project_id'),
            "error": result.get('error')
        }
        
    except Exception as e:
        print(f"❌ Deployment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Feedback Endpoint
@app.post("/api/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Collect user feedback for continuous improvement
    """
    try:
        # In production, save to database
        print(f"📝 Feedback received:")
        print(f"   Requirement: {request.requirement[:100]}...")
        print(f"   Feedback: {request.feedback}")
        print(f"   System ID: {request.system_id}")
        
        # For now, just acknowledge
        return {
            "success": True,
            "message": "Thank you for your feedback! We use this to improve CrewBuilder."
        }
        
    except Exception as e:
        print(f"❌ Feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper Functions
def extract_system_name(requirement: str) -> str:
    """Extract a meaningful system name from requirement"""
    req_lower = requirement.lower()
    
    # Look for key terms
    if "heygen" in req_lower and "video" in req_lower:
        return "Video Generation System"
    elif "crm" in req_lower or "gohighlevel" in req_lower:
        return "CRM Automation System"
    elif "content" in req_lower and "script" in req_lower:
        return "Content Creation System"
    elif "research" in req_lower:
        return "Research Automation System"
    else:
        # Extract first meaningful noun
        words = requirement.split()[:10]
        for word in words:
            if len(word) > 4 and word.isalpha():
                return f"{word.title()} System"
        return "AI Agent System"

def count_agents_in_code(code: str) -> int:
    """Count agents in generated code"""
    count = code.lower().count('agent(')
    return max(count, 3)  # Minimum 3 agents

def determine_complexity(result: Dict[str, Any]) -> str:
    """Determine system complexity"""
    review = result.get('quality_review', '')
    code_length = len(result.get('generated_code', ''))
    
    if 'simple' in review.lower() or code_length < 1000:
        return 'simple'
    elif 'complex' in review.lower() or code_length > 3000:
        return 'complex'
    return 'moderate'

def format_pipeline_stages(result: Dict[str, Any]) -> list:
    """Format pipeline stages for frontend"""
    stages = []
    
    # Define stage mapping
    stage_info = {
        'clarification_questions': 'Clarification',
        'api_report': 'API Verification',
        'architecture': 'Architecture Design',
        'generated_code': 'Code Generation',
        'quality_review': 'Quality Review',
        'documentation': 'Documentation'
    }
    
    for key, name in stage_info.items():
        if key in result and result[key]:
            stages.append({
                'stage': name,
                'status': 'completed',
                'output': result[key][:200] if isinstance(result[key], str) else str(result[key])
            })
    
    return stages

def generate_env_example(api_keys: Dict[str, str]) -> str:
    """Generate .env.example file content"""
    env_content = "# Environment Variables for Generated CrewAI System\n\n"
    
    # Always include OpenAI
    env_content += "# Required - OpenAI API Key\n"
    env_content += "OPENAI_API_KEY=your_openai_key_here\n\n"
    
    # Add other keys mentioned
    for key, description in api_keys.items():
        if key.upper() != 'OPENAI_API_KEY':
            env_content += f"# {description}\n"
            env_content += f"{key.upper()}=your_{key.lower()}_key_here\n\n"
    
    return env_content

# Run the server
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    print(f"\n🚀 Starting CrewBuilder V2 API on port {port}...")
    print(f"📍 Docs available at: http://localhost:{port}/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)