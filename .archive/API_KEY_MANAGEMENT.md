# CrewBuilder API Key Management Guide

## 🔑 Required API Keys

### Core AI Functionality
- **OPENAI_API_KEY** - Primary LLM for all agents (required for enhanced mode)
- **ANTHROPIC_API_KEY** - Alternative LLM (optional, for Claude models)

### Optional Enhancement APIs (Generated systems may need these)
- **GOOGLE_API_KEY** - Google services (Gmail, Analytics, etc.)
- **GITHUB_TOKEN** - Code repository access
- **SLACK_BOT_TOKEN** - Slack integrations  
- **SENDGRID_API_KEY** - Email automation
- **TWITTER_API_KEY** - Social media automation
- **LINKEDIN_API_KEY** - LinkedIn automation

### Platform/Deployment APIs
- **RAILWAY_TOKEN** - Railway deployment (if using Railway)
- **VERCEL_TOKEN** - Vercel deployment (if using Vercel)
- **AWS_ACCESS_KEY_ID** / **AWS_SECRET_ACCESS_KEY** - AWS services
- **AZURE_SUBSCRIPTION_KEY** - Azure services

## 🛡️ Secure Storage Strategy

### Development Environment

1. **Create .env file** (NEVER commit this)
```bash
# .env file in project root
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-api-key-here
GITHUB_TOKEN=ghp_your-github-token-here

# Optional APIs
SLACK_BOT_TOKEN=xoxb-your-slack-token-here
SENDGRID_API_KEY=SG.your-sendgrid-key-here
```

2. **Create .env.example** (safe to commit)
```bash
# .env.example - Template for required environment variables
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-api-key-here
GITHUB_TOKEN=ghp_your-github-token-here

# Optional APIs for enhanced functionality
SLACK_BOT_TOKEN=xoxb-your-slack-token-here
SENDGRID_API_KEY=SG.your-sendgrid-key-here
TWITTER_API_KEY=your-twitter-api-key-here
LINKEDIN_API_KEY=your-linkedin-api-key-here

# Platform APIs (for deployment)
RAILWAY_TOKEN=your-railway-token-here
VERCEL_TOKEN=your-vercel-token-here
AWS_ACCESS_KEY_ID=your-aws-access-key-here
AWS_SECRET_ACCESS_KEY=your-aws-secret-key-here
```

### Production Environment

1. **Use Platform Environment Variables**
   - Railway: Dashboard → Environment Variables
   - Vercel: Dashboard → Settings → Environment Variables
   - AWS: Systems Manager Parameter Store (SecureString)
   - Azure: Key Vault
   - Google Cloud: Secret Manager

2. **Use Secret Management Services**
   - **HashiCorp Vault** - Enterprise secret management
   - **AWS Secrets Manager** - AWS native secrets
   - **Azure Key Vault** - Azure native secrets
   - **1Password** - Business secret management

## 📁 File Security Configuration

### .gitignore Setup
```bash
# Environment Variables (CRITICAL)
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# API Keys and Secrets
api_keys.txt
secrets.json
config/secrets.yml
*.key
*.pem

# OS and IDE files
.DS_Store
Thumbs.db
.vscode/settings.json
.idea/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log
```

### Environment Loading Code
```python
# config/environment.py
import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Secure configuration management"""
    
    def __init__(self):
        # Load environment variables from .env file
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        # Core AI APIs
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Optional APIs
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
        
        # Platform APIs
        self.railway_token = os.getenv('RAILWAY_TOKEN')
        self.vercel_token = os.getenv('VERCEL_TOKEN')
        
        # Validate critical keys
        self._validate_keys()
    
    def _validate_keys(self):
        """Validate that critical API keys are present"""
        if not self.openai_api_key:
            print("⚠️ WARNING: OPENAI_API_KEY not found - running in fallback mode")
        
        if not self.openai_api_key and not self.anthropic_api_key:
            print("⚠️ WARNING: No AI API keys found - limited functionality")
    
    def has_openai(self) -> bool:
        """Check if OpenAI API key is available"""
        return bool(self.openai_api_key)
    
    def has_anthropic(self) -> bool:
        """Check if Anthropic API key is available"""
        return bool(self.anthropic_api_key)

# Usage in agents
config = Config()

if config.has_openai():
    # Use enhanced AI features
    pass
else:
    # Use fallback mode
    pass
```

## 🚀 Deployment Security Best Practices

### Railway Deployment
```bash
# Set environment variables in Railway dashboard
railway login
railway link
railway variables:set OPENAI_API_KEY=sk-your-key-here
railway variables:set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Vercel Deployment
```bash
# Set environment variables via CLI
vercel env add OPENAI_API_KEY
vercel env add ANTHROPIC_API_KEY

# Or use Vercel dashboard: Settings → Environment Variables
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Don't put secrets in Dockerfile!
# Use docker run -e or docker-compose.yml with env_file

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Use environment variables at runtime
CMD ["python", "api_server.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  crewbuilder:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env  # Load from .env file (not committed)
    environment:
      - ENVIRONMENT=production
```

## 🔄 Progressive Enhancement Strategy

### Tier 1: Basic Functionality (No API Keys)
- Fallback mode with intelligent analysis
- Pattern-based agent generation
- Static recommendations

### Tier 2: Enhanced AI (OpenAI API Key)
- Real AI-powered requirement analysis
- Dynamic agent generation
- Custom architecture optimization

### Tier 3: Full Integration (Multiple API Keys)
- Real system integration testing
- Live API recommendations
- End-to-end deployment validation

## 🛡️ Security Checklist

### Development
- [ ] .env file created and added to .gitignore
- [ ] .env.example created with placeholders
- [ ] No hardcoded API keys in source code
- [ ] Environment loading implemented
- [ ] Fallback mode functional without keys

### Pre-Commit
- [ ] git status shows no .env files
- [ ] No API keys visible in git diff
- [ ] .gitignore includes all secret patterns
- [ ] Code review for hardcoded secrets

### Production
- [ ] Environment variables set in platform
- [ ] API keys never logged or displayed
- [ ] Secrets rotated regularly
- [ ] Access logs monitored
- [ ] Rate limiting implemented

## 📋 Quick Setup Commands

### Initial Setup
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your API keys
nano .env  # or your preferred editor

# 3. Verify .gitignore includes .env
echo ".env" >> .gitignore

# 4. Test without committing
python api_server.py  # Should work with or without keys
```

### Production Deployment
```bash
# Railway
railway variables:set OPENAI_API_KEY=your-key-here

# Vercel  
vercel env add OPENAI_API_KEY

# Manual server
export OPENAI_API_KEY=your-key-here
python api_server.py
```

This approach ensures your API keys are secure while maintaining functionality across development and production environments.
