# CLAUDE.md - AI Assistant Context File

## Project Overview
CrewBuilder is an AI-powered meta-system that generates complete, production-ready CrewAI agent systems from natural language business requirements. The project is ~40-50% complete with the core agent pipeline implemented but missing critical infrastructure (database, auth, file handling, payment system).

### Two Distinct Systems
1. **CrewBuilder Platform** - Our hosted service (this codebase)
   - 11 specialized AI agents that build other agent systems
   - Hosted on Railway (backend) + Vercel (frontend)
   - Auto-deploys from GitHub
   
2. **Client Systems** - What CrewBuilder generates
   - Independent CrewAI agent systems for each client
   - Deployed to shared Railway infrastructure
   - Each client gets their own dashboard and API keys
   - Completely isolated from CrewBuilder and other clients

## Live URLs
- Backend API: https://web-production-bd955.up.railway.app
- Frontend App: https://crewbuilder.vercel.app

## Current Status (Last Updated: 2025-07-21)

### What's Actually Working
- **Backend (Railway)**: ✅ Running and accessible with env vars shared
- **Frontend (Vercel)**: ✅ Live at https://crewbuilder.vercel.app
- **Basic UI**: ✅ Can input requirements and see results
- **Agents Initialize**: ✅ All 11 agents start up successfully

### What's Not Working
- **CrewAI LLM Connection**: ❌ "LLM Failed" error - agents can't use OpenAI
- **Clarification Flow**: ❌ Frontend skips clarification, goes straight to generate
- **Agent Count Display**: ❌ Shows "0 AI Agents" (parsing issue)
- **File Download**: ❌ Completely fake - just shows alert
- **Actual AI Generation**: ❌ Using fallback templates, not real AI

### Key Issues Found
- **CrewAI Configuration**: Despite OPENAI_API_KEY being set, CrewAI can't connect
- **No Agent Orchestration**: Agents run sequentially, not as a crew
- **Frontend Integration**: Missing clarification flow, fake downloads
- **Fallback Everything**: System uses templates when AI fails

### What's Completely Missing
- **Database**: ❌ No user tracking, system history, or persistence
- **Authentication**: ❌ No login, users, or sessions
- **File Processing**: ❌ Can't upload existing code or handle attachments
- **Payment System**: ❌ No billing or subscription management
- **Monitoring**: ❌ No error tracking or analytics
- **Real Testing**: ❌ Never validated with actual users

### Critical Issue: Railway Deployment Crash
- **Symptom**: Railway builds successfully but crashes immediately after deployment
- **Error**: Startup crash, likely import or initialization issue
- **Test Tools**: Created `test_api.py` for direct backend testing
- **Next Steps**: Check Railway logs for startup diagnostics

## MVP Architecture

### Client Journey
1. **Clarification** - Chat with AI to refine requirements
2. **Generation** - 11-agent pipeline creates their system
3. **Deployment** - Automatic deployment to managed infrastructure
4. **Access** - Client receives dashboard URL + setup key
5. **Configuration** - Client adds their API keys via dashboard
6. **Production** - System runs independently

### Deployment Model
- **Managed Infrastructure**: CrewBuilder owns Railway account
- **Service Isolation**: Each client gets dedicated Railway service
- **Client Dashboard**: Simple web UI for each deployment
  - `/setup` - Initial API key configuration
  - `/status` - System health monitoring
  - `/test` - Agent testing interface
  - `/api-keys` - Secure key management

## Key Commands & Scripts
```bash
# Frontend (Next.js)
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run type-check   # TypeScript checking

# Backend (FastAPI)
cd backend
python -m venv venv  # Create virtual environment
venv\Scripts\activate # Activate (Windows)
pip install -r requirements.txt
python main.py       # Start server

# Testing
pytest              # Run backend tests
npm test           # Run frontend tests (if configured)
```

## Project Structure
```
crewbuilder/
├── backend/         # FastAPI server with CrewAI agents
│   ├── agents/      # 10 specialized AI agents
│   ├── api/         # API endpoints
│   └── main.py      # Server entry point
├── frontend/        # Next.js web interface
│   ├── src/         # React components
│   └── public/      # Static assets
├── deployment/      # Deployment configurations
└── docs/           # Documentation
```

## Active Development Areas
1. **Clarification Agent** - Interactive requirements refinement before generation
2. **Client Dashboard Generation** - Auto-generate dashboard with each system
3. **Railway Service Deployment** - Deploy as services, not separate projects
2. **API Key Management UI** - Implemented but untested
3. **Error Handling** - Needs improvement for edge cases
4. **Cost Optimization** - API usage needs analysis

