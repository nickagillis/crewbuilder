"""
CrewBuilder Tasks - Where the actual work happens
Following CrewAI best practices: Tasks contain the logic, not agents
"""

from crewai import Task
from typing import List, Dict, Any

def create_clarification_task(requirement: str):
    """Task to generate clarification questions based on user requirement"""
    return Task(
        description=f"""
        Analyze this business automation requirement and generate 3-5 highly specific 
        clarification questions that will help build a better system.
        
        User Requirement: {requirement}
        
        Focus your questions on:
        1. Specific integrations mentioned (APIs, tools, platforms)
        2. Volume and frequency of operations
        3. Current pain points and manual processes
        4. Success criteria and expected outcomes
        5. Technical constraints or preferences
        
        Make questions specific to their use case, not generic. For example, if they mention
        HeyGen, ask about avatar IDs, video length, templates. If they mention a CRM, ask
        about specific workflows, contact segments, etc.
        
        Output format:
        QUESTION 1: [Specific question]
        CONTEXT: [Why this matters for their system]
        
        QUESTION 2: [Specific question]
        CONTEXT: [Why this matters]
        
        (Continue for 3-5 questions)
        """,
        expected_output="3-5 specific clarification questions with context",
        agent=None  # Will be assigned when creating crew
    )

def create_api_verification_task(requirement: str, clarifications: Dict[str, str] = None):
    """Task to verify API availability and integration options"""
    return Task(
        description=f"""
        Research and verify API availability for all systems mentioned in this requirement.
        
        Requirement: {requirement}
        {f"Additional context: {clarifications}" if clarifications else ""}
        
        For EACH system/tool mentioned:
        1. Check if it has an API (REST, GraphQL, webhooks)
        2. Note authentication method (API key, OAuth, etc.)
        3. Find pricing/rate limits
        4. Identify key endpoints needed
        5. If NO API exists, suggest alternatives (CSV export, email parsing, RPA, etc.)
        
        Output format:
        SYSTEM: [Name]
        API AVAILABLE: Yes/No
        AUTH METHOD: [Type]
        PRICING: [Free tier limits, paid tiers]
        KEY ENDPOINTS: [List relevant endpoints]
        ALTERNATIVE: [If no API]
        
        INTEGRATION FEASIBILITY: [High/Medium/Low]
        ESTIMATED MONTHLY COST: $[amount]
        """,
        expected_output="Complete API availability report with integration recommendations",
        agent=None,
        context=[]  # Will reference clarification task if available
    )

def create_architecture_design_task(requirement: str, api_report: str):
    """Task to design the CrewAI architecture"""
    return Task(
        description=f"""
        Design a CrewAI architecture for this requirement following best practices.
        
        Requirement: {requirement}
        API Report: {api_report}
        
        Design decisions to make:
        1. Process type: Sequential, Hierarchical, or Consensual?
        2. Number of agents (aim for 3-5 simple agents)
        3. Whether to use Crews, Flows, or hybrid approach
        4. Agent roles and specializations
        
        For EACH agent, define:
        - Role: [Specific title]
        - Goal: [Clear objective]
        - Backstory: [1-2 sentences establishing expertise]
        - Tools needed: [List any specific tools]
        
        Architecture output:
        PROCESS TYPE: [Sequential/Hierarchical/Consensual]
        RATIONALE: [Why this process type]
        
        AGENT 1:
        Role: [Title]
        Goal: [Objective]
        Backstory: [Experience]
        Tools: [List]
        
        (Continue for all agents)
        
        WORKFLOW SUMMARY: [How agents work together]
        """,
        expected_output="Complete CrewAI architecture design with agent definitions",
        agent=None,
        context=[]  # Will reference API verification task
    )

def create_task_flow_design_task(architecture: str):
    """Task to design detailed task flows"""
    return Task(
        description=f"""
        Create detailed task definitions for this CrewAI architecture.
        
        Architecture: {architecture}
        
        For EACH major step in the workflow, create a task definition:
        
        TASK NAME: [Descriptive name]
        DESCRIPTION: [What the task does - be specific]
        EXPECTED OUTPUT: [Exact format/content expected]
        ASSIGNED AGENT: [Which agent handles this]
        DEPENDENCIES: [Which tasks must complete first]
        CONTEXT NEEDED: [What information from previous tasks]
        
        Remember CrewAI best practices:
        - Tasks do the work, not agents
        - Single purpose, single output per task
        - Clear dependencies and context flow
        - Explicit expected outputs
        
        Include at least 5-8 tasks that cover the full workflow.
        """,
        expected_output="Complete task flow design with all task definitions",
        agent=None,
        context=[]  # Will reference architecture task
    )

