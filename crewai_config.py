"""
Global CrewAI configuration to ensure all agents use OpenAI properly
"""

import os

# Set default LLM for CrewAI
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'  # Use the mini model for cost efficiency

# CrewAI specific settings
os.environ['OPENAI_API_BASE'] = 'https://api.openai.com/v1'
os.environ['OPENAI_API_TYPE'] = 'openai'

# LiteLLM settings (used internally by CrewAI)
os.environ['LITELLM_LOG'] = 'DEBUG'  # Enable debug logging
os.environ['LITELLM_TELEMETRY'] = 'False'  # Disable telemetry
os.environ['OPENAI_API_VERSION'] = '2023-05-15'  # API version

# Force IPv4 for OpenAI (Railway might default to IPv6)
import socket
original_getaddrinfo = socket.getaddrinfo

def forced_ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """Force IPv4 for OpenAI API calls"""
    if host in ['api.openai.com', 'openai.com']:
        family = socket.AF_INET  # Force IPv4
    return original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = forced_ipv4_getaddrinfo

# Ensure the API key is set
if not os.getenv('OPENAI_API_KEY'):
    print("WARNING: OPENAI_API_KEY not found in environment!")
else:
    # CrewAI looks for this specific env var
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    print(f"✓ CrewAI configured with OpenAI API key: {os.getenv('OPENAI_API_KEY')[:20]}...")

# Set CrewAI to use OpenAI
os.environ['CREWAI_LLM_PROVIDER'] = 'openai'