## Known Issues & TODOs
- [ ] Test full deployment flow with actual Railway tokens
- [x] Railway deployment implementation is complete
- [x] Add Clarification Agent for requirements refinement (backend complete)
- [ ] Integrate clarification flow in frontend UI (Option 1: Front-loaded)
- [ ] Future: Implement Option 3 (Hybrid approach with assumptions)
- [ ] Implement client dashboard generation
- [ ] Switch to service-based deployment model
- [ ] Validate deployed systems work in production
- [ ] Calculate real API costs per system generation
- [ ] Implement proper error boundaries in frontend
- [ ] Add comprehensive logging for debugging (partially done)
- [ ] User authentication and session management
- [ ] Add debugging capabilities to generated crews:
  - [ ] Built-in health check endpoints
  - [ ] Error tracking and reporting
  - [ ] API connection validation on startup
  - [ ] Test mode with smaller models
  - [ ] Self-diagnostic agent for monitoring
  - [ ] Comprehensive error messages
  - [ ] Performance metrics and cost tracking

### Deployment Implementation Status
The deployment process has 3 steps:
1. **Generate system code** - Working ✅
2. **Deploy to Railway** - Implemented ✅
3. **Set environment variables** - Implemented ✅

**Recent Updates:**
- Implemented full Railway API integration in `railway_deployer.py`
- Added Railway GitHub integration support in `railway_github_deployer.py`
- System now attempts GitHub integration first, falls back to direct deployment
- Added comprehensive logging throughout deployment process

**Deployment Methods:**
1. **GitHub Integration** (preferred) - Uses Railway's GitHub integration
   - Requires: `GITHUB_TOKEN` and `CREWBUILDER_GITHUB_REPO` env vars
   - Creates branches and pushes code via GitHub API
   
2. **Direct Deployment** (fallback) - Creates tarball and uploads directly
   - Works with just `RAILWAY_TOKEN`
   - Uses Railway GraphQL API

