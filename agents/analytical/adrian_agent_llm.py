"""
Adrian Kowalski - Legal Analyst (LLM-Powered)
Legal Research and Compliance Expert

UPGRADE: Uses local LLM at 192.168.200.226 for real legal analysis
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime

# Import LLM client
from src.llm import get_llm_client, ADRIAN_SYSTEM_PROMPT


class AdrianAgentLLM(BaseAgent):
    """
    Adrian Kowalski - Legal Analyst (LLM-Powered)

    Role: Legal Research and Compliance Expert
    Specialization: Legal analysis, Regulatory compliance, Contract analysis,
                   Litigation risk, Criminal law support

    UPGRADE: Real AI legal reasoning instead of templates
    """

    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Adrian Kowalski",
            role="Legal Analyst",
            specialization="Legal research, Regulatory compliance, Contract analysis, Criminal law",
            project_id=project_id
        )

        # Initialize LLM client
        self.llm = get_llm_client()

        # Legal practice areas
        self.practice_areas = [
            "Corporate law", "Contract law", "Regulatory compliance",
            "Criminal law", "Securities law", "Data privacy (GDPR)",
            "Litigation", "International law"
        ]

    def _execute_work(self, task: Task) -> TaskResult:
        """Execute legal analysis work using LLM"""

        start_time = datetime.now()
        task_lower = task.description.lower()

        context = self.load_context(task.description, limit=3)

        # Route to appropriate analysis method (KEEP routing logic)
        if any(word in task_lower for word in ["litigation", "lawsuit", "court", "claim"]):
            result = self._litigation_analysis_llm(task, context)
        elif any(word in task_lower for word in ["compliance", "regulatory", "regulation", "gdpr"]):
            result = self._compliance_analysis_llm(task, context)
        elif any(word in task_lower for word in ["contract", "agreement", "terms"]):
            result = self._contract_review_llm(task, context)
        elif any(word in task_lower for word in ["criminal", "fraud", "violation", "offense"]):
            result = self._criminal_law_analysis_llm(task, context)
        else:
            result = self._general_legal_analysis_llm(task, context)

        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken

        return result

    def _litigation_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """Litigation risk and case assessment using LLM"""

        context_text = self._format_context(context)

        user_prompt = f"""
LITIGATION ANALYSIS REQUEST:

Case/Matter: {task.title}
Details: {task.description}

Previous Context:
{context_text}

Perform comprehensive litigation assessment:

1. CASE STRENGTH ANALYSIS
   - Merits of claims/defenses
   - Legal theories applicable
   - Burden of proof assessment
   - Evidence evaluation

2. PROCEDURAL ANALYSIS
   - Jurisdiction and venue
   - Statute of limitations
   - Standing and capacity
   - Procedural requirements

3. RISK ASSESSMENT
   - Probability of success (plaintiff/defendant perspective)
   - Potential damages/exposure (quantified ranges)
   - Litigation costs estimate
   - Timeline estimate

4. STRATEGIC CONSIDERATIONS
   - Settlement vs trial analysis
   - Discovery risks
   - Reputational impact
   - Precedent implications

5. RECOMMENDATIONS
   - Litigation strategy
   - Settlement parameters
   - Risk mitigation steps
   - Next actions

Be specific, quantify risks, and provide clear strategic recommendations.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=ADRIAN_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "litigation",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["litigation_assessment.md", "risk_quantification.md"],
                next_steps="Coordinate with Marcus for financial exposure analysis"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _compliance_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """Regulatory compliance assessment using LLM"""

        context_text = self._format_context(context)

        user_prompt = f"""
REGULATORY COMPLIANCE ANALYSIS:

Subject: {task.title}
Description: {task.description}

Context:
{context_text}

Perform compliance assessment:

1. APPLICABLE REGULATIONS
   - Primary regulatory frameworks
   - Jurisdictions involved
   - Specific provisions applicable
   - Recent regulatory changes

2. COMPLIANCE STATUS
   - Current compliance level
   - Gaps identified
   - Violations or deficiencies
   - Documentation requirements

3. RISK ASSESSMENT
   - Severity of non-compliance (Critical/High/Medium/Low)
   - Regulatory penalties (fines, sanctions)
   - Operational impact
   - Reputational risk

4. REMEDIATION PLAN
   - Immediate actions required
   - Short-term fixes (< 90 days)
   - Long-term compliance program
   - Monitoring and testing

5. COST-BENEFIT ANALYSIS
   - Cost of compliance
   - Cost of non-compliance
   - Resource requirements
   - Timeline for full compliance

For criminal investigation context: identify potential criminal violations.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=ADRIAN_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3500
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "compliance",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["compliance_report.md", "remediation_plan.md"],
                next_steps="Review with regulatory affairs team"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _contract_review_llm(self, task: Task, context: list) -> TaskResult:
        """Contract analysis using LLM"""

        context_text = self._format_context(context)

        user_prompt = f"""
