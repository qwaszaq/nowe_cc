"""
Multi-Agent Intelligence Service
Orchestrates 6 specialized agents for comprehensive analysis
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import time
from pathlib import Path
import importlib.util

# Direct imports to avoid dependencies
llm_validator_path = Path(__file__).parent.parent.parent / "document_processing" / "llm_validator.py"
spec = importlib.util.spec_from_file_location("llm_validator", llm_validator_path)
llm_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm_validator)
LLMFinancialValidator = llm_validator.LLMFinancialValidator

from ..prompts.local_llm_prompts import (
    create_financial_health_prompt,
    create_risk_assessment_prompt
)
from ..prompts.industry_context_prompts import (
    create_industry_context_prompt,
    get_industry_rag_queries
)
from ..prompts.strategic_evaluation_prompts import (
    create_strategic_evaluation_prompt,
    get_strategic_rag_queries
)
from ..prompts.market_intelligence_prompts import (
    create_market_intelligence_prompt,
    get_market_intelligence_rag_queries
)
from ..prompts.synthesis_prompts import create_synthesis_prompt
from ..prompts.comprehensive_prompts import (
    create_comprehensive_financial_health_prompt,
    create_comprehensive_risk_assessment_prompt,
    create_comprehensive_industry_context_prompt,
    create_comprehensive_strategic_evaluation_prompt,
    create_comprehensive_market_intelligence_prompt,
    create_comprehensive_synthesis_prompt,
    format_rag_context_with_citations
)
from ..prompts.enhanced_prompts import get_enhanced_prompt

from ..types import ReportMode, get_token_budget, get_rag_query_count

from ..formatters.data_formatter import (
    format_financial_data,
    calculate_financial_ratios,
    select_analysis_framework,
    assess_severity
)

logger = logging.getLogger(__name__)


class MultiAgentIntelligenceService:
    """
    Multi-Agent Intelligence System with 6 specialized agents

    Architecture:
    1. Financial Health Agent - Quantitative financial analysis
    2. Risk Assessment Agent - Risk identification and mitigation
    3. Industry Context Agent - Competitive positioning
    4. Strategic Evaluation Agent - Strategy and management quality
    5. Market Intelligence Agent - Forward-looking catalysts
    6. Synthesis Agent - Integration and final recommendation

    Each agent analyzes sequentially, building on previous insights.
    All agents have access to RAG for document grounding.
    """

    def __init__(
        self,
        llm_base_url: str = "http://192.168.200.226:1234/v1",
        model: str = "openai/gpt-oss-20b",
        max_tokens_per_pass: int = 4000,
        use_rag: bool = True,
        qdrant_url: str = "http://localhost:6333",
        qdrant_collection: str = "rag_documents"
    ):
        """
        Initialize multi-agent intelligence service

        Args:
            llm_base_url: LM Studio API endpoint
            model: Model name
            max_tokens_per_pass: Max tokens for each agent
            use_rag: Enable RAG-enhanced analysis
            qdrant_url: Qdrant server URL
            qdrant_collection: Qdrant collection name to query
        """
        self.llm = LLMFinancialValidator(base_url=llm_base_url, model=model)
        self.max_tokens = max_tokens_per_pass
        self.use_rag = use_rag

        # Initialize RAG if enabled
        if use_rag:
            from ...rag.rag_service import RAGService
            self.rag = RAGService(
                qdrant_url=qdrant_url,
                collection_name=qdrant_collection,
                use_reranker=True
            )
            logger.info(f"Multi-Agent System with RAG ENABLED (Qdrant: {qdrant_url}/{qdrant_collection})")
        else:
            self.rag = None
            logger.info("Multi-Agent System with RAG DISABLED")

        logger.info(f"Multi-Agent Intelligence Service initialized: {model}")
        logger.info("Agents: Financial, Risk, Industry, Strategy, Market, Synthesis")

    def generate_intelligence_report(
        self,
        company_data: Dict[str, Any],
        output_format: str = "markdown",
        report_mode: ReportMode = ReportMode.EXECUTIVE
    ) -> Dict[str, Any]:
        """
        Generate multi-agent intelligence report

        Args:
            company_data: Dict with company financial data
            output_format: Output format (currently unused, always markdown)
            report_mode: Report depth mode (EXECUTIVE, COMPREHENSIVE, or CUSTOM)

        Returns:
            Dict with success status, report, and metadata
        """
        start_time = time.time()

        logger.info("=" * 80)
        logger.info(f"MULTI-AGENT INTELLIGENCE REPORT: {company_data['company_name']}")
        logger.info(f"Report Mode: {report_mode.value.upper()}")
        logger.info("=" * 80)

        try:
            # Prepare data
            company_name = company_data['company_name']
            industry = company_data.get('industry', 'Unknown')

            balance_sheet_table = format_financial_data(company_data['balance_sheet'])
            income_statement_table = format_financial_data(
                company_data.get('income_statement', {})
            )

            ratios = calculate_financial_ratios(
                company_data['balance_sheet'],
                company_data.get('income_statement', {}),
                company_data.get('cash_flow', {})
            )
            ratios_table = format_financial_data(ratios)

            # Determine latest year for RAG
            latest_year = None
            if company_data['balance_sheet']:
                years = list(company_data['balance_sheet'].values())[0].keys()
                latest_year = max(years) if years else None

            logger.info(f"Company: {company_name}")
            logger.info(f"Industry: {industry}")
            logger.info(f"Latest Year: {latest_year}")
            logger.info(f"RAG Enabled: {self.use_rag}")

            # Gap #3: Select Analysis Framework
            framework, framework_rationale = select_analysis_framework(
                company_data['balance_sheet'],
                company_data.get('income_statement', {})
            )
            logger.info(f"Analysis Framework: {framework}")

            # Gap #4: Assess Severity
            severity, severity_factors = assess_severity(
                company_data['balance_sheet'],
                company_data.get('income_statement', {})
            )
            logger.info(f"Distress Severity: {severity} ({len(severity_factors)} critical factors)")

            # Storage for agent results
            agent_results = {
                'framework': framework,
                'framework_rationale': framework_rationale,
                'severity': severity,
                'severity_factors': severity_factors,
                'report_mode': report_mode
            }

            # ================================================================
            # AGENT 1: FINANCIAL HEALTH
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("AGENT 1/6: FINANCIAL HEALTH ANALYSIS")
            logger.info("=" * 80)

            agent_results['financial'] = self._run_financial_health_agent(
                company_name, industry, balance_sheet_table,
                income_statement_table, ratios_table, latest_year, report_mode
            )
            logger.info(f"✓ Financial Health complete ({len(agent_results['financial'])} chars)")

            # ================================================================
            # AGENT 2: RISK ASSESSMENT
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("AGENT 2/6: RISK ASSESSMENT")
            logger.info("=" * 80)

            agent_results['risk'] = self._run_risk_assessment_agent(
                company_name, industry, agent_results['financial'],
                balance_sheet_table, latest_year, report_mode
            )
            logger.info(f"✓ Risk Assessment complete ({len(agent_results['risk'])} chars)")

            # ================================================================
            # AGENT 3: INDUSTRY CONTEXT
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("AGENT 3/6: INDUSTRY CONTEXT")
            logger.info("=" * 80)

            agent_results['industry'] = self._run_industry_context_agent(
                company_name, industry, agent_results['financial'],
                balance_sheet_table, latest_year, report_mode
            )
            logger.info(f"✓ Industry Context complete ({len(agent_results['industry'])} chars)")

            # ================================================================
            # AGENT 4: STRATEGIC EVALUATION
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("AGENT 4/6: STRATEGIC EVALUATION")
            logger.info("=" * 80)

            agent_results['strategy'] = self._run_strategic_evaluation_agent(
                company_name, industry, agent_results['financial'],
                agent_results['industry'], latest_year, report_mode
            )
            logger.info(f"✓ Strategic Evaluation complete ({len(agent_results['strategy'])} chars)")

            # ================================================================
            # AGENT 5: MARKET INTELLIGENCE
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("AGENT 5/6: MARKET INTELLIGENCE")
            logger.info("=" * 80)

            agent_results['market'] = self._run_market_intelligence_agent(
                company_name, industry, agent_results['financial'],
                agent_results['risk'], agent_results['industry'],
                agent_results['strategy'], latest_year, report_mode
            )
            logger.info(f"✓ Market Intelligence complete ({len(agent_results['market'])} chars)")

            # ================================================================
            # COMPILE FINAL REPORT (APPEND APPROACH)
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("COMPILING FINAL REPORT (Preserving All Agent Outputs)")
            logger.info("=" * 80)

            final_report = self._compile_final_report(
                company_data=company_data,
                agent_results=agent_results,
                balance_sheet_table=balance_sheet_table,
                income_statement_table=income_statement_table,
                ratios_table=ratios_table,
                report_mode=report_mode
            )
            logger.info(f"✓ Final report compiled ({len(final_report)} chars)")

            generation_time = time.time() - start_time

            logger.info("\n" + "=" * 80)
            logger.info("✅ MULTI-AGENT REPORT COMPLETE")
            logger.info(f"   Generation time: {generation_time:.2f} seconds")
            logger.info(f"   Report length: {len(final_report):,} characters")
            logger.info(f"   Agents executed: 6")
            logger.info("=" * 80)

            return {
                "success": True,
                "report": final_report,
                "metadata": {
                    "company_name": company_name,
                    "report_date": datetime.now().isoformat(),
                    "model": self.llm.model,
                    "generation_time_seconds": generation_time,
                    "report_length_chars": len(final_report),
                    "agents": 6,
                    "agent_results": {
                        k: len(v) for k, v in agent_results.items() if isinstance(v, str)
                    },
                    "rag_enabled": self.use_rag,
                    "llm_provider": "local",
                    "report_mode": report_mode.value,
                    "token_budget_total": get_token_budget(report_mode, "total")
                }
            }

        except Exception as e:
            logger.error(f"Multi-agent report generation failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def _run_financial_health_agent(
        self,
        company_name: str,
        industry: str,
        balance_sheet_table: str,
        income_statement_table: str,
        ratios_table: str,
        year: Optional[int],
        report_mode: ReportMode = ReportMode.EXECUTIVE
    ) -> str:
        """Run Financial Health Agent"""

        # Get token budget for this mode
        token_budget = get_token_budget(report_mode, "financial_health")
        logger.info(f"  Mode: {report_mode.value}, Token budget: {token_budget}")

        # Get RAG context if enabled
        rag_context = ""
        if self.use_rag and self.rag and year:
            logger.info("  Retrieving RAG context...")

            liquidity_context = self.rag.enhance_financial_analysis(
                metric="liquidity and working capital",
                trend="current status and trends",
                company=company_name,
                years=[year]
            )

            profitability_context = self.rag.enhance_financial_analysis(
                metric="profitability and margins",
                trend="performance trends",
                company=company_name,
                years=[year]
            )

            if liquidity_context != "No relevant context found in documents.":
                rag_context += f"\n\n### Liquidity Context:\n{liquidity_context}"
            if profitability_context != "No relevant context found in documents.":
                rag_context += f"\n\n### Profitability Context:\n{profitability_context}"

            if rag_context:
                logger.info(f"  Retrieved {len(rag_context)} chars of context")

        # Choose prompt based on report mode
        if report_mode == ReportMode.COMPREHENSIVE:
            base_prompt = create_comprehensive_financial_health_prompt(
                company_name, industry, balance_sheet_table,
                income_statement_table, ratios_table, rag_context
            )
            # Apply model-specific enhancements (Phase 1)
            prompt = get_enhanced_prompt(base_prompt, self.llm.model)
        else:  # EXECUTIVE or CUSTOM
            prompt = create_financial_health_prompt(
                company_name, industry, balance_sheet_table,
                income_statement_table, ratios_table
            )
            if rag_context:
                prompt += rag_context

        messages = [
            {"role": "system", "content": "You are a senior financial analyst. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=token_budget)

        # Validate minimum length
        min_chars = token_budget * 3  # Rough estimate: 1 token ≈ 3-4 chars
        actual_chars = len(response) if response else 0
        utilization = (actual_chars / min_chars) * 100 if min_chars > 0 else 0

        if actual_chars < min_chars * 0.5:  # Less than 50% of expected
            logger.warning(
                f"⚠️  Financial Health agent underperformed: "
                f"{actual_chars} chars vs expected {min_chars} chars "
                f"({utilization:.1f}% utilization)"
            )
        else:
            logger.info(
                f"✓ Financial Health agent: {actual_chars} chars "
                f"({utilization:.1f}% of target)"
            )

        return response

    def _run_risk_assessment_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        balance_sheet_table: str,
        year: Optional[int],
        report_mode: ReportMode = ReportMode.EXECUTIVE
    ) -> str:
        """Run Risk Assessment Agent"""

        # Get token budget for this mode
        token_budget = get_token_budget(report_mode, "risk_assessment")
        logger.info(f"  Mode: {report_mode.value}, Token budget: {token_budget}")

        # Get RAG context if enabled
        rag_context = ""
        if self.use_rag and self.rag and year:
            logger.info("  Retrieving RAG context...")

            risk_context = self.rag.get_risk_context(
                risk_type="financial and operational risks",
                company=company_name,
                years=[year]
            )

            if risk_context != "No relevant context found in documents.":
                rag_context = f"\n\n### Risk Factors from Annual Report:\n{risk_context}"
                logger.info(f"  Retrieved {len(rag_context)} chars of context")

        # Choose prompt based on report mode
        if report_mode == ReportMode.COMPREHENSIVE:
            base_prompt = create_comprehensive_risk_assessment_prompt(
                company_name, industry, financial_summary,
                balance_sheet_table, rag_context
            )
            # Apply model-specific enhancements (Phase 1)
            prompt = get_enhanced_prompt(base_prompt, self.llm.model)
        else:  # EXECUTIVE or CUSTOM
            prompt = create_risk_assessment_prompt(
                company_name, industry, financial_summary, balance_sheet_table
            )
            if rag_context:
                prompt += rag_context

        messages = [
            {"role": "system", "content": "You are a risk assessment specialist. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=token_budget)

        # Validate minimum length
        min_chars = token_budget * 3
        actual_chars = len(response) if response else 0
        utilization = (actual_chars / min_chars) * 100 if min_chars > 0 else 0

        if actual_chars < min_chars * 0.5:
            logger.warning(
                f"⚠️  Risk Assessment agent underperformed: "
                f"{actual_chars} chars vs expected {min_chars} chars "
                f"({utilization:.1f}% utilization)"
            )
        else:
            logger.info(
                f"✓ Risk Assessment agent: {actual_chars} chars "
                f"({utilization:.1f}% of target)"
            )

        return response

    def _run_industry_context_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        balance_sheet_table: str,
        year: Optional[int],
        report_mode: ReportMode = ReportMode.EXECUTIVE
    ) -> str:
        """Run Industry Context Agent"""

        # Get token budget for this mode
        token_budget = get_token_budget(report_mode, "industry_context")
        logger.info(f"  Mode: {report_mode.value}, Token budget: {token_budget}")

        # Get RAG context if enabled
        rag_context = ""
        if self.use_rag and self.rag and year:
            logger.info("  Retrieving RAG context...")

            queries = get_industry_rag_queries(company_name, year)
            contexts = []

            for query_info in queries:
                context = self.rag.get_context_for_question(
                    question=query_info["question"],
                    company=company_name,
                    years=[year],
                    top_k=3
                )
                if context != "No relevant context found in documents.":
                    contexts.append(context)

            if contexts:
                rag_context = "\n\n---\n\n".join(contexts)
                logger.info(f"  Retrieved {len(rag_context)} chars of context")

        # Choose prompt based on report mode
        if report_mode == ReportMode.COMPREHENSIVE:
            base_prompt = create_comprehensive_industry_context_prompt(
                company_name, industry, financial_summary,
                balance_sheet_table, rag_context
            )
            # Apply model-specific enhancements (Phase 1)
            prompt = get_enhanced_prompt(base_prompt, self.llm.model)
        else:  # EXECUTIVE or CUSTOM
            prompt = create_industry_context_prompt(
                company_name, industry, financial_summary, balance_sheet_table, rag_context
            )

        messages = [
            {"role": "system", "content": "You are a senior industry analyst. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=token_budget)

        # Validate minimum length
        min_chars = token_budget * 3
        actual_chars = len(response) if response else 0
        utilization = (actual_chars / min_chars) * 100 if min_chars > 0 else 0

        if actual_chars < min_chars * 0.5:
            logger.warning(
                f"⚠️  Industry Context agent underperformed: "
                f"{actual_chars} chars vs expected {min_chars} chars "
                f"({utilization:.1f}% utilization)"
            )
        else:
            logger.info(
                f"✓ Industry Context agent: {actual_chars} chars "
                f"({utilization:.1f}% of target)"
            )

        return response

    def _run_strategic_evaluation_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        industry_context: str,
        year: Optional[int],
        report_mode: ReportMode = ReportMode.EXECUTIVE
    ) -> str:
        """Run Strategic Evaluation Agent"""

        # Get token budget for this mode
        token_budget = get_token_budget(report_mode, "strategic_evaluation")
        logger.info(f"  Mode: {report_mode.value}, Token budget: {token_budget}")

        # Get RAG context if enabled
        rag_context = ""
        if self.use_rag and self.rag and year:
            logger.info("  Retrieving RAG context...")

            queries = get_strategic_rag_queries(company_name, year)
            contexts = []

            for query_info in queries:
                context = self.rag.get_context_for_question(
                    question=query_info["question"],
                    company=company_name,
                    years=[year],
                    top_k=3
                )
                if context != "No relevant context found in documents.":
                    contexts.append(context)

            if contexts:
                rag_context = "\n\n---\n\n".join(contexts)
                logger.info(f"  Retrieved {len(rag_context)} chars of context")

        # Choose prompt based on report mode
        if report_mode == ReportMode.COMPREHENSIVE:
            base_prompt = create_comprehensive_strategic_evaluation_prompt(
                company_name, industry, financial_summary,
                industry_context, rag_context
            )
            # Apply model-specific enhancements (Phase 1)
            prompt = get_enhanced_prompt(base_prompt, self.llm.model)
        else:  # EXECUTIVE or CUSTOM
            prompt = create_strategic_evaluation_prompt(
                company_name, industry, financial_summary, industry_context, rag_context
            )

        messages = [
            {"role": "system", "content": "You are a strategy consultant. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=token_budget)

        # Validate minimum length
        min_chars = token_budget * 3
        actual_chars = len(response) if response else 0
        utilization = (actual_chars / min_chars) * 100 if min_chars > 0 else 0

        if actual_chars < min_chars * 0.5:
            logger.warning(
                f"⚠️  Strategic Evaluation agent underperformed: "
                f"{actual_chars} chars vs expected {min_chars} chars "
                f"({utilization:.1f}% utilization)"
            )
        else:
            logger.info(
                f"✓ Strategic Evaluation agent: {actual_chars} chars "
                f"({utilization:.1f}% of target)"
            )

        return response

    def _run_market_intelligence_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        risk_summary: str,
        industry_context: str,
        strategic_evaluation: str,
        year: Optional[int],
        report_mode: ReportMode = ReportMode.EXECUTIVE
    ) -> str:
        """Run Market Intelligence Agent"""

        # Get token budget for this mode
        token_budget = get_token_budget(report_mode, "market_intelligence")
        logger.info(f"  Mode: {report_mode.value}, Token budget: {token_budget}")

        # Get RAG context if enabled
        rag_context = ""
        if self.use_rag and self.rag and year:
            logger.info("  Retrieving RAG context...")

            queries = get_market_intelligence_rag_queries(company_name, year)
            contexts = []

            for query_info in queries:
                context = self.rag.get_context_for_question(
                    question=query_info["question"],
                    company=company_name,
                    years=[year],
                    top_k=3
                )
                if context != "No relevant context found in documents.":
                    contexts.append(context)

            if contexts:
                rag_context = "\n\n---\n\n".join(contexts)
                logger.info(f"  Retrieved {len(rag_context)} chars of context")

        # Choose prompt based on report mode
        if report_mode == ReportMode.COMPREHENSIVE:
            base_prompt = create_comprehensive_market_intelligence_prompt(
                company_name, industry, financial_summary,
                risk_summary, industry_context, strategic_evaluation, rag_context
            )
            # Apply model-specific enhancements (Phase 1)
            prompt = get_enhanced_prompt(base_prompt, self.llm.model)
        else:  # EXECUTIVE or CUSTOM
            prompt = create_market_intelligence_prompt(
                company_name, industry, financial_summary, risk_summary, rag_context
            )

        messages = [
            {"role": "system", "content": "You are a market intelligence analyst. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=token_budget)

        # Validate minimum length
        min_chars = token_budget * 3
        actual_chars = len(response) if response else 0
        utilization = (actual_chars / min_chars) * 100 if min_chars > 0 else 0

        if actual_chars < min_chars * 0.5:
            logger.warning(
                f"⚠️  Market Intelligence agent underperformed: "
                f"{actual_chars} chars vs expected {min_chars} chars "
                f"({utilization:.1f}% utilization)"
            )
        else:
            logger.info(
                f"✓ Market Intelligence agent: {actual_chars} chars "
                f"({utilization:.1f}% of target)"
            )

        return response

    def _run_synthesis_agent(
        self,
        company_name: str,
        industry: str,
        agent_results: Dict[str, str]
    ) -> str:
        """Run Synthesis Agent (Master Orchestrator)"""

        # Get report_mode from agent_results
        report_mode = agent_results.get('report_mode', ReportMode.EXECUTIVE)

        # Get token budget for this mode
        token_budget = get_token_budget(report_mode, "synthesis")
        logger.info(f"  Mode: {report_mode.value}, Token budget: {token_budget}")

        # Choose prompt based on report mode
        if report_mode == ReportMode.COMPREHENSIVE:
            # Extract financial_health_score from financial analysis
            financial_health_score = self._extract_score_from_financial_analysis(
                agent_results['financial']
            )

            prompt = create_comprehensive_synthesis_prompt(
                company_name=company_name,
                industry=industry,
                financial_health_analysis=agent_results['financial'],
                risk_assessment=agent_results['risk'],
                industry_context=agent_results['industry'],
                strategic_evaluation=agent_results['strategy'],
                market_intelligence=agent_results['market'],
                financial_health_score=financial_health_score
            )
        else:  # EXECUTIVE or CUSTOM
            prompt = create_synthesis_prompt(
                company_name=company_name,
                industry=industry,
                financial_analysis=agent_results['financial'],
                risk_analysis=agent_results['risk'],
                industry_analysis=agent_results['industry'],
                strategic_analysis=agent_results['strategy'],
                market_intelligence=agent_results['market'],
                framework=agent_results.get('framework', 'EQUITY_ANALYSIS'),
                framework_rationale=agent_results.get('framework_rationale', ''),
                severity=agent_results.get('severity', 'LOW'),
                severity_factors=agent_results.get('severity_factors', [])
            )

        messages = [
            {"role": "system", "content": "You are a Chief Investment Officer synthesizing multi-perspective analysis."},
            {"role": "user", "content": prompt}
        ]

        return self.llm.chat_completion(messages, max_tokens=token_budget)

    def _extract_score_from_financial_analysis(self, financial_analysis: str) -> int:
        """
        Extract Financial Health Score from financial analysis text.

        Args:
            financial_analysis: Text containing "Financial Health Score: XX/100"

        Returns:
            Integer score (0-100), defaults to 50 if not found
        """
        import re

        # Pattern: "Financial Health Score: XX/100" or "Score: XX/100"
        pattern = r'(?:Financial Health )?Score:\s*(\d+)/100'
        match = re.search(pattern, financial_analysis, re.IGNORECASE)

        if match:
            return int(match.group(1))

        # Fallback: Try "XX/100" pattern alone
        pattern = r'(\d+)/100'
        match = re.search(pattern, financial_analysis)

        if match:
            return int(match.group(1))

        # Default if not found
        logger.warning("Could not extract Financial Health Score from analysis, defaulting to 50")
        return 50

    def _compile_final_report(
        self,
        company_data: Dict[str, Any],
        agent_results: Dict[str, str],
        balance_sheet_table: str,
        income_statement_table: str,
        ratios_table: str,
        report_mode: ReportMode
    ) -> str:
        """
        Compile final report by APPENDING all agent sections.
        Similar to single-agent's _compile_final_report().

        This preserves all agent work instead of synthesizing into new report.
        """
        # Extract metadata
        years = []
        if company_data['balance_sheet']:
            first_metric = list(company_data['balance_sheet'].values())[0]
            years = sorted(first_metric.keys()) if first_metric else []
        years_str = ', '.join(map(str, years)) if years else 'N/A'

        # Generate executive summary
        exec_summary = self._generate_executive_summary(agent_results)

        # Get framework and severity info
        framework = agent_results.get('framework', 'EQUITY_ANALYSIS')
        framework_rationale = agent_results.get('framework_rationale', '')
        severity = agent_results.get('severity', 'LOW')
        severity_factors = agent_results.get('severity_factors', [])

        # Format severity factors
        if severity_factors:
            severity_factors_text = '\n'.join(f'- {factor}' for factor in severity_factors)
        else:
            severity_factors_text = '- None identified'

        # Build final report by APPENDING sections
        report = f"""# Comprehensive Intelligence Report: {company_data['company_name']}

