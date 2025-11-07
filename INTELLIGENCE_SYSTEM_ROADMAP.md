# Intelligence System Development Roadmap
## From Data Extraction to Strategic Intelligence

**Project:** Comprehensive Multi-Perspective Company Analysis System
**Target:** Generate investment-grade intelligence reports for decision-makers
**Timeline:** 8-12 weeks (MVP in 4 weeks)
**Current State:** Financial data extraction working (80.6% quality, 100% accuracy)
**Target State:** Automated generation of 15-20 page analyst reports with multi-perspective insights

---

# 🎯 PRIORITY RANKING

## Priority 1: Prototype Single-Agent Intelligence System (Week 1-2)
**Effort:** 2 weeks | **Value:** High | **Risk:** Low
**Goal:** Prove the concept - generate a basic but useful intelligence report

**Why First:**
- ✅ Fastest path to demonstrable value
- ✅ Validates LLM capabilities for complex analysis
- ✅ Provides immediate utility (usable reports)
- ✅ Foundation for everything else
- ✅ Low risk (uses existing extraction + single LLM call)

**Deliverable:** Working system that generates 5-10 page analyst report from extracted financial data

---

## Priority 2: RAG Document Ingestion (Week 3-4)
**Effort:** 2 weeks | **Value:** High | **Risk:** Medium
**Goal:** Ground analysis in actual company documents, not just numbers

**Why Second:**
- ✅ Dramatically improves report quality (cites actual sources)
- ✅ Enables "why" questions (Why did margins decline? → finds answer in annual report)
- ✅ Builds on Priority 1 (enhances existing reports)
- ✅ Required foundation for multi-agent system
- ✅ Proven technology (E5 embeddings already working)

**Deliverable:** RAG system ingesting annual reports, supporting contextual queries during analysis

---

## Priority 3: Multi-Agent Orchestration Architecture (Week 5-8)
**Effort:** 4 weeks | **Value:** Very High | **Risk:** Medium
**Goal:** Specialized expert perspectives + synthesis for comprehensive intelligence

**Why Third:**
- ✅ Requires Priorities 1-2 as foundation
- ✅ Highest quality output (multiple expert views)
- ✅ Most complex to implement (needs orchestration)
- ✅ Scales analysis depth significantly
- ✅ Production-grade system architecture

**Deliverable:** 6 specialized agents (Financial, Industry, Risk, Strategy, Market, Synthesis) generating comprehensive reports

---

## Priority 4: Detailed Implementation Plan (Week 9-12)
**Effort:** 4 weeks | **Value:** Medium | **Risk:** Low
**Goal:** Polish, productionize, add advanced features

**Why Last:**
- ✅ Refinement of working system
- ✅ Adds advanced features (knowledge graph, external APIs)
- ✅ Production hardening (error handling, monitoring)
- ✅ Performance optimization
- ✅ User interface development

**Deliverable:** Production-ready system with UI, advanced features, monitoring

---

# 📋 DETAILED ROADMAP

---

# PRIORITY 1: Prototype Single-Agent Intelligence System

**Timeline:** Week 1-2 (10-15 hours effort)
**Dependencies:** Existing extraction system (✅ working)
**Risk Level:** 🟢 Low
**Value:** 🟡 High

## Week 1: Core Intelligence Engine

### Day 1-2: Design Report Structure

**Task 1.1: Define Report Template**
```markdown
# File: src/intelligence/templates/basic_report_template.md

# Company Intelligence Report: {company_name}

## EXECUTIVE SUMMARY
[2-3 paragraphs + clear recommendation]

## 1. FINANCIAL HEALTH ANALYSIS
### 1.1 Balance Sheet Assessment
- Liquidity Analysis (Current Ratio, Quick Ratio, Working Capital)
- Leverage Analysis (Debt/Equity, Interest Coverage)
- Trend Analysis (5-year view)

### 1.2 Key Financial Metrics
[Table with 5-year trends]

### 1.3 Financial Health Score
[0-100 score with explanation]

## 2. RISK ASSESSMENT
### 2.1 Financial Risks
### 2.2 Operational Risks
### 2.3 Market Risks
### 2.4 Risk Matrix
[Table: Risk | Severity | Probability | Mitigation]

## 3. STRENGTHS & WEAKNESSES
### 3.1 Key Strengths (5 bullets)
### 3.2 Key Concerns (5 bullets)
### 3.3 Critical Red Flags (if any)

## 4. INVESTMENT THESIS
### 4.1 Bull Case (best case scenario)
### 4.2 Bear Case (worst case scenario)
### 4.3 Base Case & Recommendation

## 5. CONCLUSION
[Investment recommendation: BUY/HOLD/SELL with rationale]

## APPENDIX
- Data sources
- Methodology
- Assumptions
```

**Deliverable:** `src/intelligence/templates/basic_report_template.md`

---

**Task 1.2: Create Prompt Engineering Framework**
```python
# File: src/intelligence/prompts/analyst_prompts.py

SYSTEM_PROMPT = """
You are a senior equity research analyst with 20 years of experience analyzing
European industrial companies, specializing in chemicals and materials sector.

Your reports are known for:
- Rigorous financial analysis with specific numbers and trends
- Clear identification of risks and opportunities
- Balanced perspective (bull case AND bear case)
- Actionable recommendations for decision-makers
- Professional tone, no hype, evidence-based conclusions

You have deep expertise in:
- Financial statement analysis (ratios, trends, quality of earnings)
- Industry dynamics (competitive position, market trends, regulations)
- Risk assessment (credit, operational, market, ESG risks)
- Valuation methodologies (DCF, comparable companies, precedent transactions)
"""

ANALYSIS_PROMPT_TEMPLATE = """
{system_prompt}

---

## ASSIGNMENT

Generate a comprehensive intelligence report for investment decision-makers.

**Company:** {company_name}
**Industry:** {industry}
**Report Date:** {report_date}

---

## FINANCIAL DATA (5-Year Trends)

### Balance Sheet (in thousands {currency})
{balance_sheet_data}

### Income Statement (in thousands {currency})
{income_statement_data}

### Cash Flow Statement (in thousands {currency})
{cash_flow_data}

---

## REPORT REQUIREMENTS

Follow this structure exactly:

1. **EXECUTIVE SUMMARY** (2-3 paragraphs)
   - Overall assessment
   - Key finding (most important insight)
   - Clear recommendation (BUY/HOLD/SELL)

2. **FINANCIAL HEALTH ANALYSIS**
   - Calculate and interpret: Current Ratio, Quick Ratio, Debt/Equity, ROE, ROA, Net Margin
   - Identify 5-year trends (improving/stable/declining)
   - Assign Financial Health Score (0-100) with justification

3. **RISK ASSESSMENT**
   - Identify top 5 risks (financial, operational, market)
   - For each risk: severity (High/Medium/Low), probability, potential impact
   - Create risk matrix table

4. **STRENGTHS & WEAKNESSES**
   - 5 key strengths (with supporting data)
   - 5 key concerns (with supporting data)
   - Any critical red flags

5. **INVESTMENT THESIS**
   - Bull Case: Best case scenario (3-5 points)
   - Bear Case: Worst case scenario (3-5 points)
   - Base Case: Most likely outcome + clear recommendation

6. **CONCLUSION**
   - Restate recommendation
   - Key action items for decision-makers
   - Monitoring points (what to watch going forward)

---

## ANALYSIS GUIDELINES

- **Be specific:** Cite exact numbers, percentages, trends
- **Be balanced:** Present both positive and negative aspects
- **Be actionable:** Recommendations must be clear and justified
- **Be professional:** Investment-grade quality, no speculation
- **Calculate ratios:** Don't just present data, analyze it
- **Identify trends:** 5-year patterns matter more than single year
- **Flag anomalies:** Call out unusual changes or red flags

Generate the full report now.
"""

def create_analysis_prompt(
    company_name: str,
    industry: str,
    balance_sheet: dict,
    income_statement: dict,
    cash_flow: dict,
    currency: str = "PLN"
) -> str:
    """
    Create full analysis prompt with company data
    """
    return ANALYSIS_PROMPT_TEMPLATE.format(
        system_prompt=SYSTEM_PROMPT,
        company_name=company_name,
        industry=industry,
        report_date=datetime.now().strftime("%Y-%m-%d"),
        currency=currency,
        balance_sheet_data=format_financial_data(balance_sheet),
        income_statement_data=format_financial_data(income_statement),
        cash_flow_data=format_financial_data(cash_flow)
    )
```

**Deliverable:** `src/intelligence/prompts/analyst_prompts.py`

