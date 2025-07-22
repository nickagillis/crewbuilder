"""
Monitoring Engineer Agent for CrewBuilder
Creates comprehensive monitoring, observability, and alerting systems for AI agent systems.
"""

from crewai import Agent, Task
from .llm_config import get_configured_llm
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field


class SystemMonitoring(BaseModel):
    """Represents comprehensive system monitoring configuration"""
    monitoring_stack: str = Field(description="Primary monitoring solution (e.g., 'Prometheus + Grafana', 'DataDog', 'New Relic')")
    health_checks: List[str] = Field(description="Application and infrastructure health monitoring")
    uptime_monitoring: List[str] = Field(description="Service availability and uptime tracking")
    performance_metrics: List[str] = Field(description="Key performance indicators and metrics")
    resource_monitoring: List[str] = Field(description="CPU, memory, disk, and network monitoring")
    application_monitoring: List[str] = Field(description="Application-specific performance tracking")
    database_monitoring: List[str] = Field(description="Database performance and optimization monitoring")
    api_monitoring: List[str] = Field(description="API endpoint performance and reliability monitoring")
    log_aggregation: str = Field(description="Log collection and analysis configuration")
    metrics_retention: str = Field(description="Data retention policies and storage optimization")


class CostMonitoring(BaseModel):
    """Represents cost monitoring and optimization system"""
    cost_tracking_platform: str = Field(description="Primary cost monitoring solution")
    real_time_cost_alerts: List[str] = Field(description="Real-time spending alerts and thresholds")
    budget_management: List[str] = Field(description="Budget tracking and enforcement")
    cost_optimization_recommendations: List[str] = Field(description="Automated cost reduction suggestions")
    resource_utilization_tracking: List[str] = Field(description="Resource efficiency monitoring")
    billing_anomaly_detection: List[str] = Field(description="Unusual spending pattern detection")
    cost_allocation: List[str] = Field(description="Cost attribution by service and team")
    optimization_automation: List[str] = Field(description="Automated cost optimization actions")
    reporting_dashboards: List[str] = Field(description="Cost reporting and executive summaries")
    forecasting: List[str] = Field(description="Cost projection and planning capabilities")


class SecurityMonitoring(BaseModel):
    """Represents security monitoring and incident response"""
    security_monitoring_platform: str = Field(description="Primary security monitoring solution")
    access_log_monitoring: List[str] = Field(description="User access and authentication monitoring")
    vulnerability_scanning: List[str] = Field(description="Automated security vulnerability detection")
    intrusion_detection: List[str] = Field(description="Network and system intrusion monitoring")
    compliance_monitoring: List[str] = Field(description="Regulatory compliance tracking")
    incident_response_automation: List[str] = Field(description="Automated security incident response")
    threat_intelligence: List[str] = Field(description="Security threat detection and analysis")
    audit_logging: List[str] = Field(description="Comprehensive audit trail maintenance")
    security_alerting: List[str] = Field(description="Security incident notification and escalation")
    forensic_capabilities: List[str] = Field(description="Security investigation and analysis tools")


class AlertingSystem(BaseModel):
    """Represents comprehensive alerting and notification system"""
    alerting_platform: str = Field(description="Primary alerting solution")
    notification_channels: List[str] = Field(description="Alert delivery methods (email, Slack, SMS, etc.)")
    escalation_procedures: List[str] = Field(description="Alert escalation rules and procedures")
    alert_categorization: List[str] = Field(description="Alert severity levels and classification")
    automated_responses: List[str] = Field(description="Automated remediation and response actions")
    alert_suppression: List[str] = Field(description="Alert deduplication and noise reduction")
    on_call_management: List[str] = Field(description="On-call rotation and scheduling")
    incident_management: List[str] = Field(description="Incident tracking and resolution workflow")
    communication_templates: List[str] = Field(description="Standardized alert and incident communication")
    alert_analytics: List[str] = Field(description="Alert pattern analysis and optimization")


class DashboardConfiguration(BaseModel):
    """Represents custom dashboard and reporting configuration"""
    dashboard_platform: str = Field(description="Primary dashboard solution")
    executive_dashboards: List[str] = Field(description="High-level business and operational summaries")
    technical_dashboards: List[str] = Field(description="Detailed technical metrics and system health")
    business_dashboards: List[str] = Field(description="Business KPIs and performance indicators")
    operational_dashboards: List[str] = Field(description="Day-to-day operational monitoring")
    custom_reports: List[str] = Field(description="Scheduled and on-demand reporting")
    mobile_dashboards: List[str] = Field(description="Mobile-optimized monitoring interfaces")
    public_status_pages: List[str] = Field(description="Customer-facing system status communication")
    data_visualization: List[str] = Field(description="Advanced analytics and trend visualization")
    dashboard_automation: List[str] = Field(description="Automated dashboard updates and maintenance")


class PerformanceOptimization(BaseModel):
    """Represents performance monitoring and optimization system"""
    performance_monitoring_platform: str = Field(description="Primary performance monitoring solution")
    application_performance: List[str] = Field(description="Application response time and throughput monitoring")
    database_optimization: List[str] = Field(description="Database performance tuning and monitoring")
    bottleneck_detection: List[str] = Field(description="System bottleneck identification and analysis")
    capacity_planning: List[str] = Field(description="Resource capacity forecasting and planning")
    optimization_recommendations: List[str] = Field(description="Automated performance improvement suggestions")
    load_testing_integration: List[str] = Field(description="Performance testing and validation")
    user_experience_monitoring: List[str] = Field(description="End-user experience tracking")
    service_dependency_mapping: List[str] = Field(description="Service interaction and dependency analysis")
    performance_baselines: List[str] = Field(description="Performance baseline establishment and tracking")


