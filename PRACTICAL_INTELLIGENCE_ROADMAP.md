# Practical Intelligence System Roadmap
## Using Existing Infrastructure & Local LLM

**Constraints:**
- ✅ Use existing system (PostgreSQL + local file storage)
- ✅ Local LLM only (openai/gpt-oss-20b, 44k context window)
- ✅ Local data only (manually provided financial data + PDFs)
- ✅ No external APIs (no Yahoo Finance, NewsAPI, etc.)
- ✅ No new databases (no ChromaDB, no Neo4j - reuse what you have)

**Current Assets:**
- ✅ Financial extraction system (regex-based, 100% accuracy)
- ✅ E5 embeddings (via LM Studio)
- ✅ Local LLM (openai/gpt-oss-20b via LM Studio)
- ✅ PDF parsing (pdfplumber, Camelot)
- ✅ File storage system

**Timeline:** 6-8 weeks to production-ready system
**Effort:** 50-70 hours total

---

# 🎯 REVISED PRIORITY RANKING

## Priority 1: Single-Agent Intelligence Engine (Week 1-2)
**Effort:** 12-15 hours | **Risk:** Low | **Value:** High

**What You're Building:**
A Python script that takes extracted financial data and generates a 5-10 page analyst report using your local LLM.

**Key Innovation:**
Given 44k context limit, we'll use **strategic chunking** - analyze in phases, accumulate findings.

---

## Priority 2: Multi-Year Extraction Pipeline (Week 3)
**Effort:** 6-8 hours | **Risk:** Low | **Value:** High

**What You're Building:**
Extract financial data from multiple years of PDFs, build time-series datasets.

**Storage:**
Store in JSON files (simple, no new DB needed).

---

## Priority 3: PDF Text RAG (Simple Version) (Week 4-5)
**Effort:** 10-12 hours | **Risk:** Low | **Value:** Medium

**What You're Building:**
Simple RAG using E5 embeddings + local file-based vector storage (no Qdrant needed).

**Storage:**
- Embeddings: NumPy arrays saved to disk
- Index: Simple JSON file mapping chunk IDs to metadata
- Search: In-memory cosine similarity (fast enough for single-company analysis)

---

## Priority 4: Multi-Perspective Analysis (Simulated Multi-Agent) (Week 6-8)
**Effort:** 20-25 hours | **Risk:** Medium | **Value:** Very High

**What You're Building:**
Sequential multi-perspective analysis (simulate agents) within 44k token budget.

**Architecture:**
Instead of parallel agents, **sequential specialist perspectives** that accumulate knowledge.

---

# 📋 DETAILED IMPLEMENTATION PLAN

---

# PRIORITY 1: Single-Agent Intelligence Engine

## Architecture: Strategic Chunking for 44k Context Window

**Problem:** 44k tokens is ~33,000 words. A full intelligence report needs more context.

**Solution:** Multi-pass analysis with accumulation:
```
Pass 1: Financial Health Analysis (15k tokens used)
  └─> Output: Financial health summary (2k tokens)

Pass 2: Risk Assessment (15k tokens used)
  └─> Input: Financial health summary
  └─> Output: Risk assessment (2k tokens)

Pass 3: Investment Thesis (20k tokens used)
  └─> Input: Financial summary + Risk summary + Raw data
  └─> Output: Investment recommendation (3k tokens)

Pass 4: Final Report Compilation (10k tokens used)
  └─> Input: All summaries
  └─> Output: Complete formatted report
```

Each pass stays well under 44k limit, and accumulates knowledge.

---

## Week 1: Core Engine Implementation

### Day 1-2: Prompt Engineering Framework

**File: `src/intelligence/prompts/local_llm_prompts.py`**

