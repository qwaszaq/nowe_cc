"""Damian Rousseau - Devil's Advocate (LLM-Powered)"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from src.llm import get_llm_client, DAMIAN_SYSTEM_PROMPT

class DamianAgentLLM(BaseAgent):
    def __init__(self, project_id="destiny-analytical-team"):
        super().__init__(name="Damian Rousseau", role="Devil's Advocate",
                        specialization="Critical analysis, Alternative perspectives, Risk assessment",
                        project_id=project_id)
        self.llm = get_llm_client()

    def _execute_work(self, task: Task) -> TaskResult:
        start = datetime.now()
        prompt = f"""CRITICAL CHALLENGE: {task.title}
Team Conclusions: {task.description}

Challenge everything:
1. What might we be missing?
2. Alternative explanations?
3. Assumptions to test?
4. How will defense attack this?
5. Weaknesses in our case?
6. Additional analysis needed?

Be tough but constructive."""
        
        analysis = self.llm.chat(DAMIAN_SYSTEM_PROMPT, prompt, temperature=0.7, max_tokens=3000)
        result = TaskResult(task.task_id, self.name, TaskStatus.DONE,
                           {"analysis_type": "critique", "llm_powered": True},
                           analysis, (datetime.now()-start).total_seconds(),
                           ["critical_review.md"], "Team refines analysis")
        return result

if __name__ == "__main__":
    print("✅ Damian Rousseau (LLM) - Critical Analysis 😈")
