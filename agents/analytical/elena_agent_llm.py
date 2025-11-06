"""Elena Volkov - OSINT Specialist (LLM-Powered)"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from src.llm import get_llm_client, ELENA_SYSTEM_PROMPT

class ElenaAgentLLM(BaseAgent):
    def __init__(self, project_id="destiny-analytical-team"):
        super().__init__(name="Elena Volkov", role="OSINT Specialist",
                        specialization="Open source intelligence, Digital footprint, Social media intelligence",
                        project_id=project_id)
        self.llm = get_llm_client()

    def _execute_work(self, task: Task) -> TaskResult:
        start = datetime.now()
        prompt = f"""OSINT INVESTIGATION: {task.title}
Target: {task.description}

Conduct open source intelligence:
1. Digital Footprint (online presence, social media, websites)
2. Key Findings (important discoveries)
3. Background Intelligence (public records, associations)
4. Red Flags (suspicious activities, connections, patterns)
5. Evidence Sources (links and citations)
6. Investigative Leads (follow-up directions)

Everything online leaves traces."""
        
        analysis = self.llm.chat(ELENA_SYSTEM_PROMPT, prompt, temperature=0.7, max_tokens=3000)
        result = TaskResult(task.task_id, self.name, TaskStatus.DONE,
                           {"analysis_type": "osint", "llm_powered": True},
                           analysis, (datetime.now()-start).total_seconds(),
                           ["osint_report.md"], "Verify findings with additional sources")
        return result

if __name__ == "__main__":
    print("✅ Elena Volkov (LLM) - OSINT Intelligence 🔍")