```python
"""
Prompts optimized for local LLM (44k context window)
"""

# System prompts for different analysis perspectives
FINANCIAL_ANALYST_SYSTEM = """You are a senior financial analyst with 20 years of experience analyzing European industrial companies, specializing in the chemicals and materials sector.

Your analysis is known for:
- Precise ratio calculations and trend identification
- Clear identification of financial strengths and weaknesses
- Evidence-based conclusions citing specific numbers
- Professional, balanced assessments

You provide actionable insights for investment decision-makers."""

RISK_ANALYST_SYSTEM = """You are a risk assessment specialist focusing on corporate financial and operational risks.

Your expertise includes:
- Credit risk evaluation (default probability, refinancing risk)
- Operational risk assessment (supply chain, production, market)
- Risk quantification (severity, probability, impact)
- Risk mitigation strategies

You identify both obvious and subtle risk factors."""

INVESTMENT_STRATEGIST_SYSTEM = """You are an investment strategist who synthesizes financial and risk analysis into actionable investment recommendations.

Your recommendations:
- Balance bull case and bear case scenarios
- Provide clear BUY/HOLD/SELL guidance with rationale
- Identify key monitoring points
- Consider both short-term and long-term perspectives

You help decision-makers make informed choices."""


def create_financial_health_prompt(
    company_name: str,
    industry: str,
    balance_sheet_table: str,
    income_statement_table: str,
    ratios_table: str
) -> str:
    """
    Create prompt for financial health analysis

    Args:
        company_name: Company name
        industry: Industry sector
        balance_sheet_table: Formatted balance sheet markdown table
        income_statement_table: Formatted income statement table
        ratios_table: Calculated financial ratios table

    Returns:
        Prompt string optimized for 44k window
    """
    return f"""
{FINANCIAL_ANALYST_SYSTEM}

## ASSIGNMENT

Analyze the financial health of {company_name} ({industry}) and provide a structured assessment.

---

## FINANCIAL DATA

### Balance Sheet (in thousands PLN)
{balance_sheet_table}

### Income Statement (in thousands PLN)
{income_statement_table}

### Calculated Financial Ratios
{ratios_table}

---

## ANALYSIS REQUIREMENTS

Provide a comprehensive financial health assessment covering:

### 1. LIQUIDITY ANALYSIS
- Evaluate current ratio, quick ratio, working capital
- Assess ability to meet short-term obligations
- Identify any liquidity concerns or strengths
- Trend: Is liquidity improving, stable, or deteriorating?

### 2. PROFITABILITY ANALYSIS
- Evaluate ROE, ROA, net margin trends
- Assess profit generation efficiency
- Compare to typical industry benchmarks (if known)
- Identify profitability drivers or concerns

### 3. LEVERAGE ANALYSIS
- Assess debt-to-equity ratio
- Evaluate refinancing risk
- Determine financial risk level (Low/Medium/High)
- Identify any solvency concerns

### 4. OVERALL FINANCIAL HEALTH SCORE
Provide a score from 0-100 where:
- 85-100: Excellent financial health
- 70-84: Good financial health
- 50-69: Adequate but concerning
- 30-49: Weak financial health
- 0-29: Critical financial distress

### 5. KEY FINDINGS
- Top 3 Financial Strengths (with specific data)
- Top 3 Financial Concerns (with specific data)
- Critical Red Flags (if any)

---

## OUTPUT FORMAT

Use this exact structure:

**FINANCIAL HEALTH SCORE: [0-100]/100**

**LIQUIDITY ASSESSMENT**
Status: [Strong/Adequate/Weak]
Key Metrics: [cite specific ratios]
Trend: [improving/stable/declining over time period]
Analysis: [2-3 sentences explaining liquidity position]

**PROFITABILITY ASSESSMENT**
Status: [Strong/Adequate/Weak]
Key Metrics: [cite specific ratios]
Trend: [improving/stable/declining]
Analysis: [2-3 sentences on profitability drivers]

**LEVERAGE ASSESSMENT**
Status: [Low/Medium/High Risk]
Key Metrics: [cite debt ratios]
Analysis: [2-3 sentences on debt burden and solvency]

**TOP 3 STRENGTHS**
1. [Specific strength with supporting numbers]
2. [Specific strength with supporting numbers]
3. [Specific strength with supporting numbers]

**TOP 3 CONCERNS**
1. [Specific concern with supporting numbers]
2. [Specific concern with supporting numbers]
3. [Specific concern with supporting numbers]

**RED FLAGS** (if any)
- [Critical issues requiring immediate attention]

Be specific, cite exact numbers, and provide clear assessments.
""".strip()


def create_risk_assessment_prompt(
    company_name: str,
    industry: str,
    financial_summary: str,
    balance_sheet_table: str
) -> str:
    """
    Create prompt for risk assessment

    Args:
        company_name: Company name
        industry: Industry sector
        financial_summary: Output from financial health analysis
        balance_sheet_table: Balance sheet data

    Returns:
        Risk assessment prompt
    """
    return f"""
{RISK_ANALYST_SYSTEM}

## ASSIGNMENT

Assess the key risks facing {company_name} ({industry}) based on financial data and industry context.

---

## CONTEXT

### Financial Health Summary (from previous analysis)
{financial_summary}

### Balance Sheet Data
{balance_sheet_table}

---

## RISK ASSESSMENT REQUIREMENTS

Identify and evaluate risks across four categories:

### 1. FINANCIAL RISKS
- Liquidity risk (ability to meet short-term obligations)
- Credit risk (default probability)
- Refinancing risk (debt maturity, covenant compliance)
- Currency/commodity exposure (if applicable)

### 2. OPERATIONAL RISKS
- Production disruptions
- Supply chain vulnerabilities
- Key person dependencies
- Technological obsolescence

### 3. MARKET RISKS
- Industry cyclicality (chemical/fertilizer sector volatility)
- Competitive pressure
- Commodity price exposure
- Regulatory changes (EU environmental rules, etc.)

### 4. STRATEGIC RISKS
- Execution risk on growth plans
- M&A integration risk
- Capital allocation missteps

---

## OUTPUT FORMAT

For each risk category, provide:

**[RISK CATEGORY]**

Top Risks:
1. [Risk name] - Severity: [High/Medium/Low] | Probability: [High/Medium/Low]
   Impact: [Describe potential impact]
   Mitigation: [Existing or recommended mitigation strategies]

2. [Risk name] - Severity: [High/Medium/Low] | Probability: [High/Medium/Low]
   Impact: [Describe potential impact]
   Mitigation: [Existing or recommended mitigation strategies]

[Continue for all significant risks in category]

**OVERALL RISK PROFILE**
Summary: [2-3 sentences summarizing overall risk exposure]
Risk Level: [Low/Medium/High/Critical]
Key Monitoring Points: [What to watch going forward]

Be specific about risk triggers, quantify impact where possible, and provide actionable mitigation strategies.
""".strip()


def create_investment_thesis_prompt(
    company_name: str,
    industry: str,
    financial_summary: str,
    risk_summary: str,
    current_price: str = "N/A"
) -> str:
    """
    Create prompt for investment thesis and recommendation

    Args:
        company_name: Company name
        industry: Industry sector
        financial_summary: Financial health analysis output
        risk_summary: Risk assessment output
        current_price: Current stock price (if available)

    Returns:
        Investment thesis prompt
    """
    return f"""
{INVESTMENT_STRATEGIST_SYSTEM}

## ASSIGNMENT

Develop an investment thesis and provide a clear recommendation for {company_name} ({industry}).

---

## CONTEXT

### Financial Health Analysis
{financial_summary}

### Risk Assessment
{risk_summary}

### Market Context
Current Stock Price: {current_price}
Industry: {industry}

---

## INVESTMENT THESIS REQUIREMENTS

Develop a balanced investment perspective:

### 1. BULL CASE (Best Case Scenario)
What are the 3-5 strongest arguments for investing?
- Specific financial strengths
- Growth opportunities
- Competitive advantages
- Positive catalysts

### 2. BEAR CASE (Worst Case Scenario)
What are the 3-5 strongest arguments against investing?
- Financial weaknesses
- Key risks
- Competitive threats
- Negative catalysts

### 3. BASE CASE (Most Likely Outcome)
Given the bull and bear arguments, what's the most realistic scenario?
- Expected financial trajectory
- Likelihood of risks materializing
- Balanced probability assessment

### 4. INVESTMENT RECOMMENDATION
Clear guidance: BUY | HOLD | SELL
- Recommendation rationale (2-3 sentences)
- Key factors supporting this recommendation
- What would change your recommendation? (triggers to revisit)

### 5. KEY MONITORING POINTS
What metrics/events should be monitored going forward?
- Financial metrics to track
- Industry developments to watch
- Risk triggers that would require reassessment

---

## OUTPUT FORMAT

**BULL CASE: Why This Could Be a Good Investment**
1. [Strong positive argument with supporting evidence]
2. [Strong positive argument with supporting evidence]
3. [Strong positive argument with supporting evidence]
[Add 4-5 if applicable]

**BEAR CASE: Why This Could Be a Poor Investment**
1. [Strong negative argument with supporting evidence]
2. [Strong negative argument with supporting evidence]
3. [Strong negative argument with supporting evidence]
[Add 4-5 if applicable]

**BASE CASE: Most Likely Outcome**
[3-4 sentences describing the balanced, most probable scenario]

**INVESTMENT RECOMMENDATION: [BUY/HOLD/SELL]**
Rationale: [Clear explanation of recommendation based on bull/bear/base analysis]
Confidence Level: [High/Medium/Low]
Time Horizon: [Short-term (6-12 months) / Long-term (2+ years)]

**KEY MONITORING POINTS**
1. [Metric or event to monitor]
2. [Metric or event to monitor]
3. [Metric or event to monitor]

**TRIGGERS FOR REASSESSMENT**
- Upgrade to BUY if: [conditions]
- Downgrade to SELL if: [conditions]

Provide clear, actionable guidance backed by evidence from financial and risk analysis.
""".strip()
```

