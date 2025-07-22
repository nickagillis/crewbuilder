"""
Cost Optimization for CrewAI Agents
"""

def optimize_agent_config(agent):
    """Add token limits and optimize agent configuration"""
    # Set reasonable token limits
    if hasattr(agent, 'llm') and agent.llm:
        agent.max_iter = 2  # Strict limit on iterations
        agent.max_retry = 1  # Only 1 retry on failure
        
    # Disable verbose mode in production to save tokens
    agent.verbose = False
    
    # Disable memory for non-critical agents
    if hasattr(agent, 'memory'):
        agent.memory = False
        
    return agent

def get_token_limits():
    """Get token limits for different agent types"""
    return {
        'clarification': 500,   # Very focused questions only
        'api_analyst': 800,     # Just API availability
        'architect': 1500,      # Core design only
        'task_designer': 1000,  # Brief task descriptions
        'code_writer': 2000,    # Actual code generation
        'interface_builder': 2000,  # UI code generation
        'execution_wrapper': 1500,  # Service wrapper
        'quality_reviewer': 800,    # Key issues only
        'deployment': 800,      # Essential configs
        'documentation': 1200,  # Core docs only
        'manager': 500         # Brief coordination
    }

def add_context_focus(task_description, focus_points):
    """Add focus points to reduce token usage"""
    return f"""{task_description}

IMPORTANT - Focus ONLY on:
{chr(10).join(f'- {point}' for point in focus_points)}

Be concise and specific. Avoid unnecessary elaboration."""

def calculate_generation_cost(token_count, model="gpt-3.5-turbo"):
    """Calculate estimated cost for a generation"""
    rates = {
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},  # per 1K tokens
        "gpt-4": {"input": 0.01, "output": 0.03}  # per 1K tokens
    }
    
    # Rough estimate: 60% input, 40% output
    input_tokens = token_count * 0.6
    output_tokens = token_count * 0.4
    
    rate = rates.get(model, rates["gpt-3.5-turbo"])
    cost = (input_tokens * rate["input"] + output_tokens * rate["output"]) / 1000
    
    return cost

def enforce_cost_limit(crew, max_cost=2.0):
    """Enforce a maximum cost limit per generation"""
    if hasattr(crew, 'agents'):
        total_agents = len(crew.agents)
        # Rough estimate: each agent makes 3-5 calls
        estimated_calls = total_agents * 4
        # Average tokens per call
        avg_tokens_per_call = 1500
        
        estimated_tokens = estimated_calls * avg_tokens_per_call
        estimated_cost = calculate_generation_cost(estimated_tokens)
        
        if estimated_cost > max_cost:
            # Reduce verbosity and iterations
            for agent in crew.agents:
                agent.max_iter = 1
                agent.verbose = False
                if hasattr(agent, 'memory'):
                    agent.memory = False
                    
            print(f"⚠️ Cost control activated: Estimated ${estimated_cost:.2f} > ${max_cost:.2f} limit")