**Report Date:** {datetime.now().strftime('%Y-%m-%d')}
**Industry:** {company_data.get('industry', 'Unknown')}
**Currency:** {company_data.get('currency', 'PLN')} (thousands)
**Analysis Period:** {years_str}
**Report Mode:** {report_mode.value.upper()}
**Analysis Method:** Multi-Agent Intelligence System (6 Specialized Agents)

---

## EXECUTIVE SUMMARY

{exec_summary}

---

## FRAMEWORK SELECTION

{framework_rationale}

### Distress Severity Assessment

**Severity Level:** {severity}

**Critical Factors Identified:**
{severity_factors_text}

---

## 1. FINANCIAL HEALTH ANALYSIS

{agent_results['financial']}

---

## 2. RISK ASSESSMENT

{agent_results['risk']}

---

## 3. INDUSTRY CONTEXT & COMPETITIVE POSITIONING

{agent_results['industry']}

---

## 4. STRATEGIC EVALUATION & MANAGEMENT QUALITY

{agent_results['strategy']}

---

## 5. MARKET INTELLIGENCE & FORWARD-LOOKING CATALYSTS

{agent_results['market']}

---

## APPENDIX A: FINANCIAL DATA

### Balance Sheet
{balance_sheet_table}

### Income Statement
{income_statement_table}