**Deliverable:** `src/intelligence/prompts/local_llm_prompts.py`

---

### Day 3-4: Intelligence Service with Multi-Pass Analysis

**File: `src/intelligence/services/local_intelligence_service.py`**

```python
"""
Intelligence service optimized for local LLM (44k context window)
Uses multi-pass analysis to stay within token limits
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import time

from ...document_processing.llm_validator import LLMFinancialValidator
from ..prompts.local_llm_prompts import (
    create_financial_health_prompt,
    create_risk_assessment_prompt,
    create_investment_thesis_prompt
)
from ..formatters.data_formatter import (
    format_financial_data,
    calculate_financial_ratios
)

logger = logging.getLogger(__name__)


class LocalIntelligenceService:
    """
    Intelligence report generation using local LLM with strategic chunking
    """

    def __init__(
        self,
        llm_base_url: str = "http://192.168.200.226:1234/v1",
        model: str = "openai/gpt-oss-20b",
        max_tokens_per_pass: int = 4000  # Conservative for 44k context
    ):
        """
        Initialize intelligence service

        Args:
            llm_base_url: LM Studio API endpoint
            model: Model name
            max_tokens_per_pass: Max tokens for each LLM response
        """
        self.llm = LLMFinancialValidator(base_url=llm_base_url, model=model)
        self.max_tokens = max_tokens_per_pass

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
                - income_statement: dict (multi-year)
                - cash_flow: dict (optional)
                - currency: str

        Returns:
            Dict with success, report, metadata
        """
        start_time = time.time()

        logger.info(f"=== GENERATING INTELLIGENCE REPORT: {company_data['company_name']} ===")

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

            # Step 2: PASS 1 - Financial Health Analysis
            logger.info("Step 2: Financial Health Analysis (Pass 1)...")
            financial_summary = self._analyze_financial_health(
                company_name=company_data['company_name'],
                industry=company_data.get('industry', 'Unknown'),
                balance_sheet_table=balance_sheet_table,
                income_statement_table=income_statement_table,
                ratios_table=ratios_table
            )

            # Step 3: PASS 2 - Risk Assessment
            logger.info("Step 3: Risk Assessment (Pass 2)...")
            risk_summary = self._assess_risks(
                company_name=company_data['company_name'],
                industry=company_data.get('industry', 'Unknown'),
                financial_summary=financial_summary,
                balance_sheet_table=balance_sheet_table
            )

            # Step 4: PASS 3 - Investment Thesis
            logger.info("Step 4: Investment Thesis (Pass 3)...")
            investment_thesis = self._develop_investment_thesis(
                company_name=company_data['company_name'],
                industry=company_data.get('industry', 'Unknown'),
                financial_summary=financial_summary,
                risk_summary=risk_summary
            )

            # Step 5: PASS 4 - Compile Final Report
            logger.info("Step 5: Compiling final report...")
            final_report = self._compile_final_report(
                company_data=company_data,
                financial_summary=financial_summary,
                risk_summary=risk_summary,
                investment_thesis=investment_thesis,
                balance_sheet_table=balance_sheet_table,
                ratios_table=ratios_table
            )

            generation_time = time.time() - start_time

            logger.info(f"✅ Report generated in {generation_time:.2f} seconds")

            return {
                "success": True,
                "report": final_report,
                "metadata": {
                    "company_name": company_data['company_name'],
                    "report_date": datetime.now().isoformat(),
                    "model": self.llm.model,
                    "generation_time_seconds": generation_time,
                    "report_length_chars": len(final_report),
                    "passes": 4
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
        ratios_table: str
    ) -> str:
        """
        PASS 1: Analyze financial health

        Returns:
            Financial health summary (text)
        """
        prompt = create_financial_health_prompt(
            company_name=company_name,
            industry=industry,
            balance_sheet_table=balance_sheet_table,
            income_statement_table=income_statement_table,
            ratios_table=ratios_table
        )

        messages = [
            {"role": "system", "content": "You are a senior financial analyst."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=self.max_tokens)

        if not response:
            raise Exception("LLM failed to generate financial health analysis")

        logger.info(f"Financial health analysis: {len(response)} characters")
        return response

    def _assess_risks(
        self,
        company_name: str,
        industry: str,
        financial_summary: str,
        balance_sheet_table: str
    ) -> str:
        """
        PASS 2: Assess risks

        Returns:
            Risk assessment summary (text)
        """
        prompt = create_risk_assessment_prompt(
            company_name=company_name,
            industry=industry,
            financial_summary=financial_summary,
            balance_sheet_table=balance_sheet_table
        )

        messages = [
            {"role": "system", "content": "You are a risk assessment specialist."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=self.max_tokens)

        if not response:
            raise Exception("LLM failed to generate risk assessment")

        logger.info(f"Risk assessment: {len(response)} characters")
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

        messages = [
            {"role": "system", "content": "You are an investment strategist."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.chat_completion(messages, max_tokens=self.max_tokens)

        if not response:
            raise Exception("LLM failed to generate investment thesis")

        logger.info(f"Investment thesis: {len(response)} characters")
        return response

    def _compile_final_report(
        self,
        company_data: Dict[str, Any],
        financial_summary: str,
        risk_summary: str,
        investment_thesis: str,
        balance_sheet_table: str,
        ratios_table: str
    ) -> str:
        """
        PASS 4: Compile all analyses into final report

        Returns:
            Complete formatted report (markdown)
        """
        report = f"""
# Comprehensive Intelligence Report: {company_data['company_name']}

**Report Date:** {datetime.now().strftime('%Y-%m-%d')}
**Industry:** {company_data.get('industry', 'Unknown')}
**Currency:** {company_data.get('currency', 'PLN')} (thousands)
**Analysis Method:** Local LLM Intelligence System

---

## EXECUTIVE SUMMARY

{self._extract_executive_summary(financial_summary, risk_summary, investment_thesis)}

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

## APPENDIX

### Balance Sheet Data
{balance_sheet_table}

### Financial Ratios (Calculated)
{ratios_table}

### Analysis Methodology
- **System:** Local LLM Intelligence System
- **Model:** {self.llm.model}
- **Analysis Approach:** Multi-pass sequential analysis (4 passes)
- **Context Window:** 44k tokens per pass
- **Passes:**
  1. Financial Health Analysis
  2. Risk Assessment
  3. Investment Thesis Development
  4. Final Report Compilation

### Data Sources
- Financial statements: {', '.join(map(str, sorted(company_data['balance_sheet'].get('Total Assets', {}).keys())))}
- Extraction method: Automated PDF extraction (regex-based)
- Validation: Accounting equation verified

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
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
        import re
        score_match = re.search(r'FINANCIAL HEALTH SCORE:\s*(\d+)', financial_summary)
        health_score = score_match.group(1) if score_match else "N/A"

        # Extract recommendation
        rec_match = re.search(r'INVESTMENT RECOMMENDATION:\s*(\w+)', investment_thesis)
        recommendation = rec_match.group(1) if rec_match else "N/A"

        # Build summary
        summary = f"""
**Financial Health Score:** {health_score}/100
**Investment Recommendation:** {recommendation}

This report provides a comprehensive analysis across three dimensions: financial health, risk assessment, and investment thesis. The analysis is based on automated extraction of financial statements and ratios, evaluated through specialized analytical perspectives.

{self._extract_key_finding(financial_summary, "LIQUIDITY ASSESSMENT")}

{self._extract_key_finding(risk_summary, "OVERALL RISK PROFILE")}

{self._extract_key_finding(investment_thesis, "INVESTMENT RECOMMENDATION")}
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
        import re

        # Find section
        pattern = rf'\*\*{section_header}\*\*(.*?)(?=\n\*\*|\Z)'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            return f"**{section_header}**{match.group(1).strip()}"

        return ""
```

