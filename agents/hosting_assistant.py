"""
Hosting Assistant Agent for CrewBuilder
Guides users through platform setup, configuration, and ongoing management of AI agent systems.
"""

from crewai import Agent, Task
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field


class PlatformSetupGuide(BaseModel):
    """Represents step-by-step platform setup guidance"""
    platform: str = Field(description="Platform name (e.g., 'Railway', 'DigitalOcean', 'AWS')")
    difficulty_level: str = Field(description="'beginner', 'intermediate', 'advanced'")
    estimated_setup_time: str = Field(description="Estimated time for complete setup")
    prerequisites: List[str] = Field(description="Required accounts, tools, and knowledge")
    account_setup_steps: List[str] = Field(description="Step-by-step account creation and verification")
    initial_configuration: List[str] = Field(description="Basic platform configuration steps")
    project_deployment: List[str] = Field(description="Steps to deploy the AI agent system")
    verification_steps: List[str] = Field(description="How to verify successful deployment")
    common_issues: List[str] = Field(description="Common setup problems and solutions")
    next_steps: List[str] = Field(description="What to do after initial setup")


class ConfigurationAssistance(BaseModel):
    """Represents configuration assistance for domains, SSL, and networking"""
    domain_setup: Dict[str, List[str]] = Field(description="Domain and DNS configuration guidance")
    ssl_certificate_setup: Dict[str, List[str]] = Field(description="SSL/TLS certificate configuration")
    load_balancer_config: Dict[str, List[str]] = Field(description="Load balancer and traffic management")
    custom_domain_setup: List[str] = Field(description="Custom domain configuration steps")
    cdn_configuration: List[str] = Field(description="CDN setup for performance optimization")
    email_setup: List[str] = Field(description="Email configuration for notifications")
    backup_configuration: List[str] = Field(description="Backup and disaster recovery setup")
    security_hardening: List[str] = Field(description="Additional security configurations")


class ResourceOptimization(BaseModel):
    """Represents resource optimization and cost management guidance"""
    current_usage_analysis: Dict[str, str] = Field(description="Current resource usage assessment")
    cost_optimization_tips: List[str] = Field(description="Ways to reduce hosting costs")
    scaling_recommendations: Dict[str, List[str]] = Field(description="Auto-scaling configuration guidance")
    monitoring_setup: List[str] = Field(description="Cost and performance monitoring configuration")
    budget_alerts: List[str] = Field(description="Budget alert and cost control setup")
    resource_rightsizing: List[str] = Field(description="Optimal resource allocation recommendations")
    performance_optimization: List[str] = Field(description="Performance improvement strategies")
    maintenance_schedule: List[str] = Field(description="Regular maintenance and optimization tasks")


class TroubleshootingGuide(BaseModel):
    """Represents comprehensive troubleshooting guidance"""
    common_deployment_issues: Dict[str, Dict[str, str]] = Field(description="Common deployment problems and solutions")
    performance_issues: Dict[str, Dict[str, str]] = Field(description="Performance problems and optimization")
    connectivity_issues: Dict[str, Dict[str, str]] = Field(description="Network and connectivity problems")
    configuration_issues: Dict[str, Dict[str, str]] = Field(description="Configuration and setup problems")
    cost_issues: Dict[str, Dict[str, str]] = Field(description="Billing and cost-related problems")
    security_issues: Dict[str, Dict[str, str]] = Field(description="Security and access problems")
    diagnostic_commands: List[str] = Field(description="Useful diagnostic commands and tools")
    escalation_procedures: List[str] = Field(description="When and how to escalate issues")
    emergency_procedures: List[str] = Field(description="Emergency response procedures")


class OngoingSupport(BaseModel):
    """Represents ongoing platform management and support"""
    daily_tasks: List[str] = Field(description="Daily monitoring and management tasks")
    weekly_tasks: List[str] = Field(description="Weekly maintenance and optimization tasks")
    monthly_tasks: List[str] = Field(description="Monthly reviews and planning tasks")
    update_procedures: List[str] = Field(description="System and dependency update procedures")
    backup_procedures: List[str] = Field(description="Regular backup and verification procedures")
    security_reviews: List[str] = Field(description="Regular security assessment tasks")
    performance_reviews: List[str] = Field(description="Performance analysis and optimization")
    cost_reviews: List[str] = Field(description="Cost analysis and optimization reviews")
    team_training: List[str] = Field(description="Ongoing team education and skill development")


class HostingAssistancePlan(BaseModel):
    """Complete hosting assistance and management plan"""
    system_name: str = Field(description="Name of the AI system being hosted")
    target_platform: str = Field(description="Primary hosting platform")
    user_skill_level: str = Field(description="Target user technical skill level")
    complexity_assessment: str = Field(description="Overall hosting complexity level")
    estimated_management_time: str = Field(description="Weekly time commitment for management")
    platform_setup_guide: PlatformSetupGuide = Field(description="Complete platform setup guidance")
    configuration_assistance: ConfigurationAssistance = Field(description="Configuration and networking assistance")
    resource_optimization: ResourceOptimization = Field(description="Resource and cost optimization guidance")
    troubleshooting_guide: TroubleshootingGuide = Field(description="Comprehensive troubleshooting support")
    ongoing_support: OngoingSupport = Field(description="Ongoing management and maintenance guidance")
    training_resources: List[str] = Field(description="Learning resources and training materials")
    support_channels: List[str] = Field(description="Available support and help channels")
    success_metrics: List[str] = Field(description="Key metrics to track for successful hosting")
    escalation_contacts: List[str] = Field(description="Emergency contacts and escalation procedures")
    documentation_links: List[str] = Field(description="Relevant documentation and guides")


