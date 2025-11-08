# Priority 3: Multi-Depth Report Architecture Design

**Date**: 2025-11-07
**Status**: Design Phase
**Goal**: Enable comprehensive analysis of 200+ page documents with dual-depth reporting

---

## Problem Statement

**Current Issue**: 200+ page source documents compressed to 2-3 page reports (100:1 ratio) lose critical information and nuance needed for serious investment decisions.

**User Requirement**:
> "Reports that agents produce cannot be 2-3 pages long if they analyze 200 pages of original text. They need to contain more data, and be more descriptive and multi-angle. There is a place for a short version report and a long version report."

**Solution**: Hierarchical two-tier reporting system that generates BOTH executive summaries AND comprehensive analyses from the same source data.

---

## 1. Report Mode Enumeration

### ReportMode Enum

```python
from enum import Enum

class ReportMode(Enum):
    """Report depth modes for intelligence generation"""

    EXECUTIVE = "executive"
    """
    Executive Mode: Quick decision-making summary
    - Length: 2-3 pages (~3,000 tokens)
    - Use case: Board presentations, quick reviews, screening
    - Focus: Key findings, headline numbers, clear recommendation
    - RAG queries: 3-5 per agent (current)
    """

    COMPREHENSIVE = "comprehensive"
    """
    Comprehensive Mode: Detailed multi-angle analysis
    - Length: 20-30 pages (~15,000-18,000 tokens)
    - Use case: Due diligence, deep analysis, research reports
    - Focus: Evidence-based analysis, detailed rationale, citations
    - RAG queries: 10-15 per agent (enhanced)
    """

    CUSTOM = "custom"
    """
    Custom Mode: User-defined depth
    - Length: Variable (user specifies token budget per agent)
    - Use case: Special purpose reports, specific depth requirements
    - Focus: Flexible based on user needs
    - RAG queries: Configurable
    """
```

---

## 2. Token Budget Allocation

### Executive Mode (Current System)

**Total Output**: ~3,000 tokens (2-3 pages)

| Agent | Token Budget | Page Estimate | Purpose |
|-------|--------------|---------------|---------|
| Agent 1: Financial Health | 500 | 0.5 pages | Key ratios, headline score |
| Agent 2: Risk Assessment | 500 | 0.5 pages | Top 3 risks summary |
| Agent 3: Industry Context | 500 | 0.5 pages | Competitive position |
| Agent 4: Strategic Evaluation | 500 | 0.5 pages | Strategy assessment |
| Agent 5: Market Intelligence | 500 | 0.5 pages | Key catalysts |
| Agent 6: Synthesis | 500 | 0.5 pages | Final recommendation |
| **TOTAL** | **3,000** | **2-3 pages** | Complete executive summary |

**Characteristics**:
- Quick read (5-10 minutes)
- Highlights only
- Minimal citations
- Clear actionable recommendation

### Comprehensive Mode (NEW)

**Total Output**: ~15,000-18,000 tokens (20-30 pages)

| Agent | Token Budget | Page Estimate | Purpose |
|-------|--------------|---------------|---------|
| Agent 1: Financial Health | 2,500-3,000 | 5-7 pages | Deep financial dive with trend analysis |
| Agent 2: Risk Assessment | 2,000-2,500 | 4-6 pages | Detailed risk scenarios and mitigation |
| Agent 3: Industry Context | 2,000-2,500 | 4-5 pages | Competitive dynamics and benchmarking |
| Agent 4: Strategic Evaluation | 1,500-2,000 | 3-4 pages | Strategy analysis and management quality |
| Agent 5: Market Intelligence | 1,500-2,000 | 3-4 pages | Market trends and forward-looking analysis |
| Agent 6: Synthesis | 1,500-2,000 | 2-3 pages | Integrated view and recommendation rationale |
| Appendices | 1,000 | 2 pages | Key data tables, methodology notes |
| **TOTAL** | **15,000-18,000** | **20-30 pages** | Complete comprehensive analysis |

**Characteristics**:
- In-depth read (45-60 minutes)
- Evidence-based with citations
- Multiple perspectives per topic
- Detailed rationale for all conclusions

### Custom Mode (Future)

**Total Output**: Variable (user-specified)

User provides:
```python
custom_config = {
    "financial_health": 1500,    # Tokens for Agent 1
    "risk_assessment": 1000,     # Tokens for Agent 2
    "industry_context": 800,     # Tokens for Agent 3
    "strategic_evaluation": 600, # Tokens for Agent 4
    "market_intelligence": 600,  # Tokens for Agent 5
    "synthesis": 500             # Tokens for Agent 6
}
```