CONTRACT REVIEW REQUEST:

Contract: {task.title}
Details: {task.description}

Context:
{context_text}

Perform legal contract review:

1. KEY TERMS ANALYSIS
   - Parties and their obligations
   - Performance requirements
   - Payment terms
   - Duration and termination
   - Warranties and representations

2. RISK ASSESSMENT
   - Unfavorable provisions
   - Ambiguous language
   - Missing protections
   - Enforcement risks
   - Jurisdictional issues

3. LIABILITY EXPOSURE
   - Indemnification obligations
   - Limitation of liability
   - Insurance requirements
   - Breach consequences

4. COMPLIANCE REVIEW
   - Regulatory compliance
   - Corporate authority
   - Anti-corruption/bribery
   - Data privacy provisions

5. RECOMMENDATIONS
   - Must-have changes (deal-breakers)
   - Should-have changes (risk reduction)
   - Nice-to-have changes (optimization)
   - Alternative approaches

Provide specific redline suggestions where applicable.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=ADRIAN_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3500
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "contract",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["contract_review.md", "redline_suggestions.md"],
                next_steps="Negotiate terms with counterparty"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _criminal_law_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """Criminal law analysis for prosecutors"""

        context_text = self._format_context(context)

        user_prompt = f"""
CRIMINAL LAW ANALYSIS (PROSECUTOR SUPPORT):

Investigation: {task.title}
Details: {task.description}

Context:
{context_text}

Provide criminal law assessment:

1. POTENTIAL CHARGES
   - Criminal statutes applicable
   - Elements of each offense
   - Degree/classification of crimes
   - Potential enhancements

2. EVIDENCE REQUIREMENTS
   - Elements to prove
   - Burden of proof (beyond reasonable doubt)
   - Evidence strengths
   - Evidence gaps

3. LEGAL THEORIES
   - Direct liability
   - Conspiracy/RICO applicability
   - Aiding and abetting
   - Corporate criminal liability

4. PROCEDURAL CONSIDERATIONS
   - Statute of limitations
   - Jurisdiction
   - Venue
   - Immunity/cooperation issues

5. CASE STRENGTH ASSESSMENT
   - Probability of conviction
   - Potential defenses
   - Weaknesses to address
   - Investigation priorities

6. SENTENCING CONSIDERATIONS
   - Sentencing guidelines range
   - Aggravating/mitigating factors
   - Mandatory minimums
   - Restitution/forfeiture

This is for prosecution. Be thorough and strategic.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=ADRIAN_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "criminal_law",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["criminal_assessment.md", "prosecution_strategy.md"],
                next_steps="Coordinate with Marcus for financial fraud assessment if applicable"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _general_legal_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """General legal intelligence"""

        context_text = self._format_context(context)

        user_prompt = f"""
LEGAL ANALYSIS REQUEST:

Matter: {task.title}
Description: {task.description}

Context:
{context_text}

Provide legal analysis:
1. Legal issues identified
2. Applicable law and precedents
3. Risk assessment
4. Recommended actions
5. Timeline and next steps

Focus on practical, actionable legal guidance.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=ADRIAN_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "general_legal",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["legal_analysis.md"],
                next_steps="Review and implement recommendations"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    # Helper methods

    def _format_context(self, context: list) -> str:
        """Format context for LLM"""
        if not context:
            return "No previous context."
        formatted = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                formatted.append(f"{i}. {ctx.get('content', str(ctx))}")
            else:
                formatted.append(f"{i}. {ctx}")
        return "\n".join(formatted)

    def _create_error_result(self, task: Task, error: Exception) -> TaskResult:
        """Create error result"""
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.ERROR,
            output={"error": str(error), "llm_powered": False},
            thoughts=f"Legal analysis failed: {str(error)}",
            time_taken=0,
            artifacts=[],
            next_steps="Review error and retry"
        )


# Test
if __name__ == "__main__":
    print("Testing Adrian Agent (LLM-Powered)...")
    try:
        adrian = AdrianAgentLLM()
        print(f"✅ {adrian.name} initialized with LLM")
        print(f"   Role: {adrian.role}")
        print(f"   LLM: openai/gpt-oss-20b at 192.168.200.226")
        print(f"   Specialty: Real AI legal intelligence ⚖️")

        health = adrian.llm.health_check()
        print(f"\n🔗 LLM Status: {health['status']}")

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