## Recent Changes
- Added Clarification Agent (#11) for interactive requirements refinement
- Implemented shared Railway project deployment for client systems
- Created client dashboard generator for deployed systems
- Fixed Railway/Vercel deployment separation (backend/frontend)
- Made new agent imports optional to prevent production crashes
- Added `vercel.json` to properly configure frontend deployment
- Removed frontend build from Railway's `start.sh`
- Fixed frontend SystemOutput component data mapping
- Added JSON serialization fixes for backend responses
- Created `test_api.py` for direct backend testing
- Added startup diagnostics to debug Railway crashes

## AI Agent Capabilities
The system includes 11 specialized agents:
1. **Requirements Analyst** - Parses business requirements
2. **System Architect** - Designs system architecture
3. **Code Generator** - Generates CrewAI agent code
4. **Quality Assurance** - Tests and validates systems
5. **API Detective** - Discovers and integrates APIs
6. **Documentation Specialist** - Creates comprehensive docs
7. **Infrastructure Analyst** - Optimizes infrastructure
8. **Deployment Engineer** - Handles deployment configs
9. **Hosting Assistant** - Manages hosting setup
10. **Monitoring Engineer** - Sets up monitoring/logging
11. **Clarification Agent** - Interactive requirements refinement (NEW)

## Development Best Practices
1. Always run lint and type-check before committing
2. Test API endpoints with the live backend URL
3. Use environment variables for sensitive data
4. Follow existing code patterns and conventions
5. Update PROGRESS.md when completing major features

## Deployment Architecture
- **Backend (Railway)**: Runs only the FastAPI server via `start.sh`
- **Frontend (Vercel)**: Deploys from the `/web` directory
- **Important**: Do NOT have Railway build the frontend - it lacks npm
- **Vercel Config**: Uses `vercel.json` in root to specify web directory

## Environment Variables
```
# Backend
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
RAILWAY_TOKEN=your_token

# Frontend
NEXT_PUBLIC_API_URL=https://web-production-bd955.up.railway.app
```

## Quick Troubleshooting
- **CORS errors**: Check backend CORS configuration includes frontend URL
- **TypeScript errors**: Run `npm run type-check` to identify issues
- **API connection**: Verify NEXT_PUBLIC_API_URL is set correctly
- **Railway deployment**: Ensure RAILWAY_TOKEN is valid and has proper permissions
- **Railway npm errors**: Railway only runs backend - frontend deploys to Vercel
- **Vercel can't find app**: Check vercel.json points to web directory
- **Import errors**: New agents may need optional imports for production
- **Deployment not triggering**: May need empty commit after plan changes
- **Railway startup crash**: Check logs for import errors, use startup diagnostics
- **Backend 500 errors**: Check JSON serialization, all objects must be serializable
- **Testing backend**: Use `test_api.py` script for direct API testing

## Next Session Priorities
1. **Fix CrewAI LLM Connection** - Debug why "LLM Failed" despite API key
2. **Integrate Clarification Flow** - Frontend needs to call /api/clarify first
3. **Remove All Fallbacks** - Force real AI or fail
4. **Implement Real Downloads** - Package generated code as zip
5. **Create Proper Crew** - Orchestrate agents instead of sequential calls

## Debugging Notes
- OPENAI_API_KEY is set and accessible in Railway
- CrewAI version 0.141.0 might have issues
- Tried multiple config approaches, all fail with "LLM Failed"
- Need to check CrewAI GitHub issues or try different version

### Test Case Ready
User requirement for testing:
```
I need set up an agent that will take in a list of content ideas. 
Research the topics and news using open ai deep research or something similar. 
generate a short 2-3 minute script then generate videos using hey gen with a 
certain avatar id that I've created and then send them to people in my crm gohighlevel.
```

## Lessons Learned
- Railway and Vercel need separate deployments (backend/frontend)
- New agent imports should be optional for production stability
- Always test imports before pushing to production
- Deployment webhooks may need reauthorization after plan changes
- Railway builds can succeed but still crash on startup
- Need comprehensive startup diagnostics for debugging
- Test scripts are essential for backend validation

## Major Architecture Refactor (2025-07-22)

### Complete Rebuild Following CrewAI Best Practices
We discovered we were building AGAINST CrewAI's design patterns. Major changes:

1. **Simple Agents** - Replaced complex agent classes with simple definitions
   - Before: Each agent had internal crews, methods, complex logic
   - After: Agents are just role/goal/backstory (as CrewAI intended)

2. **Smart Tasks** - Moved all logic from agents to tasks
   - Before: 80% effort on agents, 20% on tasks
   - After: 20% effort on agents, 80% on tasks (CrewAI best practice)

3. **Proper Orchestration** - Using CrewAI's hierarchical process
   - Before: Manual sequential pipeline calling each agent
   - After: One Crew with hierarchical process, manager coordinates

4. **No More Fallbacks** - If it fails, we fix it properly
   - Before: Fallback to bad patterns when things break
   - After: Fix the root cause, teach proper patterns

### Key Files in New Architecture
- `/agents/simple_agents.py` - Simple agent definitions (8 specialists)
- `/tasks/crewbuilder_tasks.py` - Task definitions with all logic
- `/crewbuilder_crew_v2.py` - Proper CrewAI orchestration
- `/api_server.py` - Clean V2 API implementation
- `/web/components/GenerationProgressV2.tsx` - Updated UI for new flow
- Updated to CrewAI 0.148.0 (from 0.141.0)

### What We Removed/Archived
- All old complex agent files (moved to `.archive/old_agents/`)
- Old orchestrator pattern (`.archive/crewbuilder_orchestrator.py`)
- Serena memories (not applicable - that was Claude Desktop)
- PROGRESS.md (was tracking old system)
- Demo files that used old patterns

### Current Focus
- **NOT teaching users to build** - We build FOR them
- **Hosted solution** - Deploy to our Railway infrastructure
- **Value proposition** - They describe, we deliver working system
- **Simple dashboard** - Just API keys and status (not complex UI)

### Previous Debugging Discoveries
1. **API Key Newline Issue** - Railway environment variables can contain hidden newlines/spaces
   - Solution: Clean all API keys with `.replace('\n', '').strip()`
   
2. **CrewOutput Type Error** - CrewAI returns CrewOutput objects, not strings
   - Solution: Always use `str(result)` after `crew.kickoff()`
   
3. **Connection vs Authentication** - Different errors need different solutions
   - Connection errors: Often IPv4/IPv6 or firewall issues
   - Authentication errors: Invalid or malformed API keys

### Lessons for Generated Crews:
- Use simple agents with clear specializations
- Put the work in tasks, not agents
- Follow CrewAI patterns exactly - they exist for good reasons
- Always validate environment variables on startup
- Include proper error handling with clear messages
- Convert CrewOutput to strings before processing
- Add health check endpoints for debugging

## Documentation & Resources

### Primary Documentation Files
This is the primary AI context file. Other documentation files provide specific details:

- **PROGRESS.md** - Detailed progress tracking for all components (~90% claim needs revision)
- **CONSOLIDATED_STRATEGY.md** - Honest assessment of current state and realistic next steps
- **README.md** - User-facing documentation and quick start guide
- **RAILWAY_SETUP.md** - Step-by-step Railway deployment guide
- **DEPLOYMENT_ARCHITECTURE.md** - Two-layer deployment model explanation
- **DEPLOYMENT_CHECKLIST.md** - Pre-deployment verification checklist
- **DEPLOYMENT_SUCCESS.md** - Live URLs and testing checklist

### Repository Structure
- Repository: [Check git remote for URL]
- Backend: `/backend` - FastAPI + CrewAI agents
- Frontend: `/web` - Next.js interface
- Deployment: `/deployment` - Railway/GitHub integration

### Important Notes
- The project is realistically ~40-50% complete (not 90% as claimed in PROGRESS.md)
- Major missing pieces: database, auth, file handling, real deployment testing
- Clarification Agent has hardcoded responses (not fully implemented)