**Use cases**:
- Focus reports (deep dive on one aspect, lighter on others)
- Budget-constrained analysis
- Special purpose reports

---

## 3. Agent Output Schema

### Dual-Depth Agent Output Structure

Each agent will produce structured output supporting both depths:

```python
{
    "agent": "Financial Health",
    "mode": "comprehensive",  # or "executive"

    # Executive summary (always present, mode-agnostic)
    "executive_summary": {
        "key_findings": [
            "Finding 1 with specific number",
            "Finding 2 with specific number",
            "Finding 3 with specific number"
        ],
        "score": 38,
        "score_rationale": "Brief 1-2 sentence rationale",
        "confidence": "high",  # high/medium/low
        "word_count": 450
    },

    # Comprehensive analysis (only in comprehensive mode)
    "comprehensive_analysis": {
        "sections": {
            "balance_sheet_analysis": {
                "content": "Detailed multi-paragraph analysis...",
                "key_metrics": [...],
                "citations": [
                    {"source": "Annual Report 2024", "page": 87, "quote": "..."}
                ],
                "word_count": 800
            },
            "income_statement_analysis": {
                "content": "...",
                "key_metrics": [...],
                "citations": [...],
                "word_count": 700
            },
            "cash_flow_analysis": {
                "content": "...",
                "key_metrics": [...],
                "citations": [...],
                "word_count": 600
            },
            "ratio_analysis": {
                "content": "...",
                "benchmarks": [...],
                "citations": [...],
                "word_count": 500
            },
            "score_breakdown": {
                "content": "...",
                "methodology": "...",
                "sensitivity_analysis": "...",
                "word_count": 400
            }
        },
        "total_word_count": 3000
    },

    # Metadata for debugging and quality control
    "metadata": {
        "rag_queries_executed": 12,
        "rag_chunks_retrieved": 48,
        "generation_time_seconds": 15.3,
        "token_count_actual": 2847,
        "token_count_target": 3000
    }
}
```

---

## 4. RAG Query Strategy

### Executive Mode RAG (Current)

**Queries per agent**: 3-5 queries
**Total chunks retrieved**: 15-25 per agent
**Strategy**: High-precision, top results only

**Example (Financial Health Agent)**:
```python
rag_queries_executive = [
    "balance sheet assets liabilities 2024 2023 2022",
    "revenue profit margin operating income trends",
    "debt levels liquidity working capital"
]
```

**Characteristics**:
- Broad queries covering main topics
- Top 5 results per query (25 chunks total)
- Rerank and take top 15 overall
- Focus on latest year data

### Comprehensive Mode RAG (NEW)

**Queries per agent**: 10-15 queries
**Total chunks retrieved**: 50-75 per agent
**Strategy**: Deep coverage, multiple angles, historical depth

**Example (Financial Health Agent)**:
```python
rag_queries_comprehensive = [
    # Balance Sheet Deep Dive (4 queries)
    "current assets breakdown cash receivables inventory 2024 2023 2022",
    "non-current assets property plant equipment intangibles",
    "current liabilities short-term debt payables obligations",
    "long-term debt structure maturity schedule interest rates",

    # Income Statement Deep Dive (3 queries)
    "revenue breakdown by segment product geography trend analysis",
    "operating costs COGS SG&A R&D expenses margin analysis",
    "EBITDA operating profit net income profitability trends",

    # Cash Flow Deep Dive (3 queries)
    "operating cash flow free cash flow generation quality",
    "investing activities capex acquisitions asset sales",
    "financing activities debt issuance repayments dividends",

    # Ratios and Benchmarking (3 queries)
    "liquidity ratios current ratio quick ratio working capital",
    "leverage ratios debt-to-equity interest coverage solvency",
    "profitability ratios ROE ROA margins efficiency"
]
```

**Characteristics**:
- Specific, targeted queries
- Top 5 results per query (75 chunks total max)
- Rerank and take top 40-50 overall
- Multi-year historical data
- Segment-level granularity

### Query Expansion Strategy

**For comprehensive mode**, each agent should:

1. **Query Planning Phase**:
   - Identify 3-4 major topics per agent
   - Generate 3-5 sub-queries per topic
   - Total: 10-15 targeted queries

2. **Retrieval Phase**:
   - Execute queries in parallel (if possible)
   - Retrieve top 5 chunks per query
   - Deduplicate chunks

