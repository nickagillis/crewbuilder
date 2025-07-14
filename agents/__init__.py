"""CrewBuilder Agents Package"""

from .requirements_analyst import (
    BusinessRequirement,
    TechnicalSpecification,
    RequirementsAnalyst,
    create_requirements_analyst
)

from .system_architect import (
    AgentSpecification,
    TaskSpecification,
    CrewWorkflow,
    CrewArchitecture,
    GeneratedCode,
    SystemArchitect,
    create_system_architect
)

from .code_generator import (
    CodeGenerator,
    create_code_generator
)

from .quality_assurance import (
    CodeQualityIssue,
    TestResult,
    ValidationReport,
    QualityAssurance,
    create_quality_assurance
)

from .api_detective import (
    APIRequirement,
    APIRecommendation,
    IntegrationPlan,
    APIDetective,
    create_api_detective
)

from .documentation_specialist import (
    UserGuide,
    TechnicalDocumentation,
    DeploymentGuide,
    DocumentationPlan,
    DocumentationSpecialist,
    create_documentation_specialist
)

from .infrastructure_analyst import (
    PlatformEvaluation,
    CostAnalysis,
    SecurityAssessment,
    InfrastructureRecommendation,
    InfrastructureAnalyst,
    create_infrastructure_analyst
)

from .deployment_engineer import (
    DeploymentConfiguration,
    CICDPipeline,
    SecretsManagement,
    MonitoringIntegration,
    DeploymentPlan,
    DeploymentEngineer,
    create_deployment_engineer
)

from .hosting_assistant import (
    PlatformSetupGuide,
    ConfigurationAssistance,
    ResourceOptimization,
    TroubleshootingGuide,
    OngoingSupport,
    HostingAssistancePlan,
    HostingAssistant,
    create_hosting_assistant
)

from .monitoring_engineer import (
    SystemMonitoring,
    CostMonitoring,
    SecurityMonitoring,
    AlertingSystem,
    DashboardConfiguration,
    PerformanceOptimization,
    MonitoringPlan,
    MonitoringEngineer,
    create_monitoring_engineer
)

__all__ = [
    # Data Models
    'BusinessRequirement',
    'TechnicalSpecification', 
    'AgentSpecification',
    'TaskSpecification',
    'CrewWorkflow',
    'CrewArchitecture',
    'GeneratedCode',
    'CodeQualityIssue',
    'TestResult',
    'ValidationReport',
    'APIRequirement',
    'APIRecommendation',
    'IntegrationPlan',
    'UserGuide',
    'TechnicalDocumentation',
    'DeploymentGuide',
    'DocumentationPlan',
    'PlatformEvaluation',
    'CostAnalysis',
    'SecurityAssessment',
    'InfrastructureRecommendation',
    'DeploymentConfiguration',
    'CICDPipeline',
    'SecretsManagement',
    'MonitoringIntegration',
    'DeploymentPlan',
    'PlatformSetupGuide',
    'ConfigurationAssistance',
    'ResourceOptimization',
    'TroubleshootingGuide',
    'OngoingSupport',
    'HostingAssistancePlan',
    'SystemMonitoring',
    'CostMonitoring',
    'SecurityMonitoring',
    'AlertingSystem',
    'DashboardConfiguration',
    'PerformanceOptimization',
    'MonitoringPlan',
    
    # Agents
    'RequirementsAnalyst',
    'SystemArchitect',
    'CodeGenerator',
    'QualityAssurance',
    'APIDetective',
    'DocumentationSpecialist',
    'InfrastructureAnalyst',
    'DeploymentEngineer',
    'HostingAssistant',
    'MonitoringEngineer',
    
    # Factory Functions
    'create_requirements_analyst',
    'create_system_architect',
    'create_code_generator',
    'create_quality_assurance',
    'create_api_detective',
    'create_documentation_specialist',
    'create_infrastructure_analyst',
    'create_deployment_engineer',
    'create_hosting_assistant',
    'create_monitoring_engineer'
]