def create_code_generation_task(architecture: str, task_flow: str):
    """Task to generate the actual CrewAI implementation"""
    return Task(
        description=f"""
        Generate production-ready CrewAI implementation code.
        
        Architecture: {architecture}
        Task Flow: {task_flow}
        
        Generate the following files:
        
        1. main.py with:
           - All agent definitions (simple, focused)
           - All task definitions (detailed, specific)
           - Crew setup with proper process type
           - Error handling and logging
           - Configuration from environment variables
           - if __name__ == "__main__" block
        
        2. requirements.txt with:
           - crewai==0.148.0
           - crewai-tools
           - All other dependencies with versions
        
        3. .env.example with:
           - All required environment variables
           - Clear descriptions for each
        
        Code requirements:
        - Follow CrewAI 0.148.0 patterns exactly
        - Include proper error handling
        - Add helpful comments
        - Make it immediately runnable
        
        Use markdown code blocks for each file.
        """,
        expected_output="Complete implementation with main.py, requirements.txt, and .env.example",
        agent=None,
        context=[]  # Will reference architecture and task flow
    )

def create_quality_review_task(generated_code: str, requirement: str):
    """Task to review generated code for quality and correctness"""
    return Task(
        description=f"""
        Review this generated CrewAI code for quality and correctness.
        
        Original Requirement: {requirement}
        Generated Code: {generated_code}
        
        Check for:
        
        1. REQUIREMENT ALIGNMENT
           - Does it solve the user's actual problem?
           - Are all features implemented?
           
        2. CREWAI BEST PRACTICES
           - Simple agents (not over-engineered)?
           - Tasks contain the logic?
           - Proper process type selected?
           - Good task dependencies?
           
        3. CODE QUALITY
           - Syntax errors?
           - Import issues?
           - Error handling present?
           - Environment variables used?
           
        4. COMMON ISSUES
           - API rate limits considered?
           - Authentication handled properly?
           - Costs reasonable?
           
        Output format:
        REQUIREMENT ALIGNMENT: Pass/Fail - [Details]
        BEST PRACTICES: Pass/Fail - [Details]
        CODE QUALITY: Pass/Fail - [Details]
        
        CRITICAL ISSUES: [List any that must be fixed]
        IMPROVEMENTS: [Suggested enhancements]
        
        OVERALL: Ready to Deploy / Needs Fixes
        """,
        expected_output="Quality review report with pass/fail assessment",
        agent=None,
        context=[]  # Will reference code generation task
    )

def create_deployment_config_task(generated_code: str):
    """Task to create deployment configuration"""
    return Task(
        description=f"""
        Create Railway deployment configuration for this CrewAI system.
        
        Generated Code: {generated_code}
        
        Create the following deployment files:
        
        1. railway.toml:
           - Python 3.11 runtime
           - Build and start commands
           - Health check endpoint if applicable
        
        2. Dockerfile (if needed):
           - Multi-stage build for efficiency
           - Proper Python setup
           - Security best practices
        
        3. start.sh:
           - Environment setup
           - Dependency installation
           - Application startup
        
        4. Deployment Instructions:
           - Step-by-step Railway deployment
           - Environment variable setup
           - Monitoring setup
           - Cost estimates
        
        Include security considerations:
        - Never commit API keys
        - Use Railway environment variables
        - Implement rate limiting if needed
        """,
        expected_output="Complete deployment configuration with instructions",
        agent=None,
        context=[]  # Will reference code generation
    )

def create_documentation_task(generated_code: str, deployment_config: str):
    """Task to create comprehensive documentation"""
    return Task(
        description=f"""
        Create user-friendly documentation for this CrewAI system.
        
        Code: {generated_code}
        Deployment: {deployment_config}
        
        Create a comprehensive README.md with:
        
        1. OVERVIEW
           - What the system does
           - Key features
           - Architecture diagram (ASCII)
        
        2. QUICK START
           - Prerequisites
           - Installation steps
           - First run example
        
        3. CONFIGURATION
           - All environment variables
           - Optional settings
           - API key setup guides
        
        4. USAGE
           - Basic examples
           - Advanced features
           - Common workflows
        
        5. TROUBLESHOOTING
           - Common errors and fixes
           - Debug tips
           - FAQ
        
        6. API REFERENCE
           - If system has API endpoints
           - Input/output formats
           - Error codes
        
        Make it friendly and example-heavy. Include code snippets.
        """,
        expected_output="Complete README.md documentation",
        agent=None,
        context=[]  # Will reference code and deployment
    )

def create_final_package_task():
    """Task to package everything for delivery"""
    return Task(
        description="""
        Package all generated artifacts into a final deliverable.
        
        Create a summary that includes:
        
        1. SYSTEM OVERVIEW
           - What was built
           - Key capabilities
           - Architecture summary
        
        2. FILES GENERATED
           - List all files created
           - Brief description of each
        
        3. NEXT STEPS
           - Deployment checklist
           - Testing recommendations
           - Monitoring setup
        
        4. SUPPORT RESOURCES
           - Documentation links
           - Community resources
           - Common modifications
        
        Format as a clean, professional summary suitable for delivery to the user.
        """,
        expected_output="Final package summary with all deliverables organized",
        agent=None,
        context=[]  # Will reference all previous tasks
    )