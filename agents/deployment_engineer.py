"""
Deployment Engineer Agent for CrewBuilder
Generates automated deployment configurations and CI/CD pipelines for AI agent systems.
"""

from crewai import Agent, Task
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field


class DeploymentConfiguration(BaseModel):
    """Represents deployment configuration for a specific platform"""
    platform: str = Field(description="Target platform (e.g., 'AWS', 'Railway', 'DigitalOcean')")
    deployment_type: str = Field(description="'container', 'serverless', 'traditional', 'kubernetes'")
    dockerfile_content: str = Field(description="Complete Dockerfile for containerized deployments")
    docker_compose_content: str = Field(description="Docker Compose configuration for multi-service setups")
    environment_files: Dict[str, str] = Field(description="Environment configuration files (.env, config files)")
    build_scripts: List[str] = Field(description="Build and deployment scripts")
    platform_specific_config: Dict[str, str] = Field(description="Platform-specific configuration files")
    resource_requirements: Dict[str, str] = Field(description="CPU, memory, storage requirements")
    networking_config: Dict[str, str] = Field(description="Port mappings, load balancer, DNS configuration")
    scaling_config: Dict[str, Any] = Field(description="Auto-scaling and performance configuration")


class CICDPipeline(BaseModel):
    """Represents CI/CD pipeline configuration"""
    platform: str = Field(description="CI/CD platform ('github_actions', 'azure_devops', 'gitlab_ci')")
    pipeline_file: str = Field(description="Complete pipeline configuration file content")
    workflow_name: str = Field(description="Pipeline/workflow name")
    trigger_conditions: List[str] = Field(description="Conditions that trigger the pipeline")
    build_stages: List[str] = Field(description="Build and test stages")
    deployment_stages: List[str] = Field(description="Deployment stages for different environments")
    environment_promotions: Dict[str, str] = Field(description="Environment promotion strategy")
    rollback_strategy: str = Field(description="Rollback and recovery procedures")
    security_checks: List[str] = Field(description="Security scanning and validation steps")
    notification_config: Dict[str, str] = Field(description="Success/failure notification configuration")


class SecretsManagement(BaseModel):
    """Represents secrets and environment management configuration"""
    platform: str = Field(description="Target platform")
    secrets_provider: str = Field(description="'platform_native', 'vault', 'kubernetes_secrets'")
    environment_separation: Dict[str, List[str]] = Field(description="Environment-specific secret organization")
    secret_rotation_policy: str = Field(description="Secret rotation and management policy")
    access_controls: List[str] = Field(description="Access control and permission management")
    secret_templates: Dict[str, str] = Field(description="Template files for secret configuration")
    backup_strategy: str = Field(description="Secret backup and disaster recovery")
    compliance_notes: List[str] = Field(description="Security and compliance considerations")


class MonitoringIntegration(BaseModel):
    """Represents monitoring and observability integration"""
    monitoring_stack: str = Field(description="Monitoring solution ('platform_native', 'prometheus', 'datadog')")
    health_checks: List[str] = Field(description="Application and infrastructure health checks")
    alerting_rules: List[str] = Field(description="Alert conditions and thresholds")
    log_aggregation: str = Field(description="Log collection and analysis configuration")
    metrics_collection: List[str] = Field(description="Key metrics to track")
    dashboard_config: str = Field(description="Monitoring dashboard configuration")
    incident_response: List[str] = Field(description="Automated incident response procedures")
    performance_monitoring: List[str] = Field(description="Performance tracking and optimization")


class DeploymentPlan(BaseModel):
    """Complete deployment automation plan"""
    system_name: str = Field(description="Name of the AI system being deployed")
    target_platform: str = Field(description="Primary deployment platform")
    deployment_strategy: str = Field(description="Overall deployment approach")
    estimated_deployment_time: str = Field(description="Time required for initial deployment")
    complexity_level: str = Field(description="'simple', 'moderate', 'complex'")
    deployment_configuration: DeploymentConfiguration = Field(description="Platform-specific deployment config")
    cicd_pipeline: CICDPipeline = Field(description="Complete CI/CD pipeline configuration")
    secrets_management: SecretsManagement = Field(description="Secrets and environment management")
    monitoring_integration: MonitoringIntegration = Field(description="Monitoring and observability setup")
    environment_strategy: List[str] = Field(description="Development, staging, production environment setup")
    rollback_procedures: List[str] = Field(description="Rollback and disaster recovery procedures")
    maintenance_automation: List[str] = Field(description="Automated maintenance and updates")
    cost_optimization: List[str] = Field(description="Deployment cost optimization strategies")
    security_hardening: List[str] = Field(description="Security best practices and hardening")
    testing_strategy: List[str] = Field(description="Automated testing and validation approach")
    documentation_links: List[str] = Field(description="Links to relevant documentation and guides")