3. **Reranking Phase**:
   - Use BGE reranker on all retrieved chunks
   - Select top 40-50 chunks based on relevance
   - Organize by topic

4. **Citation Phase**:
   - Track source document + page for each chunk
   - Include citations in comprehensive analysis

---

## 5. Comprehensive Report Template Structure

### Part I: Financial Health Analysis (5-7 pages, 2500-3000 tokens)

**Sections**:

1. **Executive Summary** (200 tokens)
   - Financial Health Score: XX/100
   - Key finding #1
   - Key finding #2
   - Key finding #3

2. **Balance Sheet Deep Dive** (800 tokens)
   - Asset composition and quality
   - Current assets: Cash, receivables, inventory (trends, quality issues)
   - Non-current assets: PP&E, intangibles (valuations, impairments)
   - Liability structure
   - Current liabilities: Short-term debt, payables (maturity profile)
   - Long-term debt: Structure, covenants, interest rates
   - Equity position: Retained earnings, capital structure
   - Citations: [Annual Report 2024, p.87], [Financial Statements 2023, p.45]

3. **Income Statement Analysis** (700 tokens)
   - Revenue trends and drivers
   - Segment breakdown and performance
   - Geographic/product mix changes
   - Operating cost structure
   - COGS trends and gross margin evolution
   - SG&A efficiency
   - R&D investment levels
   - Profitability analysis
   - EBITDA margin trends
   - Operating leverage
   - Net income quality (one-time items, adjustments)

4. **Cash Flow Analysis** (600 tokens)
   - Operating cash flow generation
   - Quality of earnings (OCF vs Net Income)
   - Working capital management
   - Investing activities
   - CapEx trends and intensity
   - Acquisitions and disposals
   - Financing activities
   - Debt refinancing and capital raises
   - Dividend policy
   - Free cash flow generation and sustainability

5. **Financial Ratios & Benchmarking** (500 tokens)
   - Liquidity ratios vs industry peers
   - Leverage ratios vs sector norms
   - Profitability ratios vs competitors
   - Efficiency ratios (asset turnover, inventory days)
   - Trend analysis (3-5 year view)
   - Best-in-class comparisons

6. **Score Breakdown Methodology** (400 tokens)
   - How the XX/100 score was calculated
   - Component scores and weightings
   - Key drivers of score
   - Sensitivity analysis (what would change score)
   - Comparison to previous periods

**Citation Requirements**: Every data point cited to source document and page number.

### Part II: Risk Assessment (4-6 pages, 2000-2500 tokens)

**Sections**:

1. **Executive Summary** (200 tokens)

2. **Financial Risks** (600 tokens)
   - Liquidity risk (detailed analysis)
   - Solvency risk (debt structure, covenants)
   - Credit risk (counterparty exposures)
   - Interest rate risk
   - Currency risk

3. **Operational Risks** (600 tokens)
   - Supply chain vulnerabilities
   - Production risks (capacity, efficiency)
   - Key dependencies (suppliers, customers)
   - Technology and innovation risks

4. **Market Risks** (500 tokens)
   - Demand volatility
   - Competitive threats
   - Pricing pressures
   - Market share erosion risks

5. **Strategic Risks** (400 tokens)
   - Management execution risk
   - M&A integration risks
   - Regulatory and compliance risks

6. **Risk Mitigation Assessment** (300 tokens)
   - Existing risk management practices
   - Hedging strategies
   - Contingency plans
   - Recommendations for improvement

### Part III: Industry Context (4-5 pages, 2000-2500 tokens)

**Sections**:

1. **Executive Summary** (200 tokens)

2. **Industry Structure & Dynamics** (700 tokens)
   - Porter's Five Forces analysis
   - Industry growth trends and drivers
   - Regulatory environment
   - Technology disruption potential

3. **Competitive Positioning** (700 tokens)
   - Market share analysis
   - Competitive strengths (moats, advantages)
   - Competitive weaknesses (vulnerabilities)
   - Comparison to top 3-5 competitors

4. **Value Chain Analysis** (500 tokens)
   - Upstream dynamics (suppliers, raw materials)
   - Company's position in value chain
   - Downstream dynamics (customers, distribution)

5. **Industry Outlook** (400 tokens)
   - Growth forecasts
   - Secular trends (tailwinds/headwinds)
   - Emerging opportunities and threats

### Part IV: Strategic Evaluation (3-4 pages, 1500-2000 tokens)

**Sections**:

1. **Executive Summary** (200 tokens)

