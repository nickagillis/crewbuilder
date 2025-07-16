#!/usr/bin/env python3
"""
Environment Configuration for CrewBuilder
Secure API key management with fallback modes
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import warnings

# Try to load dotenv for development
try:
    from dotenv import load_dotenv
    # Load .env file if it exists
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ Environment variables loaded from .env file")
    else:
        print("📝 No .env file found - using system environment variables")
except ImportError:
    print("📝 python-dotenv not installed - using system environment variables only")

class CrewBuilderConfig:
    """Secure configuration management for CrewBuilder"""
    
    def __init__(self):
        # Core AI APIs
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Optional Integration APIs
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.linkedin_api_key = os.getenv('LINKEDIN_API_KEY')
        
        # Platform APIs
        self.railway_token = os.getenv('RAILWAY_TOKEN')
        self.vercel_token = os.getenv('VERCEL_TOKEN')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        # Application Settings
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # Check API availability
        self._check_api_availability()
    
    def _check_api_availability(self):
        """Check which APIs are available and report status"""
        
        available_apis = []
        missing_apis = []
        
        # Core AI APIs
        if self.openai_api_key:
            available_apis.append("OpenAI")
        else:
            missing_apis.append("OpenAI")
            
        if self.anthropic_api_key:
            available_apis.append("Anthropic")
        else:
            missing_apis.append("Anthropic")
        
        # Optional APIs
        optional_apis = {
            'Google': self.google_api_key,
            'GitHub': self.github_token,
            'Slack': self.slack_bot_token,
            'SendGrid': self.sendgrid_api_key,
            'Twitter': self.twitter_api_key,
            'LinkedIn': self.linkedin_api_key
        }
        
        for name, key in optional_apis.items():
            if key:
                available_apis.append(name)
        
        # Platform APIs  
        platform_apis = {
            'Railway': self.railway_token,
            'Vercel': self.vercel_token,
            'AWS': self.aws_access_key_id and self.aws_secret_access_key
        }
        
        for name, available in platform_apis.items():
            if available:
                available_apis.append(name)
        
        # Report status
        print("\n🔑 API Key Status:")
        print("=" * 30)
        
        if available_apis:
            print("✅ Available APIs:")
            for api in available_apis:
                print(f"   • {api}")
        
        if missing_apis:
            print("⚠️  Missing Core APIs:")
            for api in missing_apis:
                print(f"   • {api}")
        
        # Functionality warnings
        if not self.openai_api_key and not self.anthropic_api_key:
            print("\n⚠️  WARNING: No AI API keys found")
            print("   CrewBuilder will run in fallback mode with limited functionality")
            print("   Add OPENAI_API_KEY or ANTHROPIC_API_KEY for enhanced features")
        
        print("=" * 30)
    
    @property
    def has_ai_api(self) -> bool:
        """Check if any AI API is available"""
        return bool(self.openai_api_key or self.anthropic_api_key)
    
    @property
    def has_openai(self) -> bool:
        """Check if OpenAI API is available"""
        return bool(self.openai_api_key)
    
    @property
    def has_anthropic(self) -> bool:
        """Check if Anthropic API is available"""
        return bool(self.anthropic_api_key)
    
    @property
    def preferred_ai_api(self) -> str:
        """Get the preferred AI API"""
        if self.openai_api_key:
            return "openai"
        elif self.anthropic_api_key:
            return "anthropic"
        else:
            return "fallback"
    
    def get_api_summary(self) -> Dict[str, Any]:
        """Get a summary of available APIs"""
        return {
            'ai_apis': {
                'openai': bool(self.openai_api_key),
                'anthropic': bool(self.anthropic_api_key)
            },
            'integration_apis': {
                'google': bool(self.google_api_key),
                'github': bool(self.github_token),
                'slack': bool(self.slack_bot_token),
                'sendgrid': bool(self.sendgrid_api_key),
                'twitter': bool(self.twitter_api_key),
                'linkedin': bool(self.linkedin_api_key)
            },
            'platform_apis': {
                'railway': bool(self.railway_token),
                'vercel': bool(self.vercel_token),
                'aws': bool(self.aws_access_key_id and self.aws_secret_access_key)
            },
            'preferred_ai': self.preferred_ai_api,
            'fallback_mode': not self.has_ai_api
        }
    
    def setup_openai_client(self):
        """Setup OpenAI client if API key is available"""
        if not self.openai_api_key:
            return None
            
        try:
            import openai
            openai.api_key = self.openai_api_key
            return openai
        except ImportError:
            warnings.warn("OpenAI package not installed. Run: pip install openai")
            return None
    
    def setup_anthropic_client(self):
        """Setup Anthropic client if API key is available"""
        if not self.anthropic_api_key:
            return None
            
        try:
            import anthropic
            return anthropic.Anthropic(api_key=self.anthropic_api_key)
        except ImportError:
            warnings.warn("Anthropic package not installed. Run: pip install anthropic")
            return None

# Global configuration instance
config = CrewBuilderConfig()

def get_config() -> CrewBuilderConfig:
    """Get the global configuration instance"""
    return config

# Quick setup helper
def setup_environment():
    """Quick environment setup with instructions"""
    
    if not config.has_ai_api:
        print("\n🚀 CrewBuilder Setup Instructions:")
        print("=" * 40)
        print("1. Copy the environment template:")
        print("   cp .env.example .env")
        print()
        print("2. Edit .env with your API keys:")
        print("   nano .env  # or your preferred editor")
        print()
        print("3. Required for enhanced functionality:")
        print("   OPENAI_API_KEY=sk-your-openai-key-here")
        print()
        print("4. Start CrewBuilder:")
        print("   python api_server.py")
        print("=" * 40)
    
    return config

if __name__ == "__main__":
    setup_environment()
