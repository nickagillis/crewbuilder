"""
LLM Configuration for CrewAI Agents
Ensures all agents use the configured OpenAI API
"""

import os
from langchain_openai import ChatOpenAI
from typing import Optional

def get_configured_llm(temperature: float = 0.7, model: str = "gpt-3.5-turbo") -> Optional[ChatOpenAI]:
    """
    Get a configured LLM instance for CrewAI agents
    
    Args:
        temperature: LLM temperature (0.0 = deterministic, 1.0 = creative)
        model: OpenAI model to use
        
    Returns:
        Configured ChatOpenAI instance or None if no API key
    """
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    if not api_key:
        print("WARNING: No OPENAI_API_KEY found, agent will use fallback mode")
        return None
    
    # Clean the API key - remove newlines and extra spaces
    api_key = api_key.replace('\n', '').replace('\r', '').strip()
    api_key = ' '.join(api_key.split())  # Remove extra spaces
        
    # Create LLM with retry and timeout settings for Railway
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key,
        max_retries=3,  # Retry failed requests
        timeout=60,  # 60 second timeout
        request_timeout=60,  # Also set request timeout
        streaming=False,  # Disable streaming for stability
        verbose=True  # Enable verbose logging
    )