**Deliverable:** `src/intelligence/services/local_intelligence_service.py`

---

### Day 5: Test Script

**File: `scripts/test_local_intelligence.py`**

```python
"""
Test local intelligence system with Grupa Azoty 2023 data
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.intelligence.services.local_intelligence_service import LocalIntelligenceService


def test_azoty_intelligence_report():
    """
    Generate intelligence report for Grupa Azoty using local LLM
    """
    print("=" * 80)
    print("TESTING LOCAL INTELLIGENCE SYSTEM")
    print("=" * 80)

    # Company data (from your extraction system)
    company_data = {
        "company_name": "Grupa Azoty S.A.",
        "industry": "Chemicals & Fertilizers",
        "currency": "PLN",

        # Balance sheet (June 30, 2023) - from LOCAL_EXTRACTION_RESULTS_2023.md
        "balance_sheet": {
            "Total Assets": {2023: 26019865},
            "Current Assets": {2023: 7904016},
            "Fixed Assets": {2023: 18115849},  # Derived
            "Total Equity": {2023: 8795144},
            "Total Liabilities": {2023: 17224721},
            "Current Liabilities": {2023: 11330491},
            "Long-term Liabilities": {2023: 5894230},  # Derived
            "Cash & Equivalents": {2023: 1405681},
            "Inventories": {2023: 2605887}
        },

        # Income statement (would extract from PDF in real usage)
        "income_statement": {
            # Placeholder - you'd extract this from actual PDFs
            # For now, empty dict
        },

        # Cash flow (would extract from PDF)
        "cash_flow": {}
    }

    # Initialize service
    print("\nInitializing Local Intelligence Service...")
    service = LocalIntelligenceService(
        llm_base_url="http://192.168.200.226:1234/v1",
        model="openai/gpt-oss-20b",
        max_tokens_per_pass=4000
    )

    # Generate report
    print("\nGenerating intelligence report...\n")
    result = service.generate_intelligence_report(company_data)

    if result['success']:
        print("\n✅ REPORT GENERATED SUCCESSFULLY\n")
        print(f"Generation time: {result['metadata']['generation_time_seconds']:.2f} seconds")
        print(f"Report length: {result['metadata']['report_length_chars']:,} characters")
        print(f"Passes: {result['metadata']['passes']}")

        # Save report
        output_dir = Path("output/intelligence_reports")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"Azoty_Intelligence_Local_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['report'])

        print(f"\n✅ Full report saved to: {output_path}")

        # Preview
        print("\n" + "=" * 80)
        print("REPORT PREVIEW (first 3000 chars):")
        print("=" * 80)
        print(result['report'][:3000])
        print("\n[...truncated...]\n")

    else:
        print("\n❌ REPORT GENERATION FAILED")
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    from datetime import datetime
    test_azoty_intelligence_report()
```

