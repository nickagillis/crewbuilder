"""
Interface Builder Agent - Creates usable interfaces for generated CrewAI systems
THIS IS CRITICAL - Without this, users can't actually USE what we build!
"""

from crewai import Agent
from .llm_config import get_configured_llm

def create_interface_builder():
    """Agent that builds the missing execution layer - API + UI"""
    return Agent(
        role="Full-Stack Interface Developer",
        goal="Create complete, usable interfaces for CrewAI systems so users can actually run them",
        backstory="""You're a practical developer who knows users need more than just agent code. 
        You build simple but complete interfaces with FastAPI backends and basic HTML frontends. 
        You always include: input forms, trigger buttons, result displays, and API key management. 
        Every system you build is immediately usable, not just theoretical code.""",
        llm=get_configured_llm(temperature=0.3),
        verbose=True,
        allow_delegation=False
    )

def create_execution_wrapper():
    """Agent that wraps CrewAI code in executable services"""
    return Agent(
        role="API Service Developer", 
        goal="Wrap CrewAI agents in production-ready API services with proper async handling",
        backstory="""You specialize in making AI agents accessible through APIs. You create 
        FastAPI services that handle long-running CrewAI tasks, manage state, store results, 
        and provide status endpoints. You ensure API keys are handled securely and systems 
        can run reliably in production.""",
        llm=get_configured_llm(temperature=0.2),
        verbose=True,
        allow_delegation=False
    )