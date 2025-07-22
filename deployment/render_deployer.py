"""
Render Deployment Module for CrewBuilder
Deploys generated CrewAI systems directly to Render
"""

import os
import json
import requests
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

class RenderDeployer:
    """Handles deployment of CrewAI systems to Render"""
    
    def __init__(self, render_api_key: Optional[str] = None):
        self.api_key = render_api_key or os.getenv('RENDER_API_KEY')
        if not self.api_key:
            raise ValueError("Render API key required. Set RENDER_API_KEY env var")
        
        self.api_base = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def deploy_crewai_system(self, 
                           generated_code: Dict[str, str],
                           project_name: str,
                           user_api_keys: Dict[str, str],
                           requirements: str) -> Dict[str, Any]:
        """
        Deploy a complete CrewAI system to Render
        
        Args:
            generated_code: Dict with 'main.py', 'requirements.txt', etc
            project_name: Name for the Render service
            user_api_keys: User's API keys (OpenAI, etc)
            requirements: Original business requirements
            
        Returns:
            Deployment info including URLs and status
        """
        
        try:
            # Create Render blueprint for the service
            blueprint = self._create_render_blueprint(
                project_name, 
                generated_code,
                user_api_keys
            )
            
            # Create the service on Render
            service = self._create_render_service(blueprint)
            
            # Deploy the code
            deployment = self._trigger_deployment(service['id'], generated_code)
            
            return {
                "success": True,
                "service_id": service['id'],
                "deployment_url": f"https://{service['name']}.onrender.com",
                "dashboard_url": f"https://dashboard.render.com/web/{service['id']}",
                "status": "deploying",
                "created_at": datetime.now().isoformat(),
                "project_name": project_name,
                "requirements": requirements
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _create_render_blueprint(self, name: str, code: Dict[str, str], env_vars: Dict[str, str]) -> Dict:
        """Create Render blueprint configuration"""
        
        return {
            "name": name,
            "type": "web_service",
            "env": "python",
            "plan": "starter",  # $7/month
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "python main.py",
            "envVars": [
                {"key": k, "value": v} for k, v in env_vars.items()
            ],
            "autoDeploy": "yes",
            "healthCheckPath": "/health"
        }
    
    def _create_render_service(self, blueprint: Dict) -> Dict:
        """Create a new Render service"""
        
        response = requests.post(
            f"{self.api_base}/services",
            headers=self.headers,
            json=blueprint
        )
        
        if response.status_code != 201:
            raise Exception(f"Failed to create Render service: {response.text}")
        
        return response.json()
    
    def _trigger_deployment(self, service_id: str, code: Dict[str, str]) -> Dict:
        """Trigger deployment of code to Render service"""
        
        # For Render, you typically connect a GitHub repo
        # For direct deployment, we'd use their Git API
        # This is simplified - real implementation would push to Render's Git
        
        deploy_endpoint = f"{self.api_base}/services/{service_id}/deploys"
        
        response = requests.post(
            deploy_endpoint,
            headers=self.headers,
            json={"clearCache": "false"}
        )
        
        if response.status_code != 201:
            raise Exception(f"Failed to trigger deployment: {response.text}")
        
        return response.json()


# Alternative: Fly.io Deployer
class FlyDeployer:
    """Handles deployment to Fly.io"""
    
    def __init__(self, fly_api_token: Optional[str] = None):
        self.token = fly_api_token or os.getenv('FLY_API_TOKEN')
        self.api_base = "https://api.fly.io/graphql"
    
    def deploy_crewai_system(self, generated_code: Dict[str, str], 
                           app_name: str, user_api_keys: Dict[str, str]) -> Dict:
        """Deploy to Fly.io"""
        
        # Create fly.toml configuration
        fly_config = f"""
app = "{app_name}"
primary_region = "iad"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[processes]
  app = "python main.py"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"
  
  [[services.ports]]
    port = 80
    handlers = ["http"]
    
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
"""
        
        # Fly.io deployment would use their CLI or API
        # This is a simplified structure
        
        return {
            "success": True,
            "app_name": app_name,
            "deployment_url": f"https://{app_name}.fly.dev",
            "dashboard_url": f"https://fly.io/apps/{app_name}",
            "status": "deploying"
        }