**Deliverable:** Working intelligence report generator using local LLM

---

## Week 2: Validation & Enhancement

### Day 6-10: Quality Validation & Iteration

**Tasks:**
1. Generate report for Grupa Azoty 2023
2. Manually review quality
3. Iterate on prompts (improve clarity, structure)
4. Add more financial statement extraction (income statement, cash flow)
5. Test multi-year support

**Deliverable:** Production-quality single-agent reports

---

# PRIORITY 2: Multi-Year Extraction Pipeline

## Week 3: Time-Series Data Extraction

### Simple JSON-Based Storage (No New DB)

**File: `src/data/multi_year_storage.py`**

```python
"""
Simple JSON-based storage for multi-year financial data
No database needed - just JSON files
"""

import json
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class MultiYearDataStore:
    """
    Store multi-year financial data in JSON files
    """

    def __init__(self, storage_dir: str = "data/companies"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_company_data(
        self,
        company_name: str,
        years_data: Dict[int, Dict[str, float]]
    ):
        """
        Save multi-year data for a company

        Args:
            company_name: Company name (sanitized for filename)
            years_data: {
                2023: {'Total Assets': 26019865, ...},
                2022: {'Total Assets': 25000000, ...}
            }
        """
        # Sanitize company name for filename
        safe_name = company_name.lower().replace(" ", "_").replace(".", "")

        filepath = self.storage_dir / f"{safe_name}.json"

        # Load existing if present
        if filepath.exists():
            with open(filepath, 'r') as f:
                existing = json.load(f)
        else:
            existing = {
                "company_name": company_name,
                "data": {}
            }

        # Merge new data
        for year, data in years_data.items():
            existing["data"][str(year)] = data

        # Save
        with open(filepath, 'w') as f:
            json.dump(existing, f, indent=2)

        logger.info(f"Saved data for {company_name}: {len(years_data)} years")

    def load_company_data(self, company_name: str) -> Dict[int, Dict[str, float]]:
        """
        Load multi-year data for a company

        Returns:
            {2023: {'Total Assets': 26019865, ...}, 2022: {...}}
        """
        safe_name = company_name.lower().replace(" ", "_").replace(".", "")
        filepath = self.storage_dir / f"{safe_name}.json"

        if not filepath.exists():
            logger.warning(f"No data found for {company_name}")
            return {}

        with open(filepath, 'r') as f:
            stored = json.load(f)

        # Convert year keys back to ints
        data = {}
        for year_str, year_data in stored.get("data", {}).items():
            data[int(year_str)] = year_data

        return data
```

