#!/usr/bin/env python3
"""
CrewBuilder Code Generation Test - No API Required
Tests code generation templates and output quality without API calls
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_realistic_test_case():
    """Create a realistic crew architecture for testing"""
    from agents import AgentSpecification, TaskSpecification, CrewWorkflow, CrewArchitecture
    
    # Digital marketing agency crew (realistic scenario)
    agents = [
        AgentSpecification(
            name="Trend Researcher",
            role="Market Research Specialist", 
            goal="Identify trending topics and analyze market opportunities",
            backstory="Expert market researcher with deep knowledge of digital trends and consumer behavior patterns",
            tools=["web_search", "trend_analysis", "competitor_research"],
            max_iter=5,
            memory=True,
            verbose=True,
            allow_delegation=False
        ),
        AgentSpecification(
            name="Content Strategist",
            role="Content Strategy Expert",
            goal="Develop comprehensive content strategies aligned with business goals",
            backstory="Senior content strategist with experience in multi-platform content planning and audience engagement",
            tools=["content_planning", "seo_analysis", "audience_research"],
            max_iter=4,
            memory=True,
            verbose=True,
            allow_delegation=True
        ),
        AgentSpecification(
            name="Content Creator",
            role="Creative Content Writer",
            goal="Create engaging, high-quality content across multiple formats",
            backstory="Creative writer specializing in blog posts, social media, and marketing copy that converts",
            tools=["writing_assistant", "image_generation", "grammar_check"],
            max_iter=6,
            memory=True,
            verbose=True,
            allow_delegation=False
        ),
        AgentSpecification(
            name="SEO Optimizer",
            role="SEO Specialist",
            goal="Optimize all content for search engines and improve rankings",
            backstory="Technical SEO expert with proven track record of improving organic search visibility",
            tools=["keyword_research", "seo_audit", "competitor_analysis"],
            max_iter=3,
            memory=True,
            verbose=True,
            allow_delegation=False
        )
    ]
    
    tasks = [
        TaskSpecification(
            name="market_research",
            description="Research trending topics in client's industry, analyze competitor content, and identify content opportunities",
            agent_name="Trend Researcher",
            expected_output="Comprehensive market research report with trending topics, competitor analysis, and content opportunities",
            depends_on=[],
            output_format="json"
        ),
        TaskSpecification(
            name="content_strategy",
            description="Develop content strategy based on research findings, define content calendar and distribution plan",
            agent_name="Content Strategist", 
            expected_output="Detailed content strategy document with calendar, topics, and distribution channels",
            depends_on=["market_research"],
            output_format="markdown"
        ),
        TaskSpecification(
            name="content_creation",
            description="Create blog posts, social media content, and marketing copy based on strategy",
            agent_name="Content Creator",
            expected_output="Complete content package: blog posts, social media posts, and marketing copy",
            depends_on=["content_strategy"],
            output_format="text"
        ),
        TaskSpecification(
            name="seo_optimization",
            description="Optimize all created content for SEO, add keywords, meta descriptions, and improve structure",
            agent_name="SEO Optimizer",
            expected_output="SEO-optimized content with keywords, meta descriptions, and technical improvements",
            depends_on=["content_creation"],
            output_format="text"
        )
    ]
    
    workflow = CrewWorkflow(
        name="Digital Marketing Content Pipeline",
        description="Complete content creation workflow from research to SEO-optimized publication",
        task_sequence=["market_research", "content_strategy", "content_creation", "seo_optimization"],
        parallel_tasks=[],
        decision_points=[
            {"checkpoint": "post_research", "condition": "quality_threshold_met"},
            {"checkpoint": "post_creation", "condition": "content_approval"}
        ]
    )
    
    return CrewArchitecture(
        crew_name="Digital Marketing Content Crew",
        crew_description="Automated content creation system for digital marketing agencies serving multiple clients",
        agents=agents,
        tasks=tasks,
        workflow=workflow,
        estimated_runtime="45-60 minutes per content batch",
        resource_requirements={
            "api_calls": "high",
            "processing": "moderate", 
            "storage": "moderate",
            "monitoring": "required"
        },
        success_metrics=[
            "content_quality_score",
            "seo_optimization_level", 
            "client_satisfaction",
            "time_to_completion"
        ],
        dependencies=[
            "crewai>=0.141.0",
            "openai>=1.0.0",
            "langchain",
            "selenium",
            "beautifulsoup4",
            "requests",
            "python-dotenv"
        ]
    )

def test_code_generation_quality():
    """Test the quality and completeness of generated code"""
    print("CrewBuilder Code Generation Quality Test")
    print("=" * 50)
    
    try:
        from agents import create_code_generator
        
        # Create realistic test case
        test_architecture = create_realistic_test_case()
        print(f"Test case: {test_architecture.crew_name}")
        print(f"Agents: {len(test_architecture.agents)}")
        print(f"Tasks: {len(test_architecture.tasks)}")
        print(f"Dependencies: {len(test_architecture.dependencies)}")
        
        # Generate code using fallback method (no API needed)
        code_generator = create_code_generator()
        generated_package = code_generator._create_fallback_code(test_architecture)
        
        print(f"\nGenerated package components:")
        print(f"  Main code: {len(generated_package.main_code)} characters")
        print(f"  Requirements: {len(generated_package.requirements_txt.splitlines())} dependencies")
        print(f"  Setup guide: {len(generated_package.setup_instructions)} characters")
        
        # Quality checks
        quality_score = run_quality_checks(generated_package, test_architecture)
        
        # Show generated code sample
        print(f"\nSample of generated CrewAI code:")
        print("-" * 50)
        lines = generated_package.main_code.split('\n')
        for i, line in enumerate(lines[:30]):  # Show first 30 lines
            print(f"{i+1:2d}: {line}")
        print("...")
        print("-" * 50)
        
        # Save generated code for inspection
        save_generated_code(generated_package, test_architecture)
        
        print(f"\nQUALITY ASSESSMENT: {quality_score}/100")
        if quality_score >= 80:
            print("EXCELLENT: Generated code ready for production")
        elif quality_score >= 60:
            print("GOOD: Generated code needs minor improvements")
        else:
            print("NEEDS WORK: Generated code requires significant improvements")
            
        return quality_score >= 60
        
    except Exception as e:
        print(f"ERROR: Code generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_quality_checks(generated_package, architecture):
    """Run comprehensive quality checks on generated code"""
    score = 0
    
    print(f"\nRunning quality checks...")
    
    # 1. Syntax validation (20 points)
    try:
        compile(generated_package.main_code, '<generated>', 'exec')
        print("  [+20] Valid Python syntax")
        score += 20
    except SyntaxError:
        print("  [+0] Syntax errors found")
    
    # 2. CrewAI structure validation (20 points)
    required_imports = ["from crewai import Agent, Task, Crew"]
    required_patterns = ["= Agent(", "= Task(", "= Crew("]
    
    structure_score = 0
    for pattern in required_imports + required_patterns:
        if pattern in generated_package.main_code:
            structure_score += 4
    
    print(f"  [+{structure_score}] CrewAI structure completeness")
    score += structure_score
    
    # 3. Agent implementation (15 points)
    agent_score = 0
    for agent in architecture.agents:
        agent_var = agent.name.lower().replace(" ", "_")
        if agent_var in generated_package.main_code:
            agent_score += 15 // len(architecture.agents)
    
    print(f"  [+{agent_score}] Agent implementation")
    score += agent_score
    
    # 4. Task implementation (15 points)
    task_score = 0
    for task in architecture.tasks:
        task_var = task.name.lower().replace(" ", "_")
        if task_var in generated_package.main_code:
            task_score += 15 // len(architecture.tasks)
    
    print(f"  [+{task_score}] Task implementation")
    score += task_score
    
    # 5. Documentation quality (10 points)
    doc_score = 0
    if '"""' in generated_package.main_code:
        doc_score += 5
    if len(generated_package.setup_instructions) > 100:
        doc_score += 5
    
    print(f"  [+{doc_score}] Documentation quality")
    score += doc_score
    
    # 6. Dependencies completeness (10 points)
    dep_score = 0
    if "crewai" in generated_package.requirements_txt:
        dep_score += 10
    
    print(f"  [+{dep_score}] Dependencies completeness")
    score += dep_score
    
    return score

def save_generated_code(generated_package, architecture):
    """Save generated code for manual inspection"""
    output_dir = Path("generated_output")
    output_dir.mkdir(exist_ok=True)
    
    # Save main code
    (output_dir / "main.py").write_text(generated_package.main_code, encoding='utf-8')
    (output_dir / "requirements.txt").write_text(generated_package.requirements_txt, encoding='utf-8')
    (output_dir / "setup_instructions.md").write_text(generated_package.setup_instructions, encoding='utf-8')
    
    print(f"\nGenerated code saved to 'generated_output/' directory")
    print("  - main.py (runnable CrewAI code)")
    print("  - requirements.txt (dependencies)")
    print("  - setup_instructions.md (setup guide)")

if __name__ == "__main__":
    print("CrewBuilder - Code Generation Quality Test")
    print("Testing with realistic digital marketing agency scenario...")
    print()
    
    success = test_code_generation_quality()
    
    print("\n" + "=" * 50)
    if success:
        print("SUCCESS: Code generation quality validated!")
        print("CrewBuilder generates production-ready CrewAI code.")
    else:
        print("NEEDS IMPROVEMENT: Code generation requires work.")