---

### Day 3-4: Build Core Intelligence Engine

**Task 1.3: Create Intelligence Service**
```python
# File: src/intelligence/services/intelligence_service.py

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import anthropic  # or openai, or your local LLM client

from ..prompts.analyst_prompts import create_analysis_prompt
from ..formatters.report_formatter import format_as_markdown, format_as_pdf

logger = logging.getLogger(__name__)


class IntelligenceService:
    """
    Core service for generating intelligence reports
    """

    def __init__(
        self,
        llm_provider: str = "anthropic",  # or "openai", "local"
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 16000
    ):
        self.llm_provider = llm_provider
        self.model = model
        self.max_tokens = max_tokens

        # Initialize LLM client
        if llm_provider == "anthropic":
            self.client = anthropic.Anthropic()
        elif llm_provider == "local":
            # Your local LLM setup
            from src.document_processing.llm_validator import LLMFinancialValidator
            self.client = LLMFinancialValidator()
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

    def generate_intelligence_report(
        self,
        company_data: Dict[str, Any],
        output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive intelligence report

        Args:
            company_data: Dict with:
                - company_name: str
                - industry: str
                - balance_sheet: dict (5-year data)
                - income_statement: dict (5-year data)
                - cash_flow: dict (5-year data)
                - currency: str (default "PLN")
            output_format: "markdown" or "pdf"

        Returns:
            Dict with:
                - success: bool
                - report: str (formatted report)
                - metadata: dict (generation info)
                - error: str (if failed)
        """
        try:
            logger.info(f"Generating intelligence report for {company_data['company_name']}")

            # Step 1: Create analysis prompt
            prompt = create_analysis_prompt(
                company_name=company_data['company_name'],
                industry=company_data.get('industry', 'Unknown'),
                balance_sheet=company_data['balance_sheet'],
                income_statement=company_data.get('income_statement', {}),
                cash_flow=company_data.get('cash_flow', {}),
                currency=company_data.get('currency', 'PLN')
            )

            logger.info(f"Prompt length: {len(prompt)} characters")

            # Step 2: Call LLM
            start_time = datetime.now()

            if self.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                report_text = response.content[0].text

            elif self.llm_provider == "local":
                # Local LLM (your setup)
                messages = [
                    {"role": "system", "content": "You are a senior equity research analyst."},
                    {"role": "user", "content": prompt}
                ]
                report_text = self.client.chat_completion(messages, max_tokens=self.max_tokens)

            else:
                raise ValueError(f"LLM provider {self.llm_provider} not implemented")

            generation_time = (datetime.now() - start_time).total_seconds()

            logger.info(f"Report generated in {generation_time:.2f} seconds")
            logger.info(f"Report length: {len(report_text)} characters")

            # Step 3: Format output
            if output_format == "markdown":
                formatted_report = format_as_markdown(report_text, company_data)
            elif output_format == "pdf":
                formatted_report = format_as_pdf(report_text, company_data)
            else:
                formatted_report = report_text

            # Step 4: Extract metadata
            metadata = {
                "company_name": company_data['company_name'],
                "report_date": datetime.now().isoformat(),
                "model": self.model,
                "generation_time_seconds": generation_time,
                "report_length_chars": len(report_text),
                "llm_provider": self.llm_provider
            }

            return {
                "success": True,
                "report": formatted_report,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Intelligence report generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Helper function for easy usage
def generate_report(company_data: Dict[str, Any]) -> str:
    """
    Simple wrapper to generate report with defaults

    Usage:
        report = generate_report({
            'company_name': 'Grupa Azoty',
            'industry': 'Chemicals',
            'balance_sheet': {...},
            'income_statement': {...},
            'cash_flow': {...}
        })
    """
    service = IntelligenceService()
    result = service.generate_intelligence_report(company_data)

    if result['success']:
        return result['report']
    else:
        raise Exception(f"Report generation failed: {result['error']}")
```

**Deliverable:** `src/intelligence/services/intelligence_service.py`

---

**Task 1.4: Create Data Formatters**
```python
# File: src/intelligence/formatters/data_formatter.py

from typing import Dict, List
import pandas as pd


def format_financial_data(data: Dict[str, Dict[int, float]]) -> str:
    """
    Format financial data as markdown table for LLM

    Input:
        {
            'Total Assets': {2020: 25000000, 2021: 26000000, ...},
            'Current Assets': {2020: 8000000, 2021: 7500000, ...}
        }

    Output:
        | Metric | 2020 | 2021 | 2022 | 2023 | 2024 | Trend |
        |--------|------|------|------|------|------|-------|
        | Total Assets | 25,000 | 26,000 | ... | | | +4.0% |
    """
    if not data:
        return "No data available"

    # Get years (sorted)
    all_years = set()
    for metric_data in data.values():
        all_years.update(metric_data.keys())
    years = sorted(all_years)

    # Build table
    rows = []
    header = f"| Metric | {' | '.join(str(y) for y in years)} | Trend (CAGR) |"
    separator = "|" + "|".join(["---"] * (len(years) + 2)) + "|"

    rows.append(header)
    rows.append(separator)

    for metric, values in data.items():
        # Format values (in thousands, with commas)
        formatted_values = []
        for year in years:
            value = values.get(year)
            if value is not None:
                # Convert to thousands and format
                formatted = f"{value/1000:,.0f}"
            else:
                formatted = "-"
            formatted_values.append(formatted)

        # Calculate trend (CAGR if we have first and last year)
        first_year = min(years)
        last_year = max(years)
        first_value = values.get(first_year)
        last_value = values.get(last_year)

        if first_value and last_value and first_value != 0:
            years_diff = last_year - first_year
            if years_diff > 0:
                cagr = ((last_value / first_value) ** (1 / years_diff) - 1) * 100
                trend = f"{cagr:+.1f}%"
            else:
                trend = "N/A"
        else:
            trend = "N/A"

        row = f"| {metric} | {' | '.join(formatted_values)} | {trend} |"
        rows.append(row)

    return "\n".join(rows)


def calculate_financial_ratios(
    balance_sheet: Dict[str, Dict[int, float]],
    income_statement: Dict[str, Dict[int, float]],
    cash_flow: Dict[str, Dict[int, float]]
) -> Dict[str, Dict[int, float]]:
    """
    Calculate key financial ratios from statements

    Returns:
        {
            'Current Ratio': {2020: 0.7, 2021: 0.65, ...},
            'ROE': {2020: 0.05, 2021: 0.03, ...},
            ...
        }
    """
    ratios = {}

    # Get years
    years = sorted(set(balance_sheet.get('Total Assets', {}).keys()))

    # Current Ratio = Current Assets / Current Liabilities
    if 'Current Assets' in balance_sheet and 'Current Liabilities' in balance_sheet:
        ratios['Current Ratio'] = {}
        for year in years:
            ca = balance_sheet['Current Assets'].get(year)
            cl = balance_sheet['Current Liabilities'].get(year)
            if ca and cl and cl != 0:
                ratios['Current Ratio'][year] = ca / cl

    # Quick Ratio = (Current Assets - Inventories) / Current Liabilities
    if all(k in balance_sheet for k in ['Current Assets', 'Inventories', 'Current Liabilities']):
        ratios['Quick Ratio'] = {}
        for year in years:
            ca = balance_sheet['Current Assets'].get(year)
            inv = balance_sheet['Inventories'].get(year, 0)
            cl = balance_sheet['Current Liabilities'].get(year)
            if ca and cl and cl != 0:
                ratios['Quick Ratio'][year] = (ca - inv) / cl

    # Debt to Equity = Total Liabilities / Total Equity
    if 'Total Liabilities' in balance_sheet and 'Total Equity' in balance_sheet:
        ratios['Debt to Equity'] = {}
        for year in years:
            debt = balance_sheet['Total Liabilities'].get(year)
            equity = balance_sheet['Total Equity'].get(year)
            if debt and equity and equity != 0:
                ratios['Debt to Equity'][year] = debt / equity

    # ROE = Net Income / Total Equity
    if 'Net Income' in income_statement and 'Total Equity' in balance_sheet:
        ratios['ROE (%)'] = {}
        for year in years:
            ni = income_statement['Net Income'].get(year)
            equity = balance_sheet['Total Equity'].get(year)
            if ni and equity and equity != 0:
                ratios['ROE (%)'][year] = (ni / equity) * 100

    # ROA = Net Income / Total Assets
    if 'Net Income' in income_statement and 'Total Assets' in balance_sheet:
        ratios['ROA (%)'] = {}
        for year in years:
            ni = income_statement['Net Income'].get(year)
            assets = balance_sheet['Total Assets'].get(year)
            if ni and assets and assets != 0:
                ratios['ROA (%)'][year] = (ni / assets) * 100

    # Net Margin = Net Income / Revenue
    if 'Net Income' in income_statement and 'Revenue' in income_statement:
        ratios['Net Margin (%)'] = {}
        for year in years:
            ni = income_statement['Net Income'].get(year)
            revenue = income_statement['Revenue'].get(year)
            if ni and revenue and revenue != 0:
                ratios['Net Margin (%)'][year] = (ni / revenue) * 100

    return ratios
```

