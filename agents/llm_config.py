"""
LLM Configuration for CrewAI Agents
Ensures all agents use the configured OpenAI API
"""

import os
from langchain_openai import ChatOpenAI
from typing import Optional

def get_configured_llm(temperature: float = 0.7, model: str = "gpt-4o-mini") -> Optional[ChatOpenAI]:
    """
    Get a configured LLM instance for CrewAI agents
    
    Args:
        temperature: LLM temperature (0.0 = deterministic, 1.0 = creative)
        model: OpenAI model to use
        
    Returns:
        Configured ChatOpenAI instance or None if no API key
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("WARNING: No OPENAI_API_KEY found, agent will use fallback mode")
        return None
        
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key
    )