# Basic Memory Integration for CrewBuilder Project

## Overview
When working on CrewBuilder, always keep Basic Memory active to capture insights and automatically sync important knowledge to the central knowledge repository.

## Workflow Instructions

### 1. Basic Memory Usage
- **Project-specific insights**: Create notes in Basic Memory's `crewbuilder` project for technical details, decisions, and learnings specific to CrewBuilder
- **Cross-project knowledge**: Create notes in Basic Memory's `knowledge` project for insights that could benefit future projects

### 2. Auto-Sync to GitHub
- **After significant insights**: Sync Basic Memory knowledge to GitHub repository `nickagillis/dev-knowledge-base`
- **Command**: "Check Basic Memory for recent activity and sync to GitHub"
- **Process**: 
  1. Use `basic-memory:recent_activity` to find new content
  2. Use `basic-memory:read_note` to get content
  3. Use `github:create_or_update_file` to sync to dev-knowledge-base

### 3. Knowledge Categories to Capture
- **Technical decisions** and their reasoning
- **Architecture insights** and patterns learned
- **Performance optimizations** discovered
- **Integration challenges** and solutions
- **User feedback** and feature ideas
- **Debugging breakthroughs** and lessons learned

### 4. Best Practices
- **Document as you go**: Don't wait until end of session
- **Include context**: Why decisions were made, not just what
- **Cross-reference**: Link to related knowledge and previous decisions
- **Categorize properly**: Use tags and folders for future findability

### 5. Example Usage
```
"Create a Basic Memory note about the new agent architecture we just implemented, 
including the reasoning behind the modular design and lessons learned about agent communication patterns.
Then sync it to the knowledge repo."
```

## Benefits
- **Never lose insights** from CrewBuilder development
- **Build institutional knowledge** that survives project changes
- **Enable knowledge reuse** in future projects
- **Facilitate team collaboration** through shared knowledge base
- **Create searchable history** of decisions and learnings

This ensures that all valuable knowledge from CrewBuilder work contributes to your growing, centralized intelligence.
