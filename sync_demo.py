#!/usr/bin/env python3
"""
Basic Memory GitHub Sync Demo

This demo script shows how to use MCP tools to sync Basic Memory content to GitHub.
It demonstrates the actual integration between Basic Memory and GitHub MCP servers.

Usage:
    python sync_demo.py
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List


class MCPSyncDemo:
    """
    Demo of Basic Memory -> GitHub sync using actual MCP tools.
    
    This would integrate with Claude's MCP tools in a real implementation.
    For now, it shows the concepts and workflow.
    """
    
    def __init__(self):
        self.github_repo = "nickagillis/dev-knowledge-base"
        self.sync_stats = {
            "files_checked": 0,
            "files_synced": 0,
            "errors": []
        }
    
    async def get_basic_memory_recent_activity(self, timeframe: str = "7d") -> Dict:
        """
        Get recent activity from Basic Memory.
        
        In a real implementation, this would call:
        basic_memory.recent_activity(timeframe=timeframe)
        """
        print(f" Checking Basic Memory recent activity (last {timeframe})")
        
        # Simulated response matching the actual Basic Memory MCP format
        return {
            "results": [
                {
                    "primary_result": {
                        "type": "entity",
                        "permalink": "main-git-hooks-implementation-commands", 
                        "title": "Git Hooks Implementation Commands",
                        "file_path": "main\\Git Hooks Implementation Commands.md",
                        "created_at": "2025-07-15T15:16:32.966658"
                    }
                },
                {
                    "primary_result": {
                        "type": "entity",
                        "permalink": "main-git-automation-implementation",
                        "title": "Git Automation Implementation", 
                        "file_path": "main\\Git Automation Implementation.md",
                        "created_at": "2025-07-15T15:16:06.452013"
                    }
                }
            ],
            "metadata": {
                "total_results": 2,
                "timeframe": "2025-07-08T15:32:13.859499"
            }
        }
    
    async def read_basic_memory_note(self, identifier: str) -> str:
        """
        Read content from Basic Memory note.
        
        In a real implementation, this would call:
        basic_memory.read_note(identifier=identifier)
        """
        print(f" Reading Basic Memory note: {identifier}")
        
        # Simulated note content
        return f"""---
title: {identifier.replace('-', ' ').title()}
type: note
permalink: {identifier}
---

# {identifier.replace('-', ' ').title()}

This is content from Basic Memory that needs to be synced to GitHub.

## Sync Information
- Generated: {datetime.now().isoformat()}
- Source: Basic Memory MCP
- Target: GitHub via MCP

This demonstrates the sync workflow between Basic Memory and GitHub.
"""
    
    async def check_github_file_exists(self, file_path: str) -> bool:
        """
        Check if file exists in GitHub repository.
        
        In a real implementation, this would call:
        github.get_file_contents(owner="nickagillis", repo="dev-knowledge-base", path=file_path)
        """
        print(f" Checking if GitHub file exists: {file_path}")
        
        # For demo purposes, assume files don't exist (so we'll create them)
        return False
    
    async def sync_file_to_github(self, file_path: str, content: str, commit_message: str) -> bool:
        """
        Sync file content to GitHub repository.
        
        In a real implementation, this would call:
        github.create_or_update_file(
            owner="nickagillis", 
            repo="dev-knowledge-base",
            path=file_path,
            content=content,
            message=commit_message,
            branch="main"
        )
        """
        print(f" Syncing to GitHub: {self.github_repo}/{file_path}")
        print(f"   Commit message: {commit_message}")
        print(f"   Content size: {len(content)} characters")
        
        # Simulate successful upload
        return True
    
    async def sync_basic_memory_to_github(self) -> Dict:
        """
        Main sync function that orchestrates the entire workflow.
        """
        print(" Starting Basic Memory -> GitHub sync")
        print("=" * 60)
        
        try:
            # Step 1: Get recent activity from Basic Memory
            recent_activity = await self.get_basic_memory_recent_activity()
            
            if not recent_activity["results"]:
                print("  No recent changes found in Basic Memory")
                return {"status": "no_changes"}
            
            # Step 2: Process each changed file
            for result in recent_activity["results"]:
                entity = result["primary_result"]
                permalink = entity["permalink"]
                file_path = entity["file_path"]
                title = entity["title"]
                
                self.sync_stats["files_checked"] += 1
                
                print(f"\n Processing: {title}")
                print(f"   Permalink: {permalink}")
                print(f"   File path: {file_path}")
                
                # Step 3: Read content from Basic Memory
                content = await self.read_basic_memory_note(permalink)
                
                # Step 4: Convert Windows path to GitHub path
                github_path = file_path.replace("\\", "/")
                
                # Step 5: Check if file exists in GitHub (optional - for update vs create)
                exists = await self.check_github_file_exists(github_path)
                action = "Update" if exists else "Create"
                
                # Step 6: Sync to GitHub
                commit_message = f"{action} {title} - Auto-sync from Basic Memory"
                
                success = await self.sync_file_to_github(github_path, content, commit_message)
                
                if success:
                    self.sync_stats["files_synced"] += 1
                    print(f"    Successfully synced to GitHub")
                else:
                    self.sync_stats["errors"].append(f"Failed to sync {title}")
                    print(f"    Failed to sync to GitHub")
            
            # Step 7: Report results
            print("\n" + "=" * 60)
            print(" Sync Summary:")
            print(f"   Files checked: {self.sync_stats['files_checked']}")
            print(f"   Files synced: {self.sync_stats['files_synced']}")
            print(f"   Errors: {len(self.sync_stats['errors'])}")
            
            if self.sync_stats["errors"]:
                print("   Error details:")
                for error in self.sync_stats["errors"]:
                    print(f"     - {error}")
            
            return {
                "status": "completed",
                "stats": self.sync_stats
            }
            
        except Exception as e:
            error_msg = f"Sync failed with error: {str(e)}"
            print(f" {error_msg}")
            self.sync_stats["errors"].append(error_msg)
            return {"status": "error", "message": error_msg}


async def main():
    """Run the sync demo."""
    print("Basic Memory GitHub Sync Demo")
    print("This demonstrates the workflow using MCP tools")
    print()
    
    # Create and run the sync demo
    sync_demo = MCPSyncDemo()
    result = await sync_demo.sync_basic_memory_to_github()
    
    print("\n Demo completed!")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n Next Steps:")
    print("1. Delete the duplicate GitHub repo: nickagillis/basic-memory-github-sync")
    print("2. Integrate this workflow with actual MCP tools in Claude Desktop")
    print("3. Set up automated scheduling (cron job, Task Scheduler, etc.)")
    print("4. Test with your real Basic Memory projects")
    print("5. Monitor sync results and handle errors gracefully")


if __name__ == "__main__":
    asyncio.run(main())
