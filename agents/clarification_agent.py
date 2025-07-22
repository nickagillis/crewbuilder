"""
Clarification Agent - Interactive Requirements Refinement
This agent ensures we fully understand what the client needs before building
"""

from crewai import Agent, Task
from typing import List, Dict, Any
from .llm_config import get_configured_llm
from pydantic import BaseModel, Field
from datetime import datetime

class ClarificationQuestion(BaseModel):
    """A question to ask the user for clarification"""
    question: str = Field(description="The question to ask")
    context: str = Field(description="Why we're asking this question")
    options: List[str] = Field(default_factory=list, description="Multiple choice options if applicable")
    question_type: str = Field(default="open", description="Type: open, multiple_choice, yes_no")

class RefinedRequirements(BaseModel):
    """The refined and clarified requirements after user interaction"""
    original_requirement: str = Field(description="What the user originally asked for")
    refined_requirement: str = Field(description="The clarified and detailed requirement")
    key_features: List[str] = Field(description="Specific features identified")
    constraints: List[str] = Field(description="Technical or business constraints")
    success_criteria: List[str] = Field(description="How to measure success")
    assumptions: List[str] = Field(description="Assumptions we're making")
    out_of_scope: List[str] = Field(description="What we're NOT building")
    estimated_complexity: str = Field(description="simple, moderate, or complex")
    
class ClarificationSession(BaseModel):
    """A complete clarification session with the user"""
    session_id: str = Field(description="Unique session identifier")
    original_requirement: str = Field(description="Initial user requirement")
    questions_asked: List[ClarificationQuestion] = Field(description="Questions we asked")
    user_responses: Dict[str, str] = Field(description="User's responses to our questions")
    refined_requirements: RefinedRequirements = Field(description="Final refined requirements")
    confidence_score: float = Field(description="How confident we are in understanding (0-1)")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

def create_clarification_agent():
    """Create the Clarification Agent that refines requirements through interaction"""
    
    # Get configured LLM
    llm = get_configured_llm(temperature=0.7)
    
    return Agent(
        role="Requirements Clarification Specialist",
        goal="Engage with users to deeply understand their needs and refine vague requirements into crystal-clear specifications",
        backstory="""You are an expert at understanding business needs and translating them into 
        technical requirements. You have years of experience as a business analyst and solution 
        architect. You know exactly what questions to ask to uncover hidden requirements, 
        constraints, and success criteria. You're friendly but thorough, ensuring nothing 
        important is missed while keeping the conversation engaging.""",
        llm=llm,  # Pass the LLM explicitly
        verbose=True,
        allow_delegation=False,
        tools=[],  # This agent uses conversation, not tools
        max_iter=5,
        memory=True
    )