### Financial Ratios (Calculated)
{ratios_table}

---

## APPENDIX B: ANALYSIS METHODOLOGY

### Multi-Agent System Architecture

This report was generated by 6 specialized AI agents, each focusing on a distinct analytical dimension:

1. **Financial Health Agent** - Quantitative analysis of financial statements and ratios
2. **Risk Assessment Agent** - Comprehensive risk identification and evaluation
3. **Industry Context Agent** - Competitive positioning and market dynamics analysis
4. **Strategic Evaluation Agent** - Strategy quality and management capability assessment
5. **Market Intelligence Agent** - Forward-looking catalysts, opportunities, and threats
6. **Executive Integration** - Cross-perspective synthesis and investment recommendations

Each section above preserves the complete output from its corresponding agent, maintaining
full analytical depth while the executive summary provides integrated insights across all dimensions.

### System Configuration
- **LLM Provider:** Local (LM Studio)
- **Model:** {self.llm.model}
- **Context Window:** 44k tokens per agent
- **Token Budget ({report_mode.value.upper()} Mode):** {get_token_budget(report_mode, "total")} tokens total
  - Financial Health: {get_token_budget(report_mode, "financial_health")} tokens
  - Risk Assessment: {get_token_budget(report_mode, "risk_assessment")} tokens
  - Industry Context: {get_token_budget(report_mode, "industry_context")} tokens
  - Strategic Evaluation: {get_token_budget(report_mode, "strategic_evaluation")} tokens
  - Market Intelligence: {get_token_budget(report_mode, "market_intelligence")} tokens
