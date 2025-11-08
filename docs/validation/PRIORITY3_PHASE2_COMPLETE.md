# Priority 3 Phase 2: Comprehensive Prompt Development - COMPLETE ✅

**Date**: 2025-11-07
**Status**: **COMPLETE**
**Files Created**: 1 (~1,600 lines)
**Implementation Time**: ~1 hour

---

## Summary

Successfully created comprehensive prompt templates for all 6 agents, enabling detailed 20-30 page investment research reports. Each agent has structured prompts with specific section requirements, token budgets, and output guidelines.

---

## Deliverables

### File Created: `src/intelligence/prompts/comprehensive_prompts.py`

**Total Lines**: ~1,600 lines
**Structure**:
- Agent 1-6 comprehensive system prompts
- Agent 1-6 comprehensive prompt generation functions
- RAG context formatting helper
- Complete documentation

---

## Agent Prompt Specifications

### Agent 1: Financial Health Analysis (COMPREHENSIVE)

**Target Output**: 2,500-3,000 tokens (5-7 pages)

**System Prompt**: `FINANCIAL_HEALTH_COMPREHENSIVE_SYSTEM`
- Role: Senior financial analyst with 20 years experience
- Focus: Deep dive, multi-angle analysis, evidence-based

**Function**: `create_comprehensive_financial_health_prompt()`
- Parameters: company_name, industry, balance_sheet_table, income_statement_table, ratios_table, rag_context
- Returns: Comprehensive prompt with 6 structured sections

**Report Structure**:
1. Executive Summary (200 tokens)
   - Financial Health Score: XX/100
   - 3-4 key findings
2. Balance Sheet Deep Dive (800 tokens)
   - Asset analysis (current + non-current)
   - Liability analysis (current + long-term)
   - Equity position
3. Income Statement Analysis (700 tokens)
   - Revenue analysis
   - Operating cost structure
   - Profitability analysis
4. Cash Flow Analysis (600 tokens)
   - Operating cash flow
   - Investing activities
   - Financing activities
   - Free cash flow
5. Financial Ratios & Benchmarking (500 tokens)
   - Liquidity ratios
   - Leverage ratios
   - Profitability ratios
   - Efficiency ratios
   - Trend summary
6. Financial Health Score Breakdown (400 tokens)
   - Score calculation methodology
   - Score drivers
   - Sensitivity analysis
   - Historical evolution

**Output Requirements**:
- Specific numbers and values (not directional statements)
- Evidence-based (reference financial data)
- Citations for RAG context
- Multi-year perspective (3+ years)
- Balanced analysis (strengths and weaknesses)

---

### Agent 2: Risk Assessment (COMPREHENSIVE)

**Target Output**: 2,000-2,500 tokens (4-6 pages)

**System Prompt**: `RISK_ASSESSMENT_COMPREHENSIVE_SYSTEM`
- Role: Corporate risk assessment specialist
- Focus: Systematic, quantitative, scenario-driven

**Function**: `create_comprehensive_risk_assessment_prompt()`
- Parameters: company_name, industry, financial_health_analysis, balance_sheet_table, rag_context
- Returns: Comprehensive risk prompt with 6 structured sections

**Report Structure**:
1. Executive Summary (200 tokens)
   - Overall risk rating
   - Top 3 material risks
   - Risk trends
2. Financial Risks (600 tokens)
   - Liquidity risk (severity, indicators, scenarios, mitigation)
   - Solvency risk
   - Credit risk
   - Interest rate risk
   - FX risk
3. Operational Risks (600 tokens)
   - Supply chain risk
   - Production risk
   - Key dependencies (customer concentration, key person, technology)
4. Market Risks (500 tokens)
   - Demand risk
   - Competitive risk
   - Pricing risk
   - Market share risk
5. Strategic Risks (400 tokens)
   - Management execution risk
   - M&A and integration risk
   - Regulatory and compliance risk
6. Risk Mitigation Assessment (300 tokens)
   - Existing risk management practices
   - Adequacy assessment
   - Recommendations

**Risk Quantification**:
- Severity: Low/Medium/High/Critical
- Scenarios: "What if revenues drop 20%? Can company meet obligations?"
- Mitigation: Assessment of existing controls

---

### Agent 3: Industry Context (COMPREHENSIVE)

**Target Output**: 2,000-2,500 tokens (4-5 pages)

**System Prompt**: `INDUSTRY_CONTEXT_COMPREHENSIVE_SYSTEM`
- Role: Industry analyst specializing in competitive dynamics
- Focus: Structured, comparative, forward-looking

**Function**: `create_comprehensive_industry_context_prompt()`
- Parameters: company_name, industry, financial_health_analysis, risk_assessment, rag_context
- Returns: Comprehensive industry prompt with 7 structured sections

**Report Structure**:
1. Executive Summary (200 tokens)
   - Industry attractiveness
   - Company's competitive position
   - Key industry themes
2. Industry Structure & Dynamics (700 tokens)
   - **Porter's Five Forces**:
     - Threat of new entrants (140 tokens)
     - Bargaining power of suppliers (140 tokens)
     - Bargaining power of buyers (140 tokens)
     - Threat of substitutes (140 tokens)
     - Industry rivalry (140 tokens)