**Usage:**
```python
# Save extracted data
store = MultiYearDataStore()
store.save_company_data("Grupa Azoty", {
    2023: extracted_2023_data,
    2022: extracted_2022_data,
    2021: extracted_2021_data
})

# Load for analysis
multi_year_data = store.load_company_data("Grupa Azoty")
```

**Deliverable:** Simple multi-year data persistence (no new DB)

---

# PRIORITY 3: Simple File-Based RAG (No Qdrant)

## Week 4-5: Lightweight RAG with E5 Embeddings

### Architecture: NumPy + JSON (No Vector DB)

**File: `src/rag/simple_rag.py`**

```python
"""
Simple file-based RAG using E5 embeddings
No Qdrant/ChromaDB - just NumPy arrays and JSON
"""

import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import logging

from ..document_processing.semantic_matcher import E5SemanticMatcher

logger = logging.getLogger(__name__)


class SimpleRAG:
    """
    File-based RAG system using E5 embeddings stored as NumPy arrays
    """

    def __init__(self, storage_dir: str = "data/rag_storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.embedder = E5SemanticMatcher()

        # In-memory cache
        self.embeddings_cache = {}
        self.metadata_cache = {}

    def ingest_document(
        self,
        company: str,
        year: int,
        text_chunks: List[str],
        metadata_list: List[Dict]
    ):
        """
        Ingest document chunks

        Args:
            company: Company name
            year: Year
            text_chunks: List of text chunks
            metadata_list: List of metadata dicts (one per chunk)
        """
        logger.info(f"Ingesting {len(text_chunks)} chunks for {company} ({year})")

        # Create embeddings
        embeddings = []
        for chunk in text_chunks:
            emb = self.embedder.embed_text(f"passage: {chunk}")
            if emb is not None:
                embeddings.append(emb)
            else:
                embeddings.append(np.zeros(1024))  # Fallback

        embeddings_array = np.array(embeddings)

        # Save to disk
        doc_id = f"{company.lower().replace(' ', '_')}_{year}"

        # Save embeddings (NumPy binary format)
        emb_path = self.storage_dir / f"{doc_id}_embeddings.npy"
        np.save(emb_path, embeddings_array)

        # Save metadata (JSON)
        metadata_path = self.storage_dir / f"{doc_id}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump({
                "company": company,
                "year": year,
                "chunks": text_chunks,
                "metadata": metadata_list
            }, f)

        logger.info(f"Saved {doc_id}: {len(embeddings)} embeddings")

    def search(
        self,
        query: str,
        company: Optional[str] = None,
        year: Optional[int] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks

        Args:
            query: Search query
            company: Filter by company
            year: Filter by year
            top_k: Number of results

        Returns:
            List of results with content, score, metadata
        """
        # Embed query
        query_emb = self.embedder.embed_text(f"query: {query}")
        if query_emb is None:
            return []

        # Load relevant documents
        docs_to_search = self._get_relevant_documents(company, year)

        all_results = []

        for doc_id in docs_to_search:
            # Load embeddings
            emb_path = self.storage_dir / f"{doc_id}_embeddings.npy"
            metadata_path = self.storage_dir / f"{doc_id}_metadata.json"

            if not emb_path.exists() or not metadata_path.exists():
                continue

            # Load
            embeddings = np.load(emb_path)
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            # Calculate similarities
            similarities = self._cosine_similarity_batch(query_emb, embeddings)

            # Get top results from this document
            for idx in np.argsort(similarities)[::-1][:top_k]:
                all_results.append({
                    "content": metadata["chunks"][idx],
                    "score": float(similarities[idx]),
                    "metadata": metadata["metadata"][idx]
                })

        # Sort all results and return top_k
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:top_k]

    def _get_relevant_documents(
        self,
        company: Optional[str],
        year: Optional[int]
    ) -> List[str]:
        """
        Get document IDs matching filters

        Args:
            company: Company filter
            year: Year filter

        Returns:
            List of document IDs to search
        """
        # List all documents in storage
        all_emb_files = list(self.storage_dir.glob("*_embeddings.npy"))

        doc_ids = []
        for emb_file in all_emb_files:
            doc_id = emb_file.stem.replace("_embeddings", "")

            # Apply filters
            if company:
                safe_company = company.lower().replace(" ", "_")
                if not doc_id.startswith(safe_company):
                    continue

            if year:
                if not doc_id.endswith(f"_{year}"):
                    continue

            doc_ids.append(doc_id)

        return doc_ids

    def _cosine_similarity_batch(
        self,
        query_emb: np.ndarray,
        doc_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Calculate cosine similarity between query and all document embeddings

        Args:
            query_emb: Query embedding (1D)
            doc_embeddings: Document embeddings (2D: N x dim)

        Returns:
            Similarity scores (1D: N)
        """
        # Normalize
        query_norm = query_emb / np.linalg.norm(query_emb)
        doc_norms = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)

        # Dot product
        similarities = np.dot(doc_norms, query_norm)

        return similarities
```

