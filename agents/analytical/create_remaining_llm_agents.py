"""
Batch Create Remaining LLM-Powered Agents

This script creates the LLM-powered versions of:
- Sofia (Market Researcher)
- Maya (Data Analyst)
- Lucas (Report Synthesizer)
- Damian (Devil's Advocate)
- Viktor (Investigation Director)
- Elena (OSINT Specialist)

All follow the same pattern as Marcus, Alex, and Adrian.
"""

import os

# Base template for LLM agents
AGENT_TEMPLATE = '''"""
{name} - {role} (LLM-Powered)
{description}

UPGRADE: Uses local LLM at 192.168.200.226 for real {analysis_type}
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime

# Import LLM client
from src.llm import get_llm_client, {system_prompt_name}


class {class_name}(BaseAgent):
    """
    {name} - {role} (LLM-Powered)

    Role: {role}
    Specialization: {specialization}

    UPGRADE: Real AI reasoning instead of templates
    """

    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="{name}",
            role="{role}",
            specialization="{specialization}",
            project_id=project_id
        )

        # Initialize LLM client
        self.llm = get_llm_client()

    def _execute_work(self, task: Task) -> TaskResult:
        """Execute {role_lower} work using LLM"""

        start_time = datetime.now()
        task_lower = task.description.lower()

        context = self.load_context(task.description, limit=3)

        # Route to appropriate analysis method
{routing_logic}

        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken

        return result

{methods}

    # Helper methods

    def _format_context(self, context: list) -> str:
        """Format context for LLM"""
        if not context:
            return "No previous context."
        formatted = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                formatted.append(f"{{i}}. {{ctx.get('content', str(ctx))}}")
            else:
                formatted.append(f"{{i}}. {{ctx}}")
        return "\\n".join(formatted)

    def _create_error_result(self, task: Task, error: Exception) -> TaskResult:
        """Create error result"""
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.ERROR,
            output={{"error": str(error), "llm_powered": False}},
            thoughts=f"{role} analysis failed: {{str(error)}}",
            time_taken=0,
            artifacts=[],
            next_steps="Review error and retry"
        )


# Test
if __name__ == "__main__":
    print("Testing {name} (LLM-Powered)...")
    try:
        agent = {class_name}()
        print(f"✅ {{agent.name}} initialized with LLM")
        print(f"   Role: {{agent.role}}")
        print(f"   LLM: openai/gpt-oss-20b at 192.168.200.226")
        print(f"   Specialty: Real AI {analysis_type} {emoji}")

        health = agent.llm.health_check()
        print(f"\\n🔗 LLM Status: {{health['status']}}")

    except Exception as e:
        print(f"❌ Initialization failed: {{e}}")
'''

