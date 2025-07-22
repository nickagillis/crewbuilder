"""
Railway Deployment Module for CrewBuilder
Deploys generated CrewAI systems directly to Railway
"""

import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import uuid
import requests
from datetime import datetime

class RailwayDeployer:
    """Handles deployment of CrewAI systems to Railway"""
    
    def __init__(self, railway_token: Optional[str] = None):
        self.token = railway_token or os.getenv('RAILWAY_TOKEN')
        if not self.token:
            raise ValueError("Railway token required. Set RAILWAY_TOKEN env var or pass to constructor")
        
        self.api_base = "https://backboard.railway.app/graphql/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def deploy_crewai_system(self, 
                           generated_code: Dict[str, str],
                           project_name: str,
                           user_api_keys: Dict[str, str],
                           requirements: str) -> Dict[str, Any]:
        """
        Deploy a complete CrewAI system to Railway
        
        Args:
            generated_code: Dict with 'main.py', 'requirements.txt', etc
            project_name: Name for the Railway project
            user_api_keys: User's API keys (OpenAI, etc)
            requirements: Original business requirements
            
        Returns:
            Deployment info including URLs and status
        """
        
        print(f"\n🚀 Starting Railway deployment for: {project_name}")
        
        try:
            # Create temporary directory for deployment
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Write generated files
                self._prepare_deployment_files(temp_path, generated_code, user_api_keys)
                
                # Initialize git repo (Railway needs this)
                self._init_git_repo(temp_path)
                
                # Create Railway project
                print("📦 Creating Railway project...")
                project_id = self._create_railway_project(project_name)
                print(f"✅ Project created: {project_id}")
                
                # Deploy to Railway
                print("🚂 Deploying code to Railway...")
                deployment_info = self._deploy_to_railway(temp_path, project_id)
                print(f"✅ Deployment initiated: {deployment_info['deployment_id']}")
                
                # Set environment variables
                print("🔐 Setting environment variables...")
                self._set_environment_variables(project_id, user_api_keys)
                print("✅ Environment variables configured")
                
                # Get deployment URL
                print("🌐 Retrieving deployment URL...")
                deployment_url = self._get_deployment_url(project_id)
                print(f"✅ Deployment URL: {deployment_url}")
                
                return {
                    "success": True,
                    "project_id": project_id,
                    "deployment_url": deployment_url,
                    "dashboard_url": f"https://railway.app/project/{project_id}",
                    "status": "deploying",
                    "created_at": datetime.now().isoformat(),
                    "project_name": project_name,
                    "requirements": requirements
                }
                
        except Exception as e:
            print(f"❌ Railway deployment failed: {type(e).__name__} - {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _prepare_deployment_files(self, temp_path: Path, generated_code: Dict[str, str], api_keys: Dict[str, str]):
        """Prepare files for Railway deployment"""
        
        # Write main.py
        (temp_path / "main.py").write_text(generated_code.get('main.py', ''))
        
        # Write requirements.txt with Railway-specific additions
        requirements = generated_code.get('requirements.txt', '')
        # Add Railway-specific requirements
        requirements += "\n# Railway deployment requirements\n"
        requirements += "gunicorn==21.2.0\n"
        requirements += "python-dotenv==1.0.0\n"
        
        (temp_path / "requirements.txt").write_text(requirements)
        
        # Create Railway.json for configuration
        railway_config = {
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "python main.py",
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 3
            }
        }
        (temp_path / "railway.json").write_text(json.dumps(railway_config, indent=2))
        
        # Create .env.example (Railway will use this as template)
        env_example = "\n".join([f"{key}=your_{key.lower()}_here" for key in api_keys.keys()])
        (temp_path / ".env.example").write_text(env_example)
        
        # Create a simple health check endpoint if not present
        if "health" not in generated_code.get('main.py', ''):
            health_check = """
# Health check endpoint for Railway
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy", "agent": "crewai-system"}

# Add this to your existing code if using FastAPI
"""
            (temp_path / "health_check.py").write_text(health_check)
    
    def _init_git_repo(self, path: Path):
        """Initialize git repository for Railway deployment"""
        os.chdir(path)
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial CrewAI system deployment"], check=True, capture_output=True)
    
    def _create_railway_project(self, name: str) -> str:
        """Create a new Railway project"""
        
        # Railway GraphQL mutation to create project
        mutation = """
        mutation CreateProject($name: String!) {
            projectCreate(input: { name: $name }) {
                id
                name
            }
        }
        """
        
        response = requests.post(
            self.api_base,
            headers=self.headers,
            json={
                "query": mutation,
                "variables": {"name": name}
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to create Railway project: {response.text}")
        
        data = response.json()
        return data['data']['projectCreate']['id']
    
    def _deploy_to_railway(self, path: Path, project_id: str) -> Dict[str, str]:
        """Deploy code to Railway project"""
        
        try:
            # Create a service in the project
            service_id = self._create_service(project_id)
            
            # Create deployment from directory
            deployment_id = self._create_deployment_from_directory(
                project_id=project_id,
                service_id=service_id,
                directory_path=path
            )
            
            return {
                "deployment_id": deployment_id,
                "service_id": service_id,
                "status": "deploying"
            }
            
        except Exception as e:
            print(f"Railway deployment error: {e}")
            raise Exception(f"Failed to deploy to Railway: {str(e)}")
    
    def _set_environment_variables(self, project_id: str, env_vars: Dict[str, str]):
        """Set environment variables in Railway project"""
        
        mutation = """
        mutation SetEnvVars($projectId: String!, $vars: JSON!) {
            variableCollectionUpsert(input: {
                projectId: $projectId,
                variables: $vars
            }) {
                id
            }
        }
        """
        
        response = requests.post(
            self.api_base,
            headers=self.headers,
            json={
                "query": mutation,
                "variables": {
                    "projectId": project_id,
                    "vars": env_vars
                }
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to set environment variables: {response.text}")
    
    def _create_service(self, project_id: str) -> str:
        """Create a new service in the Railway project"""
        
        mutation = """
        mutation CreateService($projectId: String!) {
            serviceCreate(input: { projectId: $projectId }) {
                id
            }
        }
        """
        
        response = requests.post(
            self.api_base,
            headers=self.headers,
            json={
                "query": mutation,
                "variables": {"projectId": project_id}
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to create service: {response.text}")
        
        data = response.json()
        if 'errors' in data:
            raise Exception(f"GraphQL error: {data['errors']}")
            
        return data['data']['serviceCreate']['id']
    
    def _create_deployment_from_directory(self, project_id: str, service_id: str, directory_path: Path) -> str:
        """Create a deployment from a local directory"""
        
        # Railway expects a tarball of the directory
        import tarfile
        import io
        import base64
        
        # Create in-memory tarball
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    arcname = str(file_path.relative_to(directory_path))
                    tar.add(str(file_path), arcname=arcname)
        
        tar_buffer.seek(0)
        tar_content = tar_buffer.read()
        
        # Upload the deployment
        mutation = """
        mutation CreateDeployment($serviceId: String!, $source: DeploymentSourceInput!) {
            deploymentCreate(input: {
                serviceId: $serviceId,
                source: $source
            }) {
                id
                status
            }
        }
        """
        
        response = requests.post(
            self.api_base,
            headers=self.headers,
            json={
                "query": mutation,
                "variables": {
                    "serviceId": service_id,
                    "source": {
                        "type": "TARBALL",
                        "tarball": base64.b64encode(tar_content).decode('utf-8')
                    }
                }
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to create deployment: {response.text}")
        
        data = response.json()
        if 'errors' in data:
            raise Exception(f"GraphQL error: {data['errors']}")
            
        return data['data']['deploymentCreate']['id']
    
    def _get_deployment_url(self, project_id: str) -> str:
        """Get the deployment URL for the project"""
        
        # Query for the service domain
        query = """
        query GetProjectDomains($projectId: String!) {
            project(id: $projectId) {
                services {
                    edges {
                        node {
                            id
                            domains {
                                serviceDomains {
                                    domain
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        response = requests.post(
            self.api_base,
            headers=self.headers,
            json={
                "query": query,
                "variables": {"projectId": project_id}
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            try:
                services = data['data']['project']['services']['edges']
                if services and len(services) > 0:
                    domains = services[0]['node']['domains']['serviceDomains']
                    if domains and len(domains) > 0:
                        return f"https://{domains[0]['domain']}"
            except (KeyError, IndexError):
                pass
        
        # Fallback to generated URL
        return f"https://crewai-{project_id[:8]}.up.railway.app"


class RailwayDeploymentManager:
    """Manages Railway deployments for CrewBuilder users"""
    
    def __init__(self):
        # Use shared Railway project deployment
        try:
            from .shared_railway_deployer import SharedRailwayDeployer
            self.deployer = SharedRailwayDeployer()
            self.use_shared = True
            print("🏭 Using shared Railway project for client deployments")
        except Exception as e:
            print(f"⚠️  Shared deployment not available: {e}")
            # Fallback to individual project deployment
            self.deployer = RailwayDeployer()
            self.use_shared = False
            
        self.deployments_file = Path("deployments.json")
        self.deployments = self._load_deployments()
    
    def _load_deployments(self) -> Dict[str, Any]:
        """Load existing deployments from file"""
        if self.deployments_file.exists():
            return json.loads(self.deployments_file.read_text())
        return {}
    
    def _save_deployments(self):
        """Save deployments to file"""
        self.deployments_file.write_text(json.dumps(self.deployments, indent=2))
    
    def create_deployment(self, user_id: str, generated_system: Dict[str, Any], api_keys: Dict[str, str]) -> Dict[str, Any]:
        """Create a new deployment for a user"""
        
        # Generate project name
        project_name = f"crewai-{user_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Prepare generated code
        generated_code = {
            'main.py': generated_system.get('code', ''),
            'requirements.txt': generated_system.get('requirements', '')
        }
        
        # Generate client dashboard if available
        dashboard_files = {}
        try:
            from agents.dashboard_generator import generate_client_dashboard
            dashboard_code = generate_client_dashboard(
                client_name=project_name,
                agent_system_info={
                    'requirements': generated_system.get('original_requirements', ''),
                    'agents': []  # TODO: Extract agent info from generated code
                }
            )
            
            # Convert dashboard code to dict format
            dashboard_files = {
                'app.py': dashboard_code.app_py,
                'requirements.txt': dashboard_code.requirements_txt,
                'templates/index.html': dashboard_code.templates_index,
                'templates/setup.html': dashboard_code.templates_setup,
                'templates/status.html': dashboard_code.templates_status,
                'static/style.css': dashboard_code.static_style_css
            }
        except ImportError:
            print("Warning: Dashboard generator not available")
        
        # Deploy using appropriate method
        if self.use_shared and hasattr(self.deployer, 'deploy_client_system'):
            # Use shared Railway project deployment
            deployment = self.deployer.deploy_client_system(
                client_id=user_id,
                generated_code=generated_code,
                dashboard_code=dashboard_files,
                client_name=project_name,
                api_keys=api_keys
            )
        else:
            # Use individual project deployment
            deployment = self.deployer.deploy_crewai_system(
                generated_code=generated_code,
                project_name=project_name,
                user_api_keys=api_keys,
                requirements=generated_system.get('original_requirements', '')
            )
        
        # Store deployment info
        if deployment['success']:
            self.deployments[deployment['project_id']] = {
                'user_id': user_id,
                'deployment': deployment,
                'created_at': datetime.now().isoformat()
            }
            self._save_deployments()
        
        return deployment
    
    def get_user_deployments(self, user_id: str) -> list:
        """Get all deployments for a user"""
        return [
            d['deployment'] 
            for d in self.deployments.values() 
            if d['user_id'] == user_id
        ]
    
    def get_deployment_status(self, project_id: str) -> Dict[str, Any]:
        """Get current status of a deployment"""
        # In production, this would query Railway API
        if project_id in self.deployments:
            return {
                "status": "running",
                "health": "healthy",
                "last_check": datetime.now().isoformat()
            }
        return {"status": "not_found"}