"""
Interface Building Tasks - Create usable systems, not just code
"""

from crewai import Task

def create_interface_generation_task(crew_code: str, requirements: str):
    """Generate complete FastAPI + UI wrapper for the CrewAI system"""
    return Task(
        description=f"""
        Create a complete, usable interface for this CrewAI system.
        
        Requirements: {requirements}
        CrewAI Code: {crew_code}
        
        Generate:
        
        1. app.py - FastAPI application with:
           - POST /api/execute - Run the crew with user inputs
           - GET /api/status/<id> - Check execution status  
           - GET /api/results/<id> - Get results
           - GET / - Serve the web interface
           
        2. templates/index.html - Simple web UI with:
           - Input form based on what the crew needs
           - "Run" button to execute
           - Results display area
           - Status/progress indicator
           
        3. templates/settings.html - API key management:
           - Form to enter required API keys
           - Save to environment variables
           - Clear instructions
           
        4. static/app.js - Frontend logic:
           - Submit form data
           - Poll for status
           - Display results
           
        5. Updated requirements.txt:
           - Add: fastapi, uvicorn, python-multipart, aiofiles
           
        The interface must be:
        - Immediately usable
        - Handle long-running crews (async)
        - Store results 
        - Show clear status/errors
        
        Output complete, ready-to-run code.
        """,
        expected_output="Complete FastAPI app with web UI that wraps the CrewAI system",
        agent=None  # Will be assigned
    )

def create_deployment_wrapper_task(interface_code: str):
    """Create final deployment package with everything needed"""
    return Task(
        description=f"""
        Package everything for one-click deployment to Railway.
        
        Interface Code: {interface_code}
        
        Create:
        
        1. Dockerfile:
           - Python 3.11 base
           - Install all dependencies  
           - Expose port 8000
           - Run uvicorn
           
        2. railway.toml:
           - Proper build settings
           - Environment variable setup
           - Health check endpoint
           
        3. .env.example:
           - All required API keys
           - Clear descriptions
           - Default values where appropriate
           
        4. README.md:
           - "Deploy to Railway" button
           - Quick start instructions
           - How to use the interface
           - API documentation
           
        5. File structure:
           ```
           /
           ├── app.py (FastAPI + CrewAI)
           ├── crew/ (CrewAI agents)
           ├── templates/ (Web UI)
           ├── static/ (JS/CSS)
           ├── Dockerfile
           ├── railway.toml
           └── requirements.txt
           ```
        
        Make it truly one-click deployable.
        """,
        expected_output="Complete deployment package ready for Railway",
        agent=None
    )