# CrewBuilder Migration Plan - Clean Slate Approach

## Goal
Remove all the old anti-pattern code and implement CrewBuilder properly with CrewAI best practices.

## Step 1: Archive Old Agents (Don't need them)
- Move all old agent files to `.archive/old_agents/`
- Keep only `simple_agents.py` and `llm_config.py`

## Step 2: Update API Server
- Remove `initialize_agents()` function
- Remove global `agents` dictionary
- Update `/api/generate` to use CrewBuilder V2
- Update `/api/clarify` endpoints to use new system
- Remove all imports of old agents

## Step 3: Fix Frontend
- Update `GenerationProgress.tsx` to show new stages:
  - Clarification & API Verification
  - Architecture Design
  - Task Flow Design
  - Code Generation
  - Quality Review
  - Deployment & Documentation
- Update agent count displays (8 specialists, not 11)
- Fix any hardcoded references to old agents

## Step 4: Clean Up Dependencies
- Remove `crewbuilder_orchestrator.py` (wrong approach)
- Update `main.py` to use CrewBuilder V2
- Archive old demo files
- Update deployment scripts

## Step 5: Test & Deploy
- Test with HeyGen/GoHighLevel example
- Verify frontend shows correct progress
- Deploy to Railway/Vercel
- Test live system end-to-end

## What We're Building
- 8 simple specialist agents (not 11 complex ones)
- Tasks that do the actual work
- Proper CrewAI hierarchical orchestration
- Clean, maintainable code that teaches proper patterns

## No Backwards Compatibility
- Old system was wrong, don't preserve it
- If something breaks, fix it properly
- Teach users the right way from the start