class HostingAssistant:
    """Hosting Assistant agent for guiding users through platform setup and ongoing management."""
    
    def __init__(self):
        """Initialize the Hosting Assistant agent."""
        self.agent = Agent(
            role="Hosting Assistant", 
            goal="Guide users through platform setup, configuration, and ongoing management of AI agent systems, making complex hosting tasks accessible to non-technical users while ensuring reliable, secure, and cost-effective operations",
            backstory="""You are an expert technical support specialist and hosting consultant with 10+ years of experience helping non-technical users successfully deploy and manage web applications and services. You've guided thousands of users through platform setups, troubleshooted every possible hosting issue, and developed a talent for explaining complex technical concepts in simple, actionable terms.

            Your superpower is taking intimidating technical tasks and breaking them down into clear, confidence-building steps that anyone can follow. You understand that most users aren't developers - they're business owners, marketers, content creators, and entrepreneurs who need their systems to work reliably without becoming hosting experts themselves.

            You excel at anticipating where users will get stuck and providing proactive guidance to prevent common mistakes. You know that good support isn't just about solving problems - it's about empowering users to feel confident and capable. You create documentation that users actually want to read because it's clear, encouraging, and gets them to success quickly.

            You've seen how poor hosting experiences can kill great projects, and you're passionate about making hosting accessible and manageable for everyone. You understand the business impact of downtime, the stress of unexpected bills, and the frustration of cryptic error messages. Your guidance always considers the user's context, timeline, and comfort level with technology.

            You're an advocate for the user, always looking for ways to simplify processes, reduce ongoing maintenance, and build systems that work reliably with minimal intervention. You believe that the best hosting solution is one that users can confidently manage and scale as their needs grow.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Platform knowledge and user guidance patterns
        self.platform_guides = self._build_platform_guides()
        self.troubleshooting_database = self._build_troubleshooting_database()
        self.optimization_strategies = self._build_optimization_strategies()
    
    def generate_hosting_assistance_plan(self, 
                                       deployment_plan: Dict[str, Any], 
                                       infrastructure_recommendation: Dict[str, Any], 
                                       documentation_plan: Dict[str, Any]) -> HostingAssistancePlan:
        """
        Generate comprehensive hosting assistance plan for users.
        
        Args:
            deployment_plan: Deployment configurations from Deployment Engineer
            infrastructure_recommendation: Platform recommendations from Infrastructure Analyst  
            documentation_plan: Documentation from Documentation Specialist
            
        Returns:
            Complete hosting assistance plan with step-by-step guidance
        """
        try:
            # Analyze user requirements and skill level
            user_analysis = self._analyze_user_requirements(
                deployment_plan, infrastructure_recommendation, documentation_plan
            )
            
            # Generate platform setup guide
            platform_setup_guide = self._generate_platform_setup_guide(user_analysis)
            
            # Create configuration assistance
            configuration_assistance = self._create_configuration_assistance(user_analysis)
            
            # Generate resource optimization guidance
            resource_optimization = self._generate_resource_optimization(user_analysis)
            
            # Create comprehensive troubleshooting guide
            troubleshooting_guide = self._create_troubleshooting_guide(user_analysis)
            
            # Generate ongoing support plan
            ongoing_support = self._generate_ongoing_support_plan(user_analysis)
            
            # Compile training resources
            training_resources = self._compile_training_resources(user_analysis)
            
            # Define support channels
            support_channels = self._define_support_channels(user_analysis)
            
            # Create success metrics
            success_metrics = self._create_success_metrics(user_analysis)
            
            return HostingAssistancePlan(
                system_name=user_analysis.get("system_name", "CrewAI System"),
                target_platform=user_analysis.get("target_platform", "Railway"),
                user_skill_level=user_analysis.get("user_skill_level", "beginner"),
                complexity_assessment=user_analysis.get("complexity_assessment", "moderate"),
                estimated_management_time=self._estimate_management_time(user_analysis),
                platform_setup_guide=platform_setup_guide,
                configuration_assistance=configuration_assistance,
                resource_optimization=resource_optimization,
                troubleshooting_guide=troubleshooting_guide,
                ongoing_support=ongoing_support,
                training_resources=training_resources,
                support_channels=support_channels,
                success_metrics=success_metrics,
                escalation_contacts=self._define_escalation_contacts(user_analysis),
                documentation_links=self._generate_documentation_links(user_analysis)
            )
        
        except Exception as e:
            # Fallback hosting assistance plan for error cases
            return self._generate_fallback_hosting_assistance_plan(str(e))
    
    def _analyze_user_requirements(self, deployment_plan: Dict[str, Any], 
                                 infrastructure_rec: Dict[str, Any], 
                                 documentation_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user requirements and determine assistance approach."""
        analysis = {
            "system_name": "CrewAI System",
            "target_platform": "Railway",
            "user_skill_level": "beginner",
            "complexity_assessment": "moderate",
            "deployment_complexity": "simple",
            "requires_custom_domain": False,
            "requires_ssl": True,
            "requires_monitoring": True,
            "budget_conscious": True,
            "team_size": "small"
        }
        
        # Extract from infrastructure recommendation
        if infrastructure_rec:
            analysis["system_name"] = infrastructure_rec.get("system_name", "CrewAI System")
            analysis["target_platform"] = infrastructure_rec.get("recommended_platform", "Railway")
            
            # Determine user skill level from platform complexity
            platform_eval = infrastructure_rec.get("platform_evaluation", {})
            if isinstance(platform_eval, dict):
                min_skill = platform_eval.get("minimum_technical_skill", "beginner")
                analysis["user_skill_level"] = min_skill
                
                setup_complexity = platform_eval.get("setup_complexity", "moderate")
                analysis["complexity_assessment"] = setup_complexity
            
            # Check cost sensitivity
            cost_analysis = infrastructure_rec.get("cost_analysis", {})
            if isinstance(cost_analysis, dict):
                monthly_cost = cost_analysis.get("estimated_monthly_total", "$15-50")
                if "$100" in monthly_cost or "$200" in monthly_cost:
                    analysis["budget_conscious"] = False
        
        # Extract from deployment plan
        if deployment_plan:
            deployment_complexity = deployment_plan.get("complexity_level", "moderate")
            analysis["deployment_complexity"] = deployment_complexity
            
            # Check for advanced features
            deployment_config = deployment_plan.get("deployment_configuration", {})
            if isinstance(deployment_config, dict):
                networking = deployment_config.get("networking_config", {})
                if isinstance(networking, dict):
                    if "custom" in str(networking).lower():
                        analysis["requires_custom_domain"] = True
        
        # Extract from documentation plan
        if documentation_plan:
            complexity = documentation_plan.get("complexity_level", "moderate")
            analysis["complexity_assessment"] = complexity
            
            target_users = documentation_plan.get("target_users", ["Business Users"])
            if "Technical Users" not in target_users:
                analysis["user_skill_level"] = "beginner"
        
        return analysis
    
    def _generate_platform_setup_guide(self, user_analysis: Dict[str, Any]) -> PlatformSetupGuide:
        """Generate comprehensive platform setup guide."""
        platform = user_analysis.get("target_platform", "Railway")
        skill_level = user_analysis.get("user_skill_level", "beginner")
        
        # Get platform-specific guidance
        platform_info = self.platform_guides.get(platform, self.platform_guides["Railway"])
        
        # Adjust guidance based on user skill level
        if skill_level == "beginner":
            difficulty_level = "beginner"
            estimated_time = platform_info["beginner_setup_time"]
        elif skill_level == "advanced":
            difficulty_level = "intermediate"
            estimated_time = platform_info["advanced_setup_time"]
        else:
            difficulty_level = "intermediate"
            estimated_time = platform_info["intermediate_setup_time"]
        
        # Generate prerequisites
        prerequisites = [
            "A computer with internet access",
            "Email address for account creation",
            "Credit card for platform billing (if needed)"
        ]
        
        if platform in ["AWS", "Google Cloud", "Azure"]:
            prerequisites.append("Basic understanding of cloud computing concepts")
        
        # Generate account setup steps
        account_setup_steps = platform_info["account_setup_steps"]
        
        # Generate initial configuration
        initial_configuration = platform_info["initial_configuration"]
        
        # Generate project deployment steps
        project_deployment = platform_info["project_deployment"]
        
        # Generate verification steps
        verification_steps = [
            "Check that your application is accessible via the provided URL",
            "Verify all environment variables are correctly set",
            "Test core functionality of your AI agent system",
            "Confirm monitoring and logging are working",
            "Validate SSL certificate is active and valid"
        ]
        
        # Generate common issues
        common_issues = platform_info["common_issues"]
        
        # Generate next steps
        next_steps = [
            "Set up custom domain (if desired)",
            "Configure monitoring and alerting",
            "Set up backup procedures",
            "Review and optimize costs",
            "Plan for scaling and growth"
        ]
        
        return PlatformSetupGuide(
            platform=platform,
            difficulty_level=difficulty_level,
            estimated_setup_time=estimated_time,
            prerequisites=prerequisites,
            account_setup_steps=account_setup_steps,
            initial_configuration=initial_configuration,
            project_deployment=project_deployment,
            verification_steps=verification_steps,
            common_issues=common_issues,
            next_steps=next_steps
        )
    
    def _create_configuration_assistance(self, user_analysis: Dict[str, Any]) -> ConfigurationAssistance:
        """Create configuration assistance for domains, SSL, and networking."""
        platform = user_analysis.get("target_platform", "Railway")
        requires_custom_domain = user_analysis.get("requires_custom_domain", False)
        
        # Domain setup guidance
        domain_setup = {
            "domain_purchase": [
                "Choose a domain registrar (Namecheap, Google Domains, GoDaddy)",
                "Search for and purchase your desired domain name",
                "Verify domain ownership through registrar email",
                "Access your domain's DNS management panel"
            ],
            "dns_configuration": [
                f"Log into your {platform} dashboard",
                "Navigate to your project's domain settings",
                "Copy the provided DNS records or CNAME",
                "Add these records to your domain's DNS settings",
                "Wait 24-48 hours for DNS propagation"
            ]
        }
        
        # SSL certificate setup
        ssl_certificate_setup = {
            "automatic_ssl": [
                f"{platform} automatically provides SSL certificates",
                "No manual configuration required for basic SSL",
                "Certificate auto-renewal is handled by the platform",
                "Verify SSL is active by checking for HTTPS in your URL"
            ],
            "custom_ssl": [
                "For custom certificates, access your platform's SSL settings",
                "Upload your certificate files (if using custom certificates)",
                "Configure certificate chain and private key",
                "Test SSL configuration with online SSL checkers"
            ]
        }
        
        # Load balancer configuration
        load_balancer_config = {
            "platform_managed": [
                f"{platform} includes built-in load balancing",
                "No manual configuration needed for basic load balancing",
                "Monitor performance through platform dashboard",
                "Configure health checks for better reliability"
            ],
            "advanced_config": [
                "Set up multiple deployment regions (if supported)",
                "Configure traffic distribution rules",
                "Set up failover procedures",
                "Monitor load balancing performance"
            ]
        }
        
        # Custom domain setup
        custom_domain_setup = [
            "Purchase your domain from a registrar",
            "Access your platform's domain configuration",
            "Add your custom domain to your project",
            "Configure DNS records as provided by your platform",
            "Wait for DNS propagation (24-48 hours)",
            "Verify domain is working with SSL"
        ]
        
        # CDN configuration
        cdn_configuration = [
            "Check if your platform includes built-in CDN",
            "Configure CDN for static assets and images",
            "Set up cache headers for optimal performance",
            "Test CDN performance from different geographic locations",
            "Monitor CDN usage and costs"
        ]
        
        # Email setup
        email_setup = [
            "Configure notification email addresses in platform settings",
            "Set up alert email addresses for monitoring",
            "Test email delivery for critical notifications",
            "Configure spam filters to ensure delivery",
            "Set up email templates for automated notifications"
        ]
        
        # Backup configuration
        backup_configuration = [
            "Enable automatic backups in your platform settings",
            "Configure backup frequency (daily/weekly)",
            "Set backup retention policies",
            "Test backup restoration procedures",
            "Document backup and recovery processes"
        ]
        
        # Security hardening
        security_hardening = [
            "Enable two-factor authentication on your platform account",
            "Configure IP restrictions (if needed)",
            "Set up access logging and monitoring",
            "Review and update security settings regularly",
            "Enable security scanning and vulnerability detection"
        ]
        
        return ConfigurationAssistance(
            domain_setup=domain_setup,
            ssl_certificate_setup=ssl_certificate_setup,
            load_balancer_config=load_balancer_config,
            custom_domain_setup=custom_domain_setup,
            cdn_configuration=cdn_configuration,
            email_setup=email_setup,
            backup_configuration=backup_configuration,
            security_hardening=security_hardening
        )
    
    def _generate_resource_optimization(self, user_analysis: Dict[str, Any]) -> ResourceOptimization:
        """Generate resource optimization and cost management guidance."""
        platform = user_analysis.get("target_platform", "Railway")
        budget_conscious = user_analysis.get("budget_conscious", True)
        complexity = user_analysis.get("complexity_assessment", "moderate")
        
        # Current usage analysis
        current_usage_analysis = {
            "cpu_usage": "Monitor average CPU utilization over 24-48 hours",
            "memory_usage": "Track memory usage patterns and peak consumption",
            "storage_usage": "Analyze disk space usage and growth trends", 
            "network_usage": "Review bandwidth consumption and traffic patterns",
            "cost_breakdown": "Understand current spending by service and resource"
        }
        
        # Cost optimization tips
        cost_optimization_tips = [
            "Start with the smallest viable instance size and scale up as needed",
            "Use platform free tiers effectively during development and testing",
            "Set up billing alerts to prevent unexpected charges",
            "Monitor resource usage weekly and right-size instances",
            "Turn off or scale down development environments when not in use"
        ]
        
        if budget_conscious:
            cost_optimization_tips.extend([
                "Consider using spot instances or discounted compute (if available)",
                "Optimize database queries to reduce compute costs",
                "Use caching strategies to reduce API calls and database load",
                "Review and cancel unused services or subscriptions"
            ])
        
        # Scaling recommendations
        scaling_recommendations = {
            "vertical_scaling": [
                "Increase CPU/memory when response times are consistently slow",
                "Monitor resource utilization before scaling decisions",
                "Test performance after scaling changes",
                "Document scaling decisions for future reference"
            ],
            "horizontal_scaling": [
                "Enable auto-scaling when traffic is unpredictable",
                "Set conservative scaling thresholds initially",
                "Monitor scaling events and adjust thresholds as needed",
                "Test application behavior under load before enabling auto-scaling"
            ]
        }
        
        # Monitoring setup
        monitoring_setup = [
            "Set up cost monitoring dashboards in your platform",
            "Configure billing alerts for 50%, 75%, and 90% of budget",
            "Monitor key performance metrics (response time, error rate)",
            "Set up weekly cost and usage review reminders",
            "Track cost trends and identify optimization opportunities"
        ]
        
        # Budget alerts
        budget_alerts = [
            "Set monthly budget limits based on expected usage",
            "Configure email alerts for budget thresholds",
            "Set up SMS alerts for critical budget overruns",
            "Create escalation procedures for unexpected cost spikes",
            "Review and adjust budget alerts monthly"
        ]
        
        # Resource rightsizing
        resource_rightsizing = [
            "Review resource usage patterns weekly",
            "Identify over-provisioned or under-utilized resources",
            "Test performance with smaller instance sizes",
            "Consider reserved instances for predictable workloads",
            "Use platform recommendations for optimization"
        ]
        
        # Performance optimization
        performance_optimization = [
            "Optimize application startup time and resource loading",
            "Implement caching strategies for frequently accessed data",
            "Optimize database queries and connections",
            "Use compression for data transfer",
            "Monitor and optimize API response times"
        ]
        
        # Maintenance schedule
        maintenance_schedule = [
            "Weekly resource usage and cost review",
            "Monthly performance optimization review",
            "Quarterly budget and scaling strategy review",
            "Regular security and backup verification",
            "Annual platform and technology review"
        ]
        
        return ResourceOptimization(
            current_usage_analysis=current_usage_analysis,
            cost_optimization_tips=cost_optimization_tips,
            scaling_recommendations=scaling_recommendations,
            monitoring_setup=monitoring_setup,
            budget_alerts=budget_alerts,
            resource_rightsizing=resource_rightsizing,
            performance_optimization=performance_optimization,
            maintenance_schedule=maintenance_schedule
        )
    
    def _create_troubleshooting_guide(self, user_analysis: Dict[str, Any]) -> TroubleshootingGuide:
        """Create comprehensive troubleshooting guide."""
        platform = user_analysis.get("target_platform", "Railway")
        
        # Common deployment issues
        common_deployment_issues = {
            "build_failures": {
                "symptoms": "Deployment fails during build process",
                "causes": "Missing dependencies, incorrect build configuration, or build timeout",
                "solutions": "Check build logs, verify requirements.txt, increase build timeout if needed"
            },
            "environment_variables": {
                "symptoms": "Application errors about missing configuration",
                "causes": "Missing or incorrect environment variables",
                "solutions": "Verify all required environment variables are set correctly in platform settings"
            },
            "port_configuration": {
                "symptoms": "Application not accessible after deployment",
                "causes": "Incorrect port configuration or binding",
                "solutions": "Ensure application listens on the correct port specified by platform"
            },
            "database_connection": {
                "symptoms": "Database connection errors",
                "causes": "Incorrect database URL, network issues, or authentication problems",
                "solutions": "Verify database URL, check network connectivity, validate credentials"
            }
        }
        
        # Performance issues
        performance_issues = {
            "slow_response_times": {
                "symptoms": "Application responds slowly to requests",
                "causes": "Insufficient resources, inefficient code, or database bottlenecks",
                "solutions": "Monitor resource usage, optimize database queries, consider scaling up"
            },
            "high_memory_usage": {
                "symptoms": "Memory usage consistently high or growing",
                "causes": "Memory leaks, inefficient algorithms, or large dataset processing",
                "solutions": "Profile memory usage, optimize code, implement garbage collection"
            },
            "timeout_errors": {
                "symptoms": "Requests timing out frequently",
                "causes": "Long-running operations, external API delays, or insufficient resources",
                "solutions": "Optimize operations, implement async processing, increase timeout limits"
            }
        }
        
        # Connectivity issues
        connectivity_issues = {
            "domain_not_resolving": {
                "symptoms": "Custom domain not accessible",
                "causes": "DNS configuration errors or propagation delays",
                "solutions": "Verify DNS records, wait for propagation, check with DNS lookup tools"
            },
            "ssl_certificate_errors": {
                "symptoms": "SSL certificate warnings or errors",
                "causes": "Expired certificates, misconfiguration, or certificate chain issues",
                "solutions": "Check certificate expiration, verify configuration, renew if needed"
            },
            "api_connectivity": {
                "symptoms": "External API calls failing",
                "causes": "Network restrictions, API key issues, or service outages",
                "solutions": "Verify API keys, check service status, review network configuration"
            }
        }
        
        # Configuration issues
        configuration_issues = {
            "incorrect_settings": {
                "symptoms": "Application behaving unexpectedly",
                "causes": "Wrong configuration values or missing settings",
                "solutions": "Review all configuration settings, compare with documentation"
            },
            "permission_errors": {
                "symptoms": "Access denied or permission errors",
                "causes": "Incorrect file permissions or access controls",
                "solutions": "Check file permissions, review access control settings"
            }
        }
        
        # Cost issues
        cost_issues = {
            "unexpected_charges": {
                "symptoms": "Higher than expected bills",
                "causes": "Resource overuse, unexpected scaling, or billing errors",
                "solutions": "Review usage reports, check scaling events, contact support if needed"
            },
            "billing_confusion": {
                "symptoms": "Unclear billing or charges",
                "causes": "Complex pricing models or multiple services",
                "solutions": "Review billing breakdown, understand pricing model, contact support"
            }
        }
        
        # Security issues
        security_issues = {
            "unauthorized_access": {
                "symptoms": "Suspicious login attempts or access patterns",
                "causes": "Weak passwords, compromised credentials, or security breaches",
                "solutions": "Change passwords, enable 2FA, review access logs, contact security team"
            },
            "api_key_exposure": {
                "symptoms": "API keys potentially exposed or compromised",
                "causes": "Keys in public repositories or insecure storage",
                "solutions": "Rotate all exposed keys immediately, review security practices"
            }
        }
        
        # Diagnostic commands
        diagnostic_commands = [
            "curl -I [your-domain] - Check HTTP response headers",
            "nslookup [your-domain] - Verify DNS resolution",
            "ping [your-domain] - Test basic connectivity",
            "openssl s_client -connect [domain]:443 - Check SSL certificate",
            "Check platform logs and monitoring dashboards"
        ]
        
        # Escalation procedures
        escalation_procedures = [
            "Try basic troubleshooting steps first",
            "Check platform status page for known issues",
            "Search platform documentation and community forums",
            "Contact platform support with detailed error information",
            "If critical: Use emergency support channels"
        ]
        
        # Emergency procedures
        emergency_procedures = [
            "If system is completely down: Check platform status first",
            "Verify recent changes or deployments that might have caused issues",
            "Roll back to last known good deployment if possible",
            "Contact platform emergency support if available",
            "Implement temporary workarounds if necessary"
        ]
        
        return TroubleshootingGuide(
            common_deployment_issues=common_deployment_issues,
            performance_issues=performance_issues,
            connectivity_issues=connectivity_issues,
            configuration_issues=configuration_issues,
            cost_issues=cost_issues,
            security_issues=security_issues,
            diagnostic_commands=diagnostic_commands,
            escalation_procedures=escalation_procedures,
            emergency_procedures=emergency_procedures
        )
    
    def _generate_ongoing_support_plan(self, user_analysis: Dict[str, Any]) -> OngoingSupport:
        """Generate ongoing platform management and support plan."""
        complexity = user_analysis.get("complexity_assessment", "moderate")
        
        # Daily tasks
        daily_tasks = [
            "Check system health and uptime status",
            "Review any error notifications or alerts",
            "Monitor basic performance metrics",
            "Check for any critical security notifications"
        ]
        
        if complexity in ["moderate", "complex"]:
            daily_tasks.extend([
                "Review cost and usage trends",
                "Check backup completion status"
            ])
        
        # Weekly tasks
        weekly_tasks = [
            "Review performance metrics and trends",
            "Check cost and billing reports",
            "Verify backup integrity and test restoration",
            "Review security logs and access patterns",
            "Update any necessary dependencies or patches",
            "Review and optimize resource usage"
        ]
        
        # Monthly tasks
        monthly_tasks = [
            "Comprehensive cost and usage analysis",
            "Performance optimization review and implementation",
            "Security assessment and updates",
            "Backup strategy review and testing",
            "Scaling strategy review based on growth patterns",
            "Team training and knowledge sharing session"
        ]
        
        # Update procedures
        update_procedures = [
            "Check for platform updates and new features",
            "Review and test application dependency updates",
            "Update security configurations and certificates",
            "Update monitoring and alerting configurations",
            "Document all updates and changes made"
        ]
        
        # Backup procedures
        backup_procedures = [
            "Verify automated backups are running successfully",
            "Test backup restoration process monthly",
            "Review backup retention policies",
            "Document backup and recovery procedures",
            "Ensure backup security and encryption"
        ]
        
        # Security reviews
        security_reviews = [
            "Review access controls and user permissions",
            "Update passwords and API keys as needed",
            "Check for security vulnerabilities and patches",
            "Review security logs for suspicious activity",
            "Update security documentation and procedures"
        ]
        
        # Performance reviews
        performance_reviews = [
            "Analyze performance trends and patterns",
            "Identify bottlenecks and optimization opportunities",
            "Review and optimize database performance",
            "Test application performance under load",
            "Document performance improvements and changes"
        ]
        
        # Cost reviews
        cost_reviews = [
            "Analyze cost trends and spending patterns",
            "Identify cost optimization opportunities",
            "Review resource utilization and rightsizing",
            "Compare costs with budget and projections",
            "Implement cost optimization recommendations"
        ]
        
        # Team training
        team_training = [
            "Regular platform training sessions for team members",
            "Documentation reviews and updates",
            "Best practices sharing and knowledge transfer",
            "Emergency response procedure training",
            "New feature and capability training"
        ]
        
        return OngoingSupport(
            daily_tasks=daily_tasks,
            weekly_tasks=weekly_tasks,
            monthly_tasks=monthly_tasks,
            update_procedures=update_procedures,
            backup_procedures=backup_procedures,
            security_reviews=security_reviews,
            performance_reviews=performance_reviews,
            cost_reviews=cost_reviews,
            team_training=team_training
        )
    
    def _compile_training_resources(self, user_analysis: Dict[str, Any]) -> List[str]:
        """Compile relevant training resources and learning materials."""
        platform = user_analysis.get("target_platform", "Railway")
        skill_level = user_analysis.get("user_skill_level", "beginner")
        
        base_resources = [
            "Platform-specific documentation and getting started guides",
            "Video tutorials for basic platform navigation and setup",
            "Community forums and knowledge base articles",
            "Best practices guides for hosting and deployment"
        ]
        
        # Platform-specific resources
        if platform == "Railway":
            base_resources.extend([
                "Railway documentation: https://docs.railway.app",
                "Railway community Discord for real-time help",
                "Railway blog for updates and best practices"
            ])
        elif platform == "DigitalOcean":
            base_resources.extend([
                "DigitalOcean tutorials and documentation",
                "DigitalOcean community Q&A platform",
                "DigitalOcean Kubernetes and deployment guides"
            ])
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            base_resources.extend([
                "Cloud provider training courses and certifications",
                "Well-architected framework documentation",
                "Free tier and getting started tutorials"
            ])
        
        # Skill-level specific resources
        if skill_level == "beginner":
            base_resources.extend([
                "Basic web hosting concepts and terminology",
                "Introduction to DNS and domain management",
                "Basic security best practices for beginners"
            ])
        elif skill_level == "advanced":
            base_resources.extend([
                "Advanced deployment patterns and strategies",
                "Infrastructure as code tutorials",
                "Advanced monitoring and observability"
            ])
        
        base_resources.extend([
            "Cost optimization and billing management guides",
            "Security best practices and compliance guides",
            "Performance optimization and scaling strategies",
            "Troubleshooting and debugging techniques"
        ])
        
        return base_resources
    
    def _define_support_channels(self, user_analysis: Dict[str, Any]) -> List[str]:
        """Define available support and help channels."""
        platform = user_analysis.get("target_platform", "Railway")
        
        support_channels = [
            "Platform documentation and knowledge base",
            "Community forums and user groups",
            "Email support for account and billing issues"
        ]
        
        # Platform-specific support
        if platform == "Railway":
            support_channels.extend([
                "Railway Discord community for real-time help",
                "Railway email support for technical issues",
                "Railway status page for outage information"
            ])
        elif platform == "DigitalOcean":
            support_channels.extend([
                "DigitalOcean support tickets for technical help",
                "DigitalOcean community Q&A platform",
                "DigitalOcean live chat for account issues"
            ])
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            support_channels.extend([
                "Cloud provider support plans (Basic/Developer/Business)",
                "Professional services and consulting",
                "Training and certification programs"
            ])
        
        support_channels.extend([
            "CrewBuilder documentation and user guides",
            "Emergency escalation procedures for critical issues",
            "Third-party consultants for complex technical issues"
        ])
        
        return support_channels
    
    def _create_success_metrics(self, user_analysis: Dict[str, Any]) -> List[str]:
        """Create key success metrics for hosting management."""
        return [
            "System uptime > 99.5% (excluding planned maintenance)",
            "Average response time < 3 seconds for 95% of requests",
            "Monthly costs within 10% of projected budget",
            "Zero critical security incidents",
            "Successful completion of weekly backup tests",
            "User satisfaction score > 4.0/5 for system performance",
            "Less than 4 hours average time to resolve issues",
            "Successful completion of monthly maintenance tasks",
            "Team confidence score > 4.0/5 for platform management",
            "Cost optimization savings of at least 10% annually"
        ]
    
    def _estimate_management_time(self, user_analysis: Dict[str, Any]) -> str:
        """Estimate weekly time commitment for platform management."""
        complexity = user_analysis.get("complexity_assessment", "moderate")
        skill_level = user_analysis.get("user_skill_level", "beginner")
        
        # Base time estimates
        if complexity == "simple":
            base_hours = 2
        elif complexity == "complex":
            base_hours = 8
        else:
            base_hours = 4
        
        # Adjust for skill level
        if skill_level == "beginner":
            base_hours *= 1.5
        elif skill_level == "advanced":
            base_hours *= 0.7
        
        hours = int(base_hours)
        
        if hours <= 2:
            return f"{hours} hours per week"
        elif hours <= 8:
            return f"{hours} hours per week (can be spread across days)"
        else:
            return f"{hours} hours per week (recommend dedicated time blocks)"
    
    def _define_escalation_contacts(self, user_analysis: Dict[str, Any]) -> List[str]:
        """Define escalation contacts and emergency procedures."""
        platform = user_analysis.get("target_platform", "Railway")
        
        return [
            f"{platform} technical support (for platform-specific issues)",
            f"{platform} emergency support (for critical outages)",
            "Domain registrar support (for DNS and domain issues)",
            "Third-party security consultant (for security incidents)",
            "CrewBuilder support team (for application-specific issues)",
            "Team lead or technical contact (for internal escalation)",
            "Business continuity contact (for business impact decisions)"
        ]
    
    def _generate_documentation_links(self, user_analysis: Dict[str, Any]) -> List[str]:
        """Generate relevant documentation and guide links."""
        platform = user_analysis.get("target_platform", "Railway")
        
        base_links = [
            "Platform setup and deployment guide",
            "Security best practices and configuration guide",
            "Cost optimization and billing management guide",
            "Troubleshooting and problem resolution guide",
            "Backup and disaster recovery procedures",
            "Performance monitoring and optimization guide"
        ]
        
        # Platform-specific documentation
        if platform == "Railway":
            base_links.extend([
                "Railway deployment and configuration documentation",
                "Railway environment variables and secrets guide",
                "Railway custom domains and SSL setup guide"
            ])
        elif platform == "DigitalOcean":
            base_links.extend([
                "DigitalOcean droplet and app platform guides",
                "DigitalOcean managed databases documentation",
                "DigitalOcean load balancers and networking guides"
            ])
        
        return base_links
    
    def _generate_fallback_hosting_assistance_plan(self, error_message: str) -> HostingAssistancePlan:
        """Generate a safe fallback hosting assistance plan when errors occur."""
        
        # Safe fallback platform setup guide
        fallback_platform_setup = PlatformSetupGuide(
            platform="Railway",
            difficulty_level="beginner",
            estimated_setup_time="2-4 hours",
            prerequisites=["Email address", "Credit card", "Basic computer skills"],
            account_setup_steps=[
                "Go to railway.app and click 'Sign Up'",
                "Connect your GitHub account",
                "Verify your email address",
                "Add payment method for billing"
            ],
            initial_configuration=[
                "Create a new project from GitHub repository",
                "Configure environment variables",
                "Deploy your application",
                "Verify deployment is successful"
            ],
            project_deployment=[
                "Connect your GitHub repository",
                "Configure build settings",
                "Set environment variables",
                "Deploy and verify functionality"
            ],
            verification_steps=[
                "Check application URL is accessible",
                "Verify all features are working",
                "Test API endpoints if applicable"
            ],
            common_issues=[
                "Build failures - check logs and dependencies",
                "Environment variable errors - verify all required variables are set",
                "Port configuration issues - ensure correct port binding"
            ],
            next_steps=[
                "Set up custom domain if needed",
                "Configure monitoring and alerts",
                "Set up backup procedures"
            ]
        )
        
        # Safe fallback configuration assistance
        fallback_configuration = ConfigurationAssistance(
            domain_setup={
                "basic": ["Purchase domain", "Configure DNS", "Wait for propagation"]
            },
            ssl_certificate_setup={
                "automatic": ["Railway provides automatic SSL", "No configuration needed"]
            },
            load_balancer_config={
                "platform_managed": ["Railway handles load balancing automatically"]
            },
            custom_domain_setup=["Buy domain", "Configure DNS", "Add to Railway"],
            cdn_configuration=["Railway includes CDN capabilities"],
            email_setup=["Configure notification emails in Railway settings"],
            backup_configuration=["Set up database backups if using database"],
            security_hardening=["Enable 2FA", "Use strong passwords", "Monitor access"]
        )
        
        # Safe fallback resource optimization
        fallback_optimization = ResourceOptimization(
            current_usage_analysis={"basic": "Monitor Railway dashboard for usage"},
            cost_optimization_tips=["Use free tier", "Monitor usage", "Scale appropriately"],
            scaling_recommendations={"auto": ["Enable Railway auto-scaling"]},
            monitoring_setup=["Use Railway built-in monitoring"],
            budget_alerts=["Set up billing notifications"],
            resource_rightsizing=["Start small and scale up as needed"],
            performance_optimization=["Monitor performance metrics"],
            maintenance_schedule=["Weekly usage review", "Monthly optimization check"]
        )
        
        # Safe fallback troubleshooting
        fallback_troubleshooting = TroubleshootingGuide(
            common_deployment_issues={
                "build_failure": {
                    "symptoms": "Deployment fails",
                    "causes": "Missing dependencies",
                    "solutions": "Check build logs and fix dependencies"
                }
            },
            performance_issues={
                "slow_response": {
                    "symptoms": "Slow response times",
                    "causes": "Insufficient resources",
                    "solutions": "Scale up instance size"
                }
            },
            connectivity_issues={
                "domain_issues": {
                    "symptoms": "Domain not working",
                    "causes": "DNS configuration",
                    "solutions": "Check DNS settings"
                }
            },
            configuration_issues={
                "env_vars": {
                    "symptoms": "Config errors",
                    "causes": "Missing environment variables",
                    "solutions": "Set all required variables"
                }
            },
            cost_issues={
                "unexpected_bills": {
                    "symptoms": "High costs",
                    "causes": "Resource overuse",
                    "solutions": "Monitor and optimize usage"
                }
            },
            security_issues={
                "access_issues": {
                    "symptoms": "Unauthorized access",
                    "causes": "Weak security",
                    "solutions": "Enable 2FA and strong passwords"
                }
            },
            diagnostic_commands=["Check Railway logs", "Test application endpoints"],
            escalation_procedures=["Contact Railway support", "Check status page"],
            emergency_procedures=["Roll back deployment", "Contact emergency support"]
        )
        
        # Safe fallback ongoing support
        fallback_ongoing_support = OngoingSupport(
            daily_tasks=["Check system status", "Review alerts"],
            weekly_tasks=["Review performance", "Check costs"],
            monthly_tasks=["Optimize resources", "Review security"],
            update_procedures=["Apply updates as needed"],
            backup_procedures=["Verify backups working"],
            security_reviews=["Monthly security check"],
            performance_reviews=["Analyze performance trends"],
            cost_reviews=["Review and optimize costs"],
            team_training=["Learn platform features"]
        )
        
        return HostingAssistancePlan(
            system_name="CrewAI System",
            target_platform="Railway",
            user_skill_level="beginner",
            complexity_assessment="simple",
            estimated_management_time="2-3 hours per week",
            platform_setup_guide=fallback_platform_setup,
            configuration_assistance=fallback_configuration,
            resource_optimization=fallback_optimization,
            troubleshooting_guide=fallback_troubleshooting,
            ongoing_support=fallback_ongoing_support,
            training_resources=["Railway documentation", "Basic hosting guides"],
            support_channels=["Railway support", "Community forums"],
            success_metrics=["System uptime > 99%", "Costs within budget"],
            escalation_contacts=["Railway support", "Technical team"],
            documentation_links=["Railway docs", "Setup guides"]
        )
    
    def _build_platform_guides(self) -> Dict[str, Dict[str, Any]]:
        """Build platform-specific setup guidance."""
        return {
            "Railway": {
                "beginner_setup_time": "2-3 hours",
                "intermediate_setup_time": "1-2 hours", 
                "advanced_setup_time": "30-60 minutes",
                "account_setup_steps": [
                    "Visit railway.app and click 'Start a New Project'",
                    "Sign up using GitHub, Google, or email",
                    "Verify your email address",
                    "Connect your GitHub account for repository access",
                    "Add a payment method (required even for free tier)"
                ],
                "initial_configuration": [
                    "Create a new project from your GitHub repository",
                    "Railway will automatically detect your application type",
                    "Configure environment variables in the Variables tab",
                    "Review build and start commands (usually auto-detected)",
                    "Enable public networking to get a public URL"
                ],
                "project_deployment": [
                    "Connect your GitHub repository to Railway",
                    "Configure any necessary environment variables",
                    "Trigger the first deployment",
                    "Monitor build logs for any issues",
                    "Test your deployed application URL"
                ],
                "common_issues": [
                    "Build timeouts - Increase build timeout in settings",
                    "Environment variable errors - Check variable names and values",
                    "Port binding issues - Ensure app listens on Railway's PORT variable",
                    "Memory limits - Monitor usage and upgrade plan if needed"
                ]
            },
            "DigitalOcean": {
                "beginner_setup_time": "4-6 hours",
                "intermediate_setup_time": "2-3 hours",
                "advanced_setup_time": "1-2 hours", 
                "account_setup_steps": [
                    "Create DigitalOcean account at digitalocean.com",
                    "Verify email and add payment method",
                    "Choose between Droplets or App Platform",
                    "Set up SSH keys for secure access",
                    "Enable two-factor authentication"
                ],
                "initial_configuration": [
                    "Create a new Droplet or App Platform app",
                    "Choose appropriate size and region",
                    "Configure firewall rules and security settings",
                    "Set up domain and DNS configuration",
                    "Configure monitoring and alerting"
                ],
                "project_deployment": [
                    "Upload your code via Git or direct upload",
                    "Configure build and runtime settings",
                    "Set up environment variables and secrets",
                    "Deploy and monitor deployment progress",
                    "Configure load balancing if needed"
                ],
                "common_issues": [
                    "SSH connection issues - Verify SSH keys and firewall rules",
                    "Performance issues - Monitor resource usage and scale appropriately",
                    "DNS propagation delays - Allow 24-48 hours for full propagation",
                    "Database connection errors - Check security groups and connection strings"
                ]
            },
            "AWS": {
                "beginner_setup_time": "8-12 hours",
                "intermediate_setup_time": "4-6 hours",
                "advanced_setup_time": "2-4 hours",
                "account_setup_steps": [
                    "Create AWS account and verify payment method",
                    "Set up IAM users and roles for security",
                    "Enable MFA for root and IAM accounts",
                    "Configure billing alerts and cost monitoring",
                    "Choose appropriate support plan"
                ],
                "initial_configuration": [
                    "Set up VPC and networking configuration",
                    "Configure security groups and access controls",
                    "Set up load balancers and auto-scaling groups",
                    "Configure CloudWatch monitoring and alerting",
                    "Set up backup and disaster recovery procedures"
                ],
                "project_deployment": [
                    "Deploy using ECS, Lambda, or EC2 depending on architecture",
                    "Configure container registry and image management",
                    "Set up CI/CD pipeline with CodePipeline or GitHub Actions",
                    "Configure environment-specific deployments",
                    "Set up database and storage services"
                ],
                "common_issues": [
                    "Complex pricing - Use cost calculators and monitor spend carefully",
                    "Security group misconfigurations - Review access rules regularly",
                    "Service limits - Request increases for production workloads",
                    "Region availability - Choose regions with required services"
                ]
            },
            "Render": {
                "beginner_setup_time": "2-4 hours",
                "intermediate_setup_time": "1-2 hours",
                "advanced_setup_time": "30-90 minutes",
                "account_setup_steps": [
                    "Sign up at render.com with GitHub or email",
                    "Connect your GitHub or GitLab account",
                    "Verify email address and account",
                    "Add payment method for paid services",
                    "Review service options and pricing"
                ],
                "initial_configuration": [
                    "Create a new web service from your repository",
                    "Configure build and start commands",
                    "Set up environment variables",
                    "Choose appropriate instance type",
                    "Configure custom domain if needed"
                ],
                "project_deployment": [
                    "Connect repository and configure auto-deploy",
                    "Set up environment variables and secrets",
                    "Configure health checks and monitoring",
                    "Deploy and verify application functionality",
                    "Set up database services if needed"
                ],
                "common_issues": [
                    "Build failures - Check build logs and dependencies",
                    "Cold starts - Consider using paid plans for faster startup",
                    "Resource limits - Monitor usage and upgrade as needed",
                    "Custom domain setup - Verify DNS configuration"
                ]
            }
        }
    
    def _build_troubleshooting_database(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive troubleshooting knowledge base."""
        return {
            "deployment_failures": {
                "build_timeout": {
                    "description": "Build process times out before completion",
                    "common_causes": ["Large dependencies", "Slow network", "Inefficient build process"],
                    "solutions": ["Optimize build process", "Use build caching", "Increase timeout limits"],
                    "prevention": ["Regular dependency updates", "Build optimization", "Monitor build times"]
                },
                "dependency_conflicts": {
                    "description": "Conflicting or missing dependencies cause build failures",
                    "common_causes": ["Outdated requirements", "Version conflicts", "Missing system packages"],
                    "solutions": ["Update requirements.txt", "Resolve version conflicts", "Add system dependencies"],
                    "prevention": ["Regular dependency audits", "Version pinning", "Dependency monitoring"]
                }
            },
            "performance_problems": {
                "memory_leaks": {
                    "description": "Application memory usage grows over time",
                    "common_causes": ["Unreleased resources", "Circular references", "Large object retention"],
                    "solutions": ["Profile memory usage", "Fix memory leaks", "Implement garbage collection"],
                    "prevention": ["Regular profiling", "Code reviews", "Memory monitoring"]
                },
                "database_bottlenecks": {
                    "description": "Database queries are slow or timing out",
                    "common_causes": ["Missing indexes", "Complex queries", "Database overload"],
                    "solutions": ["Add database indexes", "Optimize queries", "Scale database"],
                    "prevention": ["Query optimization", "Regular performance reviews", "Database monitoring"]
                }
            }
        }
    
    def _build_optimization_strategies(self) -> Dict[str, List[str]]:
        """Build resource optimization strategies."""
        return {
            "cost_optimization": [
                "Right-size instances based on actual usage",
                "Use reserved instances for predictable workloads",
                "Implement auto-scaling to avoid over-provisioning",
                "Monitor and optimize data transfer costs",
                "Use platform free tiers effectively",
                "Regular cost analysis and optimization reviews"
            ],
            "performance_optimization": [
                "Implement caching strategies",
                "Optimize database queries and connections",
                "Use CDN for static content delivery",
                "Optimize application startup time",
                "Monitor and tune resource allocation",
                "Implement load balancing for high traffic"
            ],
            "security_optimization": [
                "Regular security audits and assessments",
                "Implement least privilege access principles",
                "Use encryption for data at rest and in transit",
                "Regular password and key rotation",
                "Monitor access logs and suspicious activity",
                "Keep all software and dependencies updated"
            ]
        }


def create_hosting_assistant() -> HostingAssistant:
    """Factory function to create a HostingAssistant instance."""
    return HostingAssistant()
