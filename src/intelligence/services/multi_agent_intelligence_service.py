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

from ..formatters.data_formatter import (
    format_financial_data,
    calculate_financial_ratios
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
        qdrant_url: str = "http://localhost:6333"
    ):
        """
        Initialize multi-agent intelligence service

        Args:
            llm_base_url: LM Studio API endpoint
            model: Model name
            max_tokens_per_pass: Max tokens for each agent
            use_rag: Enable RAG-enhanced analysis
            qdrant_url: Qdrant server URL
        """
        self.llm = LLMFinancialValidator(base_url=llm_base_url, model=model)
        self.max_tokens = max_tokens_per_pass
        self.use_rag = use_rag

        # Initialize RAG if enabled
        if use_rag:
            from ...rag.rag_service import RAGService
            self.rag = RAGService(qdrant_url=qdrant_url, use_reranker=True)
            logger.info(f"Multi-Agent System with RAG ENABLED (Qdrant: {qdrant_url})")
        else:
            self.rag = None
            logger.info("Multi-Agent System with RAG DISABLED")

        logger.info(f"Multi-Agent Intelligence Service initialized: {model}")
        logger.info("Agents: Financial, Risk, Industry, Strategy, Market, Synthesis")

    def generate_intelligence_report(
        self,
        company_data: Dict[str, Any],
        output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive multi-agent intelligence report

        Args:
            company_data: Dict with company financial data

        Returns:
            Dict with success status, report, and metadata
        """
        start_time = time.time()

        logger.info("=" * 80)
        logger.info(f"MULTI-AGENT INTELLIGENCE REPORT: {company_data['company_name']}")
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

            # Storage for agent results
            agent_results = {}

            # ================================================================
            # AGENT 1: FINANCIAL HEALTH
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("AGENT 1/6: FINANCIAL HEALTH ANALYSIS")
            logger.info("=" * 80)

            agent_results['financial'] = self._run_financial_health_agent(
                company_name, industry, balance_sheet_table,
                income_statement_table, ratios_table, latest_year
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
                balance_sheet_table, latest_year
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
                balance_sheet_table, latest_year
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
                agent_results['industry'], latest_year
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
                agent_results['risk'], latest_year
            )
            logger.info(f"✓ Market Intelligence complete ({len(agent_results['market'])} chars)")

            # ================================================================
            # AGENT 6: SYNTHESIS
            # ================================================================
            logger.info("\n" + "=" * 80)
            logger.info("AGENT 6/6: SYNTHESIS & FINAL RECOMMENDATION")
            logger.info("=" * 80)

            final_report = self._run_synthesis_agent(
                company_name, industry, agent_results
            )
            logger.info(f"✓ Synthesis complete ({len(final_report)} chars)")

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
                        k: len(v) for k, v in agent_results.items()
                    },
                    "rag_enabled": self.use_rag,
                    "llm_provider": "local"
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
        year: Optional[int]
    ) -> str:
        """Run Financial Health Agent"""

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

        return self.llm.chat_completion(messages, max_tokens=self.max_tokens)

    def _run_risk_assessment_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        balance_sheet_table: str,
        year: Optional[int]
    ) -> str:
        """Run Risk Assessment Agent"""

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

        prompt = create_risk_assessment_prompt(
            company_name, industry, financial_summary, balance_sheet_table
        )

        if rag_context:
            prompt += rag_context

        messages = [
            {"role": "system", "content": "You are a risk assessment specialist. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        return self.llm.chat_completion(messages, max_tokens=self.max_tokens)

    def _run_industry_context_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        balance_sheet_table: str,
        year: Optional[int]
    ) -> str:
        """Run Industry Context Agent"""

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

        prompt = create_industry_context_prompt(
            company_name, industry, financial_summary, balance_sheet_table, rag_context
        )

        messages = [
            {"role": "system", "content": "You are a senior industry analyst. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        return self.llm.chat_completion(messages, max_tokens=self.max_tokens)

    def _run_strategic_evaluation_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        industry_context: str,
        year: Optional[int]
    ) -> str:
        """Run Strategic Evaluation Agent"""

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

        prompt = create_strategic_evaluation_prompt(
            company_name, industry, financial_summary, industry_context, rag_context
        )

        messages = [
            {"role": "system", "content": "You are a strategy consultant. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        return self.llm.chat_completion(messages, max_tokens=self.max_tokens)

    def _run_market_intelligence_agent(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        risk_summary: str,
        year: Optional[int]
    ) -> str:
        """Run Market Intelligence Agent"""

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

        prompt = create_market_intelligence_prompt(
            company_name, industry, financial_summary, risk_summary, rag_context
        )

        messages = [
            {"role": "system", "content": "You are a market intelligence analyst. Cite sources when document context is provided."},
            {"role": "user", "content": prompt}
        ]

        return self.llm.chat_completion(messages, max_tokens=self.max_tokens)

    def _run_synthesis_agent(
        self,
        company_name: str,
        industry: str,
        agent_results: Dict[str, str]
    ) -> str:
        """Run Synthesis Agent (Master Orchestrator)"""

        prompt = create_synthesis_prompt(
            company_name=company_name,
            industry=industry,
            financial_analysis=agent_results['financial'],
            risk_analysis=agent_results['risk'],
            industry_analysis=agent_results['industry'],
            strategic_analysis=agent_results['strategy'],
            market_intelligence=agent_results['market']
        )

        messages = [
            {"role": "system", "content": "You are a Chief Investment Officer synthesizing multi-perspective analysis."},
            {"role": "user", "content": prompt}
        ]

        return self.llm.chat_completion(messages, max_tokens=self.max_tokens)