**Deliverable:** `src/intelligence/formatters/data_formatter.py`

---

### Day 5: Integration & Testing

**Task 1.5: Create Test Script**
```python
# File: scripts/test_intelligence_report.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.intelligence.services.intelligence_service import IntelligenceService
from datetime import datetime


def test_azoty_report():
    """
    Test intelligence report generation for Grupa Azoty 2023 data
    """
    # Sample data (you'll get this from your extraction system)
    company_data = {
        "company_name": "Grupa Azoty S.A.",
        "industry": "Chemicals & Fertilizers",
        "currency": "PLN",

        # Balance sheet (thousands PLN) - June 30, 2023
        "balance_sheet": {
            "Total Assets": {2023: 26019865},
            "Current Assets": {2023: 7904016},
            "Fixed Assets": {2023: 18115849},
            "Total Equity": {2023: 8795144},
            "Total Liabilities": {2023: 17224721},
            "Current Liabilities": {2023: 11330491},
            "Long-term Liabilities": {2023: 5894230},
            "Cash & Equivalents": {2023: 1405681},
            "Inventories": {2023: 2605887}
        },

        # Income statement (would need to extract this)
        "income_statement": {
            # Placeholder - extract from actual reports
        },

        # Cash flow (would need to extract this)
        "cash_flow": {
            # Placeholder - extract from actual reports
        }
    }

    print("=" * 80)
    print("TESTING INTELLIGENCE REPORT GENERATION")
    print("=" * 80)

    # Initialize service
    service = IntelligenceService(
        llm_provider="anthropic",  # or "local" for your LLM
        model="claude-3-5-sonnet-20241022",
        max_tokens=16000
    )

    # Generate report
    result = service.generate_intelligence_report(company_data)

    if result['success']:
        print("\n✅ REPORT GENERATED SUCCESSFULLY\n")
        print(f"Generation time: {result['metadata']['generation_time_seconds']:.2f} seconds")
        print(f"Report length: {result['metadata']['report_length_chars']:,} characters")
        print("\n" + "=" * 80)
        print("REPORT PREVIEW (first 2000 chars):")
        print("=" * 80)
        print(result['report'][:2000])
        print("\n[...truncated...]\n")

        # Save to file
        output_path = Path("output/intelligence_reports")
        output_path.mkdir(parents=True, exist_ok=True)

        filename = f"Azoty_Intelligence_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        full_path = output_path / filename

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(result['report'])

        print(f"✅ Full report saved to: {full_path}")

    else:
        print("\n❌ REPORT GENERATION FAILED")
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    test_azoty_report()
```

**Deliverable:** `scripts/test_intelligence_report.py`

---

## Week 2: Enhancement & Validation

### Day 6-7: Add Multi-Year Support

**Task 1.6: Extend Extraction to Multi-Year**
```python
# File: src/document_processing/multi_year_extractor.py

from pathlib import Path
from typing import Dict, List
from .intelligent_extractor import IntelligentExtractor


class MultiYearExtractor:
    """
    Extract financial data from multiple years of reports
    """

    def __init__(self):
        self.extractor = IntelligentExtractor()

    def extract_multi_year(
        self,
        pdf_paths: Dict[int, Path]
    ) -> Dict[str, Dict[int, float]]:
        """
        Extract from multiple PDFs and combine into time series

        Args:
            pdf_paths: {2020: Path("report_2020.pdf"), 2021: ...}

        Returns:
            {
                'Total Assets': {2020: 25000000, 2021: 26000000, ...},
                'Current Assets': {2020: 8000000, 2021: 7500000, ...}
            }
        """
        combined_data = {}

        for year, pdf_path in sorted(pdf_paths.items()):
            print(f"Extracting {year} data from {pdf_path.name}...")

            result = self.extractor.extract(pdf_path)

            if result.success:
                # Add year dimension to extracted data
                for metric, value in result.data.items():
                    if metric not in combined_data:
                        combined_data[metric] = {}
                    combined_data[metric][year] = value

                print(f"  ✅ {year}: {len(result.data)} metrics extracted")
            else:
                print(f"  ❌ {year}: Failed - {result.error}")

        return combined_data
```

**Deliverable:** `src/document_processing/multi_year_extractor.py`

---

### Day 8-10: Validation & Iteration

**Task 1.7: Generate Real Report & Validate**

1. Extract Grupa Azoty 2023 data (you have this ✅)
2. Run intelligence report generation
3. **Manual Review:** Read the report, check quality
4. **Iterate on prompts:** Improve prompt based on output quality
5. **Test with different companies:** Try other Polish companies if available

**Quality Checklist:**
- [ ] Report follows template structure
- [ ] Calculations are correct (verify ratios manually)
- [ ] Analysis is specific (cites numbers, not vague)
- [ ] Recommendation is clear and justified
- [ ] Identifies real risks (not generic)
- [ ] Professional tone (investment-grade quality)
- [ ] Bull/bear cases are balanced
- [ ] Report is actionable for decision-makers

**Deliverable:** Validated intelligence report + refined prompts

---

### Week 2 Deliverables

**Completed by End of Week 2:**
- ✅ Working intelligence report generator
- ✅ Template-based report structure
- ✅ LLM integration (Claude or local)
- ✅ Financial data formatting
- ✅ Multi-year data support
- ✅ Test scripts
- ✅ Generated sample report for Grupa Azoty
- ✅ Quality validation

**Files Created:**
```
src/intelligence/
├── services/
│   └── intelligence_service.py
├── prompts/
│   └── analyst_prompts.py
├── formatters/
│   ├── data_formatter.py
│   └── report_formatter.py
├── templates/
│   └── basic_report_template.md
└── __init__.py

src/document_processing/
└── multi_year_extractor.py

scripts/
└── test_intelligence_report.py

output/
└── intelligence_reports/
    └── Azoty_Intelligence_Report_20251106.md
```

---

# PRIORITY 2: RAG Document Ingestion

**Timeline:** Week 3-4 (15-20 hours effort)
**Dependencies:** Priority 1 (✅), Existing E5 embeddings (✅)
**Risk Level:** 🟡 Medium
**Value:** 🟢 Very High

## Week 3: RAG Infrastructure

### Day 11-12: Document Ingestion Pipeline

**Task 2.1: Create Document Loader**
```python
# File: src/rag/document_loaders.py

from pathlib import Path
from typing import List, Dict, Any
import logging
from dataclasses import dataclass

# PDF loading
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Document chunk with metadata"""
    content: str
    metadata: Dict[str, Any]
    page: int
    chunk_index: int


class DocumentLoader:
    """
    Load and chunk company documents for RAG
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def load_annual_report(
        self,
        pdf_path: Path,
        company: str,
        year: int,
        document_type: str = "annual_report"
    ) -> List[Document]:
        """
        Load and chunk annual report PDF

        Args:
            pdf_path: Path to PDF
            company: Company name
            year: Report year
            document_type: Type of document

        Returns:
            List of Document chunks with metadata
        """
        logger.info(f"Loading {document_type} for {company} ({year})")

        documents = []

        try:
            # Extract text from PDF
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text()

                    if not page_text:
                        continue

                    # Clean text
                    page_text = self._clean_text(page_text)

                    # Chunk the page
                    chunks = self.text_splitter.split_text(page_text)

                    # Create Document objects
                    for chunk_idx, chunk in enumerate(chunks):
                        doc = Document(
                            content=chunk,
                            metadata={
                                "company": company,
                                "year": year,
                                "document_type": document_type,
                                "source_file": pdf_path.name,
                                "page": page_num,
                                "total_pages": len(pdf.pages)
                            },
                            page=page_num,
                            chunk_index=chunk_idx
                        )
                        documents.append(doc)

            logger.info(f"Loaded {len(documents)} chunks from {len(pdf.pages)} pages")
            return documents

        except Exception as e:
            logger.error(f"Failed to load document: {e}")
            return []

    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove excessive whitespace
        text = " ".join(text.split())

        # Remove page numbers (common pattern)
        import re
        text = re.sub(r'\b\d+\s*/\s*\d+\b', '', text)

        return text

    def load_multiple_reports(
        self,
        pdf_paths: Dict[int, Path],
        company: str
    ) -> List[Document]:
        """
        Load multiple years of reports

        Args:
            pdf_paths: {2020: Path(...), 2021: Path(...)}
            company: Company name

        Returns:
            Combined list of all document chunks
        """
        all_documents = []

        for year, pdf_path in sorted(pdf_paths.items()):
            docs = self.load_annual_report(pdf_path, company, year)
            all_documents.extend(docs)

        logger.info(f"Loaded {len(all_documents)} total chunks across {len(pdf_paths)} years")
        return all_documents
```

**Deliverable:** `src/rag/document_loaders.py`

---

**Task 2.2: Set Up Vector Database**
```python
# File: src/rag/vector_store.py

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Use Qdrant for vector storage
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# Use your existing E5 embeddings
from ..document_processing.semantic_matcher import E5SemanticMatcher

from .document_loaders import Document

logger = logging.getLogger(__name__)


class CompanyDocumentVectorStore:
    """
    Vector store for company documents using Qdrant + E5 embeddings
    """

    def __init__(
        self,
        collection_name: str = "company_documents",
        qdrant_url: str = "localhost",
        qdrant_port: int = 6333
    ):
        self.collection_name = collection_name

        # Initialize Qdrant client
        self.qdrant = QdrantClient(host=qdrant_url, port=qdrant_port)

        # Initialize E5 embeddings (reuse existing)
        self.embedder = E5SemanticMatcher()

        # Get embedding dimension
        test_embedding = self.embedder.embed_text("test")
        self.embedding_dim = len(test_embedding)

        logger.info(f"Vector store initialized: {collection_name} (dim={self.embedding_dim})")

    def create_collection(self):
        """Create Qdrant collection if not exists"""
        try:
            # Check if collection exists
            collections = self.qdrant.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)

            if not exists:
                self.qdrant.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise

    def ingest_documents(
        self,
        documents: List[Document],
        batch_size: int = 100
    ):
        """
        Ingest documents into vector store

        Args:
            documents: List of Document objects
            batch_size: Batch size for embedding/uploading
        """
        logger.info(f"Ingesting {len(documents)} documents...")

        # Create collection if needed
        self.create_collection()

        # Process in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]

            logger.info(f"Processing batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")

            # Embed batch
            texts = [f"passage: {doc.content}" for doc in batch]
            embeddings = [self.embedder.embed_text(text) for text in texts]

            # Create points
            points = []
            for idx, (doc, embedding) in enumerate(zip(batch, embeddings)):
                if embedding is None:
                    logger.warning(f"Skipping document {i+idx} (embedding failed)")
                    continue

                point = PointStruct(
                    id=i + idx,
                    vector=embedding.tolist(),
                    payload={
                        "content": doc.content,
                        "company": doc.metadata["company"],
                        "year": doc.metadata["year"],
                        "document_type": doc.metadata["document_type"],
                        "source_file": doc.metadata["source_file"],
                        "page": doc.page,
                        "chunk_index": doc.chunk_index
                    }
                )
                points.append(point)

            # Upload batch
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=points
            )

        logger.info(f"✅ Ingested {len(documents)} documents")

    def search(
        self,
        query: str,
        company: Optional[str] = None,
        year: Optional[int] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant document chunks

        Args:
            query: Search query
            company: Filter by company name
            year: Filter by year
            top_k: Number of results

        Returns:
            List of results with content and metadata
        """
        # Embed query
        query_vector = self.embedder.embed_text(f"query: {query}")

        if query_vector is None:
            logger.error("Query embedding failed")
            return []

        # Build filter
        filter_conditions = []
        if company:
            filter_conditions.append(
                FieldCondition(key="company", match=MatchValue(value=company))
            )
        if year:
            filter_conditions.append(
                FieldCondition(key="year", match=MatchValue(value=year))
            )

        query_filter = Filter(must=filter_conditions) if filter_conditions else None

        # Search
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            query_filter=query_filter,
            limit=top_k
        )

        # Format results
        formatted = []
        for result in results:
            formatted.append({
                "content": result.payload["content"],
                "score": result.score,
                "metadata": {
                    "company": result.payload["company"],
                    "year": result.payload["year"],
                    "source": result.payload["source_file"],
                    "page": result.payload["page"]
                }
            })

        return formatted
```

**Deliverable:** `src/rag/vector_store.py`

---

### Day 13-14: RAG Query Integration

**Task 2.3: Create RAG Query Service**
```python
# File: src/rag/rag_service.py

from typing import List, Dict, Any, Optional
import logging

from .vector_store import CompanyDocumentVectorStore

logger = logging.getLogger(__name__)


class RAGService:
    """
    Service for RAG-enhanced queries during analysis
    """

    def __init__(self):
        self.vector_store = CompanyDocumentVectorStore()

    def get_context_for_question(
        self,
        question: str,
        company: str,
        years: Optional[List[int]] = None,
        top_k: int = 5
    ) -> str:
        """
        Get relevant context from documents for a specific question

        Args:
            question: Analyst question
            company: Company name
            years: Filter by specific years (or None for all)
            top_k: Number of chunks to retrieve

        Returns:
            Formatted context string
        """
        logger.info(f"RAG query: '{question}' for {company}")

        # If multiple years, query each and combine
        if years and len(years) > 1:
            all_results = []
            for year in years:
                results = self.vector_store.search(
                    query=question,
                    company=company,
                    year=year,
                    top_k=top_k // len(years) + 1
                )
                all_results.extend(results)

            # Sort by score and take top_k
            all_results.sort(key=lambda x: x['score'], reverse=True)
            results = all_results[:top_k]

        else:
            # Single year or all years
            year = years[0] if years and len(years) == 1 else None
            results = self.vector_store.search(
                query=question,
                company=company,
                year=year,
                top_k=top_k
            )

        # Format context
        if not results:
            return "No relevant context found in documents."

        context_parts = []
        for i, result in enumerate(results, 1):
            source = f"{result['metadata']['source']} (page {result['metadata']['page']})"
            context_parts.append(
                f"[Source {i}: {source}, relevance: {result['score']:.2f}]\n{result['content']}"
            )

        context = "\n\n---\n\n".join(context_parts)

        logger.info(f"Retrieved {len(results)} relevant chunks")
        return context

    def enhance_financial_analysis(
        self,
        metric: str,
        trend: str,
        company: str,
        years: List[int]
    ) -> str:
        """
        Get context to explain a financial metric trend

        Args:
            metric: Financial metric (e.g., "Net Margin")
            trend: Observed trend (e.g., "declining")
            company: Company name
            years: Years to search

        Returns:
            Context explaining the trend
        """
        # Formulate question
        question = f"Why did {metric} {trend}? What were the key drivers and challenges?"

        return self.get_context_for_question(question, company, years, top_k=3)

    def get_risk_context(
        self,
        risk_type: str,
        company: str,
        years: List[int]
    ) -> str:
        """
        Get context about specific risks

        Args:
            risk_type: Type of risk (e.g., "liquidity risk", "market risk")
            company: Company name
            years: Years to search

        Returns:
            Context about the risk
        """
        question = f"What are the {risk_type} factors? What mitigation strategies are in place?"

        return self.get_context_for_question(question, company, years, top_k=3)

    def get_strategy_context(
        self,
        topic: str,
        company: str,
        years: List[int]
    ) -> str:
        """
        Get context about strategic initiatives

        Args:
            topic: Strategic topic (e.g., "growth strategy", "R&D investments")
            company: Company name
            years: Years to search

        Returns:
            Context about strategy
        """
        question = f"What is the company's {topic}? What are the key initiatives and goals?"

        return self.get_context_for_question(question, company, years, top_k=3)
```

**Deliverable:** `src/rag/rag_service.py`

---

### Day 15: Integration with Intelligence Service

**Task 2.4: Enhance Intelligence Service with RAG**
```python
# File: src/intelligence/services/intelligence_service_v2.py
# (Updated version with RAG)

from typing import Dict, Any, Optional
import logging

from ..prompts.analyst_prompts import create_analysis_prompt_with_context
from ...rag.rag_service import RAGService

logger = logging.getLogger(__name__)


class IntelligenceServiceV2:
    """
    Enhanced intelligence service with RAG support
    """

    def __init__(self, llm_provider: str = "anthropic", model: str = "claude-3-5-sonnet-20241022"):
        # ... (same initialization as V1)
        self.rag_service = RAGService()

    def generate_intelligence_report_with_rag(
        self,
        company_data: Dict[str, Any],
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Generate report with RAG-enhanced context

        Args:
            company_data: Same as V1
            use_rag: Whether to use RAG for additional context

        Returns:
            Same as V1
        """
        company = company_data['company_name']
        years = sorted(set(
            list(company_data.get('balance_sheet', {}).get('Total Assets', {}).keys()) +
            list(company_data.get('income_statement', {}).get('Revenue', {}).keys())
        ))

        rag_context = {}

        if use_rag and years:
            logger.info(f"Gathering RAG context for {company}...")

            # Get context for key questions
            rag_context['profitability'] = self.rag_service.enhance_financial_analysis(
                metric="profitability",
                trend="trend analysis",
                company=company,
                years=years
            )

            rag_context['risks'] = self.rag_service.get_risk_context(
                risk_type="operational and financial",
                company=company,
                years=years
            )

            rag_context['strategy'] = self.rag_service.get_strategy_context(
                topic="strategic priorities and growth plans",
                company=company,
                years=years
            )

            logger.info("RAG context gathered")

        # Create enhanced prompt with RAG context
        prompt = create_analysis_prompt_with_context(
            company_data=company_data,
            rag_context=rag_context
        )

        # ... (rest same as V1: call LLM, format, return)
```

**Deliverable:** `src/intelligence/services/intelligence_service_v2.py`

---

## Week 4: RAG Testing & Optimization

### Day 16-17: Document Ingestion

**Task 2.5: Ingest Grupa Azoty Reports**
```python
# File: scripts/ingest_azoty_documents.py

from pathlib import Path
from src.rag.document_loaders import DocumentLoader
from src.rag.vector_store import CompanyDocumentVectorStore


def ingest_azoty_reports():
    """
    Ingest Grupa Azoty annual reports into vector store
    """
    # Paths to reports (adjust to your actual files)
    reports = {
        2023: Path("data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2023.pdf"),
        # Add more years if you have them
        # 2022: Path("data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2022.pdf"),
        # 2021: Path("data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2021.pdf"),
    }

    # Load documents
    loader = DocumentLoader(chunk_size=1000, chunk_overlap=200)
    all_docs = loader.load_multiple_reports(reports, company="Grupa Azoty")

    print(f"Loaded {len(all_docs)} document chunks")

    # Ingest into vector store
    vector_store = CompanyDocumentVectorStore()
    vector_store.ingest_documents(all_docs)

    print("✅ Ingestion complete")

    # Test search
    print("\nTesting search...")
    results = vector_store.search(
        query="Why did profitability decline?",
        company="Grupa Azoty",
        year=2023,
        top_k=3
    )

    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (score: {result['score']:.3f}):")
        print(f"Source: {result['metadata']['source']}, page {result['metadata']['page']}")
        print(f"Content: {result['content'][:200]}...")


if __name__ == "__main__":
    ingest_azoty_reports()
```

**Deliverable:** Ingested documents in Qdrant

---

### Day 18-20: Testing & Iteration

**Task 2.6: Generate RAG-Enhanced Report**

1. Run document ingestion
2. Generate intelligence report with RAG enabled
3. Compare to baseline (non-RAG) report
4. Validate that RAG adds value (cites sources, explains "why")
5. Iterate on chunking strategy if needed (chunk size, overlap)
6. Test different queries

**Quality Metrics:**
- RAG retrieval accuracy (are retrieved chunks relevant?)
- Report quality improvement (does it explain trends better?)
- Source attribution (does it cite documents?)
- Speed (is it still fast with RAG?)

**Deliverable:** RAG-enhanced intelligence report with source citations

---

### Week 4 Deliverables

**Completed by End of Week 4:**
- ✅ Document loading pipeline
- ✅ Vector database (Qdrant) with E5 embeddings
- ✅ RAG query service
- ✅ Integration with intelligence service
- ✅ Ingested Azoty annual reports
- ✅ RAG-enhanced intelligence reports
- ✅ Quality validation

**Files Created:**
```
src/rag/
├── document_loaders.py
├── vector_store.py
├── rag_service.py
└── __init__.py

src/intelligence/services/
└── intelligence_service_v2.py

scripts/
└── ingest_azoty_documents.py

# Qdrant data (persisted)
qdrant_data/
└── company_documents/
```

---

# PRIORITY 3: Multi-Agent Orchestration Architecture

**Timeline:** Week 5-8 (30-40 hours effort)
**Dependencies:** Priority 1 (✅), Priority 2 (✅)
**Risk Level:** 🟡 Medium
**Value:** 🟢 Very High

## Week 5-6: Agent Design & Implementation

### Day 21-25: Create Specialized Agents

**Agent Architecture:**
```
┌─────────────────────────────────────────────────────┐
│              Synthesis Agent                        │
│         (Master Orchestrator)                       │
└─────────────────────────────────────────────────────┘
                        ▲
                        │ Collects outputs
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
│  Financial   │ │  Industry  │ │    Risk    │
│    Health    │ │  Context   │ │ Assessment │
│    Agent     │ │   Agent    │ │   Agent    │
└──────────────┘ └────────────┘ └────────────┘
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐        │
│  Strategic   │ │   Market   │        │
│   Insight    │ │Intelligence│        │
│    Agent     │ │   Agent    │        │
└──────────────┘ └────────────┘        │
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
                  RAG Service
                  (Document Context)
```

**Task 3.1: Create Agent Base Class**
```python
# File: src/intelligence/agents/base_agent.py

from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentAnalysis:
    """Output from an analysis agent"""
    agent_name: str
    analysis_type: str
    findings: Dict[str, Any]
    score: Optional[float] = None  # 0-100 score
    confidence: float = 0.8  # 0-1 confidence
    warnings: list = None
    recommendations: list = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.recommendations is None:
            self.recommendations = []


class AnalysisAgent:
    """
    Base class for specialized analysis agents
    """

    def __init__(
        self,
        name: str,
        expertise: str,
        llm_client: Any,
        rag_service: Optional[Any] = None
    ):
        self.name = name
        self.expertise = expertise
        self.llm = llm_client
        self.rag_service = rag_service
        self.logger = logging.getLogger(f"agent.{name}")

    def analyze(
        self,
        company_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> AgentAnalysis:
        """
        Main analysis method (implemented by subclasses)

        Args:
            company_data: Financial and company data
            context: Optional additional context

        Returns:
            AgentAnalysis with findings
        """
        raise NotImplementedError("Subclasses must implement analyze()")

    def _get_rag_context(self, query: str, company: str, years: list) -> str:
        """Get RAG context if service available"""
        if self.rag_service:
            return self.rag_service.get_context_for_question(
                question=query,
                company=company,
                years=years,
                top_k=3
            )
        return ""

    def _build_prompt(self, **kwargs) -> str:
        """Build agent-specific prompt (implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement _build_prompt()")

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured findings"""
        # Default: return as-is
        # Subclasses can override for structured parsing
        return {"raw_analysis": response}
```

**Deliverable:** `src/intelligence/agents/base_agent.py`

---

**Task 3.2: Financial Health Agent**
```python
# File: src/intelligence/agents/financial_health_agent.py

from typing import Dict, Any
from .base_agent import AnalysisAgent, AgentAnalysis
from ..formatters.data_formatter import format_financial_data, calculate_financial_ratios


class FinancialHealthAgent(AnalysisAgent):
    """
    Analyzes financial health: liquidity, profitability, leverage, efficiency
    """

    def __init__(self, llm_client, rag_service=None):
        super().__init__(
            name="Financial Health Analyst",
            expertise="Financial statement analysis, ratio analysis, trend analysis",
            llm_client=llm_client,
            rag_service=rag_service
        )

    def analyze(self, company_data: Dict[str, Any], context=None) -> AgentAnalysis:
        self.logger.info(f"Analyzing financial health for {company_data['company_name']}")

        # Calculate ratios
        ratios = calculate_financial_ratios(
            company_data['balance_sheet'],
            company_data.get('income_statement', {}),
            company_data.get('cash_flow', {})
        )

        # Get RAG context about profitability trends
        company = company_data['company_name']
        years = list(company_data['balance_sheet'].get('Total Assets', {}).keys())

        rag_context = ""
        if self.rag_service and years:
            rag_context = self._get_rag_context(
                query="Explain profitability trends, margin drivers, and operational efficiency",
                company=company,
                years=years
            )

        # Build prompt
        prompt = self._build_prompt(
            company_data=company_data,
            ratios=ratios,
            rag_context=rag_context
        )

        # Call LLM
        response = self.llm.invoke(prompt)

        # Parse response
        findings = self._parse_response(response)

        # Calculate health score (simplified - LLM can also do this)
        score = self._calculate_health_score(ratios)

        return AgentAnalysis(
            agent_name=self.name,
            analysis_type="financial_health",
            findings=findings,
            score=score,
            confidence=0.9 if rag_context else 0.7
        )

    def _build_prompt(self, company_data, ratios, rag_context) -> str:
        balance_sheet_table = format_financial_data(company_data['balance_sheet'])
        ratios_table = format_financial_data(ratios)

        prompt = f"""
You are a senior financial analyst specializing in balance sheet analysis and financial health assessment.

## COMPANY
{company_data['company_name']} - {company_data.get('industry', 'Unknown Industry')}

## BALANCE SHEET DATA
{balance_sheet_table}

## CALCULATED RATIOS
{ratios_table}

## DOCUMENT CONTEXT (from annual reports)
{rag_context if rag_context else "No additional context available"}

---

## YOUR TASK

Analyze the company's financial health across four dimensions:

1. **LIQUIDITY** (ability to meet short-term obligations)
   - Current Ratio, Quick Ratio, Working Capital
   - Trend: improving, stable, or declining?
   - Assessment: Strong, Adequate, or Weak?

2. **PROFITABILITY** (ability to generate returns)
   - ROE, ROA, Net Margin
   - Trend over time
   - Comparison to industry (if context available)

3. **LEVERAGE** (debt burden and solvency)
   - Debt-to-Equity ratio
   - Interest coverage (if data available)
   - Risk level: Low, Medium, or High?

4. **EFFICIENCY** (asset utilization)
   - Asset turnover, inventory management
   - Operational effectiveness

## OUTPUT FORMAT

Provide your analysis in this structure:

### FINANCIAL HEALTH SCORE: [0-100]

### LIQUIDITY ASSESSMENT
- Current status: [Strong/Adequate/Weak]
- Key metrics: [cite specific ratios]
- Trend: [improving/stable/declining]
- Concerns: [if any]

### PROFITABILITY ASSESSMENT
- Current status: [Strong/Adequate/Weak]
- Key metrics: [cite specific ratios]
- Trend: [improving/stable/declining]
- Drivers: [what's driving profitability?]

### LEVERAGE ASSESSMENT
- Current status: [Low/Medium/High risk]
- Key metrics: [cite specific ratios]
- Debt burden: [assessment]
- Refinancing risk: [if any]

### EFFICIENCY ASSESSMENT
- Asset utilization: [assessment]
- Operational efficiency: [assessment]

### TOP 3 STRENGTHS
1. [Specific strength with data]
2. [Specific strength with data]
3. [Specific strength with data]

### TOP 3 CONCERNS
1. [Specific concern with data]
2. [Specific concern with data]
3. [Specific concern with data]

### RED FLAGS (if any)
- [Critical issues requiring immediate attention]

Be specific, cite numbers, explain trends, and support conclusions with data.
"""
        return prompt

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response - can enhance with structured extraction"""
        return {
            "raw_analysis": response,
            # Could add structured parsing here
        }

    def _calculate_health_score(self, ratios: Dict) -> float:
        """
        Simple health score calculation (0-100)
        More sophisticated: use LLM to calculate
        """
        score = 50  # baseline

        # Liquidity component (0-25 points)
        current_ratios = list(ratios.get('Current Ratio', {}).values())
        if current_ratios:
            avg_current = sum(current_ratios) / len(current_ratios)
            if avg_current >= 1.5:
                score += 25
            elif avg_current >= 1.0:
                score += 15
            elif avg_current >= 0.7:
                score += 5

        # Profitability component (0-25 points)
        roe_values = list(ratios.get('ROE (%)', {}).values())
        if roe_values:
            avg_roe = sum(roe_values) / len(roe_values)
            if avg_roe >= 15:
                score += 25
            elif avg_roe >= 10:
                score += 15
            elif avg_roe >= 5:
                score += 10

        # Leverage component (0-25 points, inverse)
        de_ratios = list(ratios.get('Debt to Equity', {}).values())
        if de_ratios:
            avg_de = sum(de_ratios) / len(de_ratios)
            if avg_de <= 0.5:
                score += 25
            elif avg_de <= 1.0:
                score += 20
            elif avg_de <= 2.0:
                score += 10

        # Trend component (0-25 points)
        # Check if metrics improving over time
        # Simplified: just check if last year > first year
        if current_ratios and len(current_ratios) > 1:
            if current_ratios[-1] > current_ratios[0]:
                score += 10

        return min(100, max(0, score))
```

**Deliverable:** `src/intelligence/agents/financial_health_agent.py`

---

**Task 3.3: Create Remaining Agents** (Similar Structure)

Implement these agents following the same pattern:

1. **Industry Context Agent** (`industry_context_agent.py`)
   - Competitive positioning
   - Market share analysis
   - Industry trends
   - Regulatory environment

2. **Risk Assessment Agent** (`risk_assessment_agent.py`)
   - Financial risks
   - Operational risks
   - Market risks
   - ESG risks
   - Risk matrix with severity/probability

3. **Strategic Insight Agent** (`strategic_insight_agent.py`)
   - Growth strategy
   - Capital allocation
   - Management quality
   - Strategic initiatives

4. **Market Intelligence Agent** (`market_intelligence_agent.py`)
   - Recent news/developments
   - Sentiment analysis
   - Analyst ratings
   - Forward-looking indicators

5. **Synthesis Agent** (`synthesis_agent.py`)
   - Combines all agent outputs
   - Identifies contradictions
   - Weighs evidence
   - Generates final recommendation

**Deliverable:** 6 specialized agent classes

---

## Week 7: Orchestration & Integration

### Day 26-30: Build Multi-Agent Orchestrator

