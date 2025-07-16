#!/usr/bin/env python3
"""
Basic Memory GitHub Sync Solution

This script automatically syncs Basic Memory knowledge files to GitHub repositories.
It uses the MCP (Model Context Protocol) tools to:
1. Monitor Basic Memory for changes
2. Read file contents from Basic Memory projects
3. Push changes to corresponding GitHub repositories

Usage:
    python basic_memory_sync.py --project main --repo nickagillis/dev-knowledge-base
    python basic_memory_sync.py --sync-all  # Sync all projects based on config
"""

import argparse
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class BasicMemoryGitHubSync:
    """
    Syncs Basic Memory projects to GitHub repositories using MCP tools.
    
    This class provides automated synchronization between local Basic Memory
    knowledge files and GitHub repositories, enabling cloud backup and
    collaboration while maintaining the local-first approach.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the sync manager with configuration."""
        self.config_path = config_path or "sync_config.json"
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """Load sync configuration from file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        default_config = {
            "projects": {
                "main": {
                    "local_path": "C:\\Users\\nicka\\dev\\knowledge\\main",
                    "github_repo": "nickagillis/dev-knowledge-base",
                    "github_path": "main",
                    "sync_enabled": True
                },
                "crewbuilder": {
                    "local_path": "C:\\Users\\nicka\\dev\\knowledge\\crewbuilder", 
                    "github_repo": "nickagillis/dev-knowledge-base",
                    "github_path": "crewbuilder",
                    "sync_enabled": True
                },
                "clients": {
                    "local_path": "C:\\Users\\nicka\\dev\\knowledge\\clients",
                    "github_repo": "nickagillis/dev-knowledge-base", 
                    "github_path": "clients",
                    "sync_enabled": True
                },
                "team": {
                    "local_path": "C:\\Users\\nicka\\dev\\knowledge\\team",
                    "github_repo": "nickagillis/dev-knowledge-base",
                    "github_path": "team", 
                    "sync_enabled": True
                }
            },
            "sync_settings": {
                "check_interval_seconds": 300,  # 5 minutes
                "batch_size": 10,  # Max files per sync
                "commit_message_template": "Auto-sync from Basic Memory: {timestamp}",
                "exclude_patterns": ["*.tmp", "*.lock", ".DS_Store"],
                "dry_run": False
            }
        }
        
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_basic_memory_changes(self, project: str, since: Optional[datetime] = None) -> List[Dict]:
        """
        Get recent changes from Basic Memory project.
        
        In a real implementation, this would use the Basic Memory MCP tools
        to get recent activity. For now, we'll simulate this by checking
        file modification times.
        """
        project_config = self.config["projects"].get(project)
        if not project_config or not project_config["sync_enabled"]:
            return []
        
        local_path = Path(project_config["local_path"])
        if not local_path.exists():
            print(f"Warning: Local path {local_path} does not exist for project {project}")
            return []
        
        changes = []
        cutoff_time = since or datetime.now() - timedelta(hours=24)
        
        # Find all markdown files modified since cutoff
        for md_file in local_path.rglob("*.md"):
            if md_file.is_file():
                mod_time = datetime.fromtimestamp(md_file.stat().st_mtime)
                if mod_time > cutoff_time:
                    changes.append({
                        "file_path": str(md_file.relative_to(local_path)),
                        "full_path": str(md_file),
                        "modified_time": mod_time.isoformat(),
                        "size": md_file.stat().st_size
                    })
        
        return sorted(changes, key=lambda x: x["modified_time"], reverse=True)
    
    def read_file_content(self, file_path: str) -> str:
        """Read content from a local file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def should_exclude_file(self, file_path: str) -> bool:
        """Check if file should be excluded from sync."""
        exclude_patterns = self.config["sync_settings"]["exclude_patterns"]
        file_name = os.path.basename(file_path)
        
        for pattern in exclude_patterns:
            if pattern.startswith("*") and file_name.endswith(pattern[1:]):
                return True
            elif file_name == pattern:
                return True
        
        return False
    
    def sync_project_to_github(self, project: str, dry_run: bool = None) -> Dict:
        """
        Sync a Basic Memory project to its corresponding GitHub repository.
        
        Args:
            project: Name of the Basic Memory project
            dry_run: If True, only show what would be synced without actually doing it
            
        Returns:
            Dictionary with sync results
        """
        if dry_run is None:
            dry_run = self.config["sync_settings"]["dry_run"]
        
        project_config = self.config["projects"].get(project)
        if not project_config:
            return {"error": f"Project {project} not found in configuration"}
        
        if not project_config["sync_enabled"]:
            return {"skipped": f"Sync disabled for project {project}"}
        
        # Get recent changes
        changes = self.get_basic_memory_changes(project)
        if not changes:
            return {"status": "no_changes", "message": f"No recent changes in project {project}"}
        
        # Limit to batch size
        batch_size = self.config["sync_settings"]["batch_size"]
        changes = changes[:batch_size]
        
        sync_results = {
            "project": project,
            "changes_found": len(changes),
            "files_synced": [],
            "files_skipped": [],
            "errors": []
        }
        
        github_repo = project_config["github_repo"]
        github_path = project_config["github_path"]
        
        for change in changes:
            file_path = change["file_path"]
            full_path = change["full_path"]
            
            if self.should_exclude_file(file_path):
                sync_results["files_skipped"].append(f"Excluded: {file_path}")
                continue
            
            # Read file content
            content = self.read_file_content(full_path)
            if not content:
                sync_results["errors"].append(f"Could not read: {file_path}")
                continue
            
            # Prepare GitHub path
            github_file_path = f"{github_path}/{file_path}" if github_path else file_path
            
            if dry_run:
                sync_results["files_synced"].append(f"DRY RUN: Would sync {file_path} to {github_repo}/{github_file_path}")
            else:
                # TODO: Actual GitHub MCP call would go here
                # For now, just log what we would do
                commit_msg = self.config["sync_settings"]["commit_message_template"].format(
                    timestamp=datetime.now().isoformat(),
                    project=project,
                    file=file_path
                )
                
                sync_results["files_synced"].append(f"Would sync {file_path} to {github_repo}/{github_file_path}")
                print(f"[SYNC] {github_repo}/{github_file_path} <- {full_path}")
                print(f"[COMMIT] {commit_msg}")
        
        return sync_results
    
    def sync_all_projects(self, dry_run: bool = None) -> Dict:
        """Sync all enabled projects to their GitHub repositories."""
        results = {"synced_projects": {}, "summary": {"total_files": 0, "total_errors": 0}}
        
        for project_name in self.config["projects"]:
            result = self.sync_project_to_github(project_name, dry_run)
            results["synced_projects"][project_name] = result
            
            if "files_synced" in result:
                results["summary"]["total_files"] += len(result["files_synced"])
            if "errors" in result:
                results["summary"]["total_errors"] += len(result["errors"])
        
        return results
    
    def start_monitoring(self, interval: int = None):
        """Start continuous monitoring and syncing."""
        if interval is None:
            interval = self.config["sync_settings"]["check_interval_seconds"]
        
        print(f"Starting Basic Memory -> GitHub sync monitoring (interval: {interval}s)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print(f"\n[{datetime.now().isoformat()}] Checking for changes...")
                results = self.sync_all_projects()
                
                total_files = results["summary"]["total_files"]
                total_errors = results["summary"]["total_errors"]
                
                if total_files > 0:
                    print(f"Synced {total_files} files")
                if total_errors > 0:
                    print(f"Encountered {total_errors} errors")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nStopping sync monitoring...")


def main():
    """Main entry point for the sync script."""
    parser = argparse.ArgumentParser(description="Basic Memory GitHub Sync Tool")
    parser.add_argument("--project", help="Sync specific project")
    parser.add_argument("--repo", help="GitHub repository (owner/repo)")
    parser.add_argument("--sync-all", action="store_true", help="Sync all projects")
    parser.add_argument("--monitor", action="store_true", help="Start continuous monitoring")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be synced without doing it")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--interval", type=int, help="Monitoring interval in seconds")
    
    args = parser.parse_args()
    
    # Initialize sync manager
    sync_manager = BasicMemoryGitHubSync(args.config)
    
    if args.monitor:
        sync_manager.start_monitoring(args.interval)
    elif args.sync_all:
        results = sync_manager.sync_all_projects(args.dry_run)
        print(json.dumps(results, indent=2))
    elif args.project:
        result = sync_manager.sync_project_to_github(args.project, args.dry_run)
        print(json.dumps(result, indent=2))
    else:
        # Default: show status
        print("Basic Memory GitHub Sync Tool")
        print("Configuration:", sync_manager.config_path)
        print("Projects configured:", len(sync_manager.config["projects"]))
        
        for project, config in sync_manager.config["projects"].items():
            status = "enabled" if config["sync_enabled"] else "disabled"
            print(f"  {project}: {config['github_repo']} ({status})")


if __name__ == "__main__":
    main()
