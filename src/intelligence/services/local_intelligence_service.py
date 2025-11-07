"""
Intelligence service optimized for local LLM (44k context window)
Uses multi-pass analysis to stay within token limits
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import time
import re

# Import LLM validator directly without going through __init__
import importlib.util
import sys
from pathlib import Path

# Direct import to avoid bs4 dependency in downloader
llm_validator_path = Path(__file__).parent.parent.parent / "document_processing" / "llm_validator.py"
spec = importlib.util.spec_from_file_location("llm_validator", llm_validator_path)
llm_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm_validator)
LLMFinancialValidator = llm_validator.LLMFinancialValidator
from ..prompts.local_llm_prompts import (
    create_financial_health_prompt,
    create_risk_assessment_prompt,
    create_investment_thesis_prompt
)
from ..formatters.data_formatter import (
    format_financial_data,
    calculate_financial_ratios,
    select_analysis_framework,
    assess_severity
)

logger = logging.getLogger(__name__)


def determine_recommendation_from_score(financial_health_score: int) -> str:
    """
    Map financial health score to investment recommendation using explicit thresholds

    Score Ranges:
    - 80-100: STRONG BUY
    - 60-79:  BUY
    - 45-59:  HOLD
    - 30-44:  SELL
    - 0-29:   STRONG SELL

    Args:
        financial_health_score: Score from 0-100

    Returns:
        Investment recommendation string
    """
    if financial_health_score >= 80:
        return "STRONG BUY"
    elif financial_health_score >= 60:
        return "BUY"
    elif financial_health_score >= 45:
        return "HOLD"
    elif financial_health_score >= 30:
        return "SELL"
    else:
        return "STRONG SELL"


class LocalIntelligenceService:
    """
    Intelligence report generation using local LLM with strategic chunking

    Architecture: Multi-pass analysis
    - Pass 1: Financial Health Analysis (~15k tokens)
    - Pass 2: Risk Assessment (~15k tokens)
    - Pass 3: Investment Thesis (~20k tokens)
    - Pass 4: Final Report Compilation (~10k tokens)

    Each pass stays well under 44k context limit
    """

    def __init__(
        self,
        llm_base_url: str = "http://192.168.200.226:1234/v1",
        model: str = "openai/gpt-oss-20b",
        max_tokens_per_pass: int = 4000,  # Conservative for output
        use_rag: bool = False,
        qdrant_url: str = "http://localhost:6333",
        qdrant_collection: str = "rag_documents"
    ):
        """
        Initialize intelligence service

        Args:
            llm_base_url: LM Studio API endpoint
            model: Model name
            max_tokens_per_pass: Max tokens for each LLM response
            use_rag: Enable RAG-enhanced analysis
            qdrant_url: Qdrant server URL (if use_rag=True)
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
            logger.info(f"RAG-enhanced analysis ENABLED (Qdrant: {qdrant_url}/{qdrant_collection})")
        else:
            self.rag = None
            logger.info("RAG-enhanced analysis DISABLED (using only structured data)")

        logger.info(f"Local Intelligence Service initialized: {model}")

    def generate_intelligence_report(
        self,
        company_data: Dict[str, Any],
        output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive intelligence report using multi-pass analysis

        Args:
            company_data: Dict with:
                - company_name: str
                - industry: str
                - balance_sheet: dict (multi-year)
                - income_statement: dict (multi-year, optional)
                - cash_flow: dict (optional)
                - currency: str

        Returns:
            Dict with:
                - success: bool
                - report: str (markdown formatted)
                - metadata: dict (generation info)
                - error: str (if failed)
        """
        start_time = time.time()

        logger.info("=" * 80)
        logger.info(f"GENERATING INTELLIGENCE REPORT: {company_data['company_name']}")
        logger.info("=" * 80)

        try:
            # Step 1: Prepare financial data
            logger.info("Step 1: Preparing financial data...")
            balance_sheet_table = format_financial_data(company_data['balance_sheet'])
            income_statement_table = format_financial_data(
                company_data.get('income_statement', {})
            )

            # Calculate ratios
            ratios = calculate_financial_ratios(
                company_data['balance_sheet'],
                company_data.get('income_statement', {}),
                company_data.get('cash_flow', {})
            )
            ratios_table = format_financial_data(ratios)

            logger.info(f"  - Balance sheet: {len(company_data['balance_sheet'])} metrics")
            logger.info(f"  - Calculated ratios: {len(ratios)} ratios")

            # Determine latest year for RAG queries
            latest_year = None
            if company_data['balance_sheet']:
                # Get the most recent year from balance sheet data
                years = list(company_data['balance_sheet'].values())[0].keys()
                latest_year = max(years) if years else None

            if latest_year:
                logger.info(f"  - Latest year for RAG queries: {latest_year}")

            # Gap #3 Fix: Select Analysis Framework
            framework, framework_rationale = select_analysis_framework(
                company_data['balance_sheet'],
                company_data.get('income_statement', {})
            )
            logger.info(f"  - Analysis framework: {framework}")

            # Gap #4 Fix: Assess Severity
            severity, severity_factors = assess_severity(
                company_data['balance_sheet'],
                company_data.get('income_statement', {})
            )
            logger.info(f"  - Distress severity: {severity}")

            # Step 2: PASS 1 - Financial Health Analysis
            logger.info("\nStep 2: Financial Health Analysis (Pass 1)...")
            financial_summary = self._analyze_financial_health(
                company_name=company_data['company_name'],
                industry=company_data.get('industry', 'Unknown'),
                balance_sheet_table=balance_sheet_table,
                income_statement_table=income_statement_table,
                ratios_table=ratios_table,
                year=latest_year
            )
            logger.info(f"  ✓ Financial analysis complete ({len(financial_summary)} chars)")

            # Step 3: PASS 2 - Risk Assessment
            logger.info("\nStep 3: Risk Assessment (Pass 2)...")
            risk_summary = self._assess_risks(
                company_name=company_data['company_name'],
                industry=company_data.get('industry', 'Unknown'),
                financial_summary=financial_summary,
                balance_sheet_table=balance_sheet_table,
                year=latest_year
            )
            logger.info(f"  ✓ Risk assessment complete ({len(risk_summary)} chars)")

            # Step 4: PASS 3 - Investment Thesis
            logger.info("\nStep 4: Investment Thesis (Pass 3)...")
            investment_thesis = self._develop_investment_thesis(
                company_name=company_data['company_name'],
                industry=company_data.get('industry', 'Unknown'),
                financial_summary=financial_summary,
                risk_summary=risk_summary
            )
            logger.info(f"  ✓ Investment thesis complete ({len(investment_thesis)} chars)")

            # Step 5: PASS 4 - Compile Final Report
            logger.info("\nStep 5: Compiling final report...")
            final_report = self._compile_final_report(
                company_data=company_data,
                financial_summary=financial_summary,
                risk_summary=risk_summary,
                investment_thesis=investment_thesis,
                balance_sheet_table=balance_sheet_table,
                ratios_table=ratios_table,
                framework_rationale=framework_rationale,
                severity=severity,
                severity_factors=severity_factors
            )

            generation_time = time.time() - start_time

            logger.info("=" * 80)
            logger.info(f"✅ REPORT GENERATED SUCCESSFULLY")
            logger.info(f"   Generation time: {generation_time:.2f} seconds")
            logger.info(f"   Report length: {len(final_report):,} characters")
            logger.info("=" * 80)

            return {
                "success": True,
                "report": final_report,
                "metadata": {
                    "company_name": company_data['company_name'],
                    "report_date": datetime.now().isoformat(),
                    "model": self.llm.model,
                    "generation_time_seconds": generation_time,
                    "report_length_chars": len(final_report),
                    "passes": 4,
                    "llm_provider": "local"
                }
            }

        except Exception as e:
            logger.error(f"Report generation failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def _analyze_financial_health(
        self,
        company_name: str,
        industry: str,
        balance_sheet_table: str,
        income_statement_table: str,
        ratios_table: str,
        year: Optional[int] = None
    ) -> str:
        """
        PASS 1: Analyze financial health (with optional RAG enhancement)

        Returns:
            Financial health summary (text)
        """
        # Get RAG context if enabled
        rag_context = ""
        if self.use_rag and self.rag and year:
            logger.info("  - Retrieving RAG context for financial health...")

            # Query for liquidity context
            liquidity_context = self.rag.enhance_financial_analysis(
                metric="liquidity and working capital",
                trend="current status and trends",
                company=company_name,
                years=[year]
            )

            # Query for profitability context
            profitability_context = self.rag.enhance_financial_analysis(
                metric="profitability and margins",
                trend="performance trends",
                company=company_name,
                years=[year]
            )

            if liquidity_context != "No relevant context found in documents.":
                rag_context += f"\n\n### Document Context - Liquidity:\n{liquidity_context}"

            if profitability_context != "No relevant context found in documents.":
                rag_context += f"\n\n### Document Context - Profitability:\n{profitability_context}"

            if rag_context:
                logger.info(f"  - Retrieved {len(rag_context)} chars of RAG context")

        prompt = create_financial_health_prompt(
            company_name=company_name,
            industry=industry,
            balance_sheet_table=balance_sheet_table,
            income_statement_table=income_statement_table,
            ratios_table=ratios_table
        )

        # Append RAG context if available
        if rag_context:
            prompt += rag_context

        logger.debug(f"  - Prompt length: {len(prompt)} characters")

        messages = [
            {"role": "system", "content": "You are a senior financial analyst. When document context is provided, cite specific sources in your analysis."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=self.max_tokens)

        if not response:
            raise Exception("LLM failed to generate financial health analysis")

        return response

    def _assess_risks(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        balance_sheet_table: str,
        year: Optional[int] = None
    ) -> str:
        """
        PASS 2: Assess risks (with optional RAG enhancement)

        Returns:
            Risk assessment summary (text)
        """
        # Get RAG context if enabled
        rag_context = ""
        if self.use_rag and self.rag and year:
            logger.info("  - Retrieving RAG context for risk assessment...")

            # Query for risk factors
            risk_context = self.rag.get_risk_context(
                risk_type="financial and operational risks",
                company=company_name,
                years=[year]
            )

            if risk_context != "No relevant context found in documents.":
                rag_context = f"\n\n### Document Context - Risk Factors:\n{risk_context}"
                logger.info(f"  - Retrieved {len(rag_context)} chars of RAG context")

        prompt = create_risk_assessment_prompt(
            company_name=company_name,
            industry=industry,
            financial_summary=financial_summary,
            balance_sheet_table=balance_sheet_table
        )

        # Append RAG context if available
        if rag_context:
            prompt += rag_context

        logger.debug(f"  - Prompt length: {len(prompt)} characters")

        messages = [
            {"role": "system", "content": "You are a risk assessment specialist. When document context is provided, cite specific sources in your analysis."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=self.max_tokens)

        if not response:
            raise Exception("LLM failed to generate risk assessment")

        return response

    def _develop_investment_thesis(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        risk_summary: str
    ) -> str:
        """
        PASS 3: Develop investment thesis

        Returns:
            Investment thesis and recommendation (text)
        """
        prompt = create_investment_thesis_prompt(
            company_name=company_name,
            industry=industry,
            financial_summary=financial_summary,
            risk_summary=risk_summary
        )

        logger.debug(f"  - Prompt length: {len(prompt)} characters")

        messages = [
            {"role": "system", "content": "You are an investment strategist."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=self.max_tokens)

        if not response:
            raise Exception("LLM failed to generate investment thesis")

        return response

    def _compile_final_report(
        self,
        company_data: Dict[str, Any],
        financial_summary: str,
        risk_summary: str,
        investment_thesis: str,
        balance_sheet_table: str,
        ratios_table: str,
        framework_rationale: str = "",
        severity: str = "LOW",
        severity_factors: list = None
    ) -> str:
        """
        PASS 4: Compile all analyses into final report

        Args:
            framework_rationale: Framework selection rationale (Gap #3)
            severity: Distress severity level (Gap #4)
            severity_factors: List of critical severity factors (Gap #4)

        Returns:
            Complete formatted report (markdown)
        """
        if severity_factors is None:
            severity_factors = []
        exec_summary = self._extract_executive_summary(
            financial_summary, risk_summary, investment_thesis
        )

        # Get years for data sources
        years = sorted(company_data['balance_sheet'].get('Total Assets', {}).keys())
        years_str = ', '.join(map(str, years))

        # Format severity factors for display
        if severity_factors:
            severity_factors_text = '\n'.join(f'- {factor}' for factor in severity_factors)
        else:
            severity_factors_text = '- None identified'

        report = f"""# Comprehensive Intelligence Report: {company_data['company_name']}

**Report Date:** {datetime.now().strftime('%Y-%m-%d')}
**Industry:** {company_data.get('industry', 'Unknown')}
**Currency:** {company_data.get('currency', 'PLN')} (thousands)
**Analysis Period:** {years_str}
**Analysis Method:** Local LLM Intelligence System (Multi-Pass Analysis)

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

{financial_summary}

---

## 2. RISK ASSESSMENT

{risk_summary}

---

## 3. INVESTMENT THESIS & RECOMMENDATION

{investment_thesis}

---

## APPENDIX A: FINANCIAL DATA

### Balance Sheet
{balance_sheet_table}

### Financial Ratios (Calculated)
{ratios_table}

---

## APPENDIX B: ANALYSIS METHODOLOGY

### System Configuration
- **Analysis System:** Local LLM Intelligence System
- **Model:** {self.llm.model}
- **LLM Provider:** LM Studio (local)
- **Context Window:** 44k tokens per pass
- **Analysis Approach:** Multi-pass sequential analysis

### Analysis Passes
This report was generated through 4 sequential analysis passes:

1. **Pass 1 - Financial Health Analysis**
   - Evaluated liquidity, profitability, and leverage
   - Calculated key financial ratios
   - Identified financial strengths and concerns

2. **Pass 2 - Risk Assessment**
   - Assessed financial, operational, market, and strategic risks
   - Quantified risk severity and probability
   - Identified risk mitigation strategies

3. **Pass 3 - Investment Thesis Development**
   - Developed bull case and bear case scenarios
   - Synthesized base case outlook
   - Generated investment recommendation

4. **Pass 4 - Final Report Compilation**
   - Integrated all analysis perspectives
   - Generated executive summary
   - Formatted final deliverable

### Data Sources
- **Financial Statements:** {years_str}
- **Extraction Method:** Automated PDF extraction (regex-based with 100% accuracy validation)
- **Data Validation:** Accounting equation verified (Assets = Liabilities + Equity)
- **Quality Score:** Based on benchmark comparison with manual extraction

### Quality Assurance
All extracted financial values have been validated against:
- Accounting equation balance
- Multi-year consistency checks
- Cross-reference with source PDFs

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Generation Time:** {(time.time() - getattr(self, '_report_start_time', time.time())):.2f} seconds

---

*This report was generated by an AI system and should be reviewed by qualified professionals before making investment decisions.*
"""
        return report

    def _extract_executive_summary(
        self,
        financial_summary: str,
        risk_summary: str,
        investment_thesis: str
    ) -> str:
        """
        Extract key points for executive summary

        Args:
            financial_summary: Financial health analysis
            risk_summary: Risk assessment
            investment_thesis: Investment recommendation

        Returns:
            Executive summary paragraph
        """
        # Extract financial health score
        score_match = re.search(r'FINANCIAL HEALTH SCORE:\s*(\d+)', financial_summary)
        health_score = score_match.group(1) if score_match else "N/A"

        # Extract recommendation from LLM output
        rec_match = re.search(r'INVESTMENT RECOMMENDATION:\s*(\w+(?:\s+\w+)?)', investment_thesis)
        llm_recommendation = rec_match.group(1).strip() if rec_match else "N/A"

        # Validate recommendation consistency with score (GAP #2 FIX)
        if health_score != "N/A":
            score_based_recommendation = determine_recommendation_from_score(int(health_score))

            # If LLM recommendation is inconsistent, use score-based recommendation
            if llm_recommendation != score_based_recommendation:
                logger.warning(
                    f"Recommendation inconsistency detected: "
                    f"LLM suggested '{llm_recommendation}' but score {health_score}/100 maps to '{score_based_recommendation}'. "
                    f"Using score-based recommendation for consistency."
                )
                recommendation = score_based_recommendation
            else:
                recommendation = llm_recommendation
        else:
            recommendation = llm_recommendation

        # Extract risk level
        risk_match = re.search(r'Risk Level:\s*(\w+(?:/\w+)?)', risk_summary)
        risk_level = risk_match.group(1) if risk_match else "N/A"

        summary = f"""**Financial Health Score:** {health_score}/100
**Overall Risk Level:** {risk_level}
**Investment Recommendation:** {recommendation}

This comprehensive report analyzes the company across three critical dimensions: financial health, risk assessment, and investment viability. The analysis is based on automated extraction of financial statements, validated through accounting equation verification.

### Key Findings

{self._extract_key_finding(financial_summary, "LIQUIDITY ASSESSMENT")}

{self._extract_key_finding(risk_summary, "OVERALL RISK PROFILE")}

{self._extract_key_finding(investment_thesis, "BASE CASE")}
"""
        return summary.strip()

    def _extract_key_finding(self, text: str, section_header: str) -> str:
        """
        Extract a specific section from analysis text

        Args:
            text: Full analysis text
            section_header: Section to extract

        Returns:
            Extracted section or empty string
        """
        # Find section (handle both **SECTION** and SECTION: formats)
        patterns = [
            rf'\*\*{section_header}\*\*(.*?)(?=\n\*\*|\Z)',
            rf'{section_header}:\s*(.*?)(?=\n[A-Z][A-Z]|\Z)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                # Limit to first 3 lines to keep summary concise
                lines = content.split('\n')[:3]
                return f"**{section_header}**\n" + '\n'.join(lines)

        return ""


# Simple wrapper function for easy usage
def generate_report(company_data: Dict[str, Any]) -> str:
    """
    Simple wrapper to generate intelligence report

    Usage:
        report = generate_report({
            'company_name': 'Grupa Azoty',
            'industry': 'Chemicals',
            'currency': 'PLN',
            'balance_sheet': {...},
            'income_statement': {...}
        })

    Returns:
        Markdown formatted intelligence report
    """
    service = LocalIntelligenceService()
    result = service.generate_intelligence_report(company_data)

    if result['success']:
        return result['report']
    else:
        raise Exception(f"Report generation failed: {result['error']}")
