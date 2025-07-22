"""
API Detective Agent for CrewBuilder
Identifies all necessary APIs, tools, and integrations required for generated crew systems.
"""

from crewai import Agent, Task
from .llm_config import get_configured_llm
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field

class APIRequirement(BaseModel):
    """Represents a specific API requirement identified from business needs"""
    category: str = Field(description="API category: 'llm', 'search', 'data', 'communication', 'storage', 'analytics'")
    purpose: str = Field(description="What this API will be used for")
    priority: str = Field(description="'critical', 'important', 'optional'")
    estimated_usage: str = Field(description="Expected usage volume: 'low', 'medium', 'high'")
    data_flow: str = Field(description="'input', 'output', 'bidirectional'")
    requirements: List[str] = Field(description="Specific functional requirements")

class APIRecommendation(BaseModel):
    """Represents a recommended API/service for a requirement"""
    name: str = Field(description="API/service name")
    provider: str = Field(description="Provider/company name")
    category: str = Field(description="API category")
    description: str = Field(description="What this API does")
    pricing_model: str = Field(description="How pricing works")
    estimated_monthly_cost: str = Field(description="Estimated cost range")
    setup_complexity: str = Field(description="'simple', 'moderate', 'complex'")
    api_key_required: bool = Field(description="Whether API key is needed")
    rate_limits: str = Field(description="Rate limiting information")
    documentation_quality: str = Field(description="'excellent', 'good', 'fair', 'poor'")
    reliability_score: int = Field(description="Reliability score 1-10")
    integration_notes: str = Field(description="Special integration considerations")
    alternatives: List[str] = Field(default=[], description="Alternative services")

class IntegrationPlan(BaseModel):
    """Complete integration plan for all required APIs"""
    total_apis: int = Field(description="Total number of APIs required")
    critical_apis: int = Field(description="Number of critical APIs")
    estimated_setup_time: str = Field(description="Estimated time to set up all integrations")
    total_estimated_cost: str = Field(description="Total monthly cost estimate")
    complexity_score: int = Field(description="Overall complexity score 1-10")
    requirements: List[APIRequirement] = Field(description="All identified API requirements")
    recommendations: List[APIRecommendation] = Field(description="Recommended APIs and services")
    integration_sequence: List[str] = Field(description="Recommended order of integration")
    risk_factors: List[str] = Field(description="Potential risks and mitigation strategies")
    environment_variables: List[str] = Field(description="Required environment variables")
    configuration_templates: Dict[str, str] = Field(description="Configuration templates for each API")

