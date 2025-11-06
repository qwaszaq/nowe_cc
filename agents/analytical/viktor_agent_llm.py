"""Viktor Kovalenko - Investigation Director (LLM-Powered)"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from src.llm import get_llm_client, VIKTOR_SYSTEM_PROMPT

class ViktorAgentLLM(BaseAgent):
    def __init__(self, project_id="destiny-analytical-team"):
        super().__init__(name="Viktor Kovalenko", role="Investigation Director",
                        specialization="Strategic coordination, Decision-making, Case synthesis",
                        project_id=project_id)
        self.llm = get_llm_client()

    def _execute_work(self, task: Task) -> TaskResult:
        start = datetime.now()
        prompt = f"""INVESTIGATION DIRECTION: {task.title}
Case: {task.description}

Provide strategic leadership:
1. Investigation Assessment (overall evaluation)
2. Team Coordination (how specialists integrate)
3. Strategic Insights (cross-domain patterns)
4. Final Conclusions (decisive assessment with confidence level)
5. Prosecution Recommendations (strategic priorities, ranked)
6. Next Steps (concrete actions)

Prosecutors need decisive leadership."""
        
        analysis = self.llm.chat(VIKTOR_SYSTEM_PROMPT, prompt, temperature=0.7, max_tokens=3500)
        result = TaskResult(task.task_id, self.name, TaskStatus.DONE,
                           {"analysis_type": "direction", "llm_powered": True},
                           analysis, (datetime.now()-start).total_seconds(),
                           ["investigation_direction.md"], "Execute strategic plan")
        return result

if __name__ == "__main__":
    print("✅ Viktor Kovalenko (LLM) - Investigation Leadership 🎯")
