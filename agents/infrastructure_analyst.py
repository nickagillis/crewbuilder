"""
Infrastructure Analyst Agent for CrewBuilder
Evaluates hosting platforms, analyzes costs, and recommends optimal infrastructure for AI agent systems.
"""

from crewai import Agent, Task
from .llm_config import get_configured_llm
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field


class PlatformEvaluation(BaseModel):
    """Represents a comprehensive evaluation of a hosting platform"""
    platform_name: str = Field(description="Platform name (e.g., 'AWS', 'Google Cloud', 'DigitalOcean')")
    platform_type: str = Field(description="'cloud', 'serverless', 'container', 'traditional'")
    suitability_score: int = Field(description="Overall suitability score (1-10)")
    cost_estimate: str = Field(description="Monthly cost estimate range")
    performance_rating: int = Field(description="Performance rating (1-10)")
    ease_of_use: int = Field(description="Ease of setup and management (1-10)")
    scalability_rating: int = Field(description="Scalability potential (1-10)")
    geographic_coverage: List[str] = Field(description="Available regions/data centers")
    strengths: List[str] = Field(description="Platform strengths for AI systems")
    limitations: List[str] = Field(description="Platform limitations and constraints")
    setup_complexity: str = Field(description="'simple', 'moderate', 'complex'")
    minimum_technical_skill: str = Field(description="'beginner', 'intermediate', 'advanced'")


class CostAnalysis(BaseModel):
    """Represents detailed cost analysis and projections"""
    platform: str = Field(description="Platform name")
    base_monthly_cost: str = Field(description="Base hosting cost per month")
    traffic_scaling_cost: str = Field(description="Additional cost per 1000 requests")
    storage_cost: str = Field(description="Storage cost per GB per month")
    bandwidth_cost: str = Field(description="Data transfer cost per GB")
    estimated_monthly_total: str = Field(description="Total estimated monthly cost")
    cost_optimization_tips: List[str] = Field(description="Ways to reduce costs")
    free_tier_available: bool = Field(description="Whether platform offers free tier")
    free_tier_limits: str = Field(description="Free tier limitations and duration")
    scaling_cost_projection: Dict[str, str] = Field(description="Cost projections at different scales")
    hidden_costs: List[str] = Field(description="Potential hidden or unexpected costs")


class SecurityAssessment(BaseModel):
    """Represents security and compliance evaluation"""
    platform: str = Field(description="Platform name")
    security_rating: int = Field(description="Overall security score (1-10)")
    data_encryption: bool = Field(description="Data encryption at rest and in transit")
    compliance_standards: List[str] = Field(description="Supported compliance standards (SOC2, GDPR, etc.)")
    access_controls: List[str] = Field(description="Available access control features")
    network_security: List[str] = Field(description="Network security features")
    backup_options: List[str] = Field(description="Backup and disaster recovery options")
    vulnerability_management: bool = Field(description="Automated vulnerability scanning")
    incident_response: str = Field(description="Platform incident response capabilities")
    data_residency_options: List[str] = Field(description="Data residency and sovereignty options")
    security_recommendations: List[str] = Field(description="Security best practices for this platform")


class InfrastructureRecommendation(BaseModel):
    """Complete infrastructure recommendation plan"""
    system_name: str = Field(description="Name of the AI system being deployed")
    system_complexity: str = Field(description="'simple', 'moderate', 'complex'")
    recommended_platform: str = Field(description="Primary recommended platform")
    alternative_platforms: List[str] = Field(description="Alternative platform options")
    deployment_strategy: str = Field(description="Recommended deployment approach")
    estimated_setup_time: str = Field(description="Time required for initial setup")
    total_monthly_cost_estimate: str = Field(description="Total estimated monthly operational cost")
    platform_evaluation: PlatformEvaluation = Field(description="Detailed evaluation of recommended platform")
    cost_analysis: CostAnalysis = Field(description="Comprehensive cost analysis")
    security_assessment: SecurityAssessment = Field(description="Security and compliance evaluation")
    scalability_plan: List[str] = Field(description="Scaling strategy and milestones")
    monitoring_requirements: List[str] = Field(description="Required monitoring and alerting setup")
    maintenance_considerations: List[str] = Field(description="Ongoing maintenance tasks and schedule")
    risk_factors: List[str] = Field(description="Potential risks and mitigation strategies")
    success_metrics: List[str] = Field(description="Key performance indicators to track")
    implementation_roadmap: List[str] = Field(description="Step-by-step implementation plan")


