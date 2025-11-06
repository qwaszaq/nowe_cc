"""
Sofia Martinez - Market Researcher (LLM-Powered)
Market Intelligence & Competitive Analysis Expert

UPGRADE: Uses local LLM at 192.168.200.226 for real market intelligence
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from src.llm import get_llm_client, SOFIA_SYSTEM_PROMPT

class SofiaAgentLLM(BaseAgent):
    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(name="Sofia Martinez", role="Market Researcher",
                        specialization="Market trends, Competitive intelligence, Strategic positioning",
                        project_id=project_id)
        self.llm = get_llm_client()

    def _execute_work(self, task: Task) -> TaskResult:
        start_time, task_lower = datetime.now(), task.description.lower()
        context = self.load_context(task.description, limit=3)
        
        if any(w in task_lower for w in ["market", "competitor", "industry"]):
            result = self._market_analysis_llm(task, context)
        elif any(w in task_lower for w in ["competitive", "competition"]):
            result = self._competitive_intel_llm(task, context)
        else:
            result = self._general_analysis_llm(task, context)
        
        result.time_taken = (datetime.now() - start_time).total_seconds()
        return result

    def _market_analysis_llm(self, task, context):
        prompt = f"""MARKET ANALYSIS:
Task: {task.description}
Context: {self._fmt(context)}

Analyze: 1) Market size/growth 2) Key players 3) Trends 4) Opportunities 5) Threats 6) Recommendations"""
        
        analysis = self.llm.chat(SOFIA_SYSTEM_PROMPT, prompt, temperature=0.7, max_tokens=3500)
        return TaskResult(task.task_id, self.name, TaskStatus.DONE,
                         {"analysis_type": "market", "llm_powered": True},
                         analysis, 0, ["market_analysis.md"],
                         "Coordinate with Marcus for financial implications")

    def _competitive_intel_llm(self, task, context):
        prompt = f"""COMPETITIVE INTELLIGENCE:
Task: {task.description}
Context: {self._fmt(context)}

Analyze competitors: 1) Key players 2) SWOT 3) Market share 4) Strategic moves 5) Threats"""
        
        analysis = self.llm.chat(SOFIA_SYSTEM_PROMPT, prompt, temperature=0.7, max_tokens=3000)
        return TaskResult(task.task_id, self.name, TaskStatus.DONE,
                         {"analysis_type": "competitive", "llm_powered": True},
                         analysis, 0, ["competitive_analysis.md"], "Strategic planning session")

    def _general_analysis_llm(self, task, context):
        analysis = self.llm.chat(SOFIA_SYSTEM_PROMPT,
                                f"MARKET RESEARCH: {task.description}\n\nContext: {self._fmt(context)}",
                                temperature=0.7, max_tokens=2500)
        return TaskResult(task.task_id, self.name, TaskStatus.DONE,
                         {"analysis_type": "general", "llm_powered": True},
                         analysis, 0, ["market_intelligence.md"], "Review insights")

    def _fmt(self, ctx):
        return "\n".join([f"{i}. {c.get('content', str(c)) if isinstance(c, dict) else c}"
                         for i, c in enumerate(ctx, 1)]) if ctx else "No context."

if __name__ == "__main__":
    print("✅ Sofia Martinez (LLM) - Market Intelligence 📊")