class APIDetective:
    """API Detective agent for identifying and recommending integrations."""
    
    def __init__(self):
        """Initialize the API Detective agent."""
        # Get configured LLM

        llm = get_configured_llm(temperature=0.7)

        

        self.agent = Agent(
            role="API Detective", 
            goal="Identify all necessary APIs, tools, and integrations required for the generated crew system, providing comprehensive recommendations with cost analysis and setup guidance",
            backstory="""You are an expert API integration specialist with extensive knowledge of the modern API ecosystem. You have years of experience evaluating, integrating, and optimizing API usage across hundreds of different services and platforms.

            Your specialty is quickly identifying the exact APIs and tools needed for any business workflow, understanding their pricing models, rate limits, and integration complexity. You stay current with the latest API offerings and know the trade-offs between different providers.

            You excel at cost optimization, understanding how to minimize API expenses while maximizing functionality. You know which APIs have generous free tiers, which offer the best value for different usage patterns, and how to architect integrations to stay within budget constraints.

            Your recommendations are always practical and implementation-focused. You don't just suggest APIs - you provide complete integration plans with setup instructions, code templates, cost estimates, and risk assessments that enable teams to move quickly from planning to implementation.""",
            verbose=True,
            allow_delegation=False,
            llm=llm  # Pass the LLM explicitly
        ,
        memory=False  # Disable memory to avoid connection issues
        
        # API knowledge base
        self.api_database = self._build_api_database()
    
    def analyze_requirements(self, requirements_json: str, crew_architecture: Dict[str, Any]) -> IntegrationPlan:
        """
        Analyze business requirements and crew architecture to create comprehensive integration plan.
        
        Args:
            requirements_json: JSON string containing business requirements
            crew_architecture: Crew architecture from System Architect
            
        Returns:
            Complete integration plan with API recommendations
        """
        try:
            requirements = json.loads(requirements_json) if isinstance(requirements_json, str) else requirements_json
        except (json.JSONDecodeError, TypeError):
            # Fallback for non-JSON input
            requirements = {"requirements": [], "business_domain": "general"}
        
        # Identify API requirements
        api_requirements = self._identify_api_requirements(requirements, crew_architecture)
        
        # Research and recommend APIs
        api_recommendations = self._research_api_recommendations(api_requirements)
        
        # Estimate costs
        cost_analysis = self._estimate_costs(api_recommendations, requirements)
        
        # Generate configuration templates
        configurations = self._generate_configurations(api_recommendations)
        
        # Assess risks and compatibility
        risk_assessment = self._assess_risks(api_recommendations)
        
        # Create integration sequence
        integration_sequence = self._plan_integration_sequence(api_recommendations)
        
        return IntegrationPlan(
            total_apis=len(api_recommendations),
            critical_apis=len([api for api in api_recommendations if self._get_priority_for_category(api.category) == "critical"]),
            estimated_setup_time=self._estimate_setup_time(api_recommendations),
            total_estimated_cost=cost_analysis["total_monthly"],
            complexity_score=self._calculate_complexity_score(api_recommendations),
            requirements=api_requirements,
            recommendations=api_recommendations,
            integration_sequence=integration_sequence,
            risk_factors=risk_assessment,
            environment_variables=self._extract_environment_variables(api_recommendations),
            configuration_templates=configurations
        )
    
    def _identify_api_requirements(self, requirements: Dict[str, Any], crew_architecture: Dict[str, Any]) -> List[APIRequirement]:
        """Identify specific API requirements from business needs and crew architecture."""
        api_requirements = []
        
        # Always need LLM API for CrewAI
        api_requirements.append(APIRequirement(
            category="llm",
            purpose="AI model for agent reasoning and text generation",
            priority="critical",
            estimated_usage="high",
            data_flow="bidirectional",
            requirements=["Text generation", "Reasoning", "Agent decision making"]
        ))
        
        # Analyze business requirements
        business_reqs = requirements.get('requirements', [])
        business_domain = requirements.get('business_domain', 'general')
        
        for req in business_reqs:
            category = req.get('category', '')
            description = req.get('description', '').lower()
            
            # Category-specific API identification
            if category == 'content_creation':
                api_requirements.extend([
                    APIRequirement(
                        category="search",
                        purpose="Research trending topics and gather information",
                        priority="critical",
                        estimated_usage="medium",
                        data_flow="input",
                        requirements=["Web search", "News search", "Trend analysis"]
                    ),
                    APIRequirement(
                        category="analytics",
                        purpose="SEO analysis and content optimization",
                        priority="important",
                        estimated_usage="low",
                        data_flow="input",
                        requirements=["Keyword analysis", "SEO scoring", "Content metrics"]
                    )
                ])
                
                if 'social media' in description:
                    api_requirements.append(APIRequirement(
                        category="communication",
                        purpose="Social media posting and management",
                        priority="important", 
                        estimated_usage="medium",
                        data_flow="output",
                        requirements=["Post scheduling", "Multi-platform support", "Analytics"]
                    ))
            
            elif category == 'data_processing':
                api_requirements.extend([
                    APIRequirement(
                        category="data",
                        purpose="Data source integration and processing",
                        priority="critical",
                        estimated_usage="high",
                        data_flow="input",
                        requirements=["Data extraction", "Format conversion", "API access"]
                    ),
                    APIRequirement(
                        category="storage",
                        purpose="Processed data storage and retrieval",
                        priority="important",
                        estimated_usage="medium", 
                        data_flow="bidirectional",
                        requirements=["Scalable storage", "Query capabilities", "Backup"]
                    )
                ])
            
            elif category == 'customer_service':
                api_requirements.extend([
                    APIRequirement(
                        category="communication",
                        purpose="Email and chat integration",
                        priority="critical",
                        estimated_usage="high",
                        data_flow="bidirectional",
                        requirements=["Email sending/receiving", "Chat integration", "Notifications"]
                    ),
                    APIRequirement(
                        category="data",
                        purpose="Customer data and CRM integration",
                        priority="important",
                        estimated_usage="medium",
                        data_flow="bidirectional", 
                        requirements=["Customer lookup", "History tracking", "Data updates"]
                    )
                ])
            
            elif category == 'research':
                api_requirements.extend([
                    APIRequirement(
                        category="search",
                        purpose="Comprehensive web and academic search",
                        priority="critical",
                        estimated_usage="high",
                        data_flow="input",
                        requirements=["Web search", "Academic papers", "News sources"]
                    ),
                    APIRequirement(
                        category="data",
                        purpose="Data aggregation and analysis",
                        priority="important",
                        estimated_usage="medium",
                        data_flow="input",
                        requirements=["Market data", "Competitor analysis", "Trend data"]
                    )
                ])
        
        # Remove duplicates based on category and purpose
        unique_requirements = []
        seen_combinations = set()
        
        for req in api_requirements:
            key = f"{req.category}_{req.purpose.replace(' ', '_').lower()}"
            if key not in seen_combinations:
                unique_requirements.append(req)
                seen_combinations.add(key)
        
        return unique_requirements
    
    def _research_api_recommendations(self, api_requirements: List[APIRequirement]) -> List[APIRecommendation]:
        """Research and recommend specific APIs for each requirement."""
        recommendations = []
        
        for requirement in api_requirements:
            category_apis = self.api_database.get(requirement.category, [])
            
            # Find best match for this requirement
            best_api = None
            best_score = 0
            
            for api_data in category_apis:
                score = self._calculate_suitability_score(api_data, requirement)
                if score > best_score:
                    best_score = score
                    best_api = api_data
            
            if best_api:
                recommendation = APIRecommendation(
                    name=best_api["name"],
                    provider=best_api["provider"],
                    category=requirement.category,
                    description=best_api["description"],
                    pricing_model=best_api["pricing_model"],
                    estimated_monthly_cost=best_api["estimated_monthly_cost"],
                    setup_complexity=best_api["setup_complexity"],
                    api_key_required=best_api["api_key_required"],
                    rate_limits=best_api["rate_limits"],
                    documentation_quality=best_api["documentation_quality"],
                    reliability_score=best_api["reliability_score"],
                    integration_notes=best_api["integration_notes"],
                    alternatives=best_api["alternatives"]
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def _estimate_costs(self, api_recommendations: List[APIRecommendation], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate costs for recommended APIs."""
        total_monthly = 0
        cost_breakdown = []
        
        for api in api_recommendations:
            # Extract cost estimate
            cost_str = api.estimated_monthly_cost
            numbers = re.findall(r'\d+', cost_str)
            
            if numbers:
                if len(numbers) == 1:
                    monthly_cost = float(numbers[0])
                else:
                    monthly_cost = (float(numbers[0]) + float(numbers[-1])) / 2
            else:
                monthly_cost = 50.0  # Default estimate
            
            total_monthly += monthly_cost
            cost_breakdown.append({
                "api": api.name,
                "category": api.category,
                "monthly_cost": monthly_cost,
                "pricing_model": api.pricing_model
            })
        
        return {
            "total_monthly": f"${total_monthly:.0f}-{total_monthly * 1.5:.0f}",
            "total_annual": f"${total_monthly * 12:.0f}-{total_monthly * 18:.0f}",
            "breakdown": cost_breakdown,
            "optimization_tips": [
                "Start with free tiers and scale up as needed",
                "Monitor usage regularly to avoid unexpected charges",
                "Consider bulk pricing options for high-volume APIs",
                "Use caching to reduce API call frequency"
            ]
        }
    
    def _generate_configurations(self, api_recommendations: List[APIRecommendation]) -> Dict[str, str]:
        """Generate configuration templates for recommended APIs."""
        configurations = {}
        
        # Environment variables template
        env_template = "# API Configuration\n# Add these to your .env file\n\n"
        
        # Requirements.txt additions
        requirements_additions = []
        
        for api in api_recommendations:
            api_name = api.name.upper().replace(' ', '_').replace('-', '_')
            
            if api.api_key_required:
                env_template += f"{api_name}_API_KEY=your_{api_name.lower()}_api_key_here\n"
            
            # Add Python package
            package_name = self._get_python_package_name(api.name)
            if package_name:
                requirements_additions.append(package_name)
            
            # Generate code template
            code_template = self._generate_api_code_template(api)
            configurations[f"{api_name.lower()}_integration.py"] = code_template
        
        configurations[".env_template"] = env_template
        configurations["requirements_additions.txt"] = "\n".join(requirements_additions)
        
        return configurations
    
    def _assess_risks(self, api_recommendations: List[APIRecommendation]) -> List[str]:
        """Assess integration risks and provide mitigation strategies."""
        risks = []
        
        # Check for multiple LLM providers
        llm_providers = [api for api in api_recommendations if api.category == 'llm']
        if len(llm_providers) > 1:
            risks.append("Multiple LLM providers may cause configuration conflicts - use environment variables to switch")
        
        # Check for high-cost APIs
        high_cost_apis = [api for api in api_recommendations if '$100' in api.estimated_monthly_cost or '$200' in api.estimated_monthly_cost]
        if high_cost_apis:
            risks.append("High-cost APIs detected - monitor usage carefully and implement cost controls")
        
        # Check for complex setup
        complex_apis = [api for api in api_recommendations if api.setup_complexity == 'complex']
        if complex_apis:
            risks.append("Complex API setup detected - allocate extra time for integration and testing")
        
        return risks
    
    def _plan_integration_sequence(self, api_recommendations: List[APIRecommendation]) -> List[str]:
        """Plan the recommended sequence for API integration."""
        # Sort by priority and complexity
        sequence = []
        
        # First: Critical and simple APIs
        critical_simple = [api for api in api_recommendations 
                          if self._get_priority_for_category(api.category) == "critical" 
                          and api.setup_complexity == "simple"]
        sequence.extend([api.name for api in critical_simple])
        
        # Second: Critical but complex APIs
        critical_complex = [api for api in api_recommendations 
                           if self._get_priority_for_category(api.category) == "critical" 
                           and api.setup_complexity != "simple"]
        sequence.extend([api.name for api in critical_complex])
        
        # Third: Important APIs
        important = [api for api in api_recommendations 
                    if self._get_priority_for_category(api.category) == "important"]
        sequence.extend([api.name for api in important])
        
        # Last: Optional APIs
        optional = [api for api in api_recommendations 
                   if self._get_priority_for_category(api.category) == "optional"]
        sequence.extend([api.name for api in optional])
        
        return sequence
    
    def _extract_environment_variables(self, api_recommendations: List[APIRecommendation]) -> List[str]:
        """Extract required environment variables."""
        env_vars = []
        
        for api in api_recommendations:
            if api.api_key_required:
                api_name = api.name.upper().replace(' ', '_').replace('-', '_')
                env_vars.append(f"{api_name}_API_KEY")
        
        return env_vars
    
    def _estimate_setup_time(self, api_recommendations: List[APIRecommendation]) -> str:
        """Estimate total setup time for all APIs."""
        total_hours = 0
        
        time_estimates = {
            "simple": 1,
            "moderate": 3,
            "complex": 8
        }
        
        for api in api_recommendations:
            total_hours += time_estimates.get(api.setup_complexity, 3)
        
        if total_hours <= 8:
            return f"{total_hours} hours"
        elif total_hours <= 40:
            return f"{total_hours // 8} days"
        else:
            return f"{total_hours // 40} weeks"
    
    def _calculate_complexity_score(self, api_recommendations: List[APIRecommendation]) -> int:
        """Calculate overall integration complexity score (1-10)."""
        if len(api_recommendations) <= 3:
            base_score = 3
        elif len(api_recommendations) <= 6:
            base_score = 6
        else:
            base_score = 8
        
        # Adjust for complexity
        complex_count = len([api for api in api_recommendations if api.setup_complexity == "complex"])
        base_score += min(complex_count, 2)
        
        return min(10, base_score)
    
    def _calculate_suitability_score(self, api_data: Dict[str, Any], requirement: APIRequirement) -> int:
        """Calculate how suitable an API is for a specific requirement."""
        score = 50  # Base score
        
        # Priority matching
        if requirement.priority == 'critical':
            score += api_data.get('reliability_score', 5) * 3
        
        # Setup complexity preference (simpler is better)
        complexity = api_data.get('setup_complexity', 'moderate')
        if complexity == 'simple':
            score += 15
        elif complexity == 'complex':
            score -= 10
        
        # Documentation quality
        doc_quality = api_data.get('documentation_quality', 'fair')
        if doc_quality == 'excellent':
            score += 10
        elif doc_quality == 'poor':
            score -= 15
        
        # Cost consideration
        cost = api_data.get('estimated_monthly_cost', '$50')
        if '$0' in cost or 'free' in cost.lower():
            score += 5
        
        return min(100, max(0, score))
    
    def _get_priority_for_category(self, category: str) -> str:
        """Get priority level for API category."""
        priority_mapping = {
            "llm": "critical",
            "search": "critical", 
            "communication": "important",
            "data": "important",
            "storage": "important",
            "analytics": "optional"
        }
        return priority_mapping.get(category, "optional")
    
    def _get_python_package_name(self, api_name: str) -> str:
        """Get the Python package name for an API."""
        name = api_name.lower()
        
        package_mapping = {
            'openai': 'openai',
            'anthropic': 'anthropic',
            'groq': 'groq',
            'serper': 'google-search-results',
            'tavily': 'tavily-python',
            'sendgrid': 'sendgrid',
            'slack': 'slack-sdk',
            'airtable': 'pyairtable',
            'google sheets': 'google-api-python-client google-auth-httplib2 google-auth-oauthlib',
            'google analytics': 'google-analytics-data',
            'aws s3': 'boto3'
        }
        
        for key, package in package_mapping.items():
            if key in name:
                return package
        
        return 'requests'  # Default HTTP client
    
    def _generate_api_code_template(self, api: APIRecommendation) -> str:
        """Generate a code template for integrating an API."""
        env_var = api.name.upper().replace(' ', '_').replace('-', '_') + '_API_KEY'
        
        return f'''"""
{api.name} Integration Template
Generated by CrewBuilder API Detective
"""

import os
from typing import Dict, Any, Optional

# Load API key from environment
{env_var.lower()} = os.getenv("{env_var}")

if not {env_var.lower()}:
    raise ValueError("Missing {env_var} environment variable")

class {api.name.replace(' ', '').replace('-', '')}Integration:
    """Integration class for {api.name}"""
    
    def __init__(self):
        self.api_key = {env_var.lower()}
        self.base_url = "https://api.example.com"  # Update with actual URL
        
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            # Add actual connection test logic here
            return True
        except Exception as e:
            print(f"Connection test failed: {{e}}")
            return False

# Usage example
if __name__ == "__main__":
    integration = {api.name.replace(' ', '').replace('-', '')}Integration()
    
    if integration.test_connection():
        print("✅ {api.name} integration successful")
    else:
        print("❌ {api.name} integration failed")
'''
    
    def _build_api_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build the API knowledge database."""
        return {
            "llm": [
                {
                    "name": "OpenAI GPT-4",
                    "provider": "OpenAI",
                    "description": "Advanced language model for reasoning and text generation",
                    "pricing_model": "Pay-per-token",
                    "estimated_monthly_cost": "$50-200",
                    "setup_complexity": "simple",
                    "api_key_required": True,
                    "rate_limits": "10,000 RPM (varies by tier)",
                    "documentation_quality": "excellent",
                    "reliability_score": 9,
                    "integration_notes": "Well-supported in CrewAI",
                    "alternatives": ["Anthropic Claude", "Google Gemini", "Groq"]
                },
                {
                    "name": "Anthropic Claude",
                    "provider": "Anthropic", 
                    "description": "Constitutional AI model with strong reasoning capabilities",
                    "pricing_model": "Pay-per-token",
                    "estimated_monthly_cost": "$40-180",
                    "setup_complexity": "simple",
                    "api_key_required": True,
                    "rate_limits": "5,000 RPM",
                    "documentation_quality": "excellent",
                    "reliability_score": 9,
                    "integration_notes": "Excellent for complex reasoning tasks",
                    "alternatives": ["OpenAI GPT-4", "Google Gemini"]
                },
                {
                    "name": "Groq",
                    "provider": "Groq",
                    "description": "Ultra-fast inference for Llama and other models",
                    "pricing_model": "Pay-per-token (lower cost)",
                    "estimated_monthly_cost": "$20-100",
                    "setup_complexity": "simple",
                    "api_key_required": True,
                    "rate_limits": "30,000 RPM",
                    "documentation_quality": "good",
                    "reliability_score": 8,
                    "integration_notes": "Best for high-throughput applications",
                    "alternatives": ["OpenAI", "Ollama (local)"]
                }
            ],
            "search": [
                {
                    "name": "Serper API",
                    "provider": "Serper",
                    "description": "Google Search API with news, images, and web results",
                    "pricing_model": "Pay-per-search",
                    "estimated_monthly_cost": "$10-50",
                    "setup_complexity": "simple",
                    "api_key_required": True,
                    "rate_limits": "2,500 searches/month (free tier)",
                    "documentation_quality": "good",
                    "reliability_score": 8,
                    "integration_notes": "Easy integration with CrewAI search tools",
                    "alternatives": ["Tavily Search", "SerpAPI", "Bing Search API"]
                },
                {
                    "name": "Tavily Search API",
                    "provider": "Tavily",
                    "description": "AI-optimized search for real-time information",
                    "pricing_model": "Pay-per-search",
                    "estimated_monthly_cost": "$15-75",
                    "setup_complexity": "simple",
                    "api_key_required": True,
                    "rate_limits": "1,000 searches/month (free tier)",
                    "documentation_quality": "excellent",
                    "reliability_score": 9,
                    "integration_notes": "Designed specifically for AI agents",
                    "alternatives": ["Serper API", "SerpAPI"]
                }
            ],
            "communication": [
                {
                    "name": "SendGrid",
                    "provider": "Twilio SendGrid",
                    "description": "Email delivery and marketing platform",
                    "pricing_model": "Pay-per-email",
                    "estimated_monthly_cost": "$15-100",
                    "setup_complexity": "moderate",
                    "api_key_required": True,
                    "rate_limits": "100 emails/day (free tier)",
                    "documentation_quality": "excellent",
                    "reliability_score": 9,
                    "integration_notes": "Reliable email delivery with analytics",
                    "alternatives": ["Mailgun", "Amazon SES", "Postmark"]
                }
            ],
            "data": [
                {
                    "name": "Airtable API",
                    "provider": "Airtable",
                    "description": "Database and spreadsheet hybrid with API access",
                    "pricing_model": "Per-base pricing",
                    "estimated_monthly_cost": "$10-50",
                    "setup_complexity": "simple",
                    "api_key_required": True,
                    "rate_limits": "5 requests/second",
                    "documentation_quality": "excellent",
                    "reliability_score": 8,
                    "integration_notes": "Easy to set up, good for structured data",
                    "alternatives": ["Google Sheets API", "Notion API", "PostgreSQL"]
                }
            ],
            "storage": [
                {
                    "name": "AWS S3",
                    "provider": "Amazon Web Services",
                    "description": "Object storage for files and data",
                    "pricing_model": "Pay-per-GB stored and transferred",
                    "estimated_monthly_cost": "$5-50",
                    "setup_complexity": "moderate",
                    "api_key_required": True,
                    "rate_limits": "3,500 PUT/COPY/POST/DELETE and 5,500 GET/HEAD requests per second",
                    "documentation_quality": "excellent",
                    "reliability_score": 10,
                    "integration_notes": "Industry standard, highly reliable",
                    "alternatives": ["Google Cloud Storage", "Azure Blob Storage", "DigitalOcean Spaces"]
                }
            ],
            "analytics": [
                {
                    "name": "Google Analytics API",
                    "provider": "Google",
                    "description": "Website and app analytics data",
                    "pricing_model": "Free",
                    "estimated_monthly_cost": "$0",
                    "setup_complexity": "complex",
                    "api_key_required": True,
                    "rate_limits": "10,000 requests/day",
                    "documentation_quality": "good",
                    "reliability_score": 9,
                    "integration_notes": "Comprehensive but complex setup",
                    "alternatives": ["Mixpanel", "Amplitude", "Custom analytics"]
                }
            ]
        }

def create_api_detective() -> APIDetective:
    """Factory function to create an APIDetective instance."""
    return APIDetective()
