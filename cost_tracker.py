"""
Cost tracking for CrewBuilder generations
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

class CostTracker:
    def __init__(self, log_file="generation_costs.json"):
        self.log_file = log_file
        self.current_generation = {
            "start_time": None,
            "end_time": None,
            "requests": 0,
            "total_tokens": 0,
            "estimated_cost": 0.0,
            "requirement": "",
            "agents_used": []
        }
        
    def start_generation(self, requirement: str):
        """Start tracking a new generation"""
        self.current_generation = {
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "requests": 0,
            "total_tokens": 0,
            "estimated_cost": 0.0,
            "requirement": requirement[:100],
            "agents_used": []
        }
        
    def track_request(self, agent_name: str, tokens: int, model: str = "gpt-3.5-turbo"):
        """Track an API request"""
        self.current_generation["requests"] += 1
        self.current_generation["total_tokens"] += tokens
        
        # Calculate cost
        rates = {
            "gpt-3.5-turbo": 0.001,  # Average of input/output
            "gpt-4": 0.02  # Average of input/output
        }
        cost = (tokens / 1000) * rates.get(model, 0.001)
        self.current_generation["estimated_cost"] += cost
        
        if agent_name not in self.current_generation["agents_used"]:
            self.current_generation["agents_used"].append(agent_name)
            
    def end_generation(self):
        """End tracking and save results"""
        self.current_generation["end_time"] = datetime.now().isoformat()
        
        # Load existing data
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                data = json.load(f)
        else:
            data = {"generations": []}
            
        # Add current generation
        data["generations"].append(self.current_generation)
        
        # Calculate summary stats
        total_cost = sum(g["estimated_cost"] for g in data["generations"])
        avg_cost = total_cost / len(data["generations"]) if data["generations"] else 0
        
        data["summary"] = {
            "total_generations": len(data["generations"]),
            "total_cost": round(total_cost, 2),
            "average_cost": round(avg_cost, 2),
            "last_updated": datetime.now().isoformat()
        }
        
        # Save
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"\n💰 Generation Cost Summary:")
        print(f"   Requests: {self.current_generation['requests']}")
        print(f"   Tokens: {self.current_generation['total_tokens']:,}")
        print(f"   Est. Cost: ${self.current_generation['estimated_cost']:.2f}")
        print(f"   Avg Cost: ${avg_cost:.2f}")
        
        # Alert if cost is too high
        if self.current_generation["estimated_cost"] > 5.0:
            print(f"   ⚠️ WARNING: High cost generation! Consider optimization.")
            
    def get_cost_report(self) -> Dict[str, Any]:
        """Get cost report"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return {"generations": [], "summary": {}}