class InfrastructureAnalyst:
    """Infrastructure Analyst agent for evaluating hosting platforms and recommending optimal infrastructure."""
    
    def __init__(self):
        """Initialize the Infrastructure Analyst agent."""
        # Get configured LLM

        llm = get_configured_llm(temperature=0.7)

        

        self.agent = Agent(
            role="Infrastructure Analyst", 
            goal="Evaluate hosting platforms, analyze costs, and recommend optimal infrastructure solutions that balance performance, cost, security, and operational simplicity for AI agent systems",
            backstory="""You are a seasoned infrastructure architect and cloud consultant with 15+ years of experience helping organizations deploy production systems at scale. You've guided hundreds of companies through platform migrations, cost optimizations, and scaling challenges across every major cloud provider and hosting solution.

            Your expertise spans the entire spectrum from simple shared hosting to complex multi-cloud architectures. You understand not just the technical capabilities of different platforms, but the real-world operational challenges, hidden costs, and scaling bottlenecks that emerge over time. You've seen the same mistakes repeated across organizations and know how to prevent them.

            You excel at translating business requirements into infrastructure reality. You know when a startup should choose simplicity over scalability, when enterprise compliance requirements drive platform selection, and how to build systems that can evolve as organizations grow. Your recommendations are always practical, considering not just today's needs but tomorrow's growth.

            You have deep knowledge of modern deployment patterns, from traditional VPS hosting to serverless architectures, container orchestration, and edge computing. You stay current with pricing changes, new service offerings, and platform limitations across all major providers. Most importantly, you understand that the best infrastructure is the one that teams can actually manage and maintain successfully.

            Your recommendations prioritize operational sanity: systems that are observable, maintainable, secure by default, and cost-predictable. You know that premature optimization is dangerous, but so is technical debt that becomes expensive to fix later.""",
            verbose=True,
            allow_delegation=False,
            llm=llm  # Pass the LLM explicitly
        )
        
        # Platform knowledge base with real-world data
        self.platform_database = self._build_platform_database()
        self.pricing_data = self._build_pricing_database()
        self.security_standards = self._build_security_database()
    
    def analyze_infrastructure_requirements(self, 
                                          documentation_plan: Dict[str, Any], 
                                          api_integration_plan: Dict[str, Any], 
                                          system_complexity: str = "moderate") -> InfrastructureRecommendation:
        """
        Analyze infrastructure requirements and recommend optimal hosting solution.
        
        Args:
            documentation_plan: Complete documentation from Documentation Specialist
            api_integration_plan: API requirements from API Detective
            system_complexity: System complexity level ('simple', 'moderate', 'complex')
            
        Returns:
            Complete infrastructure recommendation with platform evaluation
        """
        try:
            # Analyze system requirements
            system_analysis = self._analyze_system_requirements(documentation_plan, api_integration_plan, system_complexity)
            
            # Evaluate platforms based on requirements
            platform_evaluations = self._evaluate_platforms(system_analysis)
            
            # Select optimal platform
            recommended_platform = self._select_optimal_platform(platform_evaluations, system_analysis)
            
            # Perform detailed cost analysis
            cost_analysis = self._perform_cost_analysis(recommended_platform, system_analysis)
            
            # Conduct security assessment
            security_assessment = self._conduct_security_assessment(recommended_platform, system_analysis)
            
            # Create scalability plan
            scalability_plan = self._create_scalability_plan(recommended_platform, system_analysis)
            
            # Generate monitoring requirements
            monitoring_requirements = self._generate_monitoring_requirements(recommended_platform, system_analysis)
            
            # Assess risks and create mitigation strategies
            risk_factors = self._assess_risks(recommended_platform, system_analysis)
            
            # Create implementation roadmap
            implementation_roadmap = self._create_implementation_roadmap(recommended_platform, system_analysis)
            
            return InfrastructureRecommendation(
                system_name=system_analysis.get("system_name", "CrewAI System"),
                system_complexity=system_complexity,
                recommended_platform=recommended_platform["platform_name"],
                alternative_platforms=[p["platform_name"] for p in platform_evaluations[:3] if p["platform_name"] != recommended_platform["platform_name"]],
                deployment_strategy=self._determine_deployment_strategy(recommended_platform, system_analysis),
                estimated_setup_time=self._estimate_setup_time(recommended_platform, system_analysis),
                total_monthly_cost_estimate=cost_analysis.estimated_monthly_total,
                platform_evaluation=self._create_platform_evaluation(recommended_platform),
                cost_analysis=cost_analysis,
                security_assessment=security_assessment,
                scalability_plan=scalability_plan,
                monitoring_requirements=monitoring_requirements,
                maintenance_considerations=self._generate_maintenance_considerations(recommended_platform),
                risk_factors=risk_factors,
                success_metrics=self._define_success_metrics(system_analysis),
                implementation_roadmap=implementation_roadmap
            )
        
        except Exception as e:
            # Fallback infrastructure recommendation for error cases
            return self._generate_fallback_infrastructure_recommendation(str(e), system_complexity)
    
    def _analyze_system_requirements(self, documentation_plan: Dict[str, Any], api_integration_plan: Dict[str, Any], system_complexity: str) -> Dict[str, Any]:
        """Analyze system requirements to understand infrastructure needs."""
        analysis = {
            "system_name": "CrewAI System",
            "complexity": system_complexity,
            "estimated_requests_per_month": 10000,
            "api_dependencies": 1,
            "storage_requirements": "minimal",
            "compute_requirements": "light",
            "geographic_requirements": ["global"],
            "compliance_requirements": ["basic"],
            "budget_category": "startup"
        }
        
        # Extract from documentation plan
        if documentation_plan:
            analysis["system_name"] = documentation_plan.get("system_name", "CrewAI System")
            complexity_level = documentation_plan.get("complexity_level", "moderate")
            analysis["complexity"] = complexity_level
            
            # Estimate usage based on complexity
            if complexity_level == "simple":
                analysis["estimated_requests_per_month"] = 5000
                analysis["compute_requirements"] = "light"
            elif complexity_level == "complex":
                analysis["estimated_requests_per_month"] = 50000
                analysis["compute_requirements"] = "heavy"
        
        # Extract from API integration plan
        if api_integration_plan:
            api_count = api_integration_plan.get("total_apis", 1)
            analysis["api_dependencies"] = api_count
            
            # Adjust requirements based on API usage
            if api_count > 5:
                analysis["compute_requirements"] = "heavy"
                analysis["estimated_requests_per_month"] *= 2
            
            # Extract cost insights for budget category
            total_cost = api_integration_plan.get("total_estimated_cost", "$50-100")
            if "$200" in total_cost or "$300" in total_cost:
                analysis["budget_category"] = "enterprise"
            elif "$100" in total_cost:
                analysis["budget_category"] = "professional"
        
        return analysis
    
    def _evaluate_platforms(self, system_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate all relevant platforms based on system requirements."""
        complexity = system_analysis.get("complexity", "moderate")
        compute_requirements = system_analysis.get("compute_requirements", "light")
        budget_category = system_analysis.get("budget_category", "startup")
        
        platforms = []
        
        # Add platforms based on requirements
        for platform_name, platform_data in self.platform_database.items():
            # Skip platforms that don't match basic requirements
            if compute_requirements == "heavy" and platform_data.get("max_performance", 5) < 7:
                continue
            
            if budget_category == "startup" and platform_data.get("startup_friendly", True) == False:
                continue
            
            # Calculate suitability score
            suitability_score = self._calculate_platform_suitability(platform_data, system_analysis)
            
            platform_eval = {
                "platform_name": platform_name,
                "suitability_score": suitability_score,
                **platform_data
            }
            platforms.append(platform_eval)
        
        # Sort by suitability score
        platforms.sort(key=lambda x: x["suitability_score"], reverse=True)
        
        return platforms[:5]  # Return top 5 platforms
    
    def _select_optimal_platform(self, platform_evaluations: List[Dict[str, Any]], system_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Select the optimal platform based on evaluations and requirements."""
        if not platform_evaluations:
            return self.platform_database["Railway"]  # Safe fallback
        
        # Consider special cases
        complexity = system_analysis.get("complexity", "moderate")
        budget_category = system_analysis.get("budget_category", "startup")
        
        # For simple systems, prefer ease of use
        if complexity == "simple":
            platform_evaluations.sort(key=lambda x: (x["ease_of_use"], x["suitability_score"]), reverse=True)
        
        # For complex systems, prefer performance and scalability
        elif complexity == "complex":
            platform_evaluations.sort(key=lambda x: (x["performance_rating"], x["scalability_rating"], x["suitability_score"]), reverse=True)
        
        return platform_evaluations[0]
    
    def _calculate_platform_suitability(self, platform_data: Dict[str, Any], system_analysis: Dict[str, Any]) -> int:
        """Calculate how suitable a platform is for the specific system requirements."""
        score = 5  # Base score
        
        complexity = system_analysis.get("complexity", "moderate")
        compute_requirements = system_analysis.get("compute_requirements", "light")
        budget_category = system_analysis.get("budget_category", "startup")
        
        # Complexity matching
        if complexity == "simple" and platform_data.get("ease_of_use", 5) >= 8:
            score += 2
        elif complexity == "complex" and platform_data.get("enterprise_features", False):
            score += 2
        
        # Compute requirements
        if compute_requirements == "light" and platform_data.get("cost_efficiency", 5) >= 7:
            score += 1
        elif compute_requirements == "heavy" and platform_data.get("max_performance", 5) >= 8:
            score += 2
        
        # Budget considerations
        if budget_category == "startup" and platform_data.get("startup_friendly", True):
            score += 1
        
        # Performance bonus
        score += min(platform_data.get("performance_rating", 5) // 2, 2)
        
        # Reliability bonus
        score += min(platform_data.get("reliability_rating", 5) // 3, 1)
        
        return min(10, max(1, score))
    
    def _perform_cost_analysis(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> CostAnalysis:
        """Perform detailed cost analysis for the selected platform."""
        platform_name = platform["platform_name"]
        pricing = self.pricing_data.get(platform_name, {})
        
        # Estimate costs based on system requirements
        requests_per_month = system_analysis.get("estimated_requests_per_month", 10000)
        compute_requirements = system_analysis.get("compute_requirements", "light")
        
        # Base cost calculation
        if compute_requirements == "light":
            base_cost = pricing.get("light_compute_monthly", "$10-25")
        elif compute_requirements == "heavy":
            base_cost = pricing.get("heavy_compute_monthly", "$50-150")
        else:
            base_cost = pricing.get("moderate_compute_monthly", "$25-75")
        
        # Scaling cost
        traffic_scaling = pricing.get("per_1k_requests", "$0.10-0.50")
        
        # Storage and bandwidth
        storage_cost = pricing.get("storage_per_gb_monthly", "$0.10-0.25")
        bandwidth_cost = pricing.get("bandwidth_per_gb", "$0.05-0.15")
        
        # Total estimation
        estimated_total = self._calculate_total_cost(base_cost, requests_per_month, traffic_scaling)
        
        # Scaling projections
        scaling_projections = {
            "1x current": estimated_total,
            "10x growth": self._calculate_total_cost(base_cost, requests_per_month * 10, traffic_scaling),
            "100x growth": self._calculate_total_cost(base_cost, requests_per_month * 100, traffic_scaling)
        }
        
        # Optimization tips
        optimization_tips = pricing.get("cost_optimization_tips", [
            "Use free tier limits effectively",
            "Monitor usage patterns for optimization",
            "Consider reserved instances for predictable loads",
            "Implement efficient caching strategies"
        ])
        
        # Hidden costs
        hidden_costs = pricing.get("hidden_costs", [
            "Data transfer between services",
            "Premium support costs",
            "Additional security features",
            "Backup and disaster recovery"
        ])
        
        return CostAnalysis(
            platform=platform_name,
            base_monthly_cost=base_cost,
            traffic_scaling_cost=traffic_scaling,
            storage_cost=storage_cost,
            bandwidth_cost=bandwidth_cost,
            estimated_monthly_total=estimated_total,
            cost_optimization_tips=optimization_tips,
            free_tier_available=pricing.get("free_tier_available", True),
            free_tier_limits=pricing.get("free_tier_limits", "Limited requests and storage"),
            scaling_cost_projection=scaling_projections,
            hidden_costs=hidden_costs
        )
    
    def _conduct_security_assessment(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> SecurityAssessment:
        """Conduct security and compliance assessment for the platform."""
        platform_name = platform["platform_name"]
        security_data = self.security_standards.get(platform_name, {})
        
        return SecurityAssessment(
            platform=platform_name,
            security_rating=security_data.get("security_rating", 7),
            data_encryption=security_data.get("data_encryption", True),
            compliance_standards=security_data.get("compliance_standards", ["SOC2", "GDPR"]),
            access_controls=security_data.get("access_controls", ["RBAC", "MFA", "API Keys"]),
            network_security=security_data.get("network_security", ["TLS/SSL", "Firewalls", "DDoS Protection"]),
            backup_options=security_data.get("backup_options", ["Automated backups", "Point-in-time recovery"]),
            vulnerability_management=security_data.get("vulnerability_management", True),
            incident_response=security_data.get("incident_response", "24/7 support with defined SLAs"),
            data_residency_options=security_data.get("data_residency_options", ["US", "EU", "Global"]),
            security_recommendations=security_data.get("security_recommendations", [
                "Enable two-factor authentication",
                "Use least-privilege access principles",
                "Regularly rotate API keys and credentials",
                "Monitor access logs and audit trails",
                "Keep all software dependencies updated"
            ])
        )
    
    def _create_scalability_plan(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> List[str]:
        """Create a scalability plan for the system."""
        platform_name = platform["platform_name"]
        
        base_plan = [
            "Start with minimal resource allocation to optimize costs",
            "Monitor key performance metrics (response time, error rate, resource usage)",
            "Set up automated alerting for resource thresholds",
            "Plan horizontal scaling triggers (CPU > 70%, memory > 80%)"
        ]
        
        # Platform-specific scaling strategies
        if platform_name in ["AWS", "Google Cloud", "Azure"]:
            base_plan.extend([
                "Implement auto-scaling groups with load balancers",
                "Use managed services for databases and caching",
                "Consider CDN for static content and global distribution",
                "Implement blue-green deployments for zero-downtime updates"
            ])
        elif platform_name in ["Railway", "Render", "Fly.io"]:
            base_plan.extend([
                "Use platform's built-in auto-scaling features",
                "Optimize container resource requests and limits",
                "Consider upgrading to higher-tier plans for better performance",
                "Implement database read replicas for read-heavy workloads"
            ])
        elif platform_name == "DigitalOcean":
            base_plan.extend([
                "Use managed databases and load balancers",
                "Implement droplet scaling with floating IPs",
                "Consider Kubernetes for container orchestration",
                "Use Spaces for object storage and CDN"
            ])
        
        base_plan.extend([
            "Regular performance testing and capacity planning",
            "Database optimization and query performance tuning",
            "Consider caching strategies (Redis, Memcached)",
            "Plan for disaster recovery and multi-region deployment"
        ])
        
        return base_plan
    
    def _generate_monitoring_requirements(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> List[str]:
        """Generate monitoring and alerting requirements."""
        return [
            "Application performance monitoring (APM) for response times and errors",
            "Infrastructure monitoring for CPU, memory, disk, and network usage",
            "API endpoint monitoring with uptime and latency tracking",
            "Error rate and exception monitoring with alerting thresholds",
            "Cost monitoring and budget alerts to prevent overspend",
            "Security monitoring for unauthorized access and suspicious activity",
            "Database performance monitoring for query optimization",
            "Log aggregation and analysis for debugging and troubleshooting",
            "Health checks and availability monitoring from multiple regions",
            "Custom business metrics relevant to AI agent performance",
            "Automated incident response and escalation procedures",
            "Regular backup verification and disaster recovery testing"
        ]
    
    def _assess_risks(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> List[str]:
        """Assess potential risks and create mitigation strategies."""
        platform_name = platform["platform_name"]
        complexity = system_analysis.get("complexity", "moderate")
        
        base_risks = [
            "Vendor lock-in: Platform-specific features may make migration difficult",
            "Cost escalation: Usage growth may lead to unexpected expenses",
            "Service outages: Platform downtime affects system availability",
            "API rate limiting: External API limits may impact system performance"
        ]
        
        # Platform-specific risks
        if platform_name in ["Railway", "Render", "Fly.io"]:
            base_risks.append("Platform maturity: Newer platforms may have stability concerns")
        
        if platform_name == "AWS":
            base_risks.append("Complexity overhead: Rich feature set may lead to over-engineering")
        
        if complexity == "complex":
            base_risks.extend([
                "Integration complexity: Multiple services increase failure points",
                "Security vulnerabilities: Complex systems have larger attack surfaces",
                "Operational overhead: More moving parts require more monitoring"
            ])
        
        # Add mitigation strategies
        mitigation_risks = []
        for risk in base_risks:
            if "Vendor lock-in" in risk:
                mitigation_risks.append(f"{risk} → Mitigation: Use containerization and standard APIs")
            elif "Cost escalation" in risk:
                mitigation_risks.append(f"{risk} → Mitigation: Implement budget alerts and usage monitoring")
            elif "Service outages" in risk:
                mitigation_risks.append(f"{risk} → Mitigation: Multi-region deployment and failover procedures")
            else:
                mitigation_risks.append(f"{risk} → Mitigation: Regular monitoring and incident response plans")
        
        return mitigation_risks
    
    def _create_implementation_roadmap(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> List[str]:
        """Create step-by-step implementation roadmap."""
        platform_name = platform["platform_name"]
        
        roadmap = [
            "Week 1: Platform account setup and initial configuration",
            "Week 1: Development environment deployment and testing",
            "Week 2: Production environment setup with basic monitoring",
            "Week 2: Security configuration and access controls implementation",
            "Week 3: CI/CD pipeline setup and deployment automation",
            "Week 3: Comprehensive monitoring and alerting configuration",
            "Week 4: Performance testing and optimization",
            "Week 4: Documentation update and team training",
            "Ongoing: Regular monitoring, optimization, and maintenance"
        ]
        
        # Adjust timeline based on complexity
        complexity = system_analysis.get("complexity", "moderate")
        if complexity == "simple":
            roadmap = [item.replace("Week", "Day") for item in roadmap[:6]]
            roadmap = [item.replace("Day 4", "Week 1") for item in roadmap]
        elif complexity == "complex":
            roadmap = [item.replace("Week", "Month") for item in roadmap]
        
        return roadmap
    
    def _determine_deployment_strategy(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> str:
        """Determine the optimal deployment strategy."""
        platform_name = platform["platform_name"]
        complexity = system_analysis.get("complexity", "moderate")
        
        if complexity == "simple":
            return "Single-container deployment with managed database"
        elif complexity == "complex":
            if platform_name in ["AWS", "Google Cloud", "Azure"]:
                return "Microservices architecture with container orchestration"
            else:
                return "Multi-container deployment with service mesh"
        else:
            return "Containerized deployment with horizontal scaling"
    
    def _estimate_setup_time(self, platform: Dict[str, Any], system_analysis: Dict[str, Any]) -> str:
        """Estimate time required for initial setup."""
        complexity = system_analysis.get("complexity", "moderate")
        platform_ease = platform.get("ease_of_use", 5)
        
        base_hours = 8  # Base setup time
        
        # Adjust for complexity
        if complexity == "simple":
            base_hours = 4
        elif complexity == "complex":
            base_hours = 24
        
        # Adjust for platform ease of use
        if platform_ease >= 8:
            base_hours = base_hours * 0.7
        elif platform_ease <= 4:
            base_hours = base_hours * 1.5
        
        base_hours = int(base_hours)
        
        if base_hours <= 8:
            return f"{base_hours} hours"
        elif base_hours <= 40:
            return f"{base_hours // 8} days"
        else:
            return f"{base_hours // 40} weeks"
    
    def _create_platform_evaluation(self, platform: Dict[str, Any]) -> PlatformEvaluation:
        """Create detailed platform evaluation object."""
        return PlatformEvaluation(
            platform_name=platform["platform_name"],
            platform_type=platform.get("platform_type", "cloud"),
            suitability_score=platform.get("suitability_score", 7),
            cost_estimate=platform.get("typical_monthly_cost", "$25-100"),
            performance_rating=platform.get("performance_rating", 7),
            ease_of_use=platform.get("ease_of_use", 7),
            scalability_rating=platform.get("scalability_rating", 7),
            geographic_coverage=platform.get("geographic_coverage", ["Global"]),
            strengths=platform.get("strengths", ["Reliable", "Well-documented"]),
            limitations=platform.get("limitations", ["Cost at scale"]),
            setup_complexity=platform.get("setup_complexity", "moderate"),
            minimum_technical_skill=platform.get("minimum_technical_skill", "intermediate")
        )
    
    def _generate_maintenance_considerations(self, platform: Dict[str, Any]) -> List[str]:
        """Generate maintenance considerations for the platform."""
        return [
            "Regular security updates and patch management",
            "Database maintenance and optimization (weekly)",
            "Backup verification and disaster recovery testing (monthly)",
            "Performance monitoring and optimization (ongoing)",
            "Cost analysis and optimization review (monthly)",
            "Security audit and access review (quarterly)",
            "Dependency updates and vulnerability scanning (weekly)",
            "Capacity planning and scaling review (quarterly)",
            "Documentation updates and team training (quarterly)",
            "Platform service updates and feature adoption (as needed)"
        ]
    
    def _define_success_metrics(self, system_analysis: Dict[str, Any]) -> List[str]:
        """Define key success metrics to track."""
        return [
            "System uptime > 99.9% (excluding planned maintenance)",
            "Average response time < 2 seconds for 95% of requests",
            "Error rate < 0.1% for all API endpoints",
            "Monthly cost within 10% of projected budget",
            "Zero security incidents or data breaches",
            "Successful automated backups with verified restore capability",
            "Scaling events complete within 5 minutes",
            "Mean time to recovery (MTTR) < 1 hour for incidents",
            "User satisfaction score > 4.5/5 for system performance",
            "Deployment success rate > 99% with rollback capability"
        ]
    
    def _calculate_total_cost(self, base_cost: str, requests: int, traffic_cost: str) -> str:
        """Calculate total cost estimate from components."""
        # Extract numbers from cost strings
        base_min = int(re.findall(r'\d+', base_cost.split('-')[0])[0]) if '-' in base_cost else int(re.findall(r'\d+', base_cost)[0])
        base_max = int(re.findall(r'\d+', base_cost.split('-')[1])[0]) if '-' in base_cost else base_min * 1.5
        
        # Traffic cost calculation (simplified)
        traffic_per_month = requests / 1000 * float(re.findall(r'[\d.]+', traffic_cost)[0])
        
        total_min = base_min + traffic_per_month
        total_max = base_max + traffic_per_month * 2
        
        return f"${int(total_min)}-{int(total_max)}"
    
    def _generate_fallback_infrastructure_recommendation(self, error_message: str, system_complexity: str) -> InfrastructureRecommendation:
        """Generate a safe fallback infrastructure recommendation when errors occur."""
        
        # Safe fallback to Railway (beginner-friendly platform)
        fallback_platform = PlatformEvaluation(
            platform_name="Railway",
            platform_type="container",
            suitability_score=8,
            cost_estimate="$5-25",
            performance_rating=7,
            ease_of_use=9,
            scalability_rating=6,
            geographic_coverage=["Global"],
            strengths=["Extremely easy setup", "Git-based deployments", "Automatic HTTPS"],
            limitations=["Limited customization", "Cost at high scale"],
            setup_complexity="simple",
            minimum_technical_skill="beginner"
        )
        
        fallback_cost = CostAnalysis(
            platform="Railway",
            base_monthly_cost="$5-25",
            traffic_scaling_cost="$0.10 per 1000 requests",
            storage_cost="$0.25 per GB per month",
            bandwidth_cost="$0.10 per GB",
            estimated_monthly_total="$15-50",
            cost_optimization_tips=["Use free tier effectively", "Monitor usage patterns"],
            free_tier_available=True,
            free_tier_limits="500 hours per month, limited resources",
            scaling_cost_projection={"1x": "$15-50", "10x": "$50-200", "100x": "$500-2000"},
            hidden_costs=["Bandwidth overage charges"]
        )
        
        fallback_security = SecurityAssessment(
            platform="Railway",
            security_rating=8,
            data_encryption=True,
            compliance_standards=["SOC2"],
            access_controls=["Team management", "Environment variables"],
            network_security=["Automatic HTTPS", "Network isolation"],
            backup_options=["Volume snapshots"],
            vulnerability_management=True,
            incident_response="Community support with response SLAs",
            data_residency_options=["US", "EU"],
            security_recommendations=[
                "Use environment variables for all secrets",
                "Enable team access controls",
                "Regular dependency updates"
            ]
        )
        
        return InfrastructureRecommendation(
            system_name="CrewAI System",
            system_complexity=system_complexity,
            recommended_platform="Railway",
            alternative_platforms=["DigitalOcean", "Render", "Fly.io"],
            deployment_strategy="Container deployment with managed database",
            estimated_setup_time="2-4 hours",
            total_monthly_cost_estimate="$15-50",
            platform_evaluation=fallback_platform,
            cost_analysis=fallback_cost,
            security_assessment=fallback_security,
            scalability_plan=[
                "Start with basic plan and monitor usage",
                "Scale vertically first, then horizontally",
                "Consider migration to dedicated cloud if needed"
            ],
            monitoring_requirements=[
                "Railway's built-in monitoring",
                "Application-level health checks",
                "Cost monitoring and alerts"
            ],
            maintenance_considerations=[
                "Regular deployments via git push",
                "Monitor resource usage",
                "Update dependencies regularly"
            ],
            risk_factors=[
                "Platform vendor lock-in → Use containerized approach",
                "Cost at scale → Monitor and plan migration path"
            ],
            success_metrics=[
                "System uptime > 99%",
                "Response time < 3 seconds",
                "Cost within budget"
            ],
            implementation_roadmap=[
                "Day 1: Create Railway account and connect repository",
                "Day 1: Configure environment variables and deploy",
                "Day 2: Set up custom domain and monitoring",
                "Week 1: Performance testing and optimization"
            ]
        )
    
    def _build_platform_database(self) -> Dict[str, Dict[str, Any]]:
        """Build comprehensive platform knowledge database."""
        return {
            "Railway": {
                "platform_type": "container",
                "performance_rating": 7,
                "ease_of_use": 9,
                "scalability_rating": 6,
                "reliability_rating": 8,
                "startup_friendly": True,
                "enterprise_features": False,
                "max_performance": 7,
                "cost_efficiency": 8,
                "typical_monthly_cost": "$5-50",
                "geographic_coverage": ["US", "EU", "Asia"],
                "strengths": [
                    "Extremely simple deployment via git push",
                    "Automatic HTTPS and domain management",
                    "Built-in database services",
                    "Great developer experience",
                    "Generous free tier"
                ],
                "limitations": [
                    "Limited customization options",
                    "Can become expensive at scale",
                    "Fewer advanced features than major clouds",
                    "Less control over infrastructure"
                ],
                "setup_complexity": "simple",
                "minimum_technical_skill": "beginner"
            },
            "DigitalOcean": {
                "platform_type": "cloud",
                "performance_rating": 8,
                "ease_of_use": 7,
                "scalability_rating": 8,
                "reliability_rating": 8,
                "startup_friendly": True,
                "enterprise_features": True,
                "max_performance": 8,
                "cost_efficiency": 8,
                "typical_monthly_cost": "$10-100",
                "geographic_coverage": ["Global", "14+ data centers"],
                "strengths": [
                    "Predictable pricing with no hidden costs",
                    "Strong documentation and community",
                    "Good performance for the price",
                    "Managed services (databases, Kubernetes)",
                    "Developer-friendly interface"
                ],
                "limitations": [
                    "Fewer services than AWS/GCP/Azure",
                    "Limited enterprise compliance features",
                    "Smaller ecosystem",
                    "Less advanced AI/ML services"
                ],
                "setup_complexity": "moderate",
                "minimum_technical_skill": "intermediate"
            },
            "AWS": {
                "platform_type": "cloud",
                "performance_rating": 10,
                "ease_of_use": 4,
                "scalability_rating": 10,
                "reliability_rating": 10,
                "startup_friendly": False,
                "enterprise_features": True,
                "max_performance": 10,
                "cost_efficiency": 6,
                "typical_monthly_cost": "$50-500",
                "geographic_coverage": ["Global", "30+ regions"],
                "strengths": [
                    "Unmatched service breadth and depth",
                    "Best-in-class performance and reliability",
                    "Extensive enterprise features",
                    "Strong security and compliance",
                    "Massive ecosystem and community"
                ],
                "limitations": [
                    "Steep learning curve",
                    "Complex pricing can lead to bill shock",
                    "Over-engineering risk",
                    "Vendor lock-in concerns"
                ],
                "setup_complexity": "complex",
                "minimum_technical_skill": "advanced"
            },
            "Google Cloud": {
                "platform_type": "cloud",
                "performance_rating": 9,
                "ease_of_use": 6,
                "scalability_rating": 10,
                "reliability_rating": 9,
                "startup_friendly": True,
                "enterprise_features": True,
                "max_performance": 10,
                "cost_efficiency": 7,
                "typical_monthly_cost": "$40-400",
                "geographic_coverage": ["Global", "35+ regions"],
                "strengths": [
                    "Excellent AI/ML services",
                    "Strong Kubernetes support",
                    "Competitive pricing for compute",
                    "Good documentation",
                    "Innovation in cloud-native technologies"
                ],
                "limitations": [
                    "Smaller ecosystem than AWS",
                    "Some services less mature",
                    "Learning curve for AWS migrants",
                    "Billing complexity"
                ],
                "setup_complexity": "complex",
                "minimum_technical_skill": "advanced"
            },
            "Render": {
                "platform_type": "container",
                "performance_rating": 7,
                "ease_of_use": 8,
                "scalability_rating": 7,
                "reliability_rating": 8,
                "startup_friendly": True,
                "enterprise_features": False,
                "max_performance": 7,
                "cost_efficiency": 7,
                "typical_monthly_cost": "$7-75",
                "geographic_coverage": ["US", "EU"],
                "strengths": [
                    "Simple deployment from git",
                    "Automatic SSL and CDN",
                    "Built-in monitoring",
                    "Good performance",
                    "Fair pricing"
                ],
                "limitations": [
                    "Limited geographic coverage",
                    "Fewer advanced features",
                    "No enterprise support tiers",
                    "Limited customization"
                ],
                "setup_complexity": "simple",
                "minimum_technical_skill": "beginner"
            },
            "Fly.io": {
                "platform_type": "container",
                "performance_rating": 8,
                "ease_of_use": 6,
                "scalability_rating": 8,
                "reliability_rating": 7,
                "startup_friendly": True,
                "enterprise_features": False,
                "max_performance": 8,
                "cost_efficiency": 8,
                "typical_monthly_cost": "$5-50",
                "geographic_coverage": ["Global", "Edge locations"],
                "strengths": [
                    "Edge computing capabilities",
                    "Fast global deployment",
                    "Good performance",
                    "Competitive pricing",
                    "Developer-friendly"
                ],
                "limitations": [
                    "Newer platform with less stability",
                    "Limited enterprise features",
                    "Smaller community",
                    "Learning curve for configuration"
                ],
                "setup_complexity": "moderate",
                "minimum_technical_skill": "intermediate"
            },
            "Azure": {
                "platform_type": "cloud",
                "performance_rating": 9,
                "ease_of_use": 5,
                "scalability_rating": 10,
                "reliability_rating": 9,
                "startup_friendly": False,
                "enterprise_features": True,
                "max_performance": 10,
                "cost_efficiency": 6,
                "typical_monthly_cost": "$45-450",
                "geographic_coverage": ["Global", "60+ regions"],
                "strengths": [
                    "Strong enterprise integration",
                    "Excellent Windows support",
                    "Good hybrid cloud capabilities",
                    "Strong security features",
                    "Microsoft ecosystem integration"
                ],
                "limitations": [
                    "Complex pricing and billing",
                    "Steep learning curve",
                    "UI can be overwhelming",
                    "Some services lag behind AWS"
                ],
                "setup_complexity": "complex",
                "minimum_technical_skill": "advanced"
            }
        }
    
    def _build_pricing_database(self) -> Dict[str, Dict[str, Any]]:
        """Build pricing information database."""
        return {
            "Railway": {
                "light_compute_monthly": "$5-15",
                "moderate_compute_monthly": "$15-35",
                "heavy_compute_monthly": "$35-100",
                "per_1k_requests": "$0.10",
                "storage_per_gb_monthly": "$0.25",
                "bandwidth_per_gb": "$0.10",
                "free_tier_available": True,
                "free_tier_limits": "500 execution hours, 1GB RAM, 1GB storage",
                "cost_optimization_tips": [
                    "Optimize container resource requests",
                    "Use sleep mode for development environments",
                    "Monitor usage with Railway's dashboard"
                ],
                "hidden_costs": [
                    "Bandwidth overage charges",
                    "Premium support costs"
                ]
            },
            "DigitalOcean": {
                "light_compute_monthly": "$12-25",
                "moderate_compute_monthly": "$25-75",
                "heavy_compute_monthly": "$75-200",
                "per_1k_requests": "$0.15",
                "storage_per_gb_monthly": "$0.10",
                "bandwidth_per_gb": "$0.01",
                "free_tier_available": True,
                "free_tier_limits": "$200 credit for 60 days",
                "cost_optimization_tips": [
                    "Use block storage for better pricing",
                    "Implement load balancers only when needed",
                    "Use managed databases for better cost predictability"
                ],
                "hidden_costs": [
                    "Load balancer costs ($15/month)",
                    "Managed database overhead",
                    "Snapshot storage costs"
                ]
            },
            "AWS": {
                "light_compute_monthly": "$25-75",
                "moderate_compute_monthly": "$75-200",
                "heavy_compute_monthly": "$200-1000",
                "per_1k_requests": "$0.20-0.50",
                "storage_per_gb_monthly": "$0.023",
                "bandwidth_per_gb": "$0.09",
                "free_tier_available": True,
                "free_tier_limits": "12 months, limited EC2, RDS, S3",
                "cost_optimization_tips": [
                    "Use reserved instances for predictable workloads",
                    "Implement auto-scaling to avoid over-provisioning",
                    "Use spot instances for non-critical workloads",
                    "Regular cost analysis with Cost Explorer"
                ],
                "hidden_costs": [
                    "Data transfer between services",
                    "NAT Gateway costs",
                    "Load balancer costs",
                    "CloudWatch detailed monitoring",
                    "Premium support plans"
                ]
            },
            "Google Cloud": {
                "light_compute_monthly": "$20-60",
                "moderate_compute_monthly": "$60-180",
                "heavy_compute_monthly": "$180-800",
                "per_1k_requests": "$0.15-0.40",
                "storage_per_gb_monthly": "$0.020",
                "bandwidth_per_gb": "$0.12",
                "free_tier_available": True,
                "free_tier_limits": "$300 credit + always-free tier",
                "cost_optimization_tips": [
                    "Use sustained use discounts",
                    "Implement preemptible instances",
                    "Use committed use contracts",
                    "Regular billing analysis"
                ],
                "hidden_costs": [
                    "Network egress charges",
                    "Load balancer costs",
                    "Premium support",
                    "Advanced monitoring features"
                ]
            },
            "Render": {
                "light_compute_monthly": "$7-20",
                "moderate_compute_monthly": "$20-50",
                "heavy_compute_monthly": "$50-150",
                "per_1k_requests": "$0.12",
                "storage_per_gb_monthly": "$0.30",
                "bandwidth_per_gb": "$0.10",
                "free_tier_available": True,
                "free_tier_limits": "750 hours static sites, limited web services",
                "cost_optimization_tips": [
                    "Use static site hosting for frontend",
                    "Optimize Docker images for faster builds",
                    "Monitor usage patterns"
                ],
                "hidden_costs": [
                    "Build minutes overages",
                    "Custom domain SSL (free)",
                    "Premium support features"
                ]
            },
            "Fly.io": {
                "light_compute_monthly": "$5-15",
                "moderate_compute_monthly": "$15-40",
                "heavy_compute_monthly": "$40-120",
                "per_1k_requests": "$0.08",
                "storage_per_gb_monthly": "$0.15",
                "bandwidth_per_gb": "$0.02",
                "free_tier_available": True,
                "free_tier_limits": "3 shared-cpu VMs, 3GB storage",
                "cost_optimization_tips": [
                    "Use shared CPU instances when possible",
                    "Leverage edge caching",
                    "Optimize for fewer regions initially"
                ],
                "hidden_costs": [
                    "Additional region costs",
                    "Volume storage costs",
                    "Support plan costs"
                ]
            },
            "Azure": {
                "light_compute_monthly": "$30-80",
                "moderate_compute_monthly": "$80-220",
                "heavy_compute_monthly": "$220-1200",
                "per_1k_requests": "$0.20-0.60",
                "storage_per_gb_monthly": "$0.024",
                "bandwidth_per_gb": "$0.087",
                "free_tier_available": True,
                "free_tier_limits": "$200 credit + 12 months free services",
                "cost_optimization_tips": [
                    "Use Azure Advisor for recommendations",
                    "Implement auto-shutdown for dev resources",
                    "Use reserved instances",
                    "Regular cost analysis"
                ],
                "hidden_costs": [
                    "Network security group costs",
                    "Load balancer costs",
                    "Premium support plans",
                    "Advanced monitoring features"
                ]
            }
        }
    
    def _build_security_database(self) -> Dict[str, Dict[str, Any]]:
        """Build security and compliance information database."""
        return {
            "Railway": {
                "security_rating": 8,
                "data_encryption": True,
                "compliance_standards": ["SOC2"],
                "access_controls": ["Team management", "Environment variables", "Deploy keys"],
                "network_security": ["Automatic HTTPS", "Network isolation", "Private networking"],
                "backup_options": ["Volume snapshots", "Database backups"],
                "vulnerability_management": True,
                "incident_response": "Community and email support",
                "data_residency_options": ["US", "EU"],
                "security_recommendations": [
                    "Use environment variables for all secrets",
                    "Enable team access controls",
                    "Regular dependency updates",
                    "Monitor deployment logs"
                ]
            },
            "DigitalOcean": {
                "security_rating": 8,
                "data_encryption": True,
                "compliance_standards": ["SOC2", "ISO27001", "PCI DSS"],
                "access_controls": ["Team management", "RBAC", "2FA", "SSH keys"],
                "network_security": ["Cloud Firewalls", "VPC", "Load Balancers", "DDoS protection"],
                "backup_options": ["Droplet snapshots", "Volume snapshots", "Managed database backups"],
                "vulnerability_management": True,
                "incident_response": "24/7 support with SLA",
                "data_residency_options": ["Global regions", "EU data residency"],
                "security_recommendations": [
                    "Use Cloud Firewalls for network security",
                    "Enable 2FA for account access",
                    "Use managed databases for better security",
                    "Regular security updates and patches"
                ]
            },
            "AWS": {
                "security_rating": 10,
                "data_encryption": True,
                "compliance_standards": ["SOC1/2/3", "ISO27001", "GDPR", "HIPAA", "PCI DSS", "FedRAMP"],
                "access_controls": ["IAM", "MFA", "SSO", "SAML", "Active Directory integration"],
                "network_security": ["VPC", "Security Groups", "NACLs", "WAF", "Shield DDoS"],
                "backup_options": ["Automated backups", "Cross-region replication", "Point-in-time recovery"],
                "vulnerability_management": True,
                "incident_response": "24/7 enterprise support with dedicated TAM",
                "data_residency_options": ["Global regions", "Data sovereignty controls"],
                "security_recommendations": [
                    "Follow AWS Well-Architected security pillar",
                    "Use least-privilege IAM policies",
                    "Enable CloudTrail for audit logging",
                    "Use KMS for encryption key management",
                    "Regular security assessments"
                ]
            },
            "Google Cloud": {
                "security_rating": 9,
                "data_encryption": True,
                "compliance_standards": ["SOC1/2/3", "ISO27001", "GDPR", "HIPAA", "PCI DSS"],
                "access_controls": ["Cloud IAM", "2FA", "SSO", "SAML", "LDAP integration"],
                "network_security": ["VPC", "Firewall rules", "Cloud Armor", "Private Google Access"],
                "backup_options": ["Automated backups", "Cross-region snapshots", "Point-in-time recovery"],
                "vulnerability_management": True,
                "incident_response": "24/7 support with escalation procedures",
                "data_residency_options": ["Global regions", "Data location controls"],
                "security_recommendations": [
                    "Use Organization policies for governance",
                    "Enable Cloud Security Command Center",
                    "Use Binary Authorization for container security",
                    "Regular security scanning and monitoring"
                ]
            },
            "Render": {
                "security_rating": 7,
                "data_encryption": True,
                "compliance_standards": ["SOC2"],
                "access_controls": ["Team management", "Environment variables", "Deploy keys"],
                "network_security": ["Automatic HTTPS", "Network isolation", "DDoS protection"],
                "backup_options": ["Database backups", "Persistent disk snapshots"],
                "vulnerability_management": True,
                "incident_response": "Email and chat support",
                "data_residency_options": ["US", "EU"],
                "security_recommendations": [
                    "Use environment variables for secrets",
                    "Enable team access controls",
                    "Regular dependency updates",
                    "Monitor application logs"
                ]
            },
            "Fly.io": {
                "security_rating": 7,
                "data_encryption": True,
                "compliance_standards": ["SOC2"],
                "access_controls": ["Org management", "API tokens", "Deploy tokens"],
                "network_security": ["Private networking", "Automatic HTTPS", "Firewall rules"],
                "backup_options": ["Volume snapshots", "Database backups"],
                "vulnerability_management": True,
                "incident_response": "Community and email support",
                "data_residency_options": ["Global edge locations"],
                "security_recommendations": [
                    "Use secrets for sensitive configuration",
                    "Enable private networking between services",
                    "Regular image updates",
                    "Monitor resource usage"
                ]
            },
            "Azure": {
                "security_rating": 10,
                "data_encryption": True,
                "compliance_standards": ["SOC1/2/3", "ISO27001", "GDPR", "HIPAA", "PCI DSS", "FedRAMP"],
                "access_controls": ["Azure AD", "RBAC", "MFA", "Conditional Access", "PIM"],
                "network_security": ["Virtual Networks", "NSGs", "Application Gateway", "DDoS protection"],
                "backup_options": ["Azure Backup", "Site Recovery", "Geo-redundant storage"],
                "vulnerability_management": True,
                "incident_response": "24/7 enterprise support with escalation",
                "data_residency_options": ["Global regions", "Data sovereignty controls"],
                "security_recommendations": [
                    "Use Azure Security Center for monitoring",
                    "Implement Azure Sentinel for SIEM",
                    "Use Key Vault for secrets management",
                    "Enable Just-In-Time access",
                    "Regular security assessments"
                ]
            }
        }


def create_infrastructure_analyst() -> InfrastructureAnalyst:
    """Factory function to create an InfrastructureAnalyst instance."""
    return InfrastructureAnalyst()
