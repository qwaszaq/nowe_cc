"""Maya Patel - Data Analyst (LLM-Powered)"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from src.llm import get_llm_client, MAYA_SYSTEM_PROMPT

class MayaAgentLLM(BaseAgent):
    def __init__(self, project_id="destiny-analytical-team"):
        super().__init__(name="Maya Patel", role="Data Analyst",
                        specialization="Statistical analysis, Pattern detection, Data mining",
                        project_id=project_id)
        self.llm = get_llm_client()

    def _execute_work(self, task: Task) -> TaskResult:
        start = datetime.now()
        prompt = f"""DATA ANALYSIS: {task.title}
Description: {task.description}

Perform: 1) Statistical analysis 2) Pattern detection 3) Anomaly identification 4) Correlations 5) Predictions 6) Recommendations"""
        
        analysis = self.llm.chat(MAYA_SYSTEM_PROMPT, prompt, temperature=0.7, max_tokens=3500)
        result = TaskResult(task.task_id, self.name, TaskStatus.DONE,
                           {"analysis_type": "data", "llm_powered": True},
                           analysis, (datetime.now()-start).total_seconds(),
                           ["data_analysis.md"], "Share findings with team")
        return result

if __name__ == "__main__":
    print("✅ Maya Patel (LLM) - Data Analysis 📈")