3. Competitive Landscape & Positioning (700 tokens)
   - Market structure
   - Competitive positioning (strengths/weaknesses)
   - Key competitors comparison
4. Value Chain Analysis (500 tokens)
   - Upstream dynamics
   - Company's position in value chain
   - Downstream dynamics
5. Industry Growth Trends & Outlook (500 tokens)
   - Historical growth
   - Growth forecast
   - Secular trends (tailwinds/headwinds)
   - Technology & disruption
6. Regulatory & Policy Environment (300 tokens)
   - Current regulatory framework
   - Regulatory outlook
7. Industry Outlook & Key Themes (300 tokens)
   - Overall industry outlook
   - Key investment themes

---

### Agent 4: Strategic Evaluation (COMPREHENSIVE)

**Target Output**: 1,500-2,000 tokens (3-4 pages)

**System Prompt**: `STRATEGIC_EVALUATION_COMPREHENSIVE_SYSTEM`
- Role: Strategy consultant
- Focus: Critical, evidence-based, forward-looking

**Function**: `create_comprehensive_strategic_evaluation_prompt()`
- Parameters: company_name, industry, financial_health_analysis, risk_assessment, industry_context, rag_context
- Returns: Comprehensive strategic prompt with 5 structured sections

**Report Structure**:
1. Executive Summary (200 tokens)
   - Strategic quality rating
   - Management execution rating
   - Key strategic priorities
2. Corporate Strategy Assessment (600 tokens)
   - Strategic goals & priorities (200 tokens)
   - Capital allocation strategy (200 tokens)
   - Growth strategy (200 tokens)
3. Management Quality & Execution (500 tokens)
   - Leadership team assessment (150 tokens)
   - Track record of execution (200 tokens)
   - Communication & transparency (150 tokens)
4. Strategic Initiatives Evaluation (500 tokens)
   - Current major initiatives (300 tokens) - 2-4 initiatives evaluated
   - Innovation & R&D strategy (200 tokens)
5. Governance & Organizational Capability (400 tokens)
   - Corporate governance (150 tokens)
   - Organizational capabilities (150 tokens)
   - Organizational culture (100 tokens)

---

### Agent 5: Market Intelligence (COMPREHENSIVE)

**Target Output**: 1,500-2,000 tokens (3-4 pages)

**System Prompt**: `MARKET_INTELLIGENCE_COMPREHENSIVE_SYSTEM`
- Role: Market intelligence analyst
- Focus: Forward-looking, catalyst-driven, scenario-based

**Function**: `create_comprehensive_market_intelligence_prompt()`
- Parameters: company_name, industry, financial_health_analysis, risk_assessment, industry_context, strategic_evaluation, rag_context
- Returns: Comprehensive market intelligence prompt with 5 structured sections

**Report Structure**:
1. Executive Summary (200 tokens)
   - Catalyst outlook
   - Valuation assessment
   - Base case view
2. Positive Catalysts (400 tokens)
   - Near-term catalysts (0-12 months) - 3-5 catalysts with timeline, probability, impact
   - Long-term catalysts (1-3 years) - 2-3 structural drivers
3. Negative Catalysts & Risks (400 tokens)
   - Near-term risks (0-12 months) - 3-5 risks
   - Long-term headwinds (1-3 years) - 2-3 structural pressures
4. Valuation Context (400 tokens)
   - Current valuation metrics (P/E, EV/EBITDA, P/B)
   - Peer valuation comparison (table format)
   - Implied expectations
5. Scenario Analysis (500 tokens)
   - Bull case (150 tokens) - assumptions, probability, return, triggers
   - Base case (150 tokens)
   - Bear case (150 tokens)
   - Expected value (50 tokens) - weighted expected return

---

### Agent 6: Synthesis (COMPREHENSIVE)

**Target Output**: 1,500-2,000 tokens (2-3 pages)

**System Prompt**: `SYNTHESIS_COMPREHENSIVE_SYSTEM`
- Role: Senior investment analyst
- Focus: Holistic, balanced, decisive, actionable

**Function**: `create_comprehensive_synthesis_prompt()`
- Parameters: company_name, industry, [all 5 agent outputs], financial_health_score
- Returns: Comprehensive synthesis prompt with 5 structured sections

**Report Structure**:
1. Integrated Analysis (600 tokens)
   - How factors interact (300 tokens)
   - Key trade-offs and tensions (200 tokens)
   - What must be believed (100 tokens)
2. Investment Thesis (500 tokens)
   - Bull case summary (200 tokens) - top 3 arguments
   - Bear case summary (200 tokens) - top 3 arguments
   - Which case is more compelling? (100 tokens)
3. Investment Recommendation (400 tokens)
   - Recommendation (150 tokens) - STRONG BUY/BUY/HOLD/SELL/STRONG SELL
   - Risk/reward assessment (100 tokens)
   - Who should invest? (150 tokens)
