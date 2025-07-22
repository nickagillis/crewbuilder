"""
Documentation Specialist Agent for CrewBuilder
Generates comprehensive user documentation and setup guides for non-technical users.
"""

from crewai import Agent, Task
from .llm_config import get_configured_llm
import json
import re
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class UserGuide(BaseModel):
    """Represents a user guide for non-technical users"""
    title: str = Field(description="Guide title")
    target_audience: str = Field(description="Target user type: 'beginner', 'intermediate', 'technical'")
    overview: str = Field(description="Brief system overview and purpose")
    prerequisites: List[str] = Field(description="Required tools, accounts, or knowledge")
    step_by_step_guide: List[str] = Field(description="Detailed step-by-step instructions")
    screenshots_needed: List[str] = Field(description="Where screenshots would be helpful")
    common_issues: List[str] = Field(description="Common problems users might encounter")
    success_criteria: List[str] = Field(description="How users know they succeeded")


class TechnicalDocumentation(BaseModel):
    """Represents technical documentation for developers"""
    title: str = Field(description="Documentation title")
    system_architecture: str = Field(description="High-level system architecture description")
    api_documentation: str = Field(description="API setup and configuration instructions")
    environment_setup: str = Field(description="Complete environment setup instructions")
    configuration_guide: str = Field(description="Configuration file explanations")
    integration_examples: List[str] = Field(description="Code examples for common integrations")
    troubleshooting_guide: str = Field(description="Technical troubleshooting instructions")
    maintenance_procedures: List[str] = Field(description="Ongoing maintenance tasks")


class DeploymentGuide(BaseModel):
    """Represents platform-specific deployment guides"""
    platform: str = Field(description="Deployment platform: 'local', 'cloud', 'docker', 'serverless'")
    title: str = Field(description="Deployment guide title")
    overview: str = Field(description="Deployment approach overview")
    prerequisites: List[str] = Field(description="Platform-specific prerequisites")
    setup_steps: List[str] = Field(description="Detailed deployment steps")
    configuration_notes: List[str] = Field(description="Platform-specific configuration notes")
    monitoring_setup: List[str] = Field(description="How to monitor the deployed system")
    cost_considerations: str = Field(description="Cost implications and optimization tips")
    scaling_guidelines: List[str] = Field(description="How to scale the deployment")


class DocumentationPlan(BaseModel):
    """Complete documentation plan for a CrewAI system"""
    system_name: str = Field(description="Name of the CrewAI system")
    complexity_level: str = Field(description="'simple', 'moderate', 'complex'")
    target_users: List[str] = Field(description="Primary user types")
    estimated_reading_time: str = Field(description="Total time to read all documentation")
    documentation_types: List[str] = Field(description="Types of documentation included")
    user_guide: UserGuide = Field(description="Complete user guide")
    technical_documentation: TechnicalDocumentation = Field(description="Technical documentation")
    deployment_guides: List[DeploymentGuide] = Field(description="Platform-specific deployment guides")
    video_script_outlines: List[str] = Field(description="Outlines for tutorial videos")
    quick_start_checklist: List[str] = Field(description="Quick start checklist for immediate setup")
    support_resources: List[str] = Field(description="Additional support and learning resources")