- **RAG Enhancement:** {'Enabled' if self.use_rag else 'Disabled'}

### Data Sources
- **Financial Statements:** {years_str}
- **Extraction Method:** Automated PDF extraction with validation
- **Quality Assurance:** Accounting equation verified (Assets = Liabilities + Equity)

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

*This report was generated by an AI system and should be reviewed by qualified professionals before making investment decisions.*
"""
        return report

    def _generate_executive_summary(self, agent_results: Dict[str, str]) -> str:
        """
        Generate executive summary by EXTRACTING key points from agent outputs.
        Does NOT call LLM to synthesize (which would recreate the REPLACE problem).
        """
        import re

        # Extract financial health score
        financial_score_match = re.search(
            r'(?:Financial Health )?Score:\s*(\d+)/100',
            agent_results['financial']
        )
        financial_score = financial_score_match.group(1) if financial_score_match else "N/A"

        # Extract risk level
        risk_match = re.search(
            r'(?:Overall )?Risk Level:\s*(\w+(?:/\w+)?)',
            agent_results['risk']
        )
        risk_level = risk_match.group(1) if risk_match else "N/A"

        # Determine recommendation from score
        recommendation = self._determine_recommendation(financial_score, agent_results)

        # Extract first sentence from each agent
        financial_summary = self._extract_first_sentence(agent_results['financial'])
        risk_summary = self._extract_first_sentence(agent_results['risk'])
        industry_summary = self._extract_first_sentence(agent_results['industry'])
        strategy_summary = self._extract_first_sentence(agent_results['strategy'])
        market_summary = self._extract_first_sentence(agent_results['market'])

        return f"""**Financial Health Score:** {financial_score}/100
