#!/usr/bin/env python3
"""
Interactive Requirements Process for CrewBuilder
Fixes the single-prompt problem with conversation-based refinement
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class ConversationStage(Enum):
    INITIAL_UNDERSTANDING = "initial"
    CLARIFICATION = "clarification"
    REFINEMENT = "refinement"
    VALIDATION = "validation"
    READY_TO_BUILD = "ready"

@dataclass
class RequirementConversation:
    session_id: str
    stage: ConversationStage
    original_prompt: str
    clarifying_questions: List[str]
    user_answers: Dict[str, str]
    refined_requirements: Dict[str, Any]
    confidence_score: float
    
class InteractiveRequirementsGatherer:
    """Conversation-based requirements gathering instead of single prompt"""
    
    def start_conversation(self, initial_prompt: str) -> RequirementConversation:
        """Start interactive requirements gathering"""
        
        # Analyze initial prompt for domain and complexity
        domain = self._detect_domain(initial_prompt)
        complexity = self._estimate_complexity(initial_prompt)
        
        # Generate targeted clarifying questions
        questions = self._generate_questions(initial_prompt, domain, complexity)
        
        return RequirementConversation(
            session_id=self._generate_session_id(),
            stage=ConversationStage.INITIAL_UNDERSTANDING,
            original_prompt=initial_prompt,
            clarifying_questions=questions,
            user_answers={},
            refined_requirements={},
            confidence_score=0.3  # Low until we get answers
        )
    
    def process_answers(self, conversation: RequirementConversation, 
                       answers: Dict[str, str]) -> RequirementConversation:
        """Process user answers and determine next steps"""
        
        # Update conversation with answers
        conversation.user_answers.update(answers)
        
        # Analyze answers to refine requirements
        refined_reqs = self._refine_requirements(
            conversation.original_prompt,
            conversation.user_answers
        )
        
        # Calculate confidence in our understanding
        confidence = self._calculate_confidence(conversation.user_answers)
        
        # Determine if we need more clarification
        if confidence < 0.8:
            additional_questions = self._generate_followup_questions(
                refined_reqs, conversation.user_answers
            )
            conversation.clarifying_questions.extend(additional_questions)
            conversation.stage = ConversationStage.CLARIFICATION
        else:
            conversation.stage = ConversationStage.VALIDATION
        
        conversation.refined_requirements = refined_reqs
        conversation.confidence_score = confidence
        
        return conversation
    
    def generate_validation_summary(self, conversation: RequirementConversation) -> Dict[str, Any]:
        """Generate summary for user validation"""
        
        reqs = conversation.refined_requirements
        
        return {
            "understanding": f"I understand you want to {reqs.get('main_goal', 'automate a process')}",
            "scope": reqs.get('scope_description', 'Automated business process'),
            "key_features": reqs.get('features', []),
            "integrations": reqs.get('required_integrations', []),
            "complexity": reqs.get('complexity', 'moderate'),
            "estimated_agents": reqs.get('agent_count', 3),
            "estimated_time": reqs.get('estimated_time', '2-4 weeks'),
            "estimated_cost": reqs.get('estimated_cost', '$50-100/month'),
            "confirmation_needed": [
                "Does this match what you have in mind?",
                "Are there any important features missing?", 
                "Any integrations we haven't discussed?"
            ]
        }
    
    def _detect_domain(self, prompt: str) -> str:
        """Detect the business domain from initial prompt"""
        prompt_lower = prompt.lower()
        
        domains = {
            'content': ['content', 'blog', 'social', 'post', 'article', 'writing'],
            'marketing': ['marketing', 'campaign', 'lead', 'email', 'newsletter'],
            'sales': ['sales', 'crm', 'deal', 'prospect', 'pipeline'],
            'support': ['support', 'help', 'ticket', 'customer service'],
            'operations': ['operation', 'workflow', 'process', 'automation'],
            'data': ['data', 'analytics', 'report', 'dashboard', 'metrics'],
            'ecommerce': ['shop', 'store', 'product', 'inventory', 'order'],
            'hr': ['hr', 'hiring', 'employee', 'onboard', 'payroll']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return domain
        
        return 'general'
    
    def _estimate_complexity(self, prompt: str) -> str:
        """Estimate complexity from initial prompt"""
        indicators = {
            'simple': ['simple', 'basic', 'easy', 'quick'],
            'complex': ['complex', 'enterprise', 'advanced', 'multiple systems', 'integrate']
        }
        
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in indicators['complex']) or len(prompt) > 500:
            return 'complex'
        elif any(word in prompt_lower for word in indicators['simple']) or len(prompt) < 100:
            return 'simple'
        else:
            return 'moderate'
    
    def _generate_questions(self, prompt: str, domain: str, complexity: str) -> List[str]:
        """Generate targeted clarifying questions"""
        
        base_questions = [
            "What's the main problem you're trying to solve?",
            "Who will be using this system?",
            "How are you handling this process manually now?"
        ]
        
        domain_questions = {
            'content': [
                "What type of content do you want to create?",
                "How often do you publish?",
                "What platforms do you publish to?",
                "Do you have existing content templates or style guides?"
            ],
            'marketing': [
                "What marketing channels are you currently using?",
                "What's your target audience?",
                "Do you have existing marketing tools (CRM, email platform)?",
                "What are your main marketing goals?"
            ],
            'sales': [
                "What does your current sales process look like?",
                "What CRM system do you use?",
                "How do you currently track leads?",
                "What's your average deal size and sales cycle?"
            ]
        }
        
        complexity_questions = {
            'complex': [
                "Which systems need to be integrated?",
                "Do you have any compliance requirements?",
                "What's your technical team's experience level?",
                "Do you need real-time processing or batch processing?"
            ]
        }
        
        questions = base_questions.copy()
        questions.extend(domain_questions.get(domain, []))
        
        if complexity == 'complex':
            questions.extend(complexity_questions['complex'])
        
        return questions[:6]  # Limit to avoid overwhelming
    
    def _refine_requirements(self, original_prompt: str, answers: Dict[str, str]) -> Dict[str, Any]:
        """Refine requirements based on answers"""
        
        # This would use AI to synthesize the conversation into structured requirements
        # For now, using pattern-based analysis
        
        refined = {
            'main_goal': self._extract_main_goal(original_prompt, answers),
            'scope_description': self._generate_scope_description(answers),
            'features': self._identify_features(answers),
            'required_integrations': self._identify_integrations(answers),
            'complexity': self._refine_complexity_estimate(answers),
            'agent_count': self._estimate_agent_count(answers),
            'estimated_time': self._estimate_implementation_time(answers),
            'estimated_cost': self._estimate_monthly_cost(answers)
        }
        
        return refined
    
    def _calculate_confidence(self, answers: Dict[str, str]) -> float:
        """Calculate confidence in our understanding"""
        
        # Basic scoring based on number and quality of answers
        if not answers:
            return 0.2
        
        key_areas = ['main_goal', 'platforms', 'current_process', 'integrations']
        answered_areas = sum(1 for area in key_areas if any(area in q for q in answers.keys()))
        
        base_confidence = min(0.9, 0.3 + (answered_areas * 0.15))
        
        # Boost confidence for detailed answers
        detailed_answers = sum(1 for answer in answers.values() if len(answer) > 20)
        detail_boost = min(0.2, detailed_answers * 0.05)
        
        return min(0.95, base_confidence + detail_boost)
    
    def _generate_followup_questions(self, refined_reqs: Dict[str, Any], 
                                   existing_answers: Dict[str, str]) -> List[str]:
        """Generate follow-up questions for areas that need clarification"""
        
        followup = []
        
        # Check for missing critical information
        if not refined_reqs.get('required_integrations'):
            followup.append("What tools or platforms do you currently use that should be integrated?")
        
        if refined_reqs.get('complexity') == 'complex' and 'technical team' not in ' '.join(existing_answers.values()).lower():
            followup.append("Do you have technical team members who can help with setup and maintenance?")
        
        if 'budget' not in ' '.join(existing_answers.values()).lower():
            followup.append("Do you have a budget range in mind for this automation?")
        
        return followup[:3]  # Limit follow-ups
    
    # Helper methods for requirement extraction
    def _extract_main_goal(self, prompt: str, answers: Dict[str, str]) -> str:
        # Extract the primary automation goal
        return "automate business process"  # Simplified for demo
    
    def _generate_scope_description(self, answers: Dict[str, str]) -> str:
        return "Automated business workflow"  # Simplified
    
    def _identify_features(self, answers: Dict[str, str]) -> List[str]:
        return ["feature1", "feature2"]  # Simplified
    
    def _identify_integrations(self, answers: Dict[str, str]) -> List[str]:
        return ["integration1"]  # Simplified
    
    def _refine_complexity_estimate(self, answers: Dict[str, str]) -> str:
        return "moderate"  # Simplified
    
    def _estimate_agent_count(self, answers: Dict[str, str]) -> int:
        return 3  # Simplified
    
    def _estimate_implementation_time(self, answers: Dict[str, str]) -> str:
        return "2-3 weeks"  # Simplified
    
    def _estimate_monthly_cost(self, answers: Dict[str, str]) -> str:
        return "$50-100"  # Simplified
    
    def _generate_session_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

# Example usage
if __name__ == "__main__":
    gatherer = InteractiveRequirementsGatherer()
    
    # Start conversation
    conversation = gatherer.start_conversation(
        "I need to automate content creation for my marketing agency"
    )
    
    print("Clarifying Questions:")
    for i, question in enumerate(conversation.clarifying_questions, 1):
        print(f"{i}. {question}")
    
    # Simulate user answers
    answers = {
        "content_type": "Blog posts and social media content",
        "frequency": "Daily social posts, weekly blog posts",
        "platforms": "LinkedIn, Twitter, company blog",
        "current_process": "Manual research and writing, takes 3 hours daily"
    }
    
    # Process answers
    updated_conversation = gatherer.process_answers(conversation, answers)
    
    print(f"\nConfidence Score: {updated_conversation.confidence_score}")
    print(f"Stage: {updated_conversation.stage}")
    
    if updated_conversation.stage == ConversationStage.VALIDATION:
        summary = gatherer.generate_validation_summary(updated_conversation)
        print("\nValidation Summary:")
        print(f"Understanding: {summary['understanding']}")
        print(f"Scope: {summary['scope']}")
        print("Confirmation needed:")
        for question in summary['confirmation_needed']:
            print(f"  - {question}")