class DocumentationSpecialist:
    """Documentation Specialist agent for generating comprehensive user documentation."""
    
    def __init__(self):
        """Initialize the Documentation Specialist agent."""
        # Get configured LLM

        llm = get_configured_llm(temperature=0.7)

        

        self.agent = Agent(
            role="Documentation Specialist", 
            goal="Generate comprehensive, user-friendly documentation that enables non-technical users to successfully deploy, configure, and maintain AI agent systems with minimal friction",
            backstory="""You are a world-class technical writer and documentation specialist with over a decade of experience making complex technology accessible to everyday users. You've written user guides for Fortune 500 companies, created onboarding documentation that reduced support tickets by 80%, and mastered the art of explaining technical concepts without jargon.

            Your superpower is understanding the user's journey from complete beginner to confident system operator. You know exactly where users get stuck, what they skip reading, and how to structure information so it's both comprehensive and digestible. You've seen countless software projects fail because of poor documentation, and you're passionate about preventing that.

            You excel at creating multiple documentation layers - quick-start guides for the impatient, detailed technical references for the thorough, and troubleshooting guides for when things go wrong. You understand that great documentation isn't just about being complete; it's about being empathetic to the user's context, urgency, and skill level.

            Your documentation doesn't just explain how to do something - it explains why, what to expect, how to verify success, and what to do when things don't go as planned. You create documentation that users actually want to read and that makes them feel confident rather than overwhelmed.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,  # Pass the LLM explicitly
            memory=False  # Disable memory to avoid connection issues
        )
        
        # Documentation best practices knowledge
        self.documentation_patterns = self._build_documentation_patterns()
    
    def generate_documentation(self, 
                             validated_code: str, 
                             api_integration_plan: Dict[str, Any], 
                             quality_report: Dict[str, Any]) -> DocumentationPlan:
        """
        Generate comprehensive documentation plan from validated code and integration details.
        
        Args:
            validated_code: Production-ready Python code from Quality Assurance
            api_integration_plan: API setup and cost information from API Detective
            quality_report: Quality analysis and validation results
            
        Returns:
            Complete documentation plan with guides and instructions
        """
        try:
            # Parse inputs
            code_analysis = self._analyze_code_structure(validated_code)
            api_analysis = self._analyze_api_requirements(api_integration_plan)
            complexity_assessment = self._assess_documentation_complexity(quality_report, api_analysis)
            
            # Determine target users and documentation scope
            target_users = self._identify_target_users(complexity_assessment, api_analysis)
            
            # Generate user guide
            user_guide = self._generate_user_guide(code_analysis, api_analysis, complexity_assessment)
            
            # Generate technical documentation
            technical_docs = self._generate_technical_documentation(code_analysis, api_analysis, quality_report)
            
            # Generate deployment guides
            deployment_guides = self._generate_deployment_guides(code_analysis, api_analysis, complexity_assessment)
            
            # Create video script outlines
            video_scripts = self._generate_video_script_outlines(user_guide, technical_docs)
            
            # Generate quick start checklist
            quick_start = self._generate_quick_start_checklist(user_guide, api_analysis)
            
            # Compile support resources
            support_resources = self._compile_support_resources(complexity_assessment, api_analysis)
            
            # Calculate estimated reading time
            reading_time = self._estimate_reading_time(user_guide, technical_docs, deployment_guides)
            
            return DocumentationPlan(
                system_name=code_analysis.get("system_name", "CrewAI System"),
                complexity_level=complexity_assessment["level"],
                target_users=target_users,
                estimated_reading_time=reading_time,
                documentation_types=["User Guide", "Technical Documentation", "Deployment Guides", "Video Scripts"],
                user_guide=user_guide,
                technical_documentation=technical_docs,
                deployment_guides=deployment_guides,
                video_script_outlines=video_scripts,
                quick_start_checklist=quick_start,
                support_resources=support_resources
            )
        
        except Exception as e:
            # Fallback documentation plan for error cases
            return self._generate_fallback_documentation_plan(str(e))
    
    def _analyze_code_structure(self, validated_code: str) -> Dict[str, Any]:
        """Analyze the structure of validated code to understand documentation needs."""
        analysis = {
            "system_name": "CrewAI System",
            "agents": [],
            "tasks": [],
            "tools": [],
            "main_file": "main.py",
            "config_files": [],
            "dependencies": []
        }
        
        # Extract system information from code
        if "class " in validated_code:
            # Find agent classes
            agent_matches = re.findall(r'class (\w+Agent)', validated_code)
            analysis["agents"] = agent_matches or ["CustomAgent"]
            
            # Find task definitions
            task_matches = re.findall(r'Task\s*\([^)]*goal\s*=\s*["\']([^"\']+)', validated_code)
            analysis["tasks"] = task_matches[:5] if task_matches else ["Data processing", "Analysis", "Report generation"]
        
        # Extract tools from imports or tool definitions
        tool_patterns = [
            r'from crewai_tools import (\w+)',
            r'tools\s*=\s*\[([^\]]+)\]',
            r'@tool\s*def\s+(\w+)'
        ]
        
        for pattern in tool_patterns:
            matches = re.findall(pattern, validated_code)
            analysis["tools"].extend(matches)
        
        # Clean up tools list
        analysis["tools"] = list(set(analysis["tools"]))[:10]  # Limit to 10 tools
        
        # Extract dependencies from requirements or imports
        if "import " in validated_code:
            import_matches = re.findall(r'(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)', validated_code)
            analysis["dependencies"] = [imp for imp in import_matches if imp not in ['os', 'sys', 'json', 're']][:10]
        
        return analysis
    
    def _analyze_api_requirements(self, api_integration_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze API requirements to understand setup complexity."""
        if not api_integration_plan:
            return {
                "total_apis": 1,
                "critical_apis": 1,
                "estimated_cost": "$50-100",
                "setup_complexity": "moderate",
                "environment_variables": ["OPENAI_API_KEY"],
                "platforms": ["OpenAI"]
            }
        
        return {
            "total_apis": api_integration_plan.get("total_apis", 1),
            "critical_apis": api_integration_plan.get("critical_apis", 1),
            "estimated_cost": api_integration_plan.get("total_estimated_cost", "$50-100"),
            "setup_complexity": "complex" if api_integration_plan.get("complexity_score", 5) > 6 else "moderate",
            "environment_variables": api_integration_plan.get("environment_variables", ["OPENAI_API_KEY"]),
            "platforms": [rec.get("provider", "OpenAI") for rec in api_integration_plan.get("recommendations", [])][:5]
        }
    
    def _assess_documentation_complexity(self, quality_report: Dict[str, Any], api_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Assess the complexity level for documentation purposes."""
        
        # Base complexity from APIs and code
        api_complexity = api_analysis.get("total_apis", 1)
        setup_complexity = api_analysis.get("setup_complexity", "moderate")
        
        if api_complexity <= 2 and setup_complexity == "simple":
            level = "simple"
        elif api_complexity <= 4 and setup_complexity in ["simple", "moderate"]:
            level = "moderate"
        else:
            level = "complex"
        
        return {
            "level": level,
            "reasoning": f"Based on {api_complexity} APIs with {setup_complexity} setup complexity",
            "documentation_depth": "comprehensive" if level == "complex" else "standard",
            "support_level": "high" if level == "complex" else "medium"
        }
    
    def _identify_target_users(self, complexity_assessment: Dict[str, str], api_analysis: Dict[str, Any]) -> List[str]:
        """Identify primary target user types for the documentation."""
        users = ["Business Users"]
        
        if complexity_assessment["level"] in ["moderate", "complex"]:
            users.append("Technical Users")
        
        if api_analysis.get("total_apis", 1) > 3:
            users.append("System Administrators")
        
        return users
    
    def _generate_user_guide(self, code_analysis: Dict[str, Any], api_analysis: Dict[str, Any], complexity_assessment: Dict[str, str]) -> UserGuide:
        """Generate comprehensive user guide for non-technical users."""
        
        system_name = code_analysis.get("system_name", "CrewAI System")
        agents = code_analysis.get("agents", ["Assistant"])
        
        # Determine prerequisites based on complexity
        prerequisites = ["Basic computer skills", "Internet connection"]
        
        if api_analysis.get("total_apis", 1) > 1:
            prerequisites.extend(["Email account for API signups", "Credit card for API services (if needed)"])
        
        if complexity_assessment["level"] == "complex":
            prerequisites.append("Familiarity with basic technical concepts")
        
        # Generate step-by-step guide
        steps = [
            "Download and extract the system files",
            "Install Python (version 3.8 or higher)",
            "Open terminal/command prompt in the system folder",
            "Install required packages: run 'pip install -r requirements.txt'",
        ]
        
        # Add API setup steps
        env_vars = api_analysis.get("environment_variables", [])
        if env_vars:
            steps.extend([
                f"Sign up for API accounts: {', '.join(api_analysis.get('platforms', ['OpenAI']))}",
                "Create API keys from your provider dashboards",
                "Copy the .env.template file to .env",
                f"Add your API keys to the .env file: {', '.join(env_vars[:3])}"
            ])
        
        steps.extend([
            "Test the installation: run 'python test_setup.py'",
            "Start the system: run 'python main.py'",
            "Follow the on-screen prompts to use your AI system"
        ])
        
        # Common issues
        common_issues = [
            "Python not found: Make sure Python is installed and in your PATH",
            "Permission errors: Try running as administrator (Windows) or with sudo (Mac/Linux)",
            "API key errors: Double-check your API keys are correctly copied to the .env file",
            "Package installation fails: Try 'pip install --upgrade pip' then retry"
        ]
        
        if api_analysis.get("total_apis", 1) > 2:
            common_issues.append("Rate limit errors: Wait a few minutes and try again, or check your API usage limits")
        
        # Success criteria
        success_criteria = [
            "System starts without error messages",
            "Test commands return expected results",
            f"AI agents ({', '.join(agents[:3])}) respond to your prompts",
            "Generated outputs appear in the specified folders"
        ]
        
        # Screenshots needed
        screenshots = [
            "Python installation verification",
            "Terminal/command prompt usage",
            "API key setup in .env file",
            "Successful system startup",
            "Example of system output"
        ]
        
        return UserGuide(
            title=f"User Guide: Getting Started with {system_name}",
            target_audience="beginner",
            overview=f"This guide helps you set up and use your {system_name}, which uses AI agents to automate tasks and provide intelligent assistance. No technical experience required!",
            prerequisites=prerequisites,
            step_by_step_guide=steps,
            screenshots_needed=screenshots,
            common_issues=common_issues,
            success_criteria=success_criteria
        )
    
    def _generate_technical_documentation(self, code_analysis: Dict[str, Any], api_analysis: Dict[str, Any], quality_report: Dict[str, Any]) -> TechnicalDocumentation:
        """Generate comprehensive technical documentation."""
        
        system_name = code_analysis.get("system_name", "CrewAI System")
        agents = code_analysis.get("agents", ["Assistant"])
        tools = code_analysis.get("tools", ["WebTool"])
        
        # System architecture description
        architecture = f"""
{system_name} is built using the CrewAI framework with {len(agents)} specialized AI agents:

{chr(10).join([f"• {agent}: Handles specific domain tasks" for agent in agents[:5]])}

The system follows a modular architecture where each agent has defined roles, goals, and tools. 
Agents collaborate through structured workflows to complete complex multi-step tasks.

Key Components:
- Main orchestration script (main.py)
- Agent definitions with specialized roles
- Task workflows with dependencies
- Tool integrations for external APIs
- Configuration management for environment variables
"""
        
        # API documentation
        api_docs = f"""
API Setup and Configuration:

Required APIs: {api_analysis.get('total_apis', 1)} services
Estimated Cost: {api_analysis.get('estimated_cost', '$50-100')} per month

Environment Variables:
{chr(10).join([f"• {var}: Required for API authentication" for var in api_analysis.get('environment_variables', ['OPENAI_API_KEY'])[:5]])}

Configuration Files:
• .env - Environment variables and API keys
• config/ - Additional configuration files
• requirements.txt - Python dependencies
"""
        
        # Environment setup
        env_setup = """
Development Environment Setup:

1. Python Requirements:
   - Python 3.8+ (recommended: 3.11+)
   - pip (Python package manager)
   - Virtual environment (recommended)

2. Installation:
   ```bash
   python -m venv crewai_env
   source crewai_env/bin/activate  # Linux/Mac
   crewai_env\\Scripts\\activate     # Windows
   pip install -r requirements.txt
   ```

3. Configuration:
   - Copy .env.template to .env
   - Add API keys to .env file
   - Verify setup with test_setup.py
"""
        
        # Configuration guide
        config_guide = """
Configuration Management:

1. Environment Variables (.env):
   - API_KEY variables for external services
   - DEBUG=true for development mode
   - LOG_LEVEL=INFO for logging control

2. Agent Configuration:
   - Role definitions in agent classes
   - Goal and backstory customization
   - Tool assignment and permissions

3. Task Configuration:
   - Task dependencies and workflows
   - Output formats and destinations
   - Error handling and retries
"""
        
        # Integration examples
        integrations = [
            "Custom tool integration with @tool decorator",
            "Adding new API services to existing agents",
            "Creating custom agent roles and workflows",
            "Implementing custom output formats",
            "Adding error handling and logging"
        ]
        
        # Troubleshooting
        troubleshooting = """
Technical Troubleshooting:

1. Common Issues:
   - Import errors: Check Python path and virtual environment
   - API failures: Verify keys and rate limits
   - Agent errors: Check agent configuration and tools
   - Task failures: Review task dependencies and inputs

2. Debugging:
   - Enable DEBUG mode in .env
   - Check logs/ directory for detailed errors
   - Use test scripts for component validation
   - Monitor API usage and quotas

3. Performance:
   - Monitor token usage for cost optimization
   - Adjust agent concurrency for performance
   - Cache results to reduce API calls
"""
        
        # Maintenance procedures
        maintenance = [
            "Regular monitoring of API usage and costs",
            "Updating dependencies with 'pip install -r requirements.txt --upgrade'",
            "Backing up configuration files and custom modifications",
            "Testing system functionality after updates",
            "Monitoring log files for errors and performance issues"
        ]
        
        return TechnicalDocumentation(
            title=f"Technical Documentation: {system_name}",
            system_architecture=architecture.strip(),
            api_documentation=api_docs.strip(),
            environment_setup=env_setup.strip(),
            configuration_guide=config_guide.strip(),
            integration_examples=integrations,
            troubleshooting_guide=troubleshooting.strip(),
            maintenance_procedures=maintenance
        )
    
    def _generate_deployment_guides(self, code_analysis: Dict[str, Any], api_analysis: Dict[str, Any], complexity_assessment: Dict[str, str]) -> List[DeploymentGuide]:
        """Generate platform-specific deployment guides."""
        
        guides = []
        system_name = code_analysis.get("system_name", "CrewAI System")
        estimated_cost = api_analysis.get("estimated_cost", "$50-100")
        
        # Local deployment guide
        local_guide = DeploymentGuide(
            platform="local",
            title=f"Local Deployment: {system_name}",
            overview="Run the system on your personal computer for development and testing",
            prerequisites=[
                "Python 3.8+ installed",
                "Admin/sudo access for package installation",
                "Stable internet connection for API calls",
                "Sufficient disk space (minimum 1GB recommended)"
            ],
            setup_steps=[
                "Download the system files to your preferred directory",
                "Open terminal/command prompt in the system directory",
                "Create virtual environment: python -m venv venv",
                "Activate virtual environment",
                "Install dependencies: pip install -r requirements.txt",
                "Copy .env.template to .env",
                "Add your API keys to the .env file",
                "Test installation: python test_setup.py",
                "Run the system: python main.py"
            ],
            configuration_notes=[
                "Environment variables are loaded from .env file",
                "Logs are saved to logs/ directory",
                "Generated outputs saved to output/ directory",
                "Configuration can be modified in config/ files"
            ],
            monitoring_setup=[
                "Check logs/ directory for system logs",
                "Monitor API usage through provider dashboards",
                "Use built-in health checks for system status"
            ],
            cost_considerations=f"Only API costs apply: {estimated_cost}/month. No hosting costs for local deployment.",
            scaling_guidelines=[
                "Single user deployment - not suitable for multiple concurrent users",
                "Consider cloud deployment for team usage",
                "Monitor system performance during heavy usage",
                "Upgrade hardware if processing becomes slow"
            ]
        )
        guides.append(local_guide)
        
        # Cloud deployment guide (for moderate/complex systems)
        if complexity_assessment["level"] in ["moderate", "complex"]:
            cloud_guide = DeploymentGuide(
                platform="cloud",
                title=f"Cloud Deployment: {system_name}",
                overview="Deploy to cloud platforms for scalability and team access",
                prerequisites=[
                    "Cloud platform account (AWS, Google Cloud, or Azure)",
                    "Basic familiarity with cloud services",
                    "Credit card for cloud service billing",
                    "SSH key pair for secure access"
                ],
                setup_steps=[
                    "Create cloud compute instance (e.g., t3.medium on AWS)",
                    "Configure security groups for SSH and HTTP access",
                    "Connect to instance via SSH",
                    "Install Python and dependencies on cloud instance",
                    "Upload system files to cloud instance",
                    "Configure environment variables securely",
                    "Set up process management with systemd or PM2",
                    "Configure reverse proxy (nginx) if web interface needed",
                    "Set up monitoring and logging"
                ],
                configuration_notes=[
                    "Use cloud-specific secret management for API keys",
                    "Configure auto-restart on system reboot",
                    "Set up log rotation to prevent disk space issues",
                    "Use cloud storage for persistent data"
                ],
                monitoring_setup=[
                    "Set up cloud monitoring dashboards",
                    "Configure alerting for system failures",
                    "Monitor resource usage (CPU, memory, network)",
                    "Set up log aggregation and analysis"
                ],
                cost_considerations=f"Cloud hosting: $20-100/month + API costs ({estimated_cost}/month). Consider auto-scaling to optimize costs.",
                scaling_guidelines=[
                    "Use load balancers for high availability",
                    "Implement auto-scaling for variable workloads",
                    "Consider container deployment for easier scaling",
                    "Use managed services to reduce operational overhead"
                ]
            )
            guides.append(cloud_guide)
        
        # Docker deployment guide (for complex systems)
        if complexity_assessment["level"] == "complex":
            docker_guide = DeploymentGuide(
                platform="docker",
                title=f"Docker Deployment: {system_name}",
                overview="Containerized deployment for consistent environments and easy scaling",
                prerequisites=[
                    "Docker installed and running",
                    "Docker Compose (for multi-container setups)",
                    "Basic understanding of containerization",
                    "Sufficient system resources for containers"
                ],
                setup_steps=[
                    "Review included Dockerfile and docker-compose.yml",
                    "Build the Docker image: docker build -t crewai-system .",
                    "Create .env file with your API keys",
                    "Run with Docker Compose: docker-compose up -d",
                    "Verify containers are running: docker ps",
                    "Check logs: docker-compose logs",
                    "Access the system through exposed ports"
                ],
                configuration_notes=[
                    "Environment variables passed through docker-compose.yml",
                    "Persistent volumes for data storage",
                    "Network configuration for container communication",
                    "Resource limits to prevent system overload"
                ],
                monitoring_setup=[
                    "Use docker stats for resource monitoring",
                    "Configure log drivers for centralized logging",
                    "Set up health checks in Docker containers",
                    "Use monitoring tools like Portainer or Grafana"
                ],
                cost_considerations=f"Infrastructure costs depend on deployment platform. API costs remain: {estimated_cost}/month.",
                scaling_guidelines=[
                    "Use Docker Swarm or Kubernetes for orchestration",
                    "Implement horizontal scaling with multiple replicas",
                    "Use container registries for image management",
                    "Consider serverless containers for cost optimization"
                ]
            )
            guides.append(docker_guide)
        
        return guides
    
    def _generate_video_script_outlines(self, user_guide: UserGuide, technical_docs: TechnicalDocumentation) -> List[str]:
        """Generate outlines for tutorial videos."""
        
        outlines = [
            """Video 1: Quick Start Guide (5-10 minutes)
            • Introduction: What this system does and why you'll love it
            • Prerequisites check: What you need before starting
            • Installation walkthrough: Step-by-step Python and package setup
            • API key setup: Creating accounts and adding keys
            • First run: Starting the system and seeing it work
            • Success confirmation: How to know everything is working
            • Next steps: Where to go from here""",
            
            """Video 2: API Setup Deep Dive (10-15 minutes)
            • API overview: Understanding what APIs we're using and why
            • Account creation: Signing up for each required service
            • API key generation: Finding and creating your keys
            • Environment configuration: Setting up the .env file properly
            • Cost management: Understanding pricing and setting limits
            • Troubleshooting: Common API setup problems and solutions
            • Testing: Verifying your API connections work""",
            
            """Video 3: Using Your AI System (15-20 minutes)
            • System overview: Understanding what each agent does
            • Input preparation: How to structure your requests
            • Running tasks: Step-by-step task execution
            • Understanding outputs: Interpreting and using results
            • Customization: Basic configuration changes
            • Common workflows: Typical use cases and patterns
            • Getting help: Where to find support and resources"""
        ]
        
        return outlines
    
    def _generate_quick_start_checklist(self, user_guide: UserGuide, api_analysis: Dict[str, Any]) -> List[str]:
        """Generate a quick start checklist for immediate setup."""
        
        checklist = [
            "☐ Download and extract system files",
            "☐ Install Python 3.8+ (check with: python --version)",
            "☐ Install packages: pip install -r requirements.txt",
        ]
        
        # Add API-specific checklist items
        platforms = api_analysis.get("platforms", ["OpenAI"])
        env_vars = api_analysis.get("environment_variables", ["OPENAI_API_KEY"])
        
        for platform in platforms[:3]:
            checklist.append(f"☐ Create {platform} account and generate API key")
        
        checklist.extend([
            "☐ Copy .env.template to .env",
            f"☐ Add API keys to .env file: {', '.join(env_vars[:3])}",
            "☐ Test setup: python test_setup.py",
            "☐ Run system: python main.py",
            "☐ Verify AI responses are working",
            "☐ Check output folder for generated files"
        ])
        
        return checklist
    
    def _compile_support_resources(self, complexity_assessment: Dict[str, str], api_analysis: Dict[str, Any]) -> List[str]:
        """Compile additional support and learning resources."""
        
        resources = [
            "📖 Complete README.md file in the project directory",
            "🎥 Video tutorials (see video script outlines)",
            "💬 CrewAI Community Discord for general questions",
            "📚 CrewAI Official Documentation: https://docs.crewai.com",
            "🔧 Python Installation Guide: https://python.org/downloads",
        ]
        
        # Add API-specific resources
        platforms = api_analysis.get("platforms", ["OpenAI"])
        
        if "OpenAI" in platforms:
            resources.append("🤖 OpenAI API Documentation: https://platform.openai.com/docs")
        
        if "Anthropic" in platforms:
            resources.append("🧠 Anthropic API Documentation: https://docs.anthropic.com")
        
        if complexity_assessment["level"] == "complex":
            resources.extend([
                "🐳 Docker Installation Guide: https://docs.docker.com/get-docker",
                "☁️ AWS Getting Started: https://aws.amazon.com/getting-started",
                "📊 System Monitoring Best Practices"
            ])
        
        resources.extend([
            "💡 Troubleshooting FAQ in docs/ folder",
            "🆘 Emergency contact: Check README for support information",
            "🔄 Update instructions: See maintenance documentation"
        ])
        
        return resources
    
    def _estimate_reading_time(self, user_guide: UserGuide, technical_docs: TechnicalDocumentation, deployment_guides: List[DeploymentGuide]) -> str:
        """Estimate total reading time for all documentation."""
        
        # Rough estimates based on content complexity
        user_guide_time = 15  # 15 minutes for user guide
        technical_time = 30    # 30 minutes for technical docs
        deployment_time = len(deployment_guides) * 20  # 20 minutes per deployment guide
        
        total_minutes = user_guide_time + technical_time + deployment_time
        
        if total_minutes < 60:
            return f"{total_minutes} minutes"
        else:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if minutes == 0:
                return f"{hours} hour{'s' if hours > 1 else ''}"
            else:
                return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minutes"
    
    def _generate_fallback_documentation_plan(self, error_message: str) -> DocumentationPlan:
        """Generate a basic documentation plan when errors occur."""
        
        fallback_user_guide = UserGuide(
            title="User Guide: CrewAI System Setup",
            target_audience="beginner",
            overview="This system uses AI agents to automate tasks and provide intelligent assistance.",
            prerequisites=["Python 3.8+", "Internet connection", "Basic computer skills"],
            step_by_step_guide=[
                "Install Python from python.org",
                "Download system files",
                "Run: pip install -r requirements.txt",
                "Configure API keys in .env file",
                "Run: python main.py"
            ],
            screenshots_needed=["Python installation", "API key setup", "System startup"],
            common_issues=["Python not found", "API key errors", "Package installation fails"],
            success_criteria=["System starts without errors", "AI agents respond to prompts"]
        )
        
        fallback_technical_docs = TechnicalDocumentation(
            title="Technical Documentation: CrewAI System",
            system_architecture="CrewAI-based system with specialized AI agents",
            api_documentation="Requires API keys for LLM services",
            environment_setup="Python 3.8+, pip install requirements",
            configuration_guide="Configure .env file with API keys",
            integration_examples=["Custom tool integration", "New agent creation"],
            troubleshooting_guide="Check logs for errors, verify API keys",
            maintenance_procedures=["Monitor API usage", "Update dependencies"]
        )
        
        fallback_deployment = DeploymentGuide(
            platform="local",
            title="Local Deployment Guide",
            overview="Run system locally for development",
            prerequisites=["Python", "API keys"],
            setup_steps=["Install dependencies", "Configure environment", "Run system"],
            configuration_notes=["Use .env file for configuration"],
            monitoring_setup=["Check logs directory"],
            cost_considerations="API costs only",
            scaling_guidelines=["Single user deployment"]
        )
        
        return DocumentationPlan(
            system_name="CrewAI System",
            complexity_level="moderate",
            target_users=["Business Users", "Technical Users"],
            estimated_reading_time="45 minutes",
            documentation_types=["User Guide", "Technical Documentation"],
            user_guide=fallback_user_guide,
            technical_documentation=fallback_technical_docs,
            deployment_guides=[fallback_deployment],
            video_script_outlines=["Quick start guide", "API setup tutorial"],
            quick_start_checklist=["Install Python", "Setup API keys", "Run system"],
            support_resources=["README.md", "CrewAI Documentation"]
        )
    
    def _build_documentation_patterns(self) -> Dict[str, Any]:
        """Build documentation best practices and patterns."""
        return {
            "writing_style": {
                "tone": "friendly and encouraging",
                "language": "clear and jargon-free",
                "structure": "step-by-step with clear outcomes",
                "examples": "concrete and relevant to user needs"
            },
            "user_experience": {
                "accessibility": "multiple skill levels",
                "navigation": "clear hierarchy and sections",
                "visuals": "screenshots and diagrams where helpful",
                "feedback": "success criteria and troubleshooting"
            },
            "technical_accuracy": {
                "verification": "all instructions tested",
                "updates": "version-specific guidance",
                "compatibility": "cross-platform considerations",
                "security": "best practices for API keys and data"
            }
        }


def create_documentation_specialist() -> DocumentationSpecialist:
    """Factory function to create a DocumentationSpecialist instance."""
    return DocumentationSpecialist()
