"""
Railway GitHub Integration Deployment Module
Uses Railway's GitHub integration for deployments
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
import base64

class RailwayGitHubDeployer:
    """Handles deployment using Railway's GitHub integration"""
    
    def __init__(self, github_token: Optional[str] = None, railway_token: Optional[str] = None):
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.railway_token = railway_token or os.getenv('RAILWAY_TOKEN')
        
        if not self.railway_token:
            raise ValueError("Railway token required. Set RAILWAY_TOKEN env var")
            
        self.railway_api = "https://backboard.railway.app/graphql/v2"
        self.github_api = "https://api.github.com"
        
        self.railway_headers = {
            "Authorization": f"Bearer {self.railway_token}",
            "Content-Type": "application/json"
        }
        
        self.github_headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.github_token else {}
    
    def deploy_via_github(self,
                         generated_code: Dict[str, str],
                         project_name: str,
                         user_api_keys: Dict[str, str],
                         github_repo: str,
                         branch: str = "main") -> Dict[str, Any]:
        """
        Deploy by creating a GitHub repo and connecting it to Railway
        
        Args:
            generated_code: Generated system code
            project_name: Name for the deployment
            user_api_keys: API keys to set as env vars
            github_repo: GitHub repo in format "owner/repo"
            branch: Branch to deploy from
        """
        
        try:
            print(f"\n🚀 Starting Railway deployment via GitHub integration")
            
            # Create Railway project
            print("📦 Creating Railway project...")
            project_id = self._create_railway_project(project_name)
            print(f"✅ Project created: {project_id}")
            
            # Connect to GitHub repo
            print(f"🔗 Connecting to GitHub repo: {github_repo}")
            service_id = self._connect_github_repo(project_id, github_repo, branch)
            print(f"✅ Connected to GitHub, service created: {service_id}")
            
            # Set environment variables
            print("🔐 Setting environment variables...")
            self._set_service_variables(project_id, service_id, user_api_keys)
            print("✅ Environment variables configured")
            
            # Create deployment branch with generated code
            if self.github_token:
                print(f"📝 Pushing generated code to {github_repo}/{branch}")
                self._push_code_to_github(github_repo, branch, generated_code)
                print("✅ Code pushed to GitHub")
            else:
                print("⚠️  No GitHub token provided - you'll need to push code manually")
            
            # Trigger deployment
            print("🚂 Triggering Railway deployment...")
            deployment_id = self._trigger_deployment(service_id)
            print(f"✅ Deployment triggered: {deployment_id}")
            
            # Get deployment URL
            print("🌐 Retrieving deployment URL...")
            deployment_url = self._get_service_url(project_id, service_id)
            print(f"✅ Deployment URL: {deployment_url}")
            
            return {
                "success": True,
                "project_id": project_id,
                "service_id": service_id,
                "deployment_id": deployment_id,
                "deployment_url": deployment_url,
                "dashboard_url": f"https://railway.app/project/{project_id}",
                "github_repo": github_repo,
                "branch": branch,
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
    
    def _create_railway_project(self, name: str) -> str:
        """Create a new Railway project"""
        
        mutation = """
        mutation CreateProject($name: String!) {
            projectCreate(input: { name: $name }) {
                id
                name
            }
        }
        """
        
        response = requests.post(
            self.railway_api,
            headers=self.railway_headers,
            json={
                "query": mutation,
                "variables": {"name": name}
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to create project: {response.text}")
        
        data = response.json()
        if 'errors' in data:
            raise Exception(f"GraphQL error: {data['errors']}")
            
        return data['data']['projectCreate']['id']
    
    def _connect_github_repo(self, project_id: str, github_repo: str, branch: str) -> str:
        """Connect a GitHub repo to Railway project"""
        
        mutation = """
        mutation ConnectGitHubRepo($projectId: String!, $repo: String!, $branch: String!) {
            serviceCreate(input: {
                projectId: $projectId,
                source: {
                    repo: $repo,
                    branch: $branch
                }
            }) {
                id
            }
        }
        """
        
        response = requests.post(
            self.railway_api,
            headers=self.railway_headers,
            json={
                "query": mutation,
                "variables": {
                    "projectId": project_id,
                    "repo": github_repo,
                    "branch": branch
                }
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to connect GitHub repo: {response.text}")
        
        data = response.json()
        if 'errors' in data:
            raise Exception(f"GraphQL error: {data['errors']}")
            
        return data['data']['serviceCreate']['id']
    
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
            self.railway_api,
            headers=self.railway_headers,
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
    
    def _push_code_to_github(self, repo: str, branch: str, code_files: Dict[str, str]):
        """Push generated code to GitHub repo"""
        
        if not self.github_token:
            raise Exception("GitHub token required for pushing code")
        
        owner, repo_name = repo.split('/')
        
        # Get current commit SHA for the branch
        branch_url = f"{self.github_api}/repos/{owner}/{repo_name}/git/refs/heads/{branch}"
        response = requests.get(branch_url, headers=self.github_headers)
        
        if response.status_code == 200:
            current_sha = response.json()['object']['sha']
        else:
            # Branch doesn't exist, get default branch
            repo_url = f"{self.github_api}/repos/{owner}/{repo_name}"
            repo_response = requests.get(repo_url, headers=self.github_headers)
            if repo_response.status_code != 200:
                raise Exception(f"Failed to access repo: {repo_response.text}")
            
            default_branch = repo_response.json()['default_branch']
            default_ref_url = f"{self.github_api}/repos/{owner}/{repo_name}/git/refs/heads/{default_branch}"
            default_response = requests.get(default_ref_url, headers=self.github_headers)
            if default_response.status_code != 200:
                raise Exception(f"Failed to get default branch: {default_response.text}")
            
            current_sha = default_response.json()['object']['sha']
        
        # Create blobs for each file
        tree_items = []
        for filename, content in code_files.items():
            blob_response = requests.post(
                f"{self.github_api}/repos/{owner}/{repo_name}/git/blobs",
                headers=self.github_headers,
                json={
                    "content": content,
                    "encoding": "utf-8"
                }
            )
            
            if blob_response.status_code != 201:
                raise Exception(f"Failed to create blob for {filename}: {blob_response.text}")
            
            tree_items.append({
                "path": filename,
                "mode": "100644",
                "type": "blob",
                "sha": blob_response.json()['sha']
            })
        
        # Create tree
        tree_response = requests.post(
            f"{self.github_api}/repos/{owner}/{repo_name}/git/trees",
            headers=self.github_headers,
            json={
                "base_tree": current_sha,
                "tree": tree_items
            }
        )
        
        if tree_response.status_code != 201:
            raise Exception(f"Failed to create tree: {tree_response.text}")
        
        tree_sha = tree_response.json()['sha']
        
        # Create commit
        commit_response = requests.post(
            f"{self.github_api}/repos/{owner}/{repo_name}/git/commits",
            headers=self.github_headers,
            json={
                "message": "Deploy CrewAI system via CrewBuilder",
                "tree": tree_sha,
                "parents": [current_sha]
            }
        )
        
        if commit_response.status_code != 201:
            raise Exception(f"Failed to create commit: {commit_response.text}")
        
        commit_sha = commit_response.json()['sha']
        
        # Update branch reference
        ref_update_response = requests.patch(
            f"{self.github_api}/repos/{owner}/{repo_name}/git/refs/heads/{branch}",
            headers=self.github_headers,
            json={"sha": commit_sha}
        )
        
        if ref_update_response.status_code not in [200, 201]:
            # Try to create the branch if it doesn't exist
            create_ref_response = requests.post(
                f"{self.github_api}/repos/{owner}/{repo_name}/git/refs",
                headers=self.github_headers,
                json={
                    "ref": f"refs/heads/{branch}",
                    "sha": commit_sha
                }
            )
            
            if create_ref_response.status_code != 201:
                raise Exception(f"Failed to update/create branch: {ref_update_response.text}")
    
    def _trigger_deployment(self, service_id: str) -> str:
        """Trigger a deployment for the service"""
        
        mutation = """
        mutation TriggerDeployment($serviceId: String!) {
            deploymentTrigger(input: { serviceId: $serviceId }) {
                id
                status
            }
        }
        """
        
        response = requests.post(
            self.railway_api,
            headers=self.railway_headers,
            json={
                "query": mutation,
                "variables": {"serviceId": service_id}
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to trigger deployment: {response.text}")
        
        data = response.json()
        if 'errors' in data:
            raise Exception(f"GraphQL error: {data['errors']}")
            
        return data['data']['deploymentTrigger']['id']
    
    def _get_service_url(self, project_id: str, service_id: str) -> str:
        """Get the deployment URL for a service"""
        
        query = """
        query GetServiceDomain($projectId: String!, $serviceId: String!) {
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
            self.railway_api,
            headers=self.railway_headers,
            json={
                "query": query,
                "variables": {
                    "projectId": project_id,
                    "serviceId": service_id
                }
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            try:
                services = data['data']['project']['services']['edges']
                for service in services:
                    if service['node']['id'] == service_id:
                        domains = service['node']['domains']['serviceDomains']
                        if domains and len(domains) > 0:
                            return f"https://{domains[0]['domain']}"
            except (KeyError, IndexError):
                pass
        
        # Fallback
        return f"https://crewai-{service_id[:8]}.up.railway.app"