**Deliverable:** Simple RAG without external vector database

---

# PRIORITY 4: Simulated Multi-Agent (Sequential Analysis)

## Week 6-8: Multi-Perspective Analysis within 44k Window

### Architecture: Sequential Specialist Passes (Not Parallel)

Given 44k token limit, we can't run agents in parallel. Instead, run sequential specialist analyses that accumulate knowledge.

**File: `src/intelligence/multi_perspective_service.py`**

```python
"""
Multi-perspective intelligence analysis using sequential specialist passes
Simulates multi-agent system within 44k token budget per pass
"""

import logging
from typing import Dict, Any
import time

from .services.local_intelligence_service import LocalIntelligenceService
from ..rag.simple_rag import SimpleRAG

logger = logging.getLogger(__name__)


class MultiPerspectiveIntelligenceService:
    """
    Generate intelligence reports with multiple specialist perspectives
    Sequential passes (not parallel) to fit within 44k token window
    """

    def __init__(self):
        self.llm_service = LocalIntelligenceService()
        self.rag = SimpleRAG()

    def generate_comprehensive_report(
        self,
        company_data: Dict[str, Any],
        use_rag: bool = False
    ) -> Dict[str, Any]:
        """
        Generate report with 6 specialist perspectives

        Perspectives:
        1. Financial Health (liquidity, profitability, leverage)
        2. Risk Assessment (financial, operational, market risks)
        3. Industry Context (competitive position, market trends)
        4. Strategic Evaluation (growth, management, capital allocation)
        5. Market Intelligence (recent developments, sentiment)
        6. Synthesis (integrate all perspectives, final recommendation)

        Args:
            company_data: Same as single-agent
            use_rag: Whether to use RAG for document context

        Returns:
            Comprehensive report with all perspectives
        """
        logger.info(f"=== MULTI-PERSPECTIVE ANALYSIS: {company_data['company_name']} ===")
        start_time = time.time()

        # Prepare data
        company = company_data['company_name']
        industry = company_data.get('industry', 'Unknown')

        # Perspective 1: Financial Health (reuse from single-agent)
        logger.info("Perspective 1: Financial Health Analysis...")
        financial_analysis = self.llm_service._analyze_financial_health(
            company_name=company,
            industry=industry,
            balance_sheet_table=self._format_balance_sheet(company_data),
            income_statement_table=self._format_income_statement(company_data),
            ratios_table=self._format_ratios(company_data)
        )

        # Perspective 2: Risk Assessment (reuse)
        logger.info("Perspective 2: Risk Assessment...")
        risk_analysis = self.llm_service._assess_risks(
            company_name=company,
            industry=industry,
            financial_summary=financial_analysis,
            balance_sheet_table=self._format_balance_sheet(company_data)
        )

        # Perspective 3: Industry Context (NEW)
        logger.info("Perspective 3: Industry Context Analysis...")
        industry_analysis = self._analyze_industry_context(
            company_data, financial_analysis, use_rag
        )

        # Perspective 4: Strategic Evaluation (NEW)
        logger.info("Perspective 4: Strategic Evaluation...")
        strategy_analysis = self._evaluate_strategy(
            company_data, financial_analysis, use_rag
        )

        # Perspective 5: Market Intelligence (NEW)
        logger.info("Perspective 5: Market Intelligence...")
        market_analysis = self._assess_market_intelligence(
            company_data, use_rag
        )

        # Perspective 6: Synthesis (integrate all perspectives)
        logger.info("Perspective 6: Synthesis & Recommendation...")
        synthesis = self._synthesize_perspectives(
            company_data,
            financial_analysis,
            risk_analysis,
            industry_analysis,
            strategy_analysis,
            market_analysis
        )

        # Compile final report
        logger.info("Compiling final comprehensive report...")
        report = self._compile_comprehensive_report(
            company_data,
            {
                'financial': financial_analysis,
                'risk': risk_analysis,
                'industry': industry_analysis,
                'strategy': strategy_analysis,
                'market': market_analysis,
                'synthesis': synthesis
            }
        )

        generation_time = time.time() - start_time

        logger.info(f"✅ Multi-perspective report generated in {generation_time:.2f} seconds")

        return {
            "success": True,
            "report": report,
            "metadata": {
                "company": company,
                "perspectives": 6,
                "rag_enabled": use_rag,
                "generation_time": generation_time
            }
        }

    # ... (implement helper methods for each perspective)
```