class MonitoringPlan(BaseModel):
    """Complete monitoring and observability plan"""
    system_name: str = Field(description="Name of the AI system being monitored")
    monitoring_complexity: str = Field(description="'basic', 'standard', 'advanced', 'enterprise'")
    total_monitoring_cost: str = Field(description="Estimated monthly monitoring costs")
    implementation_timeline: str = Field(description="Timeline for monitoring system implementation")
    system_monitoring: SystemMonitoring = Field(description="Comprehensive system monitoring configuration")
    cost_monitoring: CostMonitoring = Field(description="Cost tracking and optimization system")
    security_monitoring: SecurityMonitoring = Field(description="Security monitoring and incident response")
    alerting_system: AlertingSystem = Field(description="Alerting and notification configuration")
    dashboard_configuration: DashboardConfiguration = Field(description="Dashboard and reporting setup")
    performance_optimization: PerformanceOptimization = Field(description="Performance monitoring and optimization")
    data_retention_policies: List[str] = Field(description="Data retention and compliance policies")
    backup_and_recovery: List[str] = Field(description="Monitoring system backup and disaster recovery")
    team_training: List[str] = Field(description="Team training and knowledge transfer for monitoring systems")
    continuous_improvement: List[str] = Field(description="Ongoing monitoring optimization and enhancement")
    compliance_requirements: List[str] = Field(description="Regulatory and compliance monitoring requirements")
    integration_points: List[str] = Field(description="Integration with existing tools and workflows")
    success_metrics: List[str] = Field(description="KPIs for monitoring system effectiveness")
    maintenance_procedures: List[str] = Field(description="Ongoing monitoring system maintenance")
    documentation_links: List[str] = Field(description="Monitoring documentation and runbooks")