def analyze_initial_requirement(agent: Agent, requirement: str) -> List[ClarificationQuestion]:
    """
    Analyze the initial requirement and generate clarification questions
    """
    
    task = Task(
        description=f"""
        Analyze this business requirement and identify areas that need clarification:
        
        Requirement: {requirement}
        
        Generate 3-5 targeted questions that will help us understand:
        1. The specific problem they're trying to solve
        2. Who will use this system and how
        3. What success looks like to them
        4. Any technical constraints or preferences
        5. The scope and boundaries of the solution
        
        For each question:
        - Make it specific and easy to answer
        - Explain why you're asking (context)
        - Provide multiple choice options where it makes sense
        - Mark the question type (open, multiple_choice, yes_no)
        
        Focus on questions that will most impact the system design.
        """,
        agent=agent,
        expected_output="A list of clarification questions with context and options"
    )
    
    try:
        result = agent.execute_task(task)
    except Exception as e:
        print(f"Warning: Could not execute clarification task: {e}")
        result = ""
    
    # Parse the result into ClarificationQuestion objects
    questions = []
    
    # Extract questions from the agent's response
    # This is a simplified parser - in production, use better NLP
    lines = result.split('\n')
    current_question = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('Q:') or line.startswith('Question:'):
            if current_question:
                questions.append(current_question)
            current_question = ClarificationQuestion(
                question=line.split(':', 1)[1].strip(),
                context="",
                options=[],
                question_type="open"
            )
        elif line.startswith('Context:') and current_question:
            current_question.context = line.split(':', 1)[1].strip()
        elif line.startswith('Options:') and current_question:
            current_question.options = [opt.strip() for opt in line.split(':', 1)[1].split(',')]
            current_question.question_type = "multiple_choice"
        elif line.startswith('Type:') and current_question:
            current_question.question_type = line.split(':', 1)[1].strip()
    
    if current_question:
        questions.append(current_question)
    
    # If parsing fails, try to extract questions from raw text
    if not questions and result:
        # Look for any question marks in the result
        sentences = result.replace('\n', ' ').split('.')
        for sent in sentences:
            if '?' in sent:
                question_text = sent.strip()
                if question_text:
                    questions.append(ClarificationQuestion(
                        question=question_text,
                        context="This will help us better understand your requirements",
                        options=[],
                        question_type="open"
                    ))
    
    # If still no questions, generate context-aware defaults based on the requirement
    if not questions:
        # Analyze the requirement to generate relevant questions
        req_lower = requirement.lower()
        
        questions = []
        
        # Always ask about the core problem
        questions.append(ClarificationQuestion(
            question="What specific problem are you trying to solve with this AI agent system?",
            context="Understanding the core problem helps us design the right solution",
            options=[],
            question_type="open"
        ))
        
        # Ask about users/audience
        questions.append(ClarificationQuestion(
            question="Who will be the primary users of this system?",
            context="Knowing the users helps us design the right interface and features",
            options=["Internal team", "Customers", "Both internal and external", "Other"],
            question_type="multiple_choice"
        ))
        
        # Add context-specific questions based on keywords in requirement
        if any(word in req_lower for word in ['integrate', 'connect', 'api', 'system']):
            questions.append(ClarificationQuestion(
                question="What existing systems or APIs does this need to integrate with?",
                context="Integration requirements affect our technical architecture",
                options=[],
                question_type="open"
            ))
        
        if any(word in req_lower for word in ['data', 'database', 'store', 'process']):
            questions.append(ClarificationQuestion(
                question="What type and volume of data will this system handle?",
                context="Data requirements influence storage and processing design",
                options=[],
                question_type="open"
            ))
        
        if any(word in req_lower for word in ['automate', 'workflow', 'process']):
            questions.append(ClarificationQuestion(
                question="Can you describe the current manual process this will automate?",
                context="Understanding the current process helps design better automation",
                options=[],
                question_type="open"
            ))
        
        # Always ask about success criteria
        questions.append(ClarificationQuestion(
            question="What would success look like for this system?",
            context="Clear success criteria help us build the right features",
            options=[],
            question_type="open"
        ))
        
        # Ask about constraints if not already covered
        if len(questions) < 5:
            questions.append(ClarificationQuestion(
                question="Do you have any specific technical requirements or constraints?",
                context="Technical constraints affect our architecture decisions",
                options=["Must integrate with existing systems", "Specific performance requirements", 
                        "Security/compliance needs", "Budget constraints", "None"],
                question_type="multiple_choice"
            ))
    
    return questions[:5]  # Limit to 5 questions max