4. Key Monitoring Points (300 tokens)
   - Critical metrics to watch (150 tokens)
   - Re-evaluation triggers (150 tokens) - positive and negative
5. Conclusion (200 tokens)
   - Summary assessment (100 tokens)
   - Final thought (100 tokens)

**CRITICAL FEATURE**: Score-to-Recommendation Mapping
- 80-100: Excellent → BUY/STRONG BUY
- 60-79: Good → BUY/HOLD
- 40-59: Weak → HOLD/SELL
- 20-39: Poor → SELL/STRONG SELL
- 0-19: Critical → STRONG SELL

Ensures consistency between financial health score and final recommendation.

---

## Helper Functions

### `format_rag_context_with_citations(rag_results: List[Dict]) -> str`

Formats RAG retrieval results with citation markers:
```
**Context 1** [Source: Annual Report 2024, Page: 87, Relevance: 0.92]
{text}

---

**Context 2** [Source: Financial Statements 2023, Page: 45, Relevance: 0.88]
{text}
```

**Usage**: Pass to comprehensive prompt functions as `rag_context` parameter.

---

## Key Design Principles

### 1. Structured Output
Every agent has clear section headings with token budgets:
- Main sections with subsections
- Token allocation per subsection
- Markdown formatting requirements

### 2. Evidence-Based Analysis
- Require specific numbers, not vague statements
- ✅ "Current ratio declined from 2.1 to 1.3"
- ❌ "Current ratio has declined"

### 3. Citation Requirements
When referencing RAG context:
- Format: "According to the Annual Report 2024, page 87..."
- Or: "Management noted in the 2024 report (p.45) that..."

### 4. Multi-Perspective
- Financial × Risk
- Industry × Strategy
- Valuation × Catalysts
- Cross-agent integration in Synthesis

### 5. Scenario-Driven
- Risk scenarios: "What if revenues drop 20%?"
- Bull/Base/Bear cases with probabilities
- Weighted expected returns

### 6. Professional Tone
- Analytical, not promotional
- Balanced (strengths and weaknesses)
- Suitable for institutional investors
- Investment committee quality

---

## Token Budget Summary

| Agent | Executive Mode | Comprehensive Mode | Ratio |
|-------|----------------|-------------------|-------|
| 1: Financial Health | 500 | 2,500-3,000 | 5-6x |
| 2: Risk Assessment | 500 | 2,000-2,500 | 4-5x |
| 3: Industry Context | 500 | 2,000-2,500 | 4-5x |
| 4: Strategic Evaluation | 500 | 1,500-2,000 | 3-4x |
| 5: Market Intelligence | 500 | 1,500-2,000 | 3-4x |
| 6: Synthesis | 500 | 1,500-2,000 | 3-4x |
| **TOTAL** | **3,000** | **15,000-18,000** | **5-6x** |

**Page Estimates**:
- Executive: 2-3 pages
- Comprehensive: 20-30 pages

---

## Next Steps (Phase 3-6)

### Phase 3: Executive Mode Optimization
- Review and optimize current executive prompts
- Add score-to-recommendation mapping
- Include few-shot examples
- Test inconsistency rate improvement

### Phase 4: Implementation
- Add ReportMode enum to multi_agent_intelligence_service.py
- Implement report_mode parameter routing
- Integrate comprehensive prompts
- Implement citation tracking system

### Phase 5: Testing
- Test executive mode (ensure no regression)
- Test comprehensive mode with Azoty data
- Validate token counts match budgets
- Validate citation tracking

### Phase 6: Integration
- Update calling scripts
- Add mode selection to CLI/API
- Document usage examples
- Update benchmark scripts

---

## Validation Checklist

Phase 2 Success Criteria:

- [x] Create comprehensive Financial Health prompts
- [x] Create comprehensive Risk Assessment prompts
- [x] Create comprehensive Industry Context prompts
- [x] Create comprehensive Strategic Evaluation prompts
- [x] Create comprehensive Market Intelligence prompts
- [x] Create comprehensive Synthesis prompts
- [x] Each prompt includes section structure and word count guidance
- [x] Citation formatting helper implemented
- [x] Score-to-recommendation mapping in Synthesis
- [x] All prompts follow consistent structure
- [x] Token budgets clearly specified
- [x] Output requirements documented

---

## Files Affected

### Created
- `src/intelligence/prompts/comprehensive_prompts.py` (1,600 lines)

### To Be Modified (Phase 4)
- `src/intelligence/services/multi_agent_intelligence_service.py` - Add report_mode parameter
- `src/intelligence/formatters/report_formatter.py` - Update for comprehensive reports

### To Be Created (Phase 4)
- `src/intelligence/citations/citation_manager.py` - Citation tracking system

---

## Documentation Created

- **Architecture Design**: `docs/validation/PRIORITY3_ARCHITECTURE_DESIGN.md` (770 lines)
- **Phase 2 Complete**: `docs/validation/PRIORITY3_PHASE2_COMPLETE.md` (this document)

---

**Phase 2 Status**: ✅ **COMPLETE**
**Ready for**: Phase 3 - Executive Mode Optimization
**Estimated Phase 3 Effort**: 1-2 days
