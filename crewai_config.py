"""
Global CrewAI configuration to ensure all agents use OpenAI properly
"""

import os

# Set default LLM for CrewAI
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'  # Use the mini model for cost efficiency

# CrewAI specific settings
os.environ['OPENAI_API_BASE'] = 'https://api.openai.com/v1'
os.environ['OPENAI_API_TYPE'] = 'openai'

# Ensure the API key is set
if not os.getenv('OPENAI_API_KEY'):
    print("WARNING: OPENAI_API_KEY not found in environment!")
else:
    # CrewAI looks for this specific env var
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    print(f"✓ CrewAI configured with OpenAI API key: {os.getenv('OPENAI_API_KEY')[:20]}...")

# Set CrewAI to use OpenAI
os.environ['CREWAI_LLM_PROVIDER'] = 'openai'