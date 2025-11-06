"""Lucas Silva - Report Synthesizer (LLM-Powered)"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from src.llm import get_llm_client, LUCAS_SYSTEM_PROMPT

class LucasAgentLLM(BaseAgent):
    def __init__(self, project_id="destiny-analytical-team"):
        super().__init__(name="Lucas Silva", role="Report Synthesizer",
                        specialization="Multi-source synthesis, Report writing, Actionable recommendations",
                        project_id=project_id)
        self.llm = get_llm_client()

    def _execute_work(self, task: Task) -> TaskResult:
        start = datetime.now()
        prompt = f"""INTELLIGENCE SYNTHESIS: {task.title}
Data: {task.description}

Create comprehensive report:
1. Executive Summary
2. Key Findings (from all specialists)
3. Cross-cutting Themes
4. Critical Red Flags
5. Actionable Recommendations (prioritized)
6. Supporting Evidence

Make it prosecution-ready."""
        
        analysis = self.llm.chat(LUCAS_SYSTEM_PROMPT, prompt, temperature=0.7, max_tokens=4000)
        result = TaskResult(task.task_id, self.name, TaskStatus.DONE,
                           {"analysis_type": "synthesis", "llm_powered": True},
                           analysis, (datetime.now()-start).total_seconds(),
                           ["final_report.md", "executive_summary.md"],
                           "Deliver to prosecutors")
        return result

if __name__ == "__main__":
    print("✅ Lucas Silva (LLM) - Report Synthesis 📝")