2. **Corporate Strategy Assessment** (600 tokens)
   - Strategic priorities and goals
   - Capital allocation strategy
   - M&A strategy and track record
   - Geographic expansion plans
   - Product innovation roadmap

3. **Management Quality** (500 tokens)
   - Leadership team assessment
   - Track record of execution
   - Communication transparency
   - Corporate governance

4. **Strategic Initiatives Evaluation** (400 tokens)
   - Current major initiatives
   - Likelihood of success
   - Resource requirements
   - Timeline and milestones

### Part V: Market Intelligence (3-4 pages, 1500-2000 tokens)

**Sections**:

1. **Executive Summary** (200 tokens)

2. **Market Catalysts** (600 tokens)
   - Positive catalysts (near-term and long-term)
   - Negative catalysts (risks to outlook)
   - Probability and impact assessment

3. **Valuation Context** (500 tokens)
   - Current valuation metrics (P/E, EV/EBITDA, P/B)
   - Historical valuation ranges
   - Peer comparison
   - Implied expectations

4. **Scenario Analysis** (400 tokens)
   - Bull case: Key assumptions and outcomes
   - Base case: Most likely scenario
   - Bear case: Downside risks materialized

### Part VI: Synthesis & Investment Recommendation (2-3 pages, 1500-2000 tokens)

**Sections**:

1. **Integrated Analysis** (600 tokens)
   - How financial health, risks, industry, strategy, and market factors interact
   - Key trade-offs and considerations
   - Holistic assessment

2. **Investment Thesis** (500 tokens)
   - Core investment argument
   - Why buy/hold/sell?
   - What needs to be believed for this to work?

3. **Investment Recommendation** (400 tokens)
   - **Recommendation: [STRONG BUY / BUY / HOLD / SELL / STRONG SELL]**
   - Price target (if applicable)
   - Investment horizon
   - Key monitoring points
   - Triggers for re-evaluation

4. **Disclaimer & Methodology** (200 tokens)
   - Data sources and limitations
   - Methodology notes
   - Assumptions and caveats

### Appendices (2 pages, 1000 tokens)

1. **Key Financial Tables**
2. **Ratio Summary Table**
3. **Methodology Notes**
4. **Glossary of Terms**
5. **Data Sources and Citations**

---

## 6. Implementation Requirements

### Modified Service Signature

```python
class MultiAgentIntelligenceService:

    def generate_intelligence_report(
        self,
        company_data: Dict[str, Any],
        output_format: str = "markdown",
        report_mode: ReportMode = ReportMode.EXECUTIVE  # NEW PARAMETER
    ) -> Dict[str, Any]:
        """
        Generate multi-agent intelligence report

        Args:
            company_data: Financial data dict
            output_format: Output format (markdown, json, pdf)
            report_mode: Report depth (executive/comprehensive/custom)
        """
```

### Token Budget Configuration

```python
# Token budgets by mode
TOKEN_BUDGETS = {
    ReportMode.EXECUTIVE: {
        "financial_health": 500,
        "risk_assessment": 500,
        "industry_context": 500,
        "strategic_evaluation": 500,
        "market_intelligence": 500,
        "synthesis": 500,
        "total": 3000
    },
    ReportMode.COMPREHENSIVE: {
        "financial_health": 3000,
        "risk_assessment": 2500,
        "industry_context": 2500,
        "strategic_evaluation": 2000,
        "market_intelligence": 2000,
        "synthesis": 2000,
        "appendices": 1000,
        "total": 15000
    }
}

# RAG query counts by mode
RAG_QUERY_CONFIG = {
    ReportMode.EXECUTIVE: {
        "queries_per_agent": 5,
        "chunks_per_query": 5,
        "total_chunks_after_rerank": 15
    },
    ReportMode.COMPREHENSIVE: {
        "queries_per_agent": 12,
        "chunks_per_query": 5,
        "total_chunks_after_rerank": 45
    }
}
```

### Citation Tracking System

