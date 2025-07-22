"""
Robust setup template for generated CrewAI systems
Based on production debugging experience
"""

ROBUST_SETUP_CODE = '''
# Robust environment setup based on production experience
import os
import sys

def validate_environment():
    """Validate and clean environment variables before starting"""
    
    # Check and clean API key
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in environment")
        print("Please set: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Clean common issues (newlines, extra spaces)
    api_key = api_key.replace('\\n', '').replace('\\r', '').strip()
    api_key = ' '.join(api_key.split())  # Remove extra spaces
    
    # Validate format
    if len(api_key) > 200:
        print(f"❌ ERROR: API key appears corrupted (length: {len(api_key)})")
        print("Please check your environment variable for extra characters")
        sys.exit(1)
    
    if not api_key.startswith('sk-'):
        print("❌ ERROR: API key should start with 'sk-'")
        sys.exit(1)
    
    # Set cleaned key back to environment
    os.environ['OPENAI_API_KEY'] = api_key
    
    print(f"✅ Environment validated")
    print(f"   API Key: {api_key[:20]}...")
    
    return api_key

def safe_crew_execution(crew, input_data=None):
    """Execute crew with proper error handling"""
    try:
        print("\\n🚀 Starting crew execution...")
        result = crew.kickoff(inputs=input_data) if input_data else crew.kickoff()
        
        # Always convert CrewOutput to string
        result_text = str(result)
        
        print("✅ Crew execution completed successfully")
        return result_text
        
    except Exception as e:
        error_type = type(e).__name__
        
        if "AuthenticationError" in error_type:
            print(f"\\n❌ Authentication failed: {e}")
            print("Please check your API key at: https://platform.openai.com/api-keys")
        elif "RateLimitError" in error_type:
            print(f"\\n❌ Rate limit exceeded: {e}")
            print("Consider upgrading your OpenAI plan or waiting")
        elif "APIConnectionError" in error_type:
            print(f"\\n❌ Connection failed: {e}")
            print("Check your internet connection and firewall settings")
        else:
            print(f"\\n❌ Execution failed: {error_type}: {e}")
        
        raise

# Run validation on import
validate_environment()
'''

def get_robust_imports():
    """Get import statements that include error handling"""
    return '''
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
import sys
from datetime import datetime
import json
import traceback
'''

def get_llm_initialization():
    """Get robust LLM initialization code"""
    return '''
# Initialize LLM with error handling
try:
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        max_retries=3,
        timeout=60,
        api_key=os.getenv('OPENAI_API_KEY')
    )
except Exception as e:
    print(f"Failed to initialize LLM: {e}")
    sys.exit(1)
'''