#!/usr/bin/env python3
"""
CrewBuilder Quick Setup
Helps users set up API keys securely
"""

import os
import shutil
from pathlib import Path

def setup_environment_file():
    """Setup the .env file from template"""
    
    print("CrewBuilder API Key Setup")
    print("=" * 35)
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    # Check if .env already exists
    if env_file.exists():
        print("✅ .env file already exists")
        response = input("Do you want to recreate it? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return True
    
    # Copy from template
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
    else:
        print("❌ .env.example not found")
        return False
    
    print("\n📝 Next steps:")
    print("1. Edit the .env file with your API keys:")
    print("   nano .env  # or your preferred editor")
    print()
    print("2. Get API keys from:")
    print("   • OpenAI: https://platform.openai.com/api-keys")
    print("   • Anthropic: https://console.anthropic.com/")
    print()
    print("3. Replace placeholders with your actual keys")
    print("4. Save the file and restart CrewBuilder")
    
    return True

def check_security():
    """Check that security measures are in place"""
    
    print("\n🛡️ Security Check")
    print("=" * 20)
    
    issues = []
    
    # Check .gitignore
    gitignore = Path('.gitignore')
    if gitignore.exists():
        content = gitignore.read_text()
        if '.env' in content:
            print("✅ .env file is in .gitignore")
        else:
            issues.append(".env not found in .gitignore")
    else:
        issues.append(".gitignore file not found")
    
    # Check for .env in git status
    import subprocess
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if '.env' in result.stdout:
            issues.append(".env file is tracked by git (SECURITY RISK!)")
    except:
        pass  # Git not available or not a git repo
    
    if issues:
        print("⚠️ Security Issues Found:")
        for issue in issues:
            print(f"   • {issue}")
        print("\nPlease fix these issues before proceeding!")
        return False
    else:
        print("✅ Security checks passed")
        return True

def test_api_connection():
    """Test API connection if keys are available"""
    
    print("\n🧪 API Connection Test")
    print("=" * 25)
    
    try:
        from config import config
        
        if config.has_openai:
            print("✅ OpenAI API key found")
            # Could add a simple API test here
        elif config.has_anthropic:
            print("✅ Anthropic API key found")
        else:
            print("⚠️ No AI API keys found")
            print("   CrewBuilder will run in fallback mode")
        
        # Show available APIs
        summary = config.get_api_summary()
        
        ai_count = sum(summary['ai_apis'].values())
        integration_count = sum(summary['integration_apis'].values())
        platform_count = sum(summary['platform_apis'].values())
        
        print(f"📊 API Summary:")
        print(f"   • AI APIs: {ai_count}/2 available")
        print(f"   • Integration APIs: {integration_count}/6 available")
        print(f"   • Platform APIs: {platform_count}/3 available")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API configuration: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🚀 Welcome to CrewBuilder Setup!")
    print("This will help you configure API keys securely.\n")
    
    # Step 1: Setup environment file
    if not setup_environment_file():
        print("❌ Failed to setup environment file")
        return False
    
    # Step 2: Security check
    if not check_security():
        print("❌ Security check failed")
        return False
    
    # Step 3: Test configuration
    print("\nAfter you've added your API keys to .env:")
    test_choice = input("Test API configuration now? (y/N): ")
    if test_choice.lower() == 'y':
        test_api_connection()
    
    print("\n🎉 Setup complete!")
    print("=" * 20)
    print("Ready to start CrewBuilder:")
    print("1. python api_server_fallback.py  # Start API server")
    print("2. cd web && npm run dev        # Start web interface")
    print("3. Visit http://localhost:3000   # Use CrewBuilder!")
    
    return True

if __name__ == "__main__":
    main()