```python
class Citation:
    """Track source citations for comprehensive reports"""

    def __init__(self, source_doc: str, page: int, chunk_text: str):
        self.source_doc = source_doc
        self.page = page
        self.chunk_text = chunk_text
        self.citation_id = f"{source_doc}_p{page}"

    def format_inline(self) -> str:
        """Format for inline citation: [Annual Report 2024, p.87]"""
        return f"[{self.source_doc}, p.{self.page}]"

    def format_footnote(self, index: int) -> str:
        """Format for footnote: [1] Annual Report 2024, page 87: "..." """
        excerpt = self.chunk_text[:100] + "..." if len(self.chunk_text) > 100 else self.chunk_text
        return f"[{index}] {self.source_doc}, page {self.page}: \"{excerpt}\""


class CitationManager:
    """Manage citations across comprehensive report"""

    def __init__(self):
        self.citations: List[Citation] = []
        self.citation_map: Dict[str, int] = {}  # citation_id -> index

    def add_citation(self, citation: Citation) -> str:
        """Add citation and return inline reference"""
        if citation.citation_id not in self.citation_map:
            self.citations.append(citation)
            self.citation_map[citation.citation_id] = len(self.citations)

        return citation.format_inline()

    def generate_bibliography(self) -> str:
        """Generate bibliography section for report appendix"""
        lines = ["## References\n"]
        for i, citation in enumerate(self.citations, 1):
            lines.append(citation.format_footnote(i))
        return "\n".join(lines)
```

---

## 7. Success Criteria

### Phase 1 (Architecture Design) - ✅ THIS DOCUMENT

- [x] ReportMode enum defined
- [x] Token budgets allocated for executive and comprehensive modes
- [x] Agent output schema designed (dual-depth structure)
- [x] RAG query strategy defined for both modes
- [x] Comprehensive report template structure documented
- [x] Citation tracking system designed
- [x] Implementation requirements specified

### Phase 2 (Comprehensive Prompts) - NEXT

- [ ] Create comprehensive Financial Health prompts
- [ ] Create comprehensive Risk Assessment prompts
- [ ] Create comprehensive Industry Context prompts
- [ ] Create comprehensive Strategic Evaluation prompts
- [ ] Create comprehensive Market Intelligence prompts
- [ ] Create comprehensive Synthesis prompts
- [ ] Each prompt includes section structure and word count guidance

### Phase 3 (Executive Optimization) - PENDING

- [ ] Optimize current executive prompts for clarity
- [ ] Add score-to-recommendation mapping
- [ ] Include few-shot examples
- [ ] Test inconsistency rate improvement

### Phase 4 (Implementation) - PENDING

- [ ] Add report_mode parameter to service
- [ ] Implement token budget routing
- [ ] Implement comprehensive prompt routing
- [ ] Implement citation tracking
- [ ] Update report formatter for dual modes

### Phase 5 (Testing) - PENDING

- [ ] Test executive mode (ensure no regression)
- [ ] Test comprehensive mode with Azoty data
- [ ] Validate token counts match budgets
- [ ] Validate citations are tracked correctly
- [ ] Compare executive vs comprehensive output quality

### Phase 6 (Integration) - PENDING

- [ ] Update all calling scripts to support report_mode
- [ ] Add mode selection to CLI/API
- [ ] Document usage examples
- [ ] Update benchmark scripts

---

## 8. Performance Considerations

### Generation Time Estimates

**Executive Mode** (current):
- Agent 1-6: ~80 seconds total
- Report formatting: ~5 seconds
- **Total: ~85 seconds**

**Comprehensive Mode** (estimated):
- Agent 1-6: ~200 seconds total (more RAG queries, longer generation)
- Report formatting: ~10 seconds
- Citation processing: ~5 seconds
- **Total: ~220 seconds (3.5-4 minutes)**

**Optimization Opportunities** (future):
- Parallel agent execution: 220s → 90s
- Concurrent RAG queries: Additional 20% improvement
- Batching: Linear scaling for multiple companies

### Memory Considerations

**Executive Mode**:
- RAG context: ~15 chunks × 512 tokens = 7,680 tokens
- Prompt + data: ~2,000 tokens
- Generation: 500 tokens
- **Total per agent: ~10k tokens (well within 44k window)**

**Comprehensive Mode**:
- RAG context: ~45 chunks × 512 tokens = 23,040 tokens
- Prompt + data: ~3,000 tokens
- Generation: 3,000 tokens
- **Total per agent: ~29k tokens (fits in 44k window with margin)**

**Conclusion**: Both modes fit comfortably within 44k context window of openai/gpt-oss-20b.

---

## 9. Next Steps

1. **Complete Phase 1**: ✅ This document serves as Phase 1 completion
2. **Begin Phase 2**: Create comprehensive prompt templates for each agent
3. **Create test plan**: Define how to validate comprehensive mode quality
4. **Update roadmap**: Mark Phase 1 complete in INTELLIGENCE_SYSTEM_ROADMAP.md

---

**Architecture Design Status**: ✅ COMPLETE
**Ready for**: Phase 2 - Comprehensive Prompt Development
**Estimated Phase 2 Effort**: 2-3 days