def refine_requirements(agent: Agent, original: str, questions: List[ClarificationQuestion], 
                       responses: Dict[str, str]) -> RefinedRequirements:
    """
    Take the original requirement and user responses to create refined requirements
    """
    
    # Format Q&A for the agent
    qa_text = "\n".join([
        f"Q: {q.question}\nA: {responses.get(q.question, 'No response')}"
        for q in questions
    ])
    
    task = Task(
        description=f"""
        Create refined requirements based on this clarification session:
        
        Original Requirement: {original}
        
        Clarification Q&A:
        {qa_text}
        
        Based on this information, create a comprehensive refined requirement that includes:
        
        1. A clear, detailed description of what needs to be built
        2. Specific features that must be included (bullet points)
        3. Technical and business constraints
        4. Clear success criteria (measurable outcomes)
        5. Explicit assumptions we're making
        6. What is explicitly OUT of scope
        7. Complexity assessment (simple/moderate/complex)
        
        Make the refined requirement specific enough that another team could build 
        exactly what the client wants without further clarification.
        """,
        agent=agent,
        expected_output="Comprehensive refined requirements document"
    )
    
    try:
        result = agent.execute_task(task)
    except Exception as e:
        print(f"Warning: Could not execute clarification task: {e}")
        result = ""
    
    # Parse the result from the agent's response
    # Initialize with empty values
    refined_req = result if result else f"Refined version of: {original}"
    features = []
    constraints = []
    criteria = []
    assumptions = []
    out_of_scope = []
    complexity = "moderate"
    
    # Parse structured sections from the agent's response
    if result:
        lines = result.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if 'refined requirement' in line.lower() or 'description' in line.lower():
                current_section = 'refined'
            elif 'features' in line.lower() or 'feature list' in line.lower():
                current_section = 'features'
            elif 'constraint' in line.lower():
                current_section = 'constraints'
            elif 'success criteria' in line.lower() or 'criteria' in line.lower():
                current_section = 'criteria'
            elif 'assumption' in line.lower():
                current_section = 'assumptions'
            elif 'out of scope' in line.lower() or 'not included' in line.lower():
                current_section = 'out_of_scope'
            elif 'complexity' in line.lower():
                if 'simple' in line.lower():
                    complexity = 'simple'
                elif 'complex' in line.lower():
                    complexity = 'complex'
                else:
                    complexity = 'moderate'
            
            # Add items to appropriate lists
            elif line.startswith(('•', '-', '*', '▪', '◦')) or (line and line[0].isdigit() and '.' in line[:3]):
                item = line.lstrip('•-*▪◦0123456789. ')
                if current_section == 'features' and item:
                    features.append(item)
                elif current_section == 'constraints' and item:
                    constraints.append(item)
                elif current_section == 'criteria' and item:
                    criteria.append(item)
                elif current_section == 'assumptions' and item:
                    assumptions.append(item)
                elif current_section == 'out_of_scope' and item:
                    out_of_scope.append(item)
    
    # Extract refined requirement (first substantial paragraph)
    if result:
        paragraphs = [p.strip() for p in result.split('\n\n') if p.strip() and len(p.strip()) > 50]
        if paragraphs:
            refined_req = paragraphs[0]
    
    # Ensure we have at least some content in each field
    if not features:
        features = [f"Core functionality as described in: {original[:100]}..."]
    if not constraints:
        constraints = ["Requirements based on user responses"]
    if not criteria:
        criteria = ["System successfully addresses the stated need"]
    if not assumptions:
        assumptions = ["Standard technical infrastructure available"]
    if not out_of_scope:
        out_of_scope = ["Features not explicitly mentioned in requirements"]
    
    return RefinedRequirements(
        original_requirement=original,
        refined_requirement=refined_req,
        key_features=features[:10],  # Limit to 10 features
        constraints=constraints[:10],
        success_criteria=criteria[:10],
        assumptions=assumptions[:10],
        out_of_scope=out_of_scope[:10],
        estimated_complexity=complexity
    )

def create_clarification_session(agent: Agent, requirement: str, 
                               user_responses: Dict[str, str] = None) -> ClarificationSession:
    """
    Run a complete clarification session
    """
    
    # Generate questions
    questions = analyze_initial_requirement(agent, requirement)
    
    # In a real implementation, these responses would come from user interaction
    # For now, we'll use provided responses or generate mock ones
    if not user_responses:
        user_responses = {
            q.question: f"Sample response for: {q.question}"
            for q in questions
        }
    
    # Refine requirements based on responses
    refined = refine_requirements(agent, requirement, questions, user_responses)
    
    # Calculate confidence score based on response completeness
    answered_questions = sum(1 for q in questions if q.question in user_responses)
    confidence = answered_questions / len(questions) if questions else 0.5
    
    return ClarificationSession(
        session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        original_requirement=requirement,
        questions_asked=questions,
        user_responses=user_responses,
        refined_requirements=refined,
        confidence_score=confidence
    )

# Make agent available at module level
clarification_agent = create_clarification_agent()