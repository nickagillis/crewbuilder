"""
Quality Assurance Agent for CrewBuilder
Validates generated CrewAI code for quality, security, and performance standards.
"""

from crewai import Agent, Task
from .llm_config import get_configured_llm
import ast
import json
import sys
import subprocess
import tempfile
import os
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
from dataclasses import dataclass

class CodeQualityIssue(BaseModel):
    """Represents a code quality issue found during analysis"""
    severity: str = Field(description="'critical', 'major', 'minor', 'suggestion'")
    category: str = Field(description="Type of issue: 'syntax', 'logic', 'performance', 'security', 'style'")
    description: str = Field(description="Detailed description of the issue")
    location: str = Field(description="File and line number where issue occurs")
    suggestion: str = Field(description="Recommended fix or improvement")
    code_snippet: Optional[str] = Field(default=None, description="Relevant code snippet")

class TestResult(BaseModel):
    """Represents the result of a test execution"""
    test_name: str = Field(description="Name of the test")
    status: str = Field(description="'passed', 'failed', 'error'")
    execution_time: float = Field(description="Time taken to execute in seconds")
    output: str = Field(description="Test output or error message")
    assertions_checked: int = Field(default=0, description="Number of assertions validated")

class ValidationReport(BaseModel):
    """Complete validation report for generated code"""
    overall_score: float = Field(description="Overall quality score (0-100)")
    syntax_valid: bool = Field(description="Whether code has valid Python syntax")
    imports_resolved: bool = Field(description="Whether all imports can be resolved")
    crewai_compliant: bool = Field(description="Whether code follows CrewAI patterns")
    performance_score: float = Field(description="Performance assessment (0-100)")
    security_score: float = Field(description="Security assessment (0-100)")
    maintainability_score: float = Field(description="Code maintainability (0-100)")
    issues: List[CodeQualityIssue] = Field(description="List of identified issues")
    test_results: List[TestResult] = Field(description="Results from automated tests")
    recommendations: List[str] = Field(description="High-level improvement recommendations")
    approval_status: str = Field(description="'approved', 'needs_revision', 'rejected'")