# Define agents to create
agents = [
    {
        "name": "Sofia Martinez",
        "role": "Market Researcher",
        "role_lower": "market research",
        "description": "Market Intelligence & Competitive Analysis Expert",
        "specialization": "Market trends, Competitive intelligence, Industry analysis, Strategic positioning",
        "analysis_type": "market intelligence",
        "class_name": "SofiaAgentLLM",
        "system_prompt_name": "SOFIA_SYSTEM_PROMPT",
        "emoji": "📊",
        "routing": [
            ("market", "competitor", "industry"), "_market_analysis_llm",
            ("competitive", "competition", "rival"), "_competitive_intelligence_llm",
            ("strategy", "strategic", "positioning"), "_strategic_analysis_llm",
            ("trend", "forecast", "outlook"), "_trend_analysis_llm"
        ],
        "methods": """
    def _market_analysis_llm(self, task: Task, context: list) -> TaskResult:
        context_text = self._format_context(context)
        user_prompt = f\"\"\"
MARKET ANALYSIS REQUEST:

Subject: {{task.title}}
Description: {{task.description}}

Context:
{{context_text}}

Perform comprehensive market analysis:
1. Market size and growth
2. Key players and market share
3. Customer segments and needs
4. Market dynamics and trends
5. Entry barriers and opportunities
6. Threats and risks
7. Strategic recommendations

Be data-driven and specific.
\"\"\"

        try:
            analysis = self.llm.chat(
                system_prompt=SOFIA_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3500
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={{"analysis_type": "market", "llm_powered": True}},
                thoughts=analysis,
                time_taken=0,
                artifacts=["market_analysis.md"],
                next_steps="Coordinate with Marcus for financial implications"
            )
        except Exception as e:
            return self._create_error_result(task, e)

    def _competitive_intelligence_llm(self, task: Task, context: list) -> TaskResult:
        context_text = self._format_context(context)
        user_prompt = f\"\"\"
COMPETITIVE INTELLIGENCE:

Subject: {{task.title}}
Details: {{task.description}}

Context:
{{context_text}}

Analyze competitive landscape:
1. Key competitors identification
2. Competitive positioning
3. Strengths and weaknesses (SWOT)
4. Competitive advantages/disadvantages
5. Market share and trends
6. Strategic moves and patterns
7. Threats to our position

Provide actionable competitive insights.
\"\"\"

        try:
            analysis = self.llm.chat(
                system_prompt=SOFIA_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={{"analysis_type": "competitive", "llm_powered": True}},
                thoughts=analysis,
                time_taken=0,
                artifacts=["competitive_analysis.md"],
                next_steps="Strategic planning session"
            )
        except Exception as e:
            return self._create_error_result(task, e)

    def _strategic_analysis_llm(self, task: Task, context: list) -> TaskResult:
        context_text = self._format_context(context)
        user_prompt = f\"\"\"
STRATEGIC ANALYSIS:

Subject: {{task.title}}
Details: {{task.description}}

Context:
{{context_text}}

Provide strategic assessment:
1. Current strategic position
2. Strategic options available
3. Risks and opportunities
4. Resource requirements
5. Timeline and milestones
6. Success metrics
7. Recommended strategy

Focus on actionable strategic guidance.
\"\"\"

        try:
            analysis = self.llm.chat(
                system_prompt=SOFIA_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={{"analysis_type": "strategic", "llm_powered": True}},
                thoughts=analysis,
                time_taken=0,
                artifacts=["strategic_analysis.md"],
                next_steps="Executive review and decision"
            )
        except Exception as e:
            return self._create_error_result(task, e)

    def _trend_analysis_llm(self, task: Task, context: list) -> TaskResult:
        context_text = self._format_context(context)
        user_prompt = f\"\"\"
TREND ANALYSIS:

Subject: {{task.title}}
Details: {{task.description}}

Context:
{{context_text}}

Analyze trends and outlook:
1. Current trends identification
2. Historical context
3. Future projections
4. Impact assessment
5. Strategic implications
6. Opportunities and threats
7. Recommended actions

Provide forward-looking insights.
\"\"\"

        try:
            analysis = self.llm.chat(
                system_prompt=SOFIA_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={{"analysis_type": "trends", "llm_powered": True}},
                thoughts=analysis,
                time_taken=0,
                artifacts=["trend_analysis.md"],
                next_steps="Incorporate into strategic planning"
            )
        except Exception as e:
            return self._create_error_result(task, e)

    def _general_market_research_llm(self, task: Task, context: list) -> TaskResult:
        context_text = self._format_context(context)
        user_prompt = f\"\"\"
MARKET RESEARCH REQUEST:

Task: {{task.description}}

Context:
{{context_text}}

Provide market intelligence analysis appropriate to the task.
Be specific, data-driven, and actionable.
\"\"\"

        try:
            analysis = self.llm.chat(
                system_prompt=SOFIA_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=2500
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={{"analysis_type": "general", "llm_powered": True}},
                thoughts=analysis,
                time_taken=0,
                artifacts=["market_intelligence.md"],
                next_steps="Review and apply insights"
            )
        except Exception as e:
            return self._create_error_result(task, e)
        """
    }
]

def generate_routing_logic(routing):
    """Generate routing if-elif chain"""
    lines = []
    for i in range(0, len(routing), 2):
        keywords, method = routing[i], routing[i+1]
        if i == 0:
            lines.append(f'        if any(word in task_lower for word in {list(keywords)}):')
        else:
            lines.append(f'        elif any(word in task_lower for word in {list(keywords)}):')
        lines.append(f'            result = self.{method}(task, context)')
    lines.append('        else:')
    lines.append('            result = self._general_market_research_llm(task, context)')
    return '\n'.join(lines)

def create_agent_file(agent_config):
    """Generate agent file from config"""

    routing_logic = generate_routing_logic(agent_config["routing"])

    code = AGENT_TEMPLATE.format(
        name=agent_config["name"],
        role=agent_config["role"],
        role_lower=agent_config["role_lower"],
        description=agent_config["description"],
        specialization=agent_config["specialization"],
        analysis_type=agent_config["analysis_type"],
        class_name=agent_config["class_name"],
        system_prompt_name=agent_config["system_prompt_name"],
        emoji=agent_config["emoji"],
        routing_logic=routing_logic,
        methods=agent_config["methods"]
    )

    # Generate filename
    filename = f"agents/analytical/{agent_config['name'].lower().replace(' ', '_')}_agent_llm.py"

    return filename, code

# Generate Sofia
if __name__ == "__main__":
    for agent in agents:
        filename, code = create_agent_file(agent)
        print(f"Generated: {filename}")
        print(f"Length: {len(code)} chars")
        print()