**Task 3.4: Create Orchestrator**
```python
# File: src/intelligence/orchestrator/multi_agent_orchestrator.py

import asyncio
from typing import Dict, Any, List
import logging

from ..agents.financial_health_agent import FinancialHealthAgent
from ..agents.industry_context_agent import IndustryContextAgent
from ..agents.risk_assessment_agent import RiskAssessmentAgent
from ..agents.strategic_insight_agent import StrategyInsightAgent
from ..agents.market_intelligence_agent import MarketIntelligenceAgent
from ..agents.synthesis_agent import SynthesisAgent
from ...rag.rag_service import RAGService

logger = logging.getLogger(__name__)


class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents for comprehensive analysis
    """

    def __init__(self, llm_client, use_rag: bool = True):
        self.llm = llm_client

        # Initialize RAG if enabled
        self.rag_service = RAGService() if use_rag else None

        # Initialize agents
        self.financial_agent = FinancialHealthAgent(llm_client, self.rag_service)
        self.industry_agent = IndustryContextAgent(llm_client, self.rag_service)
        self.risk_agent = RiskAssessmentAgent(llm_client, self.rag_service)
        self.strategy_agent = StrategyInsightAgent(llm_client, self.rag_service)
        self.market_agent = MarketIntelligenceAgent(llm_client, self.rag_service)
        self.synthesis_agent = SynthesisAgent(llm_client)

        logger.info("Multi-agent orchestrator initialized")

    async def generate_comprehensive_report(
        self,
        company_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive multi-perspective report

        Args:
            company_data: Same as single-agent system

        Returns:
            {
                'success': bool,
                'report': str,
                'agent_analyses': dict,
                'metadata': dict
            }
        """
        logger.info(f"Starting multi-agent analysis for {company_data['company_name']}")

        # Step 1: Run specialized agents in parallel
        logger.info("Running specialized agents in parallel...")

        agent_tasks = [
            self.financial_agent.analyze(company_data),
            self.industry_agent.analyze(company_data),
            self.risk_agent.analyze(company_data),
            self.strategy_agent.analyze(company_data),
            self.market_agent.analyze(company_data)
        ]

        # Run in parallel (async)
        agent_results = await asyncio.gather(*agent_tasks)

        # Map results
        agent_analyses = {
            'financial_health': agent_results[0],
            'industry_context': agent_results[1],
            'risk_assessment': agent_results[2],
            'strategic_insight': agent_results[3],
            'market_intelligence': agent_results[4]
        }

        logger.info("All specialized analyses complete")

        # Step 2: Synthesis
        logger.info("Running synthesis agent...")

        synthesis = self.synthesis_agent.synthesize(
            agent_analyses=agent_analyses,
            company_data=company_data
        )

        logger.info("Synthesis complete")

        # Step 3: Generate final report
        report = self._generate_report_document(
            synthesis=synthesis,
            agent_analyses=agent_analyses,
            company_data=company_data
        )

        return {
            'success': True,
            'report': report,
            'agent_analyses': agent_analyses,
            'synthesis': synthesis,
            'metadata': {
                'company': company_data['company_name'],
                'agents_used': len(agent_analyses),
                'rag_enabled': self.rag_service is not None
            }
        }

    def _generate_report_document(
        self,
        synthesis: Any,
        agent_analyses: Dict,
        company_data: Dict
    ) -> str:
        """
        Combine all analyses into final report document

        Returns markdown-formatted comprehensive report
        """
        report_sections = []

        # Header
        report_sections.append(f"""
# Comprehensive Intelligence Report: {company_data['company_name']}

**Report Date:** {datetime.now().strftime('%Y-%m-%d')}
**Industry:** {company_data.get('industry', 'Unknown')}
**Analysis Method:** Multi-Agent System (6 specialized perspectives)

---
""")

        # Executive Summary (from Synthesis Agent)
        report_sections.append(f"""
## EXECUTIVE SUMMARY

{synthesis.findings.get('executive_summary', 'Summary not available')}

**Overall Assessment:** {synthesis.findings.get('overall_assessment', 'N/A')}
**Investment Recommendation:** {synthesis.findings.get('recommendation', 'N/A')}
**Confidence Level:** {synthesis.confidence:.0%}

---
""")

        # Section 1: Financial Health
        financial = agent_analyses['financial_health']
        report_sections.append(f"""
## 1. FINANCIAL HEALTH ANALYSIS

{financial.findings.get('raw_analysis', 'Analysis not available')}

**Financial Health Score:** {financial.score:.0f}/100

---
""")

        # Section 2: Industry & Competitive Position
        industry = agent_analyses['industry_context']
        report_sections.append(f"""
## 2. INDUSTRY & COMPETITIVE POSITION

{industry.findings.get('raw_analysis', 'Analysis not available')}

---
""")

        # Section 3: Risk Assessment
        risk = agent_analyses['risk_assessment']
        report_sections.append(f"""
## 3. RISK ASSESSMENT

{risk.findings.get('raw_analysis', 'Analysis not available')}

---
""")

        # Section 4: Strategic Evaluation
        strategy = agent_analyses['strategic_insight']
        report_sections.append(f"""
## 4. STRATEGIC EVALUATION

{strategy.findings.get('raw_analysis', 'Analysis not available')}

---
""")

        # Section 5: Market Intelligence
        market = agent_analyses['market_intelligence']
        report_sections.append(f"""
## 5. MARKET INTELLIGENCE

{market.findings.get('raw_analysis', 'Analysis not available')}

---
""")

        # Section 6: Investment Thesis (from Synthesis)
        report_sections.append(f"""
## 6. INVESTMENT THESIS

{synthesis.findings.get('investment_thesis', 'Thesis not available')}

### Bull Case
{synthesis.findings.get('bull_case', 'Not available')}

### Bear Case
{synthesis.findings.get('bear_case', 'Not available')}

### Base Case & Recommendation
{synthesis.findings.get('base_case', 'Not available')}

---
""")

        # Appendix
        report_sections.append(f"""
## APPENDIX

### Analysis Methodology
- **System:** Multi-Agent Intelligence System
- **Agents:** 6 specialized perspectives (Financial, Industry, Risk, Strategy, Market, Synthesis)
- **RAG:** {"Enabled - grounded in company documents" if self.rag_service else "Disabled"}
- **LLM:** {self.llm.__class__.__name__}

### Agent Confidence Scores
- Financial Health: {financial.confidence:.0%}
- Industry Context: {industry.confidence:.0%}
- Risk Assessment: {risk.confidence:.0%}
- Strategic Insight: {strategy.confidence:.0%}
- Market Intelligence: {market.confidence:.0%}
- Overall Synthesis: {synthesis.confidence:.0%}

### Data Sources
- Financial statements: {', '.join(map(str, company_data['balance_sheet'].get('Total Assets', {}).keys()))}
- Annual reports: {"Analyzed via RAG" if self.rag_service else "Not used"}
""")

        return "\n".join(report_sections)


# Async wrapper for easy usage
async def generate_multi_agent_report(company_data: Dict[str, Any]) -> str:
    """
    Simple wrapper for generating multi-agent report

    Usage:
        report = await generate_multi_agent_report(company_data)
    """
    orchestrator = MultiAgentOrchestrator(llm_client=get_llm_client())
    result = await orchestrator.generate_comprehensive_report(company_data)
    return result['report']
```

**Deliverable:** `src/intelligence/orchestrator/multi_agent_orchestrator.py`

---

## Week 8: Testing & Refinement

### Day 31-35: Comprehensive Testing

**Task 3.5: Test Multi-Agent System**

1. Generate multi-agent report for Grupa Azoty
2. Compare to single-agent report (from Priority 1)
3. Validate each agent's output quality
4. Check synthesis quality (does it integrate perspectives well?)
5. Iterate on agent prompts
6. Performance testing (is it reasonably fast with parallel execution?)

**Quality Metrics:**
- Agent output quality (each agent provides valuable insights)
- Synthesis quality (integrates perspectives, resolves contradictions)
- Report comprehensiveness (covers all dimensions)
- Actionability (clear recommendations for decision-makers)
- Speed (complete analysis in < 5 minutes)

**Deliverable:** Production-quality multi-agent reports

---

### Week 8 Deliverables

**Completed by End of Week 8:**
- ✅ 6 specialized analysis agents
- ✅ Multi-agent orchestrator
- ✅ Parallel agent execution (async)
- ✅ Synthesis logic
- ✅ Comprehensive report generation
- ✅ Quality validation
- ✅ Performance optimization

**Files Created:**
```
src/intelligence/agents/
├── base_agent.py
├── financial_health_agent.py
├── industry_context_agent.py
├── risk_assessment_agent.py
├── strategic_insight_agent.py
├── market_intelligence_agent.py
├── synthesis_agent.py
└── __init__.py

src/intelligence/orchestrator/
├── multi_agent_orchestrator.py
└── __init__.py

scripts/
└── test_multi_agent_report.py
```

---

# PRIORITY 4: Production Hardening & Advanced Features

**Timeline:** Week 9-12 (20-30 hours effort)
**Dependencies:** All previous priorities complete
**Risk Level:** 🟢 Low
**Value:** 🟡 Medium

## Week 9: External Data Integration

### Day 36-40: Add External Data Sources

**Task 4.1: Market Data Integration**
```python
# File: src/data/external/market_data_service.py

import yfinance as yf
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MarketDataService:
    """
    Fetch market data from external APIs
    """

    def get_stock_data(
        self,
        ticker: str,
        period: str = "5y"
    ) -> Dict:
        """
        Get stock price and financial data

        Args:
            ticker: Stock ticker symbol
            period: Time period (1y, 5y, max)

        Returns:
            Dict with price data, financials, etc.
        """
        try:
            stock = yf.Ticker(ticker)

            return {
                'price_history': stock.history(period=period),
                'info': stock.info,
                'financials': stock.financials,
                'balance_sheet': stock.balance_sheet,
                'cashflow': stock.cashflow,
                'recommendations': stock.recommendations
            }

        except Exception as e:
            logger.error(f"Failed to fetch market data for {ticker}: {e}")
            return {}

    def get_industry_benchmarks(
        self,
        industry_tickers: List[str]
    ) -> Dict:
        """
        Get benchmark data for industry comparison

        Args:
            industry_tickers: List of peer company tickers

        Returns:
            Dict with peer benchmarks
        """
        peer_data = {}

        for ticker in industry_tickers:
            data = self.get_stock_data(ticker, period="1y")
            if data:
                peer_data[ticker] = {
                    'market_cap': data['info'].get('marketCap'),
                    'pe_ratio': data['info'].get('trailingPE'),
                    'debt_to_equity': data['info'].get('debtToEquity'),
                    # Add more metrics
                }

        return peer_data
```

**Deliverable:** `src/data/external/market_data_service.py`

---