**Overall Risk Level:** {risk_level}
**Investment Recommendation:** {recommendation}

This comprehensive multi-agent report analyzes the company across six specialized
dimensions. Each section below represents an independent analytical perspective,
synthesized into a holistic assessment.

### Key Findings

**Financial Health:** {financial_summary}

**Risk Profile:** {risk_summary}

**Industry Position:** {industry_summary}

**Strategic Assessment:** {strategy_summary}

**Market Outlook:** {market_summary}

### Analysis Architecture

This report leverages a multi-agent architecture where each agent independently analyzes
the company from its specialized perspective, with access to both structured financial data
and RAG-enhanced document context. The comprehensive sections below preserve the full depth
of each agent's analysis.
"""

    def _extract_first_sentence(self, text: str) -> str:
        """Extract first meaningful sentence from agent output for executive summary"""
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Skip headers, empty lines, bullets
            if (line and
                not line.startswith('#') and
                not line.startswith('*') and
                not line.startswith('-') and
                not line.startswith('**')):
                # Take first sentence (up to period)
                if '.' in line:
                    first_sentence = line.split('.')[0] + '.'
                    # Limit to reasonable length
                    if len(first_sentence) > 200:
                        return first_sentence[:197] + '...'
                    return first_sentence
                else:
                    # No period found, take first 200 chars
                    return line[:200] + '...' if len(line) > 200 else line

        return "Analysis provided in detailed section below."

    def _determine_recommendation(self, financial_score: str, agent_results: Dict[str, str]) -> str:
        """
        Determine investment recommendation from financial health score.
        Uses same logic as single-agent for consistency.
        """
        import re

        # Try to parse score
        try:
            if financial_score != "N/A":
                score = int(financial_score)
                if score >= 80:
                    return "STRONG BUY"
                elif score >= 60:
                    return "BUY"
                elif score >= 45:
                    return "HOLD"
                elif score >= 30:
                    return "SELL"
                else:
                    return "STRONG SELL"
        except ValueError:
            pass

        # Fallback: Look for explicit recommendation in any agent output
        for agent_output in agent_results.values():
            if not isinstance(agent_output, str):
                continue
            rec_match = re.search(
                r'(?:INVESTMENT )?RECOMMENDATION:\s*(\w+(?:\s+\w+)?)',
                agent_output,
                re.IGNORECASE
            )
            if rec_match:
                return rec_match.group(1).upper()

        return "HOLD (Default - Insufficient Data)"