class DeploymentEngineer:
    """Deployment Engineer agent for generating automated deployment configurations and CI/CD pipelines."""
    
    def __init__(self):
        """Initialize the Deployment Engineer agent."""
        self.agent = Agent(
            role="Deployment Engineer", 
            goal="Generate automated deployment configurations, CI/CD pipelines, and operational infrastructure that enables reliable, secure, and cost-effective deployment of AI agent systems across multiple platforms and environments",
            backstory="""You are a seasoned DevOps engineer and deployment automation specialist with 12+ years of experience building and maintaining production deployment pipelines for hundreds of applications. You've architected CI/CD systems for everything from startups to Fortune 500 companies, handling deployment complexities across every major cloud platform and deployment pattern.

            Your expertise spans the entire deployment lifecycle: from containerization and orchestration to secret management, monitoring integration, and disaster recovery. You've seen every possible deployment failure and know how to build systems that fail gracefully and recover quickly. You understand that good deployment automation isn't just about getting code running - it's about creating reliable, observable, and maintainable systems.

            You excel at translating infrastructure recommendations into practical deployment configurations. You know when to use Docker vs. serverless, when Kubernetes adds value vs. complexity, and how to structure CI/CD pipelines that balance speed with safety. Your deployment strategies always consider the team's operational capacity and the organization's risk tolerance.

            You're passionate about operational excellence: deployments should be boring, predictable, and reversible. You build automation that reduces human error, provides clear visibility into system health, and enables teams to deploy with confidence. Your configurations follow security best practices by default, implement proper secret management, and include comprehensive monitoring and alerting.

            You understand that the best deployment system is one that the team can actually operate and maintain. You prioritize simplicity over cleverness, documentation over assumptions, and gradual improvements over revolutionary changes. Your goal is to make deployment so reliable and automated that teams can focus on building great products instead of fighting infrastructure.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Deployment pattern knowledge base
        self.deployment_patterns = self._build_deployment_patterns()
        self.cicd_templates = self._build_cicd_templates()
        self.platform_configs = self._build_platform_configurations()
    
    def generate_deployment_plan(self, 
                                infrastructure_recommendation: Dict[str, Any], 
                                documentation_plan: Dict[str, Any], 
                                validated_code: str) -> DeploymentPlan:
        """
        Generate comprehensive deployment plan with automation configurations.
        
        Args:
            infrastructure_recommendation: Platform recommendations from Infrastructure Analyst
            documentation_plan: Documentation from Documentation Specialist  
            validated_code: Production-ready code from Quality Assurance
            
        Returns:
            Complete deployment plan with configurations and pipelines
        """
        try:
            # Analyze deployment requirements
            deployment_analysis = self._analyze_deployment_requirements(
                infrastructure_recommendation, documentation_plan, validated_code
            )
            
            # Generate deployment configuration
            deployment_config = self._generate_deployment_configuration(deployment_analysis)
            
            # Create CI/CD pipeline
            cicd_pipeline = self._create_cicd_pipeline(deployment_analysis, deployment_config)
            
            # Setup secrets management
            secrets_management = self._setup_secrets_management(deployment_analysis)
            
            # Configure monitoring integration
            monitoring_integration = self._configure_monitoring_integration(deployment_analysis)
            
            # Create environment strategy
            environment_strategy = self._create_environment_strategy(deployment_analysis)
            
            # Generate rollback procedures
            rollback_procedures = self._generate_rollback_procedures(deployment_analysis)
            
            # Create maintenance automation
            maintenance_automation = self._create_maintenance_automation(deployment_analysis)
            
            # Generate cost optimization strategies
            cost_optimization = self._generate_cost_optimization_strategies(deployment_analysis)
            
            # Create security hardening plan
            security_hardening = self._create_security_hardening_plan(deployment_analysis)
            
            # Design testing strategy
            testing_strategy = self._design_testing_strategy(deployment_analysis)
            
            return DeploymentPlan(
                system_name=deployment_analysis.get("system_name", "CrewAI System"),
                target_platform=deployment_analysis.get("target_platform", "Railway"),
                deployment_strategy=deployment_analysis.get("deployment_strategy", "Container deployment"),
                estimated_deployment_time=self._estimate_deployment_time(deployment_analysis),
                complexity_level=deployment_analysis.get("complexity_level", "moderate"),
                deployment_configuration=deployment_config,
                cicd_pipeline=cicd_pipeline,
                secrets_management=secrets_management,
                monitoring_integration=monitoring_integration,
                environment_strategy=environment_strategy,
                rollback_procedures=rollback_procedures,
                maintenance_automation=maintenance_automation,
                cost_optimization=cost_optimization,
                security_hardening=security_hardening,
                testing_strategy=testing_strategy,
                documentation_links=self._generate_documentation_links(deployment_analysis)
            )
        
        except Exception as e:
            # Fallback deployment plan for error cases
            return self._generate_fallback_deployment_plan(str(e))
    
    def _analyze_deployment_requirements(self, infrastructure_rec: Dict[str, Any], 
                                       documentation_plan: Dict[str, Any], 
                                       validated_code: str) -> Dict[str, Any]:
        """Analyze requirements to determine optimal deployment approach."""
        analysis = {
            "system_name": "CrewAI System",
            "target_platform": "Railway",
            "complexity_level": "moderate",
            "deployment_strategy": "Container deployment",
            "requires_database": False,
            "requires_scaling": False,
            "security_requirements": "standard",
            "team_experience": "intermediate"
        }
        
        # Extract from infrastructure recommendation
        if infrastructure_rec:
            analysis["system_name"] = infrastructure_rec.get("system_name", "CrewAI System")
            analysis["target_platform"] = infrastructure_rec.get("recommended_platform", "Railway")
            analysis["complexity_level"] = infrastructure_rec.get("system_complexity", "moderate")
            analysis["deployment_strategy"] = infrastructure_rec.get("deployment_strategy", "Container deployment")
            
            # Analyze platform evaluation for requirements
            platform_eval = infrastructure_rec.get("platform_evaluation", {})
            if isinstance(platform_eval, dict):
                min_skill = platform_eval.get("minimum_technical_skill", "intermediate")
                analysis["team_experience"] = min_skill
                
                setup_complexity = platform_eval.get("setup_complexity", "moderate")
                if setup_complexity == "complex":
                    analysis["requires_scaling"] = True
        
        # Extract from documentation plan
        if documentation_plan:
            complexity = documentation_plan.get("complexity_level", "moderate")
            analysis["complexity_level"] = complexity
            
            if complexity == "complex":
                analysis["requires_database"] = True
                analysis["requires_scaling"] = True
                analysis["security_requirements"] = "enhanced"
        
        # Analyze code for specific requirements
        if validated_code:
            # Check for database usage
            if any(db_term in validated_code.lower() for db_term in ["database", "sqlite", "postgres", "mongodb"]):
                analysis["requires_database"] = True
            
            # Check for API usage (suggests scaling needs)
            if "api" in validated_code.lower() and len(validated_code) > 5000:
                analysis["requires_scaling"] = True
        
        return analysis
    
    def _generate_deployment_configuration(self, deployment_analysis: Dict[str, Any]) -> DeploymentConfiguration:
        """Generate platform-specific deployment configuration."""
        platform = deployment_analysis.get("target_platform", "Railway")
        complexity = deployment_analysis.get("complexity_level", "moderate")
        requires_database = deployment_analysis.get("requires_database", False)
        
        # Generate Dockerfile
        dockerfile_content = self._generate_dockerfile(deployment_analysis)
        
        # Generate Docker Compose (if needed)
        docker_compose_content = ""
        if requires_database or complexity == "complex":
            docker_compose_content = self._generate_docker_compose(deployment_analysis)
        
        # Generate environment files
        environment_files = self._generate_environment_files(deployment_analysis)
        
        # Generate build scripts
        build_scripts = self._generate_build_scripts(deployment_analysis)
        
        # Generate platform-specific configuration
        platform_specific_config = self._generate_platform_specific_config(deployment_analysis)
        
        # Define resource requirements
        resource_requirements = self._define_resource_requirements(deployment_analysis)
        
        # Configure networking
        networking_config = self._configure_networking(deployment_analysis)
        
        # Configure scaling
        scaling_config = self._configure_scaling(deployment_analysis)
        
        return DeploymentConfiguration(
            platform=platform,
            deployment_type=self._determine_deployment_type(deployment_analysis),
            dockerfile_content=dockerfile_content,
            docker_compose_content=docker_compose_content,
            environment_files=environment_files,
            build_scripts=build_scripts,
            platform_specific_config=platform_specific_config,
            resource_requirements=resource_requirements,
            networking_config=networking_config,
            scaling_config=scaling_config
        )
    
    def _create_cicd_pipeline(self, deployment_analysis: Dict[str, Any], 
                             deployment_config: DeploymentConfiguration) -> CICDPipeline:
        """Create CI/CD pipeline configuration."""
        
        # Determine CI/CD platform based on target platform
        cicd_platform = self._determine_cicd_platform(deployment_analysis)
        
        # Generate pipeline file content
        pipeline_file = self._generate_pipeline_file(deployment_analysis, cicd_platform)
        
        # Define workflow name
        workflow_name = f"Deploy {deployment_analysis.get('system_name', 'CrewAI System')}"
        
        # Define trigger conditions
        trigger_conditions = [
            "Push to main branch",
            "Pull request to main branch",
            "Manual deployment trigger",
            "Scheduled deployment (optional)"
        ]
        
        # Define build stages
        build_stages = [
            "Code checkout and setup",
            "Install dependencies",
            "Run unit tests",
            "Run integration tests",
            "Security scanning",
            "Build Docker image",
            "Push to registry"
        ]
        
        # Define deployment stages
        deployment_stages = [
            "Deploy to development environment",
            "Run smoke tests",
            "Deploy to staging environment",
            "Run end-to-end tests",
            "Deploy to production (with approval)",
            "Post-deployment health checks"
        ]
        
        # Define environment promotions
        environment_promotions = {
            "development": "Automatic on feature branch push",
            "staging": "Automatic on main branch merge",
            "production": "Manual approval required"
        }
        
        # Define rollback strategy
        rollback_strategy = self._define_rollback_strategy(deployment_analysis)
        
        # Define security checks
        security_checks = [
            "Dependency vulnerability scanning",
            "Container image security scanning",
            "Secret detection and validation",
            "Code quality and security analysis"
        ]
        
        # Configure notifications
        notification_config = {
            "success": "Slack/email notification on successful deployment",
            "failure": "Immediate Slack/email alert on deployment failure",
            "approval": "Notification when manual approval required"
        }
        
        return CICDPipeline(
            platform=cicd_platform,
            pipeline_file=pipeline_file,
            workflow_name=workflow_name,
            trigger_conditions=trigger_conditions,
            build_stages=build_stages,
            deployment_stages=deployment_stages,
            environment_promotions=environment_promotions,
            rollback_strategy=rollback_strategy,
            security_checks=security_checks,
            notification_config=notification_config
        )
    
    def _setup_secrets_management(self, deployment_analysis: Dict[str, Any]) -> SecretsManagement:
        """Setup secrets and environment management configuration."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        # Determine secrets provider
        secrets_provider = self._determine_secrets_provider(platform)
        
        # Define environment separation
        environment_separation = {
            "development": ["DEV_API_KEYS", "DEV_DATABASE_URL", "DEV_DEBUG_MODE"],
            "staging": ["STAGING_API_KEYS", "STAGING_DATABASE_URL", "STAGING_LOG_LEVEL"],
            "production": ["PROD_API_KEYS", "PROD_DATABASE_URL", "PROD_MONITORING_KEYS"]
        }
        
        # Define rotation policy
        secret_rotation_policy = "API keys rotated quarterly, database credentials rotated annually, certificates auto-renewed"
        
        # Define access controls
        access_controls = [
            "Role-based access to different environment secrets",
            "Multi-factor authentication for production access",
            "Audit logging for all secret access",
            "Least privilege principle for service accounts"
        ]
        
        # Generate secret templates
        secret_templates = self._generate_secret_templates(deployment_analysis)
        
        # Define backup strategy
        backup_strategy = "Encrypted backups of secret configurations stored securely, recovery procedures documented"
        
        # Define compliance notes
        compliance_notes = [
            "Secrets never stored in code or version control",
            "Production secrets accessible only to authorized personnel",
            "Regular secret access audits and reviews",
            "Encryption in transit and at rest for all secrets"
        ]
        
        return SecretsManagement(
            platform=platform,
            secrets_provider=secrets_provider,
            environment_separation=environment_separation,
            secret_rotation_policy=secret_rotation_policy,
            access_controls=access_controls,
            secret_templates=secret_templates,
            backup_strategy=backup_strategy,
            compliance_notes=compliance_notes
        )
    
    def _configure_monitoring_integration(self, deployment_analysis: Dict[str, Any]) -> MonitoringIntegration:
        """Configure monitoring and observability integration."""
        platform = deployment_analysis.get("target_platform", "Railway")
        complexity = deployment_analysis.get("complexity_level", "moderate")
        
        # Determine monitoring stack
        monitoring_stack = self._determine_monitoring_stack(platform, complexity)
        
        # Define health checks
        health_checks = [
            "Application startup and readiness checks",
            "API endpoint health and response time monitoring",
            "Database connectivity and performance checks",
            "External API dependency health verification",
            "Resource utilization monitoring (CPU, memory, disk)"
        ]
        
        # Define alerting rules
        alerting_rules = [
            "Response time > 5 seconds for 95th percentile",
            "Error rate > 1% over 5 minutes",
            "CPU utilization > 80% for 10 minutes",
            "Memory utilization > 85% for 5 minutes",
            "Disk space < 20% remaining",
            "Failed health checks for 3 consecutive attempts"
        ]
        
        # Define log aggregation
        log_aggregation = self._define_log_aggregation(platform, monitoring_stack)
        
        # Define metrics collection
        metrics_collection = [
            "Request count and response times",
            "Error rates and types",
            "Resource utilization metrics",
            "Business metrics (API calls, user actions)",
            "Cost and billing metrics"
        ]
        
        # Generate dashboard configuration
        dashboard_config = self._generate_dashboard_config(deployment_analysis, monitoring_stack)
        
        # Define incident response
        incident_response = [
            "Automated scaling on high load",
            "Automatic restart on health check failures",
            "Escalation to on-call team for critical alerts",
            "Automated rollback on deployment health failures"
        ]
        
        # Define performance monitoring
        performance_monitoring = [
            "Application Performance Monitoring (APM) integration",
            "Real user monitoring for frontend performance",
            "Database query performance tracking",
            "API endpoint performance profiling"
        ]
        
        return MonitoringIntegration(
            monitoring_stack=monitoring_stack,
            health_checks=health_checks,
            alerting_rules=alerting_rules,
            log_aggregation=log_aggregation,
            metrics_collection=metrics_collection,
            dashboard_config=dashboard_config,
            incident_response=incident_response,
            performance_monitoring=performance_monitoring
        )
    
    def _create_environment_strategy(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Create environment setup and management strategy."""
        complexity = deployment_analysis.get("complexity_level", "moderate")
        
        if complexity == "simple":
            return [
                "Development: Local development with Docker Compose",
                "Production: Single environment with staging branch for testing",
                "Environment promotion: Direct deployment from main branch",
                "Configuration: Environment variables for simple configuration management"
            ]
        elif complexity == "complex":
            return [
                "Development: Local development with full service stack",
                "Testing: Automated testing environment for CI/CD pipelines",
                "Staging: Production-like environment for final validation",
                "Production: Multi-region production deployment with load balancing",
                "Environment promotion: Gated promotions with approval workflows",
                "Configuration: Advanced configuration management with feature flags",
                "Data management: Environment-specific databases with data seeding"
            ]
        else:
            return [
                "Development: Local development with Docker Compose",
                "Staging: Pre-production environment for testing and validation",
                "Production: Production environment with monitoring and alerting",
                "Environment promotion: Automated staging, manual production approval",
                "Configuration: Environment-specific variables and secrets management",
                "Database management: Separate databases per environment with migrations"
            ]
    
    def _generate_rollback_procedures(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Generate rollback and disaster recovery procedures."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        base_procedures = [
            "Automated rollback triggers on health check failures",
            "Manual rollback capability with single command",
            "Database migration rollback procedures",
            "Blue-green deployment for zero-downtime rollbacks"
        ]
        
        # Platform-specific rollback procedures
        if platform in ["AWS", "Google Cloud", "Azure"]:
            base_procedures.extend([
                "Infrastructure as Code rollback with Terraform/CloudFormation",
                "Load balancer traffic shifting for gradual rollbacks",
                "Auto-scaling group rollback with instance replacement",
                "DNS-based rollback for multi-region deployments"
            ])
        elif platform in ["Railway", "Render", "Fly.io"]:
            base_procedures.extend([
                "Platform-native rollback using previous deployment",
                "Environment variable rollback for configuration changes",
                "Quick redeployment from previous git commit",
                "Database backup restoration procedures"
            ])
        
        base_procedures.extend([
            "Incident response playbook with escalation procedures",
            "Communication plan for stakeholder notification",
            "Post-incident review and improvement process",
            "Regular disaster recovery testing and validation"
        ])
        
        return base_procedures
    
    def _create_maintenance_automation(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Create automated maintenance and update procedures."""
        return [
            "Automated dependency updates with security scanning",
            "Regular backup verification and integrity checks",
            "Log rotation and cleanup automation",
            "Performance monitoring and optimization alerts",
            "Security patch management and deployment",
            "Database maintenance and optimization tasks",
            "Cost monitoring and optimization recommendations",
            "Health check validation and maintenance",
            "SSL certificate renewal automation",
            "Monitoring and alerting system maintenance"
        ]
    
    def _generate_cost_optimization_strategies(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Generate deployment cost optimization strategies."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        base_strategies = [
            "Right-size resources based on actual usage patterns",
            "Implement auto-scaling to avoid over-provisioning",
            "Use platform free tiers effectively during development",
            "Monitor and set up billing alerts for cost control"
        ]
        
        # Platform-specific optimizations
        if platform in ["AWS", "Google Cloud", "Azure"]:
            base_strategies.extend([
                "Use reserved instances for predictable workloads",
                "Implement spot instances for development environments",
                "Optimize data transfer costs with CDN and caching",
                "Use managed services to reduce operational overhead"
            ])
        elif platform in ["Railway", "Render"]:
            base_strategies.extend([
                "Optimize container resource requests and limits",
                "Use sleep mode for development environments",
                "Implement efficient build caching strategies",
                "Monitor usage patterns for plan optimization"
            ])
        
        base_strategies.extend([
            "Regular cost analysis and optimization reviews",
            "Implement resource cleanup automation",
            "Use infrastructure as code for cost predictability",
            "Regular cost optimization training for the team"
        ])
        
        return base_strategies
    
    def _create_security_hardening_plan(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Create security hardening and best practices plan."""
        return [
            "Implement container security scanning in CI/CD pipeline",
            "Use non-root users in containers for reduced attack surface",
            "Enable network security groups and firewall rules",
            "Implement proper secret management and rotation",
            "Regular security updates and patch management",
            "Enable audit logging for all system access",
            "Implement secure communication with TLS/SSL encryption",
            "Use least privilege access principles",
            "Regular security assessments and penetration testing",
            "Incident response plan with security breach procedures",
            "Data encryption at rest and in transit",
            "Regular backup testing and disaster recovery validation"
        ]
    
    def _design_testing_strategy(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Design comprehensive testing strategy for deployments."""
        return [
            "Unit tests with code coverage requirements (>80%)",
            "Integration tests for API endpoints and services",
            "End-to-end tests for critical user workflows",
            "Performance tests for load and stress testing",
            "Security tests for vulnerability assessment",
            "Smoke tests for deployment validation",
            "Database migration tests for data integrity",
            "Disaster recovery tests for system resilience",
            "Monitoring and alerting validation tests",
            "User acceptance tests for business requirements"
        ]
    
    def _generate_dockerfile(self, deployment_analysis: Dict[str, Any]) -> str:
        """Generate optimized Dockerfile for the system."""
        return '''# Multi-stage build for optimized production image
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PIP_NO_CACHE_DIR=1 \\
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd --gid 1001 appgroup && \\
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["python", "main.py"]'''
    
    def _generate_docker_compose(self, deployment_analysis: Dict[str, Any]) -> str:
        """Generate Docker Compose configuration for multi-service setups."""
        requires_database = deployment_analysis.get("requires_database", False)
        
        compose_content = '''version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    depends_on:'''
        
        if requires_database:
            compose_content += '''
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${DATABASE_NAME}
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  postgres_data:'''
        else:
            compose_content += '''
      - redis
    volumes:
      - ./logs:/app/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  redis_data:'''
        
        return compose_content
    
    def _generate_environment_files(self, deployment_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate environment configuration files."""
        return {
            ".env.example": '''# API Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
PORT=8000

# Security Configuration
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# External Services
REDIS_URL=redis://localhost:6379''',
            
            ".env.development": '''# Development Environment
DEBUG=true
LOG_LEVEL=DEBUG
PORT=8000

# Use development APIs
OPENAI_API_KEY=dev_openai_key
DATABASE_URL=sqlite:///dev_database.db''',
            
            ".env.production": '''# Production Environment
DEBUG=false
LOG_LEVEL=INFO
PORT=8000

# Production APIs (set in deployment platform)
# OPENAI_API_KEY=prod_openai_key
# DATABASE_URL=postgresql://prod_db_url'''
        }
    
    def _generate_build_scripts(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Generate build and deployment scripts."""
        return [
            "#!/bin/bash\\n# build.sh - Build Docker image\\ndocker build -t ${IMAGE_NAME}:${VERSION} .",
            "#!/bin/bash\\n# deploy.sh - Deploy to production\\n./build.sh && docker push ${IMAGE_NAME}:${VERSION}",
            "#!/bin/bash\\n# test.sh - Run tests\\npython -m pytest tests/ --cov=. --cov-report=html",
            "#!/bin/bash\\n# setup.sh - Local setup\\ncp .env.example .env && docker-compose up -d"
        ]
    
    def _generate_platform_specific_config(self, deployment_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate platform-specific configuration files."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        configs = {}
        
        if platform == "Railway":
            configs["railway.json"] = '''{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "python main.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300
  }
}'''
        
        elif platform == "Render":
            configs["render.yaml"] = '''services:
  - type: web
    name: crewai-system
    env: docker
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health
    envVars:
      - key: PORT
        value: 8000'''
        
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            configs["kubernetes.yaml"] = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: crewai-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: crewai-system
  template:
    metadata:
      labels:
        app: crewai-system
    spec:
      containers:
      - name: app
        image: ${IMAGE_NAME}:${VERSION}
        ports:
        - containerPort: 8000
        env:
        - name: PORT
          value: "8000"'''
        
        return configs
    
    def _define_resource_requirements(self, deployment_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Define resource requirements based on system complexity."""
        complexity = deployment_analysis.get("complexity_level", "moderate")
        
        if complexity == "simple":
            return {
                "cpu": "0.5 vCPU",
                "memory": "1GB RAM",
                "storage": "10GB",
                "network": "100MB/s"
            }
        elif complexity == "complex":
            return {
                "cpu": "4 vCPUs",
                "memory": "8GB RAM", 
                "storage": "100GB",
                "network": "1GB/s"
            }
        else:
            return {
                "cpu": "1-2 vCPUs",
                "memory": "2-4GB RAM",
                "storage": "20-50GB", 
                "network": "500MB/s"
            }
    
    def _configure_networking(self, deployment_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Configure networking settings."""
        return {
            "port": "8000",
            "protocol": "HTTP/HTTPS",
            "load_balancer": "Platform-managed",
            "ssl": "Automatic SSL/TLS certificates",
            "dns": "Custom domain configuration",
            "cdn": "Optional CDN for static assets"
        }
    
    def _configure_scaling(self, deployment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Configure auto-scaling settings."""
        complexity = deployment_analysis.get("complexity_level", "moderate")
        
        if complexity == "simple":
            return {
                "min_instances": 1,
                "max_instances": 3,
                "scaling_triggers": ["CPU > 80%", "Memory > 85%"],
                "scaling_cooldown": "5 minutes"
            }
        elif complexity == "complex":
            return {
                "min_instances": 2,
                "max_instances": 20,
                "scaling_triggers": ["CPU > 70%", "Memory > 80%", "Request queue > 100"],
                "scaling_cooldown": "2 minutes"
            }
        else:
            return {
                "min_instances": 1,
                "max_instances": 10,
                "scaling_triggers": ["CPU > 75%", "Memory > 85%"],
                "scaling_cooldown": "3 minutes"
            }
    
    def _determine_deployment_type(self, deployment_analysis: Dict[str, Any]) -> str:
        """Determine the deployment type based on platform and requirements."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        if platform in ["AWS Lambda", "Vercel", "Netlify"]:
            return "serverless"
        elif platform in ["AWS", "Google Cloud", "Azure"] and deployment_analysis.get("complexity_level") == "complex":
            return "kubernetes"
        else:
            return "container"
    
    def _determine_cicd_platform(self, deployment_analysis: Dict[str, Any]) -> str:
        """Determine the best CI/CD platform."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        # Platform-native CI/CD when available
        if platform in ["Railway", "Render", "Fly.io"]:
            return "github_actions"  # Most compatible
        elif platform == "Azure":
            return "azure_devops"
        else:
            return "github_actions"  # Default choice
    
    def _generate_pipeline_file(self, deployment_analysis: Dict[str, Any], cicd_platform: str) -> str:
        """Generate CI/CD pipeline file content."""
        if cicd_platform == "github_actions":
            return '''name: Deploy CrewAI System

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ --cov=. --cov-report=xml
    
    - name: Security scan
      run: |
        pip install safety bandit
        safety check
        bandit -r . -x tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to Railway
      uses: bervProject/railway-deploy@v1.0.0
      with:
        railway_token: ${{ secrets.RAILWAY_TOKEN }}
        service: ${{ secrets.RAILWAY_SERVICE }}'''
        
        elif cicd_platform == "azure_devops":
            return '''trigger:
- main
- develop

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Test
  jobs:
  - job: RunTests
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.11'
    
    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
      displayName: 'Install dependencies'
    
    - script: |
        python -m pytest tests/ --junitxml=test-results.xml
      displayName: 'Run tests'

- stage: Deploy
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  jobs:
  - deployment: DeployProduction
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploy to production"'''
        
        else:  # gitlab_ci
            return '''stages:
  - test
  - deploy

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python -m pytest tests/ --cov=.
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

deploy:
  stage: deploy
  script:
    - echo "Deploy to production"
  only:
    - main'''
    
    def _determine_secrets_provider(self, platform: str) -> str:
        """Determine the best secrets management provider for the platform."""
        if platform in ["Railway", "Render", "Fly.io"]:
            return "platform_native"
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            return "cloud_native"
        else:
            return "environment_variables"
    
    def _generate_secret_templates(self, deployment_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate secret management templates."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        if platform == "Railway":
            return {
                "railway_secrets.sh": '''#!/bin/bash
# Set Railway environment variables
railway variables set OPENAI_API_KEY=$OPENAI_API_KEY
railway variables set DATABASE_URL=$DATABASE_URL
railway variables set SECRET_KEY=$SECRET_KEY'''
            }
        else:
            return {
                "secrets.yaml": '''# Kubernetes secrets template
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  openai-api-key: <base64-encoded-key>
  database-url: <base64-encoded-url>'''
            }
    
    def _determine_monitoring_stack(self, platform: str, complexity: str) -> str:
        """Determine the best monitoring stack for the platform and complexity."""
        if platform in ["Railway", "Render", "Fly.io"]:
            return "platform_native"
        elif complexity == "complex":
            return "prometheus_grafana"
        else:
            return "simple_monitoring"
    
    def _define_log_aggregation(self, platform: str, monitoring_stack: str) -> str:
        """Define log aggregation strategy."""
        if platform in ["AWS", "Google Cloud", "Azure"]:
            return "Cloud-native log aggregation with retention policies and search capabilities"
        else:
            return "Platform-integrated logging with structured log formatting"
    
    def _generate_dashboard_config(self, deployment_analysis: Dict[str, Any], monitoring_stack: str) -> str:
        """Generate monitoring dashboard configuration."""
        return '''# Monitoring Dashboard Configuration
- System Health Overview
- Response Time and Throughput
- Error Rates and Types
- Resource Utilization (CPU, Memory, Disk)
- API Endpoint Performance
- Database Performance
- Cost and Billing Metrics
- Security and Compliance Status'''
    
    def _define_rollback_strategy(self, deployment_analysis: Dict[str, Any]) -> str:
        """Define rollback strategy based on platform and complexity."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        if platform in ["Railway", "Render"]:
            return "Platform-native rollback to previous deployment with health check validation"
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            return "Blue-green deployment with automated traffic shifting and health monitoring"
        else:
            return "Git-based rollback with automated redeployment and validation"
    
    def _estimate_deployment_time(self, deployment_analysis: Dict[str, Any]) -> str:
        """Estimate time required for deployment setup."""
        complexity = deployment_analysis.get("complexity_level", "moderate")
        platform = deployment_analysis.get("target_platform", "Railway")
        
        # Base time estimates
        if complexity == "simple":
            base_hours = 2
        elif complexity == "complex":
            base_hours = 8
        else:
            base_hours = 4
        
        # Platform adjustments
        if platform in ["Railway", "Render"]:
            base_hours *= 0.5  # Easier platforms
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            base_hours *= 1.5  # More complex platforms
        
        hours = int(base_hours)
        
        if hours <= 4:
            return f"{hours} hours"
        elif hours <= 16:
            return f"{hours // 4} days"
        else:
            return f"{hours // 8} business days"
    
    def _generate_documentation_links(self, deployment_analysis: Dict[str, Any]) -> List[str]:
        """Generate relevant documentation links."""
        platform = deployment_analysis.get("target_platform", "Railway")
        
        base_links = [
            "Docker containerization best practices",
            "CI/CD pipeline troubleshooting guide",
            "Secrets management security guidelines",
            "Monitoring and alerting setup instructions"
        ]
        
        # Platform-specific documentation
        if platform == "Railway":
            base_links.extend([
                "Railway deployment documentation",
                "Railway environment variables guide",
                "Railway monitoring and logs"
            ])
        elif platform == "AWS":
            base_links.extend([
                "AWS ECS deployment guide",
                "AWS CloudWatch monitoring setup",
                "AWS IAM security best practices"
            ])
        
        return base_links
    
    def _generate_fallback_deployment_plan(self, error_message: str) -> DeploymentPlan:
        """Generate a safe fallback deployment plan when errors occur."""
        
        # Safe fallback deployment configuration
        fallback_deployment_config = DeploymentConfiguration(
            platform="Railway",
            deployment_type="container",
            dockerfile_content="# Basic Dockerfile\nFROM python:3.11-slim\nCOPY . /app\nWORKDIR /app\nRUN pip install -r requirements.txt\nCMD python main.py",
            docker_compose_content="",
            environment_files={".env.example": "# Basic environment\nOPENAI_API_KEY=your_key_here\nPORT=8000"},
            build_scripts=["docker build -t app .", "docker run -p 8000:8000 app"],
            platform_specific_config={"railway.json": '{"build": {"builder": "DOCKERFILE"}}'},
            resource_requirements={"cpu": "1 vCPU", "memory": "2GB", "storage": "20GB"},
            networking_config={"port": "8000", "protocol": "HTTP"},
            scaling_config={"min_instances": 1, "max_instances": 5}
        )
        
        # Safe fallback CI/CD pipeline
        fallback_cicd = CICDPipeline(
            platform="github_actions",
            pipeline_file="# Basic GitHub Actions\nname: Deploy\non: [push]\njobs:\n  deploy:\n    runs-on: ubuntu-latest\n    steps:\n    - uses: actions/checkout@v4",
            workflow_name="Deploy CrewAI System",
            trigger_conditions=["Push to main branch"],
            build_stages=["Install dependencies", "Run tests", "Build image"],
            deployment_stages=["Deploy to production"],
            environment_promotions={"production": "Manual approval"},
            rollback_strategy="Manual rollback to previous deployment",
            security_checks=["Basic security scanning"],
            notification_config={"failure": "Email on deployment failure"}
        )
        
        # Safe fallback secrets management
        fallback_secrets = SecretsManagement(
            platform="Railway",
            secrets_provider="platform_native",
            environment_separation={"production": ["API_KEYS", "DATABASE_URL"]},
            secret_rotation_policy="Manual rotation as needed",
            access_controls=["Environment-based access"],
            secret_templates={".env": "# Environment variables\nAPI_KEY=value"},
            backup_strategy="Manual backup of environment configuration",
            compliance_notes=["Basic security practices"]
        )
        
        # Safe fallback monitoring
        fallback_monitoring = MonitoringIntegration(
            monitoring_stack="platform_native",
            health_checks=["Basic application health check"],
            alerting_rules=["High error rate alert"],
            log_aggregation="Platform logging",
            metrics_collection=["Basic performance metrics"],
            dashboard_config="Platform dashboard",
            incident_response=["Manual incident response"],
            performance_monitoring=["Basic performance tracking"]
        )
        
        return DeploymentPlan(
            system_name="CrewAI System",
            target_platform="Railway",
            deployment_strategy="Container deployment",
            estimated_deployment_time="2-4 hours",
            complexity_level="simple",
            deployment_configuration=fallback_deployment_config,
            cicd_pipeline=fallback_cicd,
            secrets_management=fallback_secrets,
            monitoring_integration=fallback_monitoring,
            environment_strategy=["Development and production environments"],
            rollback_procedures=["Manual rollback procedures"],
            maintenance_automation=["Basic maintenance tasks"],
            cost_optimization=["Monitor usage and costs"],
            security_hardening=["Basic security practices"],
            testing_strategy=["Unit and integration tests"],
            documentation_links=["Basic deployment documentation"]
        )
    
    def _build_deployment_patterns(self) -> Dict[str, Any]:
        """Build deployment pattern knowledge base."""
        return {
            "container": {
                "description": "Docker containerized deployment",
                "suitable_for": ["Most applications", "Microservices", "Cloud-native apps"],
                "complexity": "moderate",
                "scalability": "high",
                "portability": "excellent"
            },
            "serverless": {
                "description": "Function-as-a-Service deployment",
                "suitable_for": ["Event-driven apps", "APIs", "Batch processing"],
                "complexity": "low",
                "scalability": "automatic",
                "portability": "limited"
            },
            "kubernetes": {
                "description": "Kubernetes orchestrated deployment",
                "suitable_for": ["Complex applications", "Microservices", "Enterprise"],
                "complexity": "high",
                "scalability": "excellent",
                "portability": "good"
            }
        }
    
    def _build_cicd_templates(self) -> Dict[str, Any]:
        """Build CI/CD template knowledge base."""
        return {
            "github_actions": {
                "file_name": ".github/workflows/deploy.yml",
                "features": ["Matrix builds", "Secrets management", "Artifact storage"],
                "integration": "Excellent with GitHub repositories"
            },
            "azure_devops": {
                "file_name": "azure-pipelines.yml",
                "features": ["Multi-stage pipelines", "Environments", "Approvals"],
                "integration": "Best for Azure deployments"
            },
            "gitlab_ci": {
                "file_name": ".gitlab-ci.yml",
                "features": ["Auto DevOps", "Security scanning", "Review apps"],
                "integration": "Integrated with GitLab repositories"
            }
        }
    
    def _build_platform_configurations(self) -> Dict[str, Any]:
        """Build platform-specific configuration knowledge."""
        return {
            "railway": {
                "config_files": ["railway.json", "Procfile"],
                "features": ["Git-based deployment", "Auto-scaling", "Environment variables"],
                "monitoring": "Built-in metrics and logs"
            },
            "render": {
                "config_files": ["render.yaml", "Dockerfile"],
                "features": ["Auto-deploy", "Preview environments", "Health checks"],
                "monitoring": "Integrated monitoring dashboard"
            },
            "aws": {
                "config_files": ["task-definition.json", "service.yaml"],
                "features": ["ECS", "Lambda", "Auto-scaling", "Load balancing"],
                "monitoring": "CloudWatch integration"
            }
        }


def create_deployment_engineer() -> DeploymentEngineer:
    """Factory function to create a DeploymentEngineer instance."""
    return DeploymentEngineer()
