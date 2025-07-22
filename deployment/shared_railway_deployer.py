"""
Shared Railway Project Deployer
Deploys client systems as services within a shared Railway project
"""

import os
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import uuid
import requests
from datetime import datetime

class SharedRailwayDeployer:
    """Deploys client systems as services in a shared Railway project"""
    
    def __init__(self, railway_token: Optional[str] = None, shared_project_id: Optional[str] = None):
        self.token = railway_token or os.getenv('RAILWAY_TOKEN')
        if not self.token:
            raise ValueError("Railway token required. Set RAILWAY_TOKEN env var")
        
        # Use existing shared project or create one
        self.shared_project_id = shared_project_id or os.getenv('CREWBUILDER_SHARED_PROJECT_ID')
        
        self.api_base = "https://backboard.railway.app/graphql/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Initialize shared project if needed
        if not self.shared_project_id:
            self.shared_project_id = self._initialize_shared_project()
    
    def _initialize_shared_project(self) -> str:
        """Create or find the shared Railway project for all client deployments"""
        
        print("🚂 Initializing shared Railway project...")
        
        # First, try to find existing project
        query = """
        query GetProjects {
            me {
                projects {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        
        response = requests.post(
            self.api_base,
            headers=self.headers,
            json={"query": query}
        )
        
        if response.status_code == 200:
            data = response.json()
            projects = data.get('data', {}).get('me', {}).get('projects', {}).get('edges', [])
            
            # Look for existing shared project
            for project in projects:
                if project['node']['name'] == 'CrewBuilder-Client-Systems':
                    print(f"✅ Found existing shared project: {project['node']['id']}")
                    return project['node']['id']
        
        # Create new shared project
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
                "variables": {"name": "CrewBuilder-Client-Systems"}
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to create shared project: {response.text}")
        
        data = response.json()
        project_id = data['data']['projectCreate']['id']
        print(f"✅ Created shared project: {project_id}")
        
        # Save for future use
        print("💡 Set CREWBUILDER_SHARED_PROJECT_ID in your .env file to reuse this project")
        
        return project_id
    
    def deploy_client_system(self,
                           client_id: str,
                           generated_code: Dict[str, str],
                           dashboard_code: Dict[str, str],
                           client_name: str,
                           api_keys: Dict[str, str]) -> Dict[str, Any]:
        """
        Deploy a client system as a service in the shared project
        
        Args:
            client_id: Unique identifier for the client
            generated_code: The AI agent system code
            dashboard_code: Client dashboard code
            client_name: Human-readable name for the client
            api_keys: Client's API keys for their agents
        """
        
        try:
            print(f"\n🚀 Deploying client system: {client_name}")
            
            # Create service for this client
            service_name = f"client-{client_id}-{client_name.lower().replace(' ', '-')}"[:50]
            print(f"📦 Creating service: {service_name}")
            
            service_id = self._create_service(self.shared_project_id, service_name)
            print(f"✅ Service created: {service_id}")
            
            # Prepare deployment files
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Write agent system files
                (temp_path / "agent_system").mkdir()
                for filename, content in generated_code.items():
                    (temp_path / "agent_system" / filename).write_text(content)
                
                # Write dashboard files
                (temp_path / "dashboard").mkdir()
                for filename, content in dashboard_code.items():
                    (temp_path / "dashboard" / filename).write_text(content)
                
                # Create unified entry point
                self._create_unified_entry(temp_path, client_id)
                
                # Create requirements.txt combining both
                self._merge_requirements(temp_path, generated_code, dashboard_code)
                
                # Deploy to Railway
                print("🚂 Deploying to Railway...")
                deployment_id = self._deploy_service(service_id, temp_path)
                print(f"✅ Deployment initiated: {deployment_id}")
            
            # Set environment variables
            print("🔐 Setting environment variables...")
            env_vars = {
                **api_keys,
                "CLIENT_ID": client_id,
                "CLIENT_NAME": client_name,
                "PORT": "3000"
            }
            self._set_service_variables(self.shared_project_id, service_id, env_vars)
            print("✅ Environment variables set")
            
            # Get service URL
            print("🌐 Retrieving service URL...")
            service_url = self._get_service_url(service_id)
            print(f"✅ Service URL: {service_url}")
            
            return {
                "success": True,
                "client_id": client_id,
                "service_id": service_id,
                "deployment_id": deployment_id,
                "dashboard_url": service_url,
                "api_endpoint": f"{service_url}/api",
                "railway_dashboard": f"https://railway.app/project/{self.shared_project_id}/service/{service_id}",
                "status": "deploying",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Deployment failed: {type(e).__name__} - {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _create_service(self, project_id: str, service_name: str) -> str:
        """Create a new service in the project"""
        
        mutation = """
        mutation CreateService($projectId: String!, $name: String!) {
            serviceCreate(input: {
                projectId: $projectId,
                name: $name
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
                    "name": service_name
                }
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to create service: {response.text}")
        
        data = response.json()
        if 'errors' in data:
            raise Exception(f"GraphQL error: {data['errors']}")
            
        return data['data']['serviceCreate']['id']
    
    def _create_unified_entry(self, path: Path, client_id: str):
        """Create a unified entry point that runs both dashboard and agents"""
        
        entry_code = '''#!/usr/bin/env python3
"""
Unified entry point for client system
Runs both the dashboard and agent system
"""

import os
import sys
import subprocess
import threading
import time

def run_agent_system():
    """Run the AI agent system"""
    print("🤖 Starting AI agent system...")
    os.chdir("agent_system")
    subprocess.run([sys.executable, "main.py"])

def run_dashboard():
    """Run the client dashboard"""
    print("🎯 Starting client dashboard...")
    os.chdir("dashboard")
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    print(f"🚀 Starting client system for: {os.getenv('CLIENT_NAME', 'Unknown')}")
    
    # Start agent system in background thread
    agent_thread = threading.Thread(target=run_agent_system)
    agent_thread.daemon = True
    agent_thread.start()
    
    # Give agents time to initialize
    time.sleep(5)
    
    # Run dashboard in main thread
    run_dashboard()
'''
        
        (path / "main.py").write_text(entry_code)
    
    def _merge_requirements(self, path: Path, agent_code: Dict[str, str], dashboard_code: Dict[str, str]):
        """Merge requirements from both agent system and dashboard"""
        
        agent_reqs = agent_code.get('requirements.txt', '').split('\n')
        dashboard_reqs = dashboard_code.get('requirements.txt', '').split('\n')
        
        # Combine and deduplicate
        all_reqs = set(agent_reqs + dashboard_reqs + [
            'gunicorn==21.2.0',
            'uvicorn==0.24.0',
            'python-multipart==0.0.6'
        ])
        
        # Remove empty strings
        all_reqs.discard('')
        
        (path / "requirements.txt").write_text('\n'.join(sorted(all_reqs)))
    
    def _deploy_service(self, service_id: str, directory_path: Path) -> str:
        """Deploy code to a Railway service"""
        
        # This would use the same deployment method as before
        # For now, returning placeholder
        import tarfile
        import io
        import base64
        
        # Create tarball of directory
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    arcname = str(file_path.relative_to(directory_path))
                    tar.add(str(file_path), arcname=arcname)
        
        tar_buffer.seek(0)
        
        # In production, this would upload to Railway
        # For MVP, we'll need Railway CLI or GitHub integration
        
        return f"deploy_{uuid.uuid4().hex[:8]}"
    
    def _set_service_variables(self, project_id: str, service_id: str, variables: Dict[str, str]):
        """Set environment variables for a service"""
        
        mutation = """
        mutation SetServiceVariables($projectId: String!, $serviceId: String!, $variables: JSON!) {
            variableCollectionUpsert(input: {
                projectId: $projectId,
                serviceId: $serviceId,
                variables: $variables
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
                    "serviceId": service_id,
                    "variables": variables
                }
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to set variables: {response.text}")
    
    def _get_service_url(self, service_id: str) -> str:
        """Get the public URL for a service"""
        
        # Railway generates automatic domains
        # In production, query the actual domain
        return f"https://{service_id[:8]}-crewbuilder.up.railway.app"
    
    def list_client_deployments(self) -> Dict[str, Any]:
        """List all client deployments in the shared project"""
        
        query = """
        query GetProjectServices($projectId: String!) {
            project(id: $projectId) {
                services {
                    edges {
                        node {
                            id
                            name
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
                "variables": {"projectId": self.shared_project_id}
            }
        )
        
        if response.status_code != 200:
            return {"success": False, "error": "Failed to list services"}
        
        data = response.json()
        services = []
        
        try:
            for edge in data['data']['project']['services']['edges']:
                service = edge['node']
                domains = service.get('domains', {}).get('serviceDomains', [])
                
                services.append({
                    "service_id": service['id'],
                    "name": service['name'],
                    "url": f"https://{domains[0]['domain']}" if domains else None
                })
        except KeyError:
            pass
        
        return {
            "success": True,
            "project_id": self.shared_project_id,
            "services": services,
            "count": len(services)
        }