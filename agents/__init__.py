"""
CrewBuilder Agents - Simple, focused specialists following CrewAI best practices
"""

from .simple_agents import (
    create_clarification_specialist,
    create_api_analyst,
    create_crew_architect,
    create_task_designer,
    create_code_writer,
    create_quality_reviewer,
    create_deployment_specialist,
    create_documentation_writer,
    create_orchestration_manager,
    get_all_crewbuilder_agents
)

__all__ = [
    'create_clarification_specialist',
    'create_api_analyst',
    'create_crew_architect',
    'create_task_designer',
    'create_code_writer',
    'create_quality_reviewer',
    'create_deployment_specialist',
    'create_documentation_writer',
    'create_orchestration_manager',
    'get_all_crewbuilder_agents'
]