**Deliverable:** Multi-perspective analysis system using local LLM

---

# 🎯 FINAL DELIVERABLES

## End State (Week 8)

**What You'll Have:**
1. ✅ Intelligence report generator using local LLM (44k context)
2. ✅ Multi-year financial data extraction and storage (JSON)
3. ✅ Simple RAG using E5 embeddings (file-based, no external DB)
4. ✅ Multi-perspective analysis (6 specialist views)
5. ✅ 15-20 page comprehensive analyst reports
6. ✅ All using existing infrastructure (no new databases)

**System Architecture:**
```
┌─────────────────────────────────────────────────┐
│   PDF Financial Reports (manually provided)    │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│   Financial Data Extraction (regex-based)      │
│   - Balance Sheet                              │
│   - Income Statement                           │
│   - Cash Flow                                  │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│   Multi-Year Data Storage (JSON files)         │
│   data/companies/grupa_azoty.json              │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│   Simple RAG (E5 + NumPy + JSON)               │
│   - Document chunking                          │
│   - E5 embeddings (via LM Studio)              │
│   - Cosine similarity search                   │
│   data/rag_storage/*.npy, *.json               │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│   Multi-Perspective Intelligence Service       │
│   - 6 sequential specialist analyses           │
│   - Local LLM (openai/gpt-oss-20b, 44k ctx)    │
│   - Strategic chunking (multi-pass)            │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│   Comprehensive Intelligence Report            │
│   - 15-20 pages markdown                       │
│   - Financial, Risk, Industry, Strategy,       │
│     Market, Synthesis perspectives             │
│   - Investment recommendation (BUY/HOLD/SELL)  │
│   output/intelligence_reports/*.md             │
└─────────────────────────────────────────────────┘
```

---

**Next Steps:**
1. Review this practical roadmap
2. Confirm it matches your constraints
3. Start with Priority 1 (Week 1-2)
4. Generate first intelligence report for Grupa Azoty
5. Iterate and improve

**Timeline:** 6-8 weeks to full system
**MVP:** 2 weeks (Priority 1)