**Task 4.2: News Integration**
```python
# File: src/data/external/news_service.py

import requests
from typing import List, Dict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class NewsService:
    """
    Fetch recent news about companies
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"

    def get_company_news(
        self,
        company_name: str,
        days_back: int = 30,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Get recent news articles about a company

        Args:
            company_name: Company name to search
            days_back: How many days of news to fetch
            max_results: Max number of articles

        Returns:
            List of news articles with title, summary, url, date
        """
        if not self.api_key:
            logger.warning("News API key not configured")
            return []

        try:
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days_back)

            # Build request
            params = {
                'q': company_name,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'pageSize': max_results,
                'apiKey': self.api_key
            }

            response = requests.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()

            articles = response.json().get('articles', [])

            # Format results
            formatted = []
            for article in articles:
                formatted.append({
                    'title': article.get('title'),
                    'summary': article.get('description'),
                    'url': article.get('url'),
                    'published_at': article.get('publishedAt'),
                    'source': article.get('source', {}).get('name')
                })

            logger.info(f"Fetched {len(formatted)} news articles for {company_name}")
            return formatted

        except Exception as e:
            logger.error(f"Failed to fetch news: {e}")
            return []
```

**Deliverable:** `src/data/external/news_service.py`

---

## Week 10: Knowledge Graph (Optional)

### Day 41-45: Neo4j Knowledge Graph

**Task 4.3: Build Knowledge Graph**

Only implement if you want advanced relationship queries.

```python
# File: src/knowledge_graph/graph_service.py

from neo4j import GraphDatabase
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class CompanyKnowledgeGraph:
    """
    Knowledge graph for company relationships, competitors, supply chain
    """

    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_company(self, name: str, industry: str, country: str):
        """Add company node"""
        with self.driver.session() as session:
            session.run(
                "MERGE (c:Company {name: $name}) "
                "SET c.industry = $industry, c.country = $country",
                name=name, industry=industry, country=country
            )

    def add_competitor_relationship(self, company1: str, company2: str, market_share1: float, market_share2: float):
        """Add competition relationship"""
        with self.driver.session() as session:
            session.run(
                "MATCH (c1:Company {name: $company1}) "
                "MATCH (c2:Company {name: $company2}) "
                "MERGE (c1)-[r:COMPETES_WITH]->(c2) "
                "SET r.market_share_1 = $ms1, r.market_share_2 = $ms2",
                company1=company1, company2=company2, ms1=market_share1, ms2=market_share2
            )

    def get_competitors(self, company: str) -> List[str]:
        """Get all competitors of a company"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Company {name: $company})-[:COMPETES_WITH]-(comp:Company) "
                "RETURN comp.name as competitor",
                company=company
            )
            return [record["competitor"] for record in result]
```

**Deliverable:** `src/knowledge_graph/graph_service.py` (optional)

---

## Week 11: User Interface

### Day 46-50: Simple Web UI

**Task 4.4: Create Web Interface**

```python
# File: app.py (Streamlit UI)

import streamlit as st
from pathlib import Path
from src.intelligence.orchestrator.multi_agent_orchestrator import MultiAgentOrchestrator


def main():
    st.set_page_config(page_title="Company Intelligence System", layout="wide")

    st.title("🔍 Company Intelligence Report Generator")

    # Sidebar: Configuration
    with st.sidebar:
        st.header("Configuration")

        use_rag = st.checkbox("Use RAG (Document Context)", value=True)
        use_multi_agent = st.checkbox("Multi-Agent Analysis", value=True)

        st.markdown("---")
        st.markdown("### Upload Documents")

        uploaded_files = st.file_uploader(
            "Upload annual reports (PDF)",
            type=['pdf'],
            accept_multiple_files=True
        )

    # Main area: Company selection and analysis
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Company Selection")

        company_name = st.text_input("Company Name", value="Grupa Azoty S.A.")
        industry = st.text_input("Industry", value="Chemicals & Fertilizers")

        st.markdown("### Financial Data")
        st.info("Upload PDFs or enter data manually")

        # For MVP: just use pre-loaded data
        if st.button("Generate Report", type="primary"):
            with st.spinner("Generating comprehensive intelligence report..."):
                # Load company data
                company_data = load_company_data(company_name)

                # Generate report
                if use_multi_agent:
                    orchestrator = MultiAgentOrchestrator(
                        llm_client=get_llm_client(),
                        use_rag=use_rag
                    )
                    result = await orchestrator.generate_comprehensive_report(company_data)
                    report = result['report']
                else:
                    # Single-agent fallback
                    report = generate_single_agent_report(company_data)

                # Display
                st.session_state['report'] = report

    with col2:
        st.header("Intelligence Report")

        if 'report' in st.session_state:
            st.markdown(st.session_state['report'])

            # Download button
            st.download_button(
                label="Download Report (Markdown)",
                data=st.session_state['report'],
                file_name=f"{company_name}_report.md",
                mime="text/markdown"
            )
        else:
            st.info("Generate a report to see results here")


if __name__ == "__main__":
    main()
```

**Deliverable:** Streamlit web interface

---

## Week 12: Production Hardening

### Day 51-55: Error Handling, Monitoring, Documentation

**Task 4.5: Production Readiness**

1. **Error Handling**
   - Retry logic for LLM calls
   - Graceful degradation (if RAG fails, continue without it)
   - Input validation

2. **Monitoring**
   - Logging (structured logs)
   - Performance metrics (analysis time, token usage)
   - Quality metrics (confidence scores, validation results)

3. **Documentation**
   - User guide
   - API documentation
   - Deployment guide

4. **Testing**
   - Unit tests for agents
   - Integration tests for orchestrator
   - End-to-end test for full report generation

**Deliverable:** Production-ready system

---

# 🎯 SUMMARY & MILESTONES

## Milestone Checklist

### ✅ Milestone 1: Prototype Working (End of Week 2)
- [ ] Single-agent intelligence report generator
- [ ] Template-based reports
- [ ] LLM integration (Claude or local)
- [ ] Generated sample report for Grupa Azoty
- [ ] **Demo:** Show working intelligence report

### ✅ Milestone 2: RAG-Enhanced (End of Week 4)
- [ ] Document ingestion pipeline
- [ ] Vector database operational
- [ ] RAG queries working
- [ ] Reports cite sources from annual reports
- [ ] **Demo:** Compare RAG vs non-RAG report quality

### ✅ Milestone 3: Multi-Agent System (End of Week 8)
- [ ] 6 specialized agents implemented
- [ ] Multi-agent orchestration working
- [ ] Synthesis agent integrating perspectives
- [ ] Comprehensive reports (15-20 pages)
- [ ] **Demo:** Full multi-perspective intelligence report

### ✅ Milestone 4: Production System (End of Week 12)
- [ ] External data integration (market, news)
- [ ] Web UI deployed
- [ ] Error handling and monitoring
- [ ] Documentation complete
- [ ] **Demo:** Production system generating reports on-demand

---

## Resource Requirements

### Infrastructure
- **LLM Access:**
  - Option A: Claude API (recommended for quality)
  - Option B: Local LLM (your current setup)
  - Cost estimate: ~$5-20 per comprehensive report (Claude)

- **Vector Database:**
  - Qdrant (self-hosted or cloud)
  - Storage: ~1GB per 1000 pages of documents

- **Optional:**
  - Neo4j (if implementing knowledge graph)
  - Streamlit hosting (for web UI)

### External APIs (Optional)
- Market data: Yahoo Finance (free) or paid alternatives
- News: NewsAPI ($0-449/mo depending on volume)
- Industry data: Manual collection or paid subscriptions

---

## Success Criteria

**System must:**
1. Generate 15-20 page intelligence reports automatically
2. Include multi-perspective analysis (financial, industry, risk, strategy, market)
3. Cite sources from company documents (via RAG)
4. Provide clear investment recommendation (BUY/HOLD/SELL)
5. Complete analysis in < 10 minutes
6. Achieve 80%+ quality score (vs manual analyst benchmark)

**Reports must:**
1. Be actionable for decision-makers
2. Cite specific numbers and trends
3. Identify both opportunities and risks
4. Provide bull/bear/base case scenarios
5. Be professional, investment-grade quality

---

## Next Steps

**Immediate Actions:**
1. Review roadmap and confirm priorities
2. Set up development environment (LLM access, vector DB)
3. Start Priority 1: Prototype single-agent system
4. Schedule milestones and demos

**Week 1 Focus:**
- Implement basic intelligence service
- Create prompt templates
- Test with Grupa Azoty data
- Generate first automated intelligence report

---

**Last Updated:** 2025-11-06
**Status:** Ready to begin implementation
**Estimated Total Effort:** 75-105 hours over 12 weeks
**MVP Timeline:** 4 weeks (Priorities 1-2)
**Production Timeline:** 12 weeks (all priorities)