class MonitoringEngineer:
    """Monitoring Engineer agent for creating comprehensive monitoring, observability, and alerting systems."""
    
    def __init__(self):
        """Initialize the Monitoring Engineer agent."""
        # Get configured LLM

        llm = get_configured_llm(temperature=0.7)

        

        self.agent = Agent(
            role="Monitoring Engineer", 
            goal="Design and implement comprehensive monitoring, observability, and alerting systems that provide complete visibility into AI agent system performance, costs, security, and business metrics, enabling proactive management and continuous optimization",
            backstory="""You are a world-class Site Reliability Engineer and monitoring specialist with 15+ years of experience building observability systems for complex distributed applications. You've designed monitoring architectures for everything from high-growth startups to Fortune 100 enterprises, handling millions of requests per day and managing infrastructure costs in the hundreds of thousands of dollars.

            Your expertise spans the entire observability spectrum: metrics, logs, traces, alerts, dashboards, and incident response. You understand that great monitoring isn't just about collecting data - it's about providing actionable insights that enable teams to maintain reliable, performant, and cost-effective systems. You've been on-call for critical systems and know the difference between useful alerts and alert fatigue.

            You excel at designing monitoring systems that scale with organizations and complexity. You know when to use simple platform-native monitoring versus comprehensive observability stacks, how to balance monitoring costs with value, and how to create dashboards that actually help people make decisions. Your monitoring designs consider the entire lifecycle from development to production to incident response.

            You're passionate about operational excellence and understand that monitoring is the foundation of reliable systems. You design monitoring that enables teams to detect issues before customers do, optimize performance proactively, and manage costs intelligently. Your alerting strategies are precise, actionable, and respect people's time and attention.

            You believe that great monitoring makes complex systems manageable and gives teams confidence to move fast while maintaining reliability. You design observability systems that grow with organizations, provide value from day one, and enable data-driven decision making across technical and business stakeholders. Your goal is to make system operations so predictable and well-instrumented that teams can focus on building value instead of fighting fires.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,  # Pass the LLM explicitly
            memory=False  # Disable memory to avoid connection issues
        )
        
        # Monitoring knowledge base and best practices
        self.monitoring_patterns = self._build_monitoring_patterns()
        self.alerting_strategies = self._build_alerting_strategies()
        self.optimization_frameworks = self._build_optimization_frameworks()
    
    def generate_monitoring_plan(self, 
                                hosting_assistance_plan: Dict[str, Any], 
                                deployment_plan: Dict[str, Any], 
                                infrastructure_recommendation: Dict[str, Any]) -> MonitoringPlan:
        """
        Generate comprehensive monitoring and observability plan.
        
        Args:
            hosting_assistance_plan: User guidance from Hosting Assistant
            deployment_plan: Deployment configurations from Deployment Engineer
            infrastructure_recommendation: Platform recommendations from Infrastructure Analyst
            
        Returns:
            Complete monitoring plan with observability and alerting systems
        """
        try:
            # Analyze monitoring requirements
            monitoring_analysis = self._analyze_monitoring_requirements(
                hosting_assistance_plan, deployment_plan, infrastructure_recommendation
            )
            
            # Generate system monitoring configuration
            system_monitoring = self._generate_system_monitoring(monitoring_analysis)
            
            # Create cost monitoring system
            cost_monitoring = self._create_cost_monitoring(monitoring_analysis)
            
            # Setup security monitoring
            security_monitoring = self._setup_security_monitoring(monitoring_analysis)
            
            # Configure alerting system
            alerting_system = self._configure_alerting_system(monitoring_analysis)
            
            # Design dashboard configuration
            dashboard_configuration = self._design_dashboard_configuration(monitoring_analysis)
            
            # Create performance optimization system
            performance_optimization = self._create_performance_optimization(monitoring_analysis)
            
            # Generate policies and procedures
            data_retention_policies = self._generate_data_retention_policies(monitoring_analysis)
            backup_and_recovery = self._generate_backup_recovery_procedures(monitoring_analysis)
            team_training = self._generate_team_training_plan(monitoring_analysis)
            continuous_improvement = self._generate_continuous_improvement_plan(monitoring_analysis)
            
            return MonitoringPlan(
                system_name=monitoring_analysis.get("system_name", "CrewAI System"),
                monitoring_complexity=monitoring_analysis.get("monitoring_complexity", "standard"),
                total_monitoring_cost=self._estimate_monitoring_costs(monitoring_analysis),
                implementation_timeline=self._estimate_implementation_timeline(monitoring_analysis),
                system_monitoring=system_monitoring,
                cost_monitoring=cost_monitoring,
                security_monitoring=security_monitoring,
                alerting_system=alerting_system,
                dashboard_configuration=dashboard_configuration,
                performance_optimization=performance_optimization,
                data_retention_policies=data_retention_policies,
                backup_and_recovery=backup_and_recovery,
                team_training=team_training,
                continuous_improvement=continuous_improvement,
                compliance_requirements=self._generate_compliance_requirements(monitoring_analysis),
                integration_points=self._generate_integration_points(monitoring_analysis),
                success_metrics=self._generate_success_metrics(monitoring_analysis),
                maintenance_procedures=self._generate_maintenance_procedures(monitoring_analysis),
                documentation_links=self._generate_documentation_links(monitoring_analysis)
            )
        
        except Exception as e:
            # Fallback monitoring plan for error cases
            return self._generate_fallback_monitoring_plan(str(e))
    
    def _analyze_monitoring_requirements(self, hosting_plan: Dict[str, Any], 
                                       deployment_plan: Dict[str, Any], 
                                       infrastructure_rec: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze requirements to determine optimal monitoring approach."""
        analysis = {
            "system_name": "CrewAI System",
            "monitoring_complexity": "standard",
            "target_platform": "Railway",
            "user_skill_level": "intermediate",
            "budget_level": "moderate",
            "scale_requirements": "small",
            "compliance_needs": "basic",
            "security_requirements": "standard",
            "business_criticality": "moderate"
        }
        
        # Extract from hosting assistance plan
        if hosting_plan:
            analysis["system_name"] = hosting_plan.get("system_name", "CrewAI System")
            analysis["target_platform"] = hosting_plan.get("target_platform", "Railway")
            analysis["user_skill_level"] = hosting_plan.get("user_skill_level", "intermediate")
            
            complexity = hosting_plan.get("complexity_assessment", "moderate")
            if complexity == "simple":
                analysis["monitoring_complexity"] = "basic"
            elif complexity == "complex":
                analysis["monitoring_complexity"] = "advanced"
        
        # Extract from deployment plan
        if deployment_plan:
            deployment_complexity = deployment_plan.get("complexity_level", "moderate")
            if deployment_complexity == "complex":
                analysis["monitoring_complexity"] = "advanced"
                analysis["scale_requirements"] = "large"
            
            # Check for enterprise features
            if "kubernetes" in str(deployment_plan).lower():
                analysis["monitoring_complexity"] = "enterprise"
                analysis["scale_requirements"] = "enterprise"
        
        # Extract from infrastructure recommendation
        if infrastructure_rec:
            platform = infrastructure_rec.get("recommended_platform", "Railway")
            analysis["target_platform"] = platform
            
            # Determine budget level from cost estimates
            cost_analysis = infrastructure_rec.get("cost_analysis", {})
            if isinstance(cost_analysis, dict):
                monthly_cost = cost_analysis.get("estimated_monthly_total", "$15-50")
                if "$200" in monthly_cost or "$500" in monthly_cost:
                    analysis["budget_level"] = "high"
                    analysis["business_criticality"] = "high"
                elif "$100" in monthly_cost:
                    analysis["budget_level"] = "moderate"
            
            # Check security requirements
            security_assessment = infrastructure_rec.get("security_assessment", {})
            if isinstance(security_assessment, dict):
                compliance_standards = security_assessment.get("compliance_standards", [])
                if len(compliance_standards) > 2:
                    analysis["compliance_needs"] = "advanced"
                    analysis["security_requirements"] = "enhanced"
        
        return analysis
    
    def _generate_system_monitoring(self, monitoring_analysis: Dict[str, Any]) -> SystemMonitoring:
        """Generate comprehensive system monitoring configuration."""
        platform = monitoring_analysis.get("target_platform", "Railway")
        complexity = monitoring_analysis.get("monitoring_complexity", "standard")
        
        # Determine monitoring stack
        monitoring_stack = self._determine_monitoring_stack(platform, complexity)
        
        # Health checks
        health_checks = [
            "Application startup and readiness probes",
            "API endpoint health verification",
            "Database connectivity checks",
            "External service dependency health",
            "Memory and resource health validation"
        ]
        
        # Uptime monitoring
        uptime_monitoring = [
            "HTTP/HTTPS endpoint availability monitoring",
            "DNS resolution monitoring",
            "SSL certificate expiration tracking",
            "Service response time monitoring",
            "Multi-region availability checks"
        ]
        
        # Performance metrics
        performance_metrics = [
            "Request response times (p50, p95, p99)",
            "Request throughput and rate",
            "Error rates and status codes",
            "CPU and memory utilization",
            "Disk I/O and network metrics",
            "Application-specific business metrics"
        ]
        
        # Resource monitoring
        resource_monitoring = [
            "CPU utilization per service",
            "Memory usage and allocation",
            "Disk space and I/O performance",
            "Network bandwidth and latency",
            "Container resource consumption"
        ]
        
        # Application monitoring
        application_monitoring = [
            "API endpoint performance tracking",
            "User session and transaction monitoring",
            "Feature usage and adoption metrics",
            "Error tracking and stack traces",
            "Custom business logic monitoring"
        ]
        
        # Database monitoring
        database_monitoring = [
            "Query performance and slow query detection",
            "Connection pool utilization",
            "Database size and growth tracking",
            "Index usage and optimization",
            "Backup completion and integrity"
        ]
        
        # API monitoring
        api_monitoring = [
            "External API response times",
            "API rate limit consumption",
            "API error rates and failures",
            "API cost and usage tracking",
            "Service dependency mapping"
        ]
        
        # Log aggregation
        log_aggregation = self._configure_log_aggregation(platform, complexity)
        
        # Metrics retention
        metrics_retention = self._configure_metrics_retention(complexity)
        
        return SystemMonitoring(
            monitoring_stack=monitoring_stack,
            health_checks=health_checks,
            uptime_monitoring=uptime_monitoring,
            performance_metrics=performance_metrics,
            resource_monitoring=resource_monitoring,
            application_monitoring=application_monitoring,
            database_monitoring=database_monitoring,
            api_monitoring=api_monitoring,
            log_aggregation=log_aggregation,
            metrics_retention=metrics_retention
        )
    
    def _create_cost_monitoring(self, monitoring_analysis: Dict[str, Any]) -> CostMonitoring:
        """Create comprehensive cost monitoring and optimization system."""
        platform = monitoring_analysis.get("target_platform", "Railway")
        budget_level = monitoring_analysis.get("budget_level", "moderate")
        
        # Cost tracking platform
        cost_tracking_platform = self._determine_cost_tracking_platform(platform)
        
        # Real-time cost alerts
        real_time_cost_alerts = [
            "Daily spending threshold alerts",
            "Weekly budget variance notifications",
            "Monthly budget projection warnings",
            "Unexpected cost spike detection",
            "Resource usage anomaly alerts"
        ]
        
        # Budget management
        budget_management = [
            "Monthly budget tracking and enforcement",
            "Department/project cost allocation",
            "Cost center reporting and analysis",
            "Budget variance analysis and reporting",
            "Automated budget approval workflows"
        ]
        
        # Cost optimization recommendations
        cost_optimization_recommendations = [
            "Right-sizing recommendations for over-provisioned resources",
            "Reserved instance opportunities identification",
            "Unused resource detection and cleanup suggestions",
            "Auto-scaling optimization recommendations",
            "Data transfer cost optimization strategies"
        ]
        
        # Resource utilization tracking
        resource_utilization_tracking = [
            "CPU and memory efficiency monitoring",
            "Storage utilization and growth tracking",
            "Network bandwidth usage analysis",
            "Service-level cost attribution",
            "Peak vs. average usage analysis"
        ]
        
        # Billing anomaly detection
        billing_anomaly_detection = [
            "Unusual spending pattern detection",
            "Service cost spike identification",
            "Billing error detection and flagging",
            "Resource usage anomaly correlation",
            "Cost trend deviation alerts"
        ]
        
        # Cost allocation
        cost_allocation = [
            "Service-based cost breakdown",
            "Team and project cost attribution",
            "Environment-specific cost tracking",
            "Feature-based cost analysis",
            "Customer or tenant cost allocation"
        ]
        
        # Optimization automation
        optimization_automation = [
            "Automated resource cleanup for development environments",
            "Scheduled scaling based on usage patterns",
            "Automated backup lifecycle management",
            "Resource tagging for cost tracking",
            "Policy-based cost control enforcement"
        ]
        
        # Reporting dashboards
        reporting_dashboards = [
            "Executive cost summary dashboards",
            "Detailed cost breakdown reports",
            "Cost trend analysis and forecasting",
            "Budget vs. actual spending reports",
            "Cost optimization opportunity tracking"
        ]
        
        # Forecasting
        forecasting = [
            "Monthly and quarterly cost projections",
            "Growth-based scaling cost estimates",
            "Budget planning and scenario modeling",
            "Cost impact analysis for new features",
            "Long-term infrastructure cost planning"
        ]
        
        return CostMonitoring(
            cost_tracking_platform=cost_tracking_platform,
            real_time_cost_alerts=real_time_cost_alerts,
            budget_management=budget_management,
            cost_optimization_recommendations=cost_optimization_recommendations,
            resource_utilization_tracking=resource_utilization_tracking,
            billing_anomaly_detection=billing_anomaly_detection,
            cost_allocation=cost_allocation,
            optimization_automation=optimization_automation,
            reporting_dashboards=reporting_dashboards,
            forecasting=forecasting
        )
    
    def _setup_security_monitoring(self, monitoring_analysis: Dict[str, Any]) -> SecurityMonitoring:
        """Setup comprehensive security monitoring and incident response."""
        security_requirements = monitoring_analysis.get("security_requirements", "standard")
        compliance_needs = monitoring_analysis.get("compliance_needs", "basic")
        
        # Security monitoring platform
        security_monitoring_platform = self._determine_security_monitoring_platform(security_requirements)
        
        # Access log monitoring
        access_log_monitoring = [
            "User authentication and login monitoring",
            "Failed login attempt detection",
            "Privilege escalation monitoring",
            "API access pattern analysis",
            "Administrative action logging and review"
        ]
        
        # Vulnerability scanning
        vulnerability_scanning = [
            "Automated container image vulnerability scanning",
            "Dependency vulnerability monitoring",
            "Infrastructure vulnerability assessment",
            "Configuration security scanning",
            "Regular penetration testing integration"
        ]
        
        # Intrusion detection
        intrusion_detection = [
            "Network traffic anomaly detection",
            "Suspicious file access monitoring",
            "Process behavior analysis",
            "Network connection monitoring",
            "Data exfiltration detection"
        ]
        
        # Compliance monitoring
        compliance_monitoring = [
            "Data access and retention compliance",
            "Security policy compliance verification",
            "Audit trail completeness validation",
            "Regulatory requirement monitoring",
            "Compliance reporting automation"
        ]
        
        # Incident response automation
        incident_response_automation = [
            "Automated threat containment procedures",
            "Security incident ticket creation",
            "Stakeholder notification workflows",
            "Evidence collection and preservation",
            "Recovery procedure execution"
        ]
        
        # Threat intelligence
        threat_intelligence = [
            "External threat feed integration",
            "IOC (Indicators of Compromise) monitoring",
            "Threat pattern recognition",
            "Security event correlation",
            "Threat landscape analysis"
        ]
        
        # Audit logging
        audit_logging = [
            "Comprehensive system access logging",
            "Configuration change tracking",
            "Data access and modification logging",
            "Administrative action recording",
            "Audit log integrity verification"
        ]
        
        # Security alerting
        security_alerting = [
            "Real-time security incident alerts",
            "Critical vulnerability notifications",
            "Compliance violation alerts",
            "Security policy breach notifications",
            "Threat detection escalation"
        ]
        
        # Forensic capabilities
        forensic_capabilities = [
            "Log analysis and correlation tools",
            "Timeline reconstruction capabilities",
            "Evidence preservation procedures",
            "Investigation workflow automation",
            "Forensic reporting and documentation"
        ]
        
        return SecurityMonitoring(
            security_monitoring_platform=security_monitoring_platform,
            access_log_monitoring=access_log_monitoring,
            vulnerability_scanning=vulnerability_scanning,
            intrusion_detection=intrusion_detection,
            compliance_monitoring=compliance_monitoring,
            incident_response_automation=incident_response_automation,
            threat_intelligence=threat_intelligence,
            audit_logging=audit_logging,
            security_alerting=security_alerting,
            forensic_capabilities=forensic_capabilities
        )
    
    def _configure_alerting_system(self, monitoring_analysis: Dict[str, Any]) -> AlertingSystem:
        """Configure comprehensive alerting and notification system."""
        user_skill_level = monitoring_analysis.get("user_skill_level", "intermediate")
        business_criticality = monitoring_analysis.get("business_criticality", "moderate")
        
        # Alerting platform
        alerting_platform = self._determine_alerting_platform(monitoring_analysis)
        
        # Notification channels
        notification_channels = [
            "Email notifications for non-urgent alerts",
            "Slack integration for team notifications",
            "SMS alerts for critical incidents",
            "Push notifications for mobile apps",
            "Webhook integrations for custom workflows"
        ]
        
        # Escalation procedures
        escalation_procedures = [
            "Primary on-call notification (immediate)",
            "Secondary escalation after 15 minutes",
            "Management escalation for critical incidents",
            "Executive notification for business-critical outages",
            "Customer communication for external impact"
        ]
        
        # Alert categorization
        alert_categorization = [
            "Critical: Service outage or data loss",
            "High: Performance degradation or security incidents",
            "Medium: Resource utilization or configuration issues",
            "Low: Informational or maintenance notifications",
            "Info: System events and operational updates"
        ]
        
        # Automated responses
        automated_responses = [
            "Auto-scaling triggers for resource constraints",
            "Service restart for failed health checks",
            "Failover activation for service outages",
            "Security isolation for threat detection",
            "Backup initiation for data protection"
        ]
        
        # Alert suppression
        alert_suppression = [
            "Duplicate alert deduplication",
            "Maintenance window alert suppression",
            "Known issue acknowledgment and grouping",
            "Alert fatigue prevention rules",
            "Intelligent alert correlation and clustering"
        ]
        
        # On-call management
        on_call_management = [
            "On-call rotation scheduling",
            "Escalation policy management",
            "On-call handoff procedures",
            "Incident ownership assignment",
            "On-call performance analytics"
        ]
        
        # Incident management
        incident_management = [
            "Automated incident creation and tracking",
            "Incident severity classification",
            "Response team coordination",
            "Communication plan execution",
            "Post-incident review automation"
        ]
        
        # Communication templates
        communication_templates = [
            "Alert notification templates",
            "Incident status update templates",
            "Customer communication templates",
            "Post-incident report templates",
            "Maintenance notification templates"
        ]
        
        # Alert analytics
        alert_analytics = [
            "Alert volume and trend analysis",
            "False positive rate tracking",
            "Response time analytics",
            "Alert effectiveness measurement",
            "Continuous alerting optimization"
        ]
        
        return AlertingSystem(
            alerting_platform=alerting_platform,
            notification_channels=notification_channels,
            escalation_procedures=escalation_procedures,
            alert_categorization=alert_categorization,
            automated_responses=automated_responses,
            alert_suppression=alert_suppression,
            on_call_management=on_call_management,
            incident_management=incident_management,
            communication_templates=communication_templates,
            alert_analytics=alert_analytics
        )
    
    def _design_dashboard_configuration(self, monitoring_analysis: Dict[str, Any]) -> DashboardConfiguration:
        """Design custom dashboard and reporting configuration."""
        monitoring_complexity = monitoring_analysis.get("monitoring_complexity", "standard")
        business_criticality = monitoring_analysis.get("business_criticality", "moderate")
        
        # Dashboard platform
        dashboard_platform = self._determine_dashboard_platform(monitoring_analysis)
        
        # Executive dashboards
        executive_dashboards = [
            "System health and availability overview",
            "Cost and budget tracking summary",
            "Security posture and incident summary",
            "Business KPI and performance metrics",
            "Growth and scaling trend analysis"
        ]
        
        # Technical dashboards
        technical_dashboards = [
            "Infrastructure performance and resource utilization",
            "Application performance and error tracking",
            "Database performance and optimization",
            "API performance and dependency monitoring",
            "Security events and threat monitoring"
        ]
        
        # Business dashboards
        business_dashboards = [
            "User engagement and adoption metrics",
            "Feature usage and performance tracking",
            "Revenue and business impact metrics",
            "Customer satisfaction and experience",
            "Operational efficiency indicators"
        ]
        
        # Operational dashboards
        operational_dashboards = [
            "Real-time system status and alerts",
            "Incident tracking and response metrics",
            "Deployment and change management",
            "Capacity planning and resource forecasting",
            "Team performance and productivity"
        ]
        
        # Custom reports
        custom_reports = [
            "Weekly system health reports",
            "Monthly cost and optimization reports",
            "Quarterly security assessment reports",
            "Annual performance and capacity reports",
            "Ad-hoc investigation and analysis reports"
        ]
        
        # Mobile dashboards
        mobile_dashboards = [
            "Critical system status mobile view",
            "On-call incident response interface",
            "Key metrics mobile dashboard",
            "Alert acknowledgment and response",
            "Emergency contact and escalation"
        ]
        
        # Public status pages
        public_status_pages = [
            "Customer-facing system status page",
            "Service availability indicators",
            "Incident communication and updates",
            "Planned maintenance notifications",
            "Historical uptime reporting"
        ]
        
        # Data visualization
        data_visualization = [
            "Time-series performance trending",
            "Correlation analysis and insights",
            "Anomaly detection visualization",
            "Capacity planning projections",
            "Root cause analysis dashboards"
        ]
        
        # Dashboard automation
        dashboard_automation = [
            "Automated dashboard updates and refresh",
            "Dynamic threshold adjustment",
            "Intelligent alert correlation display",
            "Automated report generation and distribution",
            "Self-service dashboard creation tools"
        ]
        
        return DashboardConfiguration(
            dashboard_platform=dashboard_platform,
            executive_dashboards=executive_dashboards,
            technical_dashboards=technical_dashboards,
            business_dashboards=business_dashboards,
            operational_dashboards=operational_dashboards,
            custom_reports=custom_reports,
            mobile_dashboards=mobile_dashboards,
            public_status_pages=public_status_pages,
            data_visualization=data_visualization,
            dashboard_automation=dashboard_automation
        )
    
    def _create_performance_optimization(self, monitoring_analysis: Dict[str, Any]) -> PerformanceOptimization:
        """Create performance monitoring and optimization system."""
        scale_requirements = monitoring_analysis.get("scale_requirements", "small")
        
        # Performance monitoring platform
        performance_monitoring_platform = self._determine_performance_monitoring_platform(monitoring_analysis)
        
        # Application performance
        application_performance = [
            "End-to-end request tracing and analysis",
            "Code-level performance profiling",
            "Memory allocation and garbage collection monitoring",
            "Thread and concurrency analysis",
            "Framework-specific performance metrics"
        ]
        
        # Database optimization
        database_optimization = [
            "Query performance analysis and optimization",
            "Index usage and optimization recommendations",
            "Connection pool optimization",
            "Database capacity planning",
            "Backup and recovery performance monitoring"
        ]
        
        # Bottleneck detection
        bottleneck_detection = [
            "System resource bottleneck identification",
            "Application code bottleneck analysis",
            "Network latency and throughput analysis",
            "I/O performance bottleneck detection",
            "Service dependency bottleneck mapping"
        ]
        
        # Capacity planning
        capacity_planning = [
            "Resource usage trend analysis",
            "Growth projection and capacity forecasting",
            "Peak load planning and preparation",
            "Scaling threshold determination",
            "Cost-effective capacity optimization"
        ]
        
        # Optimization recommendations
        optimization_recommendations = [
            "Automated performance tuning suggestions",
            "Resource allocation optimization",
            "Configuration optimization recommendations",
            "Architecture improvement suggestions",
            "Code optimization opportunities"
        ]
        
        # Load testing integration
        load_testing_integration = [
            "Automated performance testing pipelines",
            "Load test result analysis and comparison",
            "Performance regression detection",
            "Capacity validation testing",
            "Stress testing and failure point identification"
        ]
        
        # User experience monitoring
        user_experience_monitoring = [
            "Real user monitoring (RUM)",
            "Page load time and rendering performance",
            "User journey and conversion tracking",
            "Mobile and cross-browser performance",
            "Geographic performance analysis"
        ]
        
        # Service dependency mapping
        service_dependency_mapping = [
            "Service interaction visualization",
            "Dependency failure impact analysis",
            "Critical path identification",
            "Service-level agreement monitoring",
            "Cascading failure prevention"
        ]
        
        # Performance baselines
        performance_baselines = [
            "Historical performance baseline establishment",
            "Performance trend analysis and comparison",
            "Seasonal performance pattern recognition",
            "Performance degradation detection",
            "Continuous baseline adjustment"
        ]
        
        return PerformanceOptimization(
            performance_monitoring_platform=performance_monitoring_platform,
            application_performance=application_performance,
            database_optimization=database_optimization,
            bottleneck_detection=bottleneck_detection,
            capacity_planning=capacity_planning,
            optimization_recommendations=optimization_recommendations,
            load_testing_integration=load_testing_integration,
            user_experience_monitoring=user_experience_monitoring,
            service_dependency_mapping=service_dependency_mapping,
            performance_baselines=performance_baselines
        )
    
    def _determine_monitoring_stack(self, platform: str, complexity: str) -> str:
        """Determine the optimal monitoring stack for the platform and complexity."""
        if platform in ["Railway", "Render", "Fly.io"]:
            if complexity == "basic":
                return "Platform-native monitoring with basic dashboards"
            else:
                return "Platform-native monitoring with Prometheus integration"
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            if complexity in ["advanced", "enterprise"]:
                return "Prometheus + Grafana + AlertManager"
            else:
                return "Cloud-native monitoring (CloudWatch/Stackdriver/Azure Monitor)"
        else:
            return "Prometheus + Grafana stack"
    
    def _configure_log_aggregation(self, platform: str, complexity: str) -> str:
        """Configure log aggregation strategy."""
        if platform in ["Railway", "Render"]:
            return "Platform-integrated logging with structured JSON format"
        elif platform in ["AWS", "Google Cloud", "Azure"]:
            return "Cloud-native log aggregation with ELK/EFK stack integration"
        else:
            return "Centralized logging with structured format and retention policies"
    
    def _configure_metrics_retention(self, complexity: str) -> str:
        """Configure metrics retention policies."""
        if complexity == "basic":
            return "30 days high-resolution, 1 year aggregated metrics"
        elif complexity in ["advanced", "enterprise"]:
            return "90 days high-resolution, 3 years aggregated, compliance-ready retention"
        else:
            return "60 days high-resolution, 2 years aggregated metrics"
    
    def _determine_cost_tracking_platform(self, platform: str) -> str:
        """Determine the best cost tracking platform."""
        if platform in ["AWS", "Google Cloud", "Azure"]:
            return f"{platform} native cost management with third-party analytics"
        else:
            return "Platform billing integration with cost monitoring dashboards"
    
    def _determine_security_monitoring_platform(self, security_requirements: str) -> str:
        """Determine the security monitoring platform."""
        if security_requirements == "enhanced":
            return "SIEM platform with threat intelligence integration"
        else:
            return "Platform-native security monitoring with log analysis"
    
    def _determine_alerting_platform(self, monitoring_analysis: Dict[str, Any]) -> str:
        """Determine the optimal alerting platform."""
        complexity = monitoring_analysis.get("monitoring_complexity", "standard")
        
        if complexity in ["advanced", "enterprise"]:
            return "PagerDuty or Opsgenie with advanced escalation"
        else:
            return "Integrated alerting with email, Slack, and SMS"
    
    def _determine_dashboard_platform(self, monitoring_analysis: Dict[str, Any]) -> str:
        """Determine the dashboard platform."""
        monitoring_complexity = monitoring_analysis.get("monitoring_complexity", "standard")
        
        if monitoring_complexity in ["advanced", "enterprise"]:
            return "Grafana with advanced visualization and custom panels"
        else:
            return "Platform dashboards with custom metrics integration"
    
    def _determine_performance_monitoring_platform(self, monitoring_analysis: Dict[str, Any]) -> str:
        """Determine performance monitoring platform."""
        scale_requirements = monitoring_analysis.get("scale_requirements", "small")
        
        if scale_requirements in ["large", "enterprise"]:
            return "APM solution (New Relic, DataDog, or Dynatrace)"
        else:
            return "Application performance monitoring with platform integration"
    
    def _estimate_monitoring_costs(self, monitoring_analysis: Dict[str, Any]) -> str:
        """Estimate total monitoring costs."""
        complexity = monitoring_analysis.get("monitoring_complexity", "standard")
        scale = monitoring_analysis.get("scale_requirements", "small")
        
        if complexity == "basic":
            base_cost = 15
        elif complexity == "enterprise":
            base_cost = 200
        else:
            base_cost = 75
        
        if scale in ["large", "enterprise"]:
            base_cost *= 2
        
        return f"${base_cost}-{base_cost * 2}/month"
    
    def _estimate_implementation_timeline(self, monitoring_analysis: Dict[str, Any]) -> str:
        """Estimate implementation timeline."""
        complexity = monitoring_analysis.get("monitoring_complexity", "standard")
        
        if complexity == "basic":
            return "1-2 weeks"
        elif complexity == "enterprise":
            return "6-8 weeks"
        else:
            return "3-4 weeks"
    
    def _generate_data_retention_policies(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate data retention policies."""
        return [
            "Metrics: High-resolution for 60 days, aggregated for 2 years",
            "Logs: Critical logs for 1 year, standard logs for 90 days",
            "Traces: Detailed traces for 30 days, sampled traces for 6 months",
            "Alerts: Alert history for 2 years for trend analysis",
            "Compliance: Audit logs retained per regulatory requirements"
        ]
    
    def _generate_backup_recovery_procedures(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate backup and recovery procedures."""
        return [
            "Daily automated backups of monitoring configuration",
            "Weekly backup validation and restore testing",
            "Monitoring infrastructure disaster recovery procedures",
            "Configuration as code for rapid recovery",
            "Cross-region backup replication for high availability"
        ]
    
    def _generate_team_training_plan(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate team training plan."""
        return [
            "Monitoring dashboard usage and interpretation training",
            "Alert response and incident management procedures",
            "Performance optimization and troubleshooting techniques",
            "Cost monitoring and optimization best practices",
            "Security monitoring and incident response training"
        ]
    
    def _generate_continuous_improvement_plan(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate continuous improvement plan."""
        return [
            "Monthly monitoring effectiveness review",
            "Quarterly alert optimization and tuning",
            "Semi-annual monitoring stack evaluation",
            "Annual monitoring strategy and roadmap review",
            "Continuous feedback collection and implementation"
        ]
    
    def _generate_compliance_requirements(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate compliance requirements."""
        return [
            "Audit trail completeness and integrity",
            "Data retention policy compliance",
            "Access control and authentication logging",
            "Incident response and notification procedures",
            "Regular compliance assessment and reporting"
        ]
    
    def _generate_integration_points(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate integration points."""
        return [
            "CI/CD pipeline integration for deployment monitoring",
            "Issue tracking system integration for incident management",
            "Communication platform integration (Slack, Teams)",
            "Business intelligence tool integration for reporting",
            "Cloud provider API integration for resource monitoring"
        ]
    
    def _generate_success_metrics(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate success metrics for monitoring system."""
        return [
            "Mean Time to Detection (MTTD) < 5 minutes for critical issues",
            "Mean Time to Resolution (MTTR) < 30 minutes for critical incidents",
            "Alert false positive rate < 5%",
            "Monitoring system uptime > 99.9%",
            "Cost optimization savings > 10% annually",
            "Security incident detection rate > 95%",
            "Team satisfaction with monitoring tools > 4.0/5",
            "Dashboard usage and engagement > 80%"
        ]
    
    def _generate_maintenance_procedures(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate maintenance procedures."""
        return [
            "Weekly monitoring system health checks",
            "Monthly alert tuning and optimization",
            "Quarterly monitoring stack updates",
            "Semi-annual monitoring architecture review",
            "Annual monitoring strategy assessment"
        ]
    
    def _generate_documentation_links(self, monitoring_analysis: Dict[str, Any]) -> List[str]:
        """Generate relevant documentation links."""
        return [
            "Monitoring system setup and configuration guide",
            "Alert response and incident management procedures",
            "Dashboard usage and customization documentation",
            "Performance optimization and troubleshooting guide",
            "Cost monitoring and optimization best practices",
            "Security monitoring and compliance procedures"
        ]
    
    def _generate_fallback_monitoring_plan(self, error_message: str) -> MonitoringPlan:
        """Generate a safe fallback monitoring plan when errors occur."""
        
        # Safe fallback system monitoring
        fallback_system_monitoring = SystemMonitoring(
            monitoring_stack="Platform-native monitoring",
            health_checks=["Basic application health checks", "HTTP endpoint monitoring"],
            uptime_monitoring=["Service availability monitoring", "Basic response time tracking"],
            performance_metrics=["Response time", "Error rate", "Basic resource usage"],
            resource_monitoring=["CPU usage", "Memory usage", "Basic disk monitoring"],
            application_monitoring=["Application logs", "Basic error tracking"],
            database_monitoring=["Database connectivity", "Basic performance monitoring"],
            api_monitoring=["External API health checks", "Basic response monitoring"],
            log_aggregation="Platform-integrated logging",
            metrics_retention="30 days retention"
        )
        
        # Safe fallback cost monitoring
        fallback_cost_monitoring = CostMonitoring(
            cost_tracking_platform="Platform billing dashboard",
            real_time_cost_alerts=["Monthly budget alerts", "Basic spending notifications"],
            budget_management=["Monthly budget tracking", "Basic cost reporting"],
            cost_optimization_recommendations=["Monitor usage patterns", "Review resource allocation"],
            resource_utilization_tracking=["Basic resource usage monitoring"],
            billing_anomaly_detection=["Unusual spending alerts"],
            cost_allocation=["Service-level cost tracking"],
            optimization_automation=["Basic resource cleanup"],
            reporting_dashboards=["Monthly cost reports"],
            forecasting=["Basic cost projections"]
        )
        
        # Safe fallback security monitoring
        fallback_security_monitoring = SecurityMonitoring(
            security_monitoring_platform="Platform security features",
            access_log_monitoring=["Login monitoring", "Basic access tracking"],
            vulnerability_scanning=["Basic dependency scanning"],
            intrusion_detection=["Basic anomaly detection"],
            compliance_monitoring=["Basic audit logging"],
            incident_response_automation=["Basic incident notification"],
            threat_intelligence=["Platform security alerts"],
            audit_logging=["Basic system access logs"],
            security_alerting=["Security incident notifications"],
            forensic_capabilities=["Basic log analysis"]
        )
        
        # Safe fallback alerting system
        fallback_alerting_system = AlertingSystem(
            alerting_platform="Email and platform notifications",
            notification_channels=["Email alerts", "Platform notifications"],
            escalation_procedures=["Email escalation", "Manual notification"],
            alert_categorization=["Critical", "Warning", "Info"],
            automated_responses=["Basic automated restarts"],
            alert_suppression=["Basic deduplication"],
            on_call_management=["Email-based on-call"],
            incident_management=["Manual incident tracking"],
            communication_templates=["Basic notification templates"],
            alert_analytics=["Basic alert tracking"]
        )
        
        # Safe fallback dashboard configuration
        fallback_dashboard_configuration = DashboardConfiguration(
            dashboard_platform="Platform dashboard",
            executive_dashboards=["System health overview"],
            technical_dashboards=["Resource usage dashboard"],
            business_dashboards=["Basic performance metrics"],
            operational_dashboards=["System status dashboard"],
            custom_reports=["Weekly status reports"],
            mobile_dashboards=["Mobile-friendly status view"],
            public_status_pages=["Basic status page"],
            data_visualization=["Basic charts and graphs"],
            dashboard_automation=["Automated dashboard refresh"]
        )
        
        # Safe fallback performance optimization
        fallback_performance_optimization = PerformanceOptimization(
            performance_monitoring_platform="Basic performance monitoring",
            application_performance=["Response time monitoring", "Basic error tracking"],
            database_optimization=["Query performance monitoring"],
            bottleneck_detection=["Basic resource bottleneck detection"],
            capacity_planning=["Basic usage trend analysis"],
            optimization_recommendations=["Manual performance reviews"],
            load_testing_integration=["Basic load testing"],
            user_experience_monitoring=["Basic user monitoring"],
            service_dependency_mapping=["Basic service monitoring"],
            performance_baselines=["Basic performance baselines"]
        )
        
        return MonitoringPlan(
            system_name="CrewAI System",
            monitoring_complexity="basic",
            total_monitoring_cost="$15-30/month",
            implementation_timeline="1-2 weeks",
            system_monitoring=fallback_system_monitoring,
            cost_monitoring=fallback_cost_monitoring,
            security_monitoring=fallback_security_monitoring,
            alerting_system=fallback_alerting_system,
            dashboard_configuration=fallback_dashboard_configuration,
            performance_optimization=fallback_performance_optimization,
            data_retention_policies=["30 days metrics", "90 days logs"],
            backup_and_recovery=["Weekly backup verification"],
            team_training=["Basic monitoring training"],
            continuous_improvement=["Monthly review process"],
            compliance_requirements=["Basic audit logging"],
            integration_points=["Platform API integration"],
            success_metrics=["System uptime > 99%", "Basic performance targets"],
            maintenance_procedures=["Weekly system checks"],
            documentation_links=["Basic monitoring documentation"]
        )
    
    def _build_monitoring_patterns(self) -> Dict[str, Any]:
        """Build monitoring pattern knowledge base."""
        return {
            "observability_pillars": {
                "metrics": "Quantitative measurements of system behavior",
                "logs": "Detailed event records for debugging and analysis",
                "traces": "Request flow tracking across distributed systems"
            },
            "monitoring_levels": {
                "infrastructure": "Hardware and platform monitoring",
                "application": "Application performance and behavior",
                "business": "Business KPIs and user experience"
            },
            "alert_strategies": {
                "symptom_based": "Alert on user-visible symptoms",
                "cause_based": "Alert on underlying causes",
                "predictive": "Alert on trends before issues occur"
            }
        }
    
    def _build_alerting_strategies(self) -> Dict[str, List[str]]:
        """Build alerting strategy knowledge base."""
        return {
            "alert_design_principles": [
                "Every alert should be actionable",
                "Alerts should be precise and avoid false positives",
                "Alert escalation should be time-sensitive",
                "Alert suppression should prevent noise",
                "Alert documentation should enable quick response"
            ],
            "escalation_best_practices": [
                "Primary notification within 1 minute",
                "Secondary escalation after 15 minutes",
                "Management escalation for extended incidents",
                "Customer communication for external impact",
                "Post-incident review for all critical alerts"
            ]
        }
    
    def _build_optimization_frameworks(self) -> Dict[str, List[str]]:
        """Build optimization framework knowledge base."""
        return {
            "performance_optimization": [
                "Identify bottlenecks through systematic analysis",
                "Optimize highest-impact areas first",
                "Measure before and after optimization",
                "Consider cost vs. performance trade-offs",
                "Implement gradual optimization changes"
            ],
            "cost_optimization": [
                "Right-size resources based on actual usage",
                "Use reserved instances for predictable workloads",
                "Implement auto-scaling for variable demand",
                "Monitor and eliminate resource waste",
                "Regular cost analysis and optimization reviews"
            ]
        }


def create_monitoring_engineer() -> MonitoringEngineer:
    """Factory function to create a MonitoringEngineer instance."""
    return MonitoringEngineer()