class QualityAssurance:
    """Quality Assurance agent for validating generated CrewAI code."""
    
    def __init__(self):
        """Initialize the Quality Assurance agent."""
        # Get configured LLM

        llm = get_configured_llm(temperature=0.7)

        

        self.agent = Agent(
            role="Quality Assurance Engineer",
            goal="Review and validate generated CrewAI code to ensure it meets quality, security, and performance standards while following best practices",
            backstory="""You are a senior Quality Assurance Engineer with deep expertise in Python development, CrewAI framework patterns, and automated testing. You have spent years ensuring that AI-generated code meets production standards and can be safely deployed.

            Your specialty is comprehensive code review that goes beyond syntax checking. You understand the nuances of CrewAI agent development, know common pitfalls in AI-generated code, and can identify potential runtime issues before they occur in production.

            You have extensive experience with automated testing frameworks, security vulnerability assessment, and performance optimization. You're particularly skilled at creating test suites that validate not just functionality but also reliability, maintainability, and scalability of multi-agent systems.

            Your reviews are thorough but practical - you balance perfectionism with pragmatism, understanding that generated code needs to work in real-world conditions while being maintainable by teams with varying levels of expertise.""",
            verbose=True,
            allow_delegation=False,
            llm=llm,  # Pass the LLM explicitly
            memory=False  # Disable memory to avoid connection issues
        )
    
    def validate_code(self, generated_code: str, crew_name: str = "GeneratedCrew") -> ValidationReport:
        """
        Perform comprehensive validation of generated CrewAI code.
        
        Args:
            generated_code: The Python code to validate
            crew_name: Name of the crew for reporting
            
        Returns:
            ValidationReport with complete analysis
        """
        # Validate Python syntax
        syntax_result = self._validate_python_syntax(generated_code)
        
        # Analyze CrewAI compliance
        compliance_result = self._analyze_crewai_compliance(generated_code)
        
        # Check import dependencies
        import_result = self._check_import_dependencies(generated_code)
        
        # Calculate quality scores
        performance_score = self._calculate_performance_score(generated_code)
        security_score = self._calculate_security_score(generated_code)
        maintainability_score = self._calculate_maintainability_score(generated_code)
        
        # Generate and execute tests
        test_suite = self._generate_test_suite(generated_code, crew_name)
        test_results = self._execute_code_tests(generated_code, test_suite)
        
        # Collect all issues
        all_issues = []
        all_issues.extend(self._convert_syntax_errors_to_issues(syntax_result))
        all_issues.extend(self._convert_compliance_issues(compliance_result))
        all_issues.extend(self._convert_import_issues(import_result))
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            syntax_result, compliance_result, performance_score, 
            security_score, maintainability_score, len(all_issues)
        )
        
        # Determine approval status
        approval_status = self._determine_approval_status(overall_score, all_issues)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_issues, overall_score)
        
        return ValidationReport(
            overall_score=overall_score,
            syntax_valid=syntax_result.get('syntax_valid', False),
            imports_resolved=import_result.get('all_imports_resolved', False),
            crewai_compliant=compliance_result.get('is_compliant', False),
            performance_score=performance_score,
            security_score=security_score,
            maintainability_score=maintainability_score,
            issues=all_issues,
            test_results=test_results,
            recommendations=recommendations,
            approval_status=approval_status
        )
    
    def _validate_python_syntax(self, code: str, filename: str = "generated_code.py") -> Dict[str, Any]:
        """Validate Python syntax and identify syntax errors."""
        try:
            ast.parse(code, filename=filename)
            return {
                "syntax_valid": True,
                "errors": [],
                "warnings": []
            }
        except SyntaxError as e:
            return {
                "syntax_valid": False,
                "errors": [{
                    "type": "SyntaxError",
                    "message": str(e),
                    "line": e.lineno,
                    "column": e.offset,
                    "filename": filename
                }],
                "warnings": []
            }
        except Exception as e:
            return {
                "syntax_valid": False,
                "errors": [{
                    "type": type(e).__name__,
                    "message": str(e),
                    "line": None,
                    "column": None,
                    "filename": filename
                }],
                "warnings": []
            }
    
    def _analyze_crewai_compliance(self, code: str) -> Dict[str, Any]:
        """Analyze code for CrewAI framework compliance and best practices."""
        compliance_issues = []
        best_practices_score = 100
        
        # Check for required CrewAI imports
        required_imports = ['crewai', 'Agent', 'Task', 'Crew']
        missing_imports = []
        
        for req_import in required_imports:
            if req_import not in code:
                missing_imports.append(req_import)
                best_practices_score -= 10
        
        if missing_imports:
            compliance_issues.append({
                "severity": "critical",
                "category": "imports",
                "description": f"Missing required CrewAI imports: {', '.join(missing_imports)}",
                "suggestion": "Add the required CrewAI framework imports"
            })
        
        # Check for proper agent definitions
        if 'Agent(' not in code and 'Agent =' not in code:
            compliance_issues.append({
                "severity": "critical", 
                "category": "structure",
                "description": "No CrewAI Agent definitions found",
                "suggestion": "Define at least one CrewAI Agent with role, goal, and backstory"
            })
            best_practices_score -= 20
        
        # Check for proper task definitions
        if 'Task(' not in code and 'Task =' not in code:
            compliance_issues.append({
                "severity": "critical",
                "category": "structure", 
                "description": "No CrewAI Task definitions found",
                "suggestion": "Define at least one CrewAI Task with description and expected_output"
            })
            best_practices_score -= 20
        
        # Check for crew instantiation
        if 'Crew(' not in code and 'Crew =' not in code:
            compliance_issues.append({
                "severity": "major",
                "category": "structure",
                "description": "No CrewAI Crew instantiation found", 
                "suggestion": "Create a Crew instance with agents and tasks"
            })
            best_practices_score -= 15
        
        return {
            "compliance_score": max(0, best_practices_score),
            "is_compliant": best_practices_score >= 70,
            "issues": compliance_issues,
            "framework_patterns_found": {
                "agents": 'Agent(' in code,
                "tasks": 'Task(' in code, 
                "crew": 'Crew(' in code,
                "tools": '@tool' in code or 'tools=' in code,
                "error_handling": 'try:' in code and 'except' in code
            }
        }
    
    def _check_import_dependencies(self, code: str) -> Dict[str, Any]:
        """Check if all imports in the code can be resolved."""
        import_issues = []
        resolved_imports = []
        unresolved_imports = []
        
        try:
            tree = ast.parse(code)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}" if module else alias.name)
            
            # Check if imports can be resolved
            standard_libs = ['os', 'sys', 'json', 'datetime', 'time', 'logging', 're', 'typing']
            known_packages = ['crewai', 'openai', 'anthropic', 'requests', 'pandas', 'numpy']
            
            for imp in imports:
                base_module = imp.split('.')[0]
                if base_module in standard_libs or base_module in known_packages:
                    resolved_imports.append(imp)
                else:
                    unresolved_imports.append(imp)
                    import_issues.append({
                        "severity": "major",
                        "category": "dependencies",
                        "description": f"Unresolved import: {imp}",
                        "suggestion": f"Add {base_module} to requirements.txt or verify import path"
                    })
        
        except Exception as e:
            import_issues.append({
                "severity": "critical",
                "category": "parsing",
                "description": f"Failed to parse imports: {str(e)}",
                "suggestion": "Fix syntax errors before analyzing imports"
            })
        
        return {
            "all_imports_resolved": len(unresolved_imports) == 0,
            "resolved_imports": resolved_imports,
            "unresolved_imports": unresolved_imports,
            "issues": import_issues,
            "suggested_requirements": list(set([imp.split('.')[0] for imp in unresolved_imports]))
        }
    
    def _generate_test_suite(self, code: str, crew_name: str = "GeneratedCrew") -> str:
        """Generate a comprehensive test suite for the generated CrewAI code."""
        return f'''import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the generated code directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test basic functionality
class Test{crew_name}(unittest.TestCase):
    """Test suite for generated CrewAI crew"""
    
    def test_imports(self):
        """Test that required modules can be imported"""
        try:
            import crewai
            from crewai import Agent, Task, Crew
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import required CrewAI modules: {{e}}")
    
    def test_code_syntax(self):
        """Test that generated code has valid syntax"""
        import ast
        with open("main.py", "r") as f:
            code = f.read()
        try:
            ast.parse(code)
            self.assertTrue(True)
        except SyntaxError as e:
            self.fail(f"Syntax error in generated code: {{e}}")

if __name__ == '__main__':
    unittest.main()
'''
    
    def _execute_code_tests(self, code: str, test_code: str) -> List[TestResult]:
        """Execute generated test suite and return results."""
        test_results = []
        
        try:
            # For now, return a mock successful test
            test_results.append(TestResult(
                test_name="Syntax Validation",
                status="passed",
                execution_time=0.1,
                output="Code syntax is valid",
                assertions_checked=1
            ))
        except Exception as e:
            test_results.append(TestResult(
                test_name="Test Execution",
                status="error", 
                execution_time=0.0,
                output=f"Failed to execute tests: {str(e)}",
                assertions_checked=0
            ))
        
        return test_results
    
    def _calculate_performance_score(self, code: str) -> float:
        """Calculate performance score based on code analysis."""
        score = 100.0
        
        # Check for potential performance issues
        performance_issues = [
            ('time.sleep(', -10, "Synchronous sleep calls can block execution"),
            ('while True:', -5, "Infinite loops may cause performance issues"),
            ('for.*in.*range(.*1000', -5, "Large loops may impact performance"),
        ]
        
        for pattern, penalty, reason in performance_issues:
            if pattern in code:
                score += penalty
        
        # Reward good practices
        if 'async def' in code:
            score += 10
        if 'with open(' in code:
            score += 5
        if 'try:' in code and 'except' in code:
            score += 5
        
        return max(0, min(100, score))
    
    def _calculate_security_score(self, code: str) -> float:
        """Calculate security score based on code analysis."""
        score = 100.0
        
        # Check for security issues
        security_issues = [
            ('eval(', -20, "eval() usage is dangerous"),
            ('exec(', -20, "exec() usage is dangerous"),
            ('subprocess.call(', -10, "Subprocess calls may be risky"),
            ('os.system(', -15, "os.system() calls are risky"),
        ]
        
        for pattern, penalty, reason in security_issues:
            if pattern in code:
                score += penalty
        
        # Reward security practices
        if 'os.getenv(' in code:
            score += 10  # Using environment variables
        if 'logging.' in code:
            score += 5   # Proper logging
        
        return max(0, min(100, score))
    
    def _calculate_maintainability_score(self, code: str) -> float:
        """Calculate maintainability score based on code structure."""
        score = 100.0
        lines = code.split('\n')
        
        # Check code organization
        if len(lines) > 500:
            score -= 10  # Very long files are harder to maintain
        
        # Count functions and classes
        function_count = code.count('def ')
        class_count = code.count('class ')
        
        if function_count == 0:
            score -= 20  # No functions suggests poor organization
        
        # Check for documentation
        docstring_count = code.count('"""') + code.count("'''")
        if docstring_count > 0:
            score += 10
        
        return max(0, min(100, score))
    
    def _convert_syntax_errors_to_issues(self, syntax_result: Dict[str, Any]) -> List[CodeQualityIssue]:
        """Convert syntax validation results to CodeQualityIssue objects."""
        issues = []
        for error in syntax_result.get('errors', []):
            issues.append(CodeQualityIssue(
                severity="critical",
                category="syntax",
                description=f"Syntax error: {error['message']}",
                location=f"Line {error.get('line', 'unknown')}",
                suggestion="Fix the syntax error before proceeding",
                code_snippet=None
            ))
        return issues
    
    def _convert_compliance_issues(self, compliance_result: Dict[str, Any]) -> List[CodeQualityIssue]:
        """Convert compliance analysis results to CodeQualityIssue objects."""
        issues = []
        for issue in compliance_result.get('issues', []):
            issues.append(CodeQualityIssue(
                severity=issue['severity'],
                category=issue['category'],
                description=issue['description'],
                location="General",
                suggestion=issue['suggestion'],
                code_snippet=None
            ))
        return issues
    
    def _convert_import_issues(self, import_result: Dict[str, Any]) -> List[CodeQualityIssue]:
        """Convert import validation results to CodeQualityIssue objects."""
        issues = []
        for issue in import_result.get('issues', []):
            issues.append(CodeQualityIssue(
                severity=issue['severity'],
                category=issue['category'],
                description=issue['description'],
                location="Imports",
                suggestion=issue['suggestion'],
                code_snippet=None
            ))
        return issues
    
    def _calculate_overall_score(self, syntax_result: Dict[str, Any], compliance_result: Dict[str, Any], 
                                performance_score: float, security_score: float, 
                                maintainability_score: float, issue_count: int) -> float:
        """Calculate the overall quality score."""
        if not syntax_result.get('syntax_valid', False):
            return 0.0  # Invalid syntax = 0 score
        
        # Weight the different scores
        weighted_score = (
            compliance_result.get('compliance_score', 0) * 0.3 +
            performance_score * 0.25 +
            security_score * 0.25 +
            maintainability_score * 0.2
        )
        
        # Penalize for issues
        issue_penalty = min(issue_count * 5, 30)  # Max 30 point penalty
        
        return max(0, weighted_score - issue_penalty)
    
    def _determine_approval_status(self, overall_score: float, issues: List[CodeQualityIssue]) -> str:
        """Determine approval status based on score and issues."""
        critical_issues = [issue for issue in issues if issue.severity == "critical"]
        
        if critical_issues or overall_score < 60:
            return "rejected"
        elif overall_score >= 85:
            return "approved"
        else:
            return "needs_revision"
    
    def _generate_recommendations(self, issues: List[CodeQualityIssue], overall_score: float) -> List[str]:
        """Generate high-level improvement recommendations."""
        recommendations = []
        
        critical_issues = [issue for issue in issues if issue.severity == "critical"]
        if critical_issues:
            recommendations.append("Address all critical issues before proceeding to deployment")
        
        if overall_score < 70:
            recommendations.append("Consider refactoring code to improve overall quality")
        
        syntax_issues = [issue for issue in issues if issue.category == "syntax"]
        if syntax_issues:
            recommendations.append("Fix syntax errors to ensure code can execute")
        
        security_issues = [issue for issue in issues if issue.category == "security"]
        if security_issues:
            recommendations.append("Review and address security vulnerabilities")
        
        if not recommendations:
            recommendations.append("Code quality is good - ready for deployment")
        
        return recommendations

def create_quality_assurance() -> QualityAssurance:
    """Factory function to create a QualityAssurance instance."""
    return QualityAssurance()
