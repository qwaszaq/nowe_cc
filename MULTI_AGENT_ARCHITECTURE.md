# Multi-Agent Intelligence Architecture

**Date:** 2025-11-06
**Status:** 🚧 **IN DESIGN**
**Goal:** 6 specialized agents providing comprehensive company analysis

---

## 🎯 Architecture Overview

```
                    ┌─────────────────────────┐
                    │   Master Orchestrator   │
                    │   (Synthesis Agent)     │
                    └───────────┬─────────────┘
                                │
                    ┌───────────┴───────────┐
                    │  Coordinates 5 agents │
                    └───────────┬───────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
    ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Financial Health │  │ Risk         │  │ Industry     │
    │ Agent            │  │ Assessment   │  │ Context      │
    │                  │  │ Agent        │  │ Agent        │
    └──────────────────┘  └──────────────┘  └──────────────┘
                │               │               │
                ▼               ▼               ▼
    ┌──────────────────┐  ┌──────────────┐
    │ Strategic        │  │ Market       │
    │ Evaluation       │  │ Intelligence │
    │ Agent            │  │ Agent        │
    └──────────────────┘  └──────────────┘

         Each agent has access to:
         - Structured financial data
         - RAG system (Qdrant)
         - Specialized prompts
         - Section-filtered retrieval
```

---

## 👥 The 6 Specialized Agents

### 1. **Financial Health Agent** ✅ (Already Built)

**Role:** Quantitative financial analysis expert

**Responsibilities:**
- Liquidity analysis (current ratio, quick ratio, working capital)
- Profitability assessment (margins, ROE, ROA)
- Leverage evaluation (debt ratios, coverage)
- Trend analysis (multi-year comparisons)

**RAG Queries:**
- "Why did liquidity decline?"
- "What explains margin compression?"
- "What are cash flow drivers?"

**Section Focus:** `financial_statements`, `management_discussion`

**Output:** Financial Health Score + detailed metrics analysis

---

### 2. **Risk Assessment Agent** ✅ (Already Built)

**Role:** Risk identification and mitigation expert

**Responsibilities:**
- Financial risks (liquidity, credit, refinancing)
- Operational risks (production, supply chain, safety)
- Market risks (demand, competition, commodities)
- Strategic risks (execution, M&A, capital allocation)

**RAG Queries:**
- "What are the disclosed risk factors?"
- "What mitigation strategies are mentioned?"
- "What regulatory risks exist?"

**Section Focus:** `risk_factors`, `notes`

**Output:** Risk matrix with severity/probability/mitigation

---

### 3. **Industry Context Agent** 🆕 (New)

**Role:** Competitive positioning and market structure expert

**Responsibilities:**
- Competitive landscape analysis
- Market share and positioning
- Industry trends and dynamics
- Peer comparison and benchmarking
- Regulatory environment

**RAG Queries:**
- "Who are the main competitors mentioned?"
- "What market share data is disclosed?"
- "What industry trends are discussed?"
- "What competitive advantages are claimed?"

**Section Focus:** `management_discussion`, `strategy`, `operations`

**Output:** Competitive Position Score + market context

---

### 4. **Strategic Evaluation Agent** 🆕 (New)

**Role:** Strategy quality and management assessment expert

**Responsibilities:**
- Growth strategy evaluation
- Capital allocation effectiveness
- Management quality indicators
- Innovation and R&D assessment
- Strategic initiatives tracking

**RAG Queries:**
- "What is the company's stated strategy?"
- "What growth initiatives are planned?"
- "What capital expenditures are disclosed?"
- "What R&D investments are mentioned?"

**Section Focus:** `strategy`, `management_discussion`

**Output:** Strategy Quality Score + management assessment

---

### 5. **Market Intelligence Agent** 🆕 (New)

**Role:** Recent developments and forward-looking analysis

**Responsibilities:**
- Recent events analysis
- Guidance and outlook assessment
- Market sentiment indicators
- Catalysts identification (positive/negative)
- Timing considerations

**RAG Queries:**
- "What recent developments are disclosed?"
- "What is management's outlook?"
- "What guidance is provided?"
- "What upcoming events are mentioned?"

**Section Focus:** `management_discussion`, `notes`

**Output:** Market Outlook + catalyst timeline

---

### 6. **Synthesis Agent (Master Orchestrator)** 🆕 (New)

**Role:** Integration and final recommendation

**Responsibilities:**
- Synthesize all agent perspectives
- Resolve conflicting analyses
- Generate investment recommendation
- Create executive summary
- Highlight key insights and blind spots

**Input:** Reports from all 5 specialized agents

**RAG Queries:**
- Cross-cutting queries to validate consistency
- Gap analysis queries

**Output:** Final comprehensive intelligence report with BUY/HOLD/SELL recommendation

---

## 🔄 Sequential vs Parallel Execution

### Option 1: Sequential (Safer, Context Builds)

```
Financial Health → Risk Assessment → Industry Context →
Strategic Evaluation → Market Intelligence → Synthesis
```

**Advantages:**
- Each agent can reference previous analyses
- Builds narrative context
- Easier to debug
- Lower memory pressure (44k context window)

**Time:** ~2-3 minutes (6 × 25-30s per agent)

### Option 2: Parallel (Faster)

```
┌─ Financial Health ─┐
├─ Risk Assessment ──┤
├─ Industry Context ─┤  → Synthesis Agent
├─ Strategic Eval ───┤
└─ Market Intel ─────┘
```

**Advantages:**
- Much faster (~40-50s total)
- No inter-agent dependencies

**Challenges:**
- Each agent works independently
- Synthesis must resolve conflicts
- Higher prompt complexity

**Recommendation:** Start with **Sequential** for quality, optimize to Parallel later

---

## 📊 Agent Communication Protocol

### Agent Input Format

```json
{
  "company_data": {
    "company_name": "Grupa Azoty S.A.",
    "industry": "Chemicals & Fertilizers",
    "balance_sheet": {...},
    "income_statement": {...},
    "ratios": {...}
  },
  "rag_available": true,
  "year": 2023,
  "context_from_previous_agents": {
    "financial_health": "...",
    "risk_assessment": "..."
  }
}
```

### Agent Output Format

```json
{
  "agent_name": "Industry Context Agent",
  "score": 65,
  "key_findings": [
    "Competitive position: Mid-tier player",
    "Market share: ~15% in Poland",
    "Industry trend: Declining demand"
  ],
  "detailed_analysis": "...",
  "rag_citations": [
    {"source": "...", "page": 15, "quote": "..."}
  ],
  "confidence": "High"
}
```

---

## 🎨 Prompt Design Strategy

### Specialized System Prompts

Each agent gets a unique system prompt defining their expertise:

**Example - Industry Context Agent:**
```
You are a senior industry analyst specializing in competitive positioning and
market structure analysis. Your role is to:

1. Assess the company's competitive position within its industry
2. Identify key competitors and market dynamics
3. Evaluate industry trends and their impact
4. Benchmark against peers when data is available

When document context is provided, cite specific sources with page numbers.
Focus on evidence-based analysis, not speculation.
```

### RAG Query Design

Each agent has specialized RAG queries optimized for their domain:

```python
# Industry Context Agent queries
rag.get_context_for_question(
    "Who are the main competitors and what is the competitive landscape?",
    company=company_name,
    years=[year],
    section_type="management_discussion"  # Filter by section
)

rag.get_context_for_question(
    "What market share and industry position data is disclosed?",
    company=company_name,
    years=[year],
    section_type="strategy"
)
```

---

## 🏗️ Implementation Plan

### Phase 1: Add 3 New Agent Prompts (2 hours)

1. Create `industry_context_prompts.py`
2. Create `strategic_evaluation_prompts.py`
3. Create `market_intelligence_prompts.py`

Each with:
- System prompt
- Analysis prompt template
- RAG query definitions
- Output format specification

### Phase 2: Agent Orchestrator (2 hours)

Create `multi_agent_intelligence_service.py`:

```python
class MultiAgentIntelligenceService:
    def __init__(self, use_rag=True):
        self.agents = {
            'financial': FinancialHealthAgent(...),
            'risk': RiskAssessmentAgent(...),
            'industry': IndustryContextAgent(...),
            'strategy': StrategicEvaluationAgent(...),
            'market': MarketIntelligenceAgent(...),
            'synthesis': SynthesisAgent(...)
        }

    def generate_report(self, company_data):
        # Sequential execution
        results = {}

        results['financial'] = self.agents['financial'].analyze(company_data)
        results['risk'] = self.agents['risk'].analyze(company_data, results)
        results['industry'] = self.agents['industry'].analyze(company_data, results)
        results['strategy'] = self.agents['strategy'].analyze(company_data, results)
        results['market'] = self.agents['market'].analyze(company_data, results)

        # Synthesis
        final_report = self.agents['synthesis'].synthesize(results)

        return final_report
```

### Phase 3: Testing & Refinement (2 hours)

1. Generate multi-agent report for Azoty
2. Compare with single-agent baseline
3. Refine prompts based on output quality
4. Optimize token usage

---

## 📈 Expected Improvements

### Quality Enhancements

**Baseline (Current Single-Agent):**
- Financial + Risk analysis only
- Limited context
- ~20,000 chars

**Multi-Agent:**
- 6 complementary perspectives
- Comprehensive context
- ~35,000-40,000 chars
- Higher confidence recommendations

### Coverage Expansion

| Aspect | Single-Agent | Multi-Agent |
|--------|--------------|-------------|
| Financial Analysis | ✅ Excellent | ✅ Excellent |
| Risk Assessment | ✅ Excellent | ✅ Excellent |
| Industry Position | ❌ Missing | ✅ Comprehensive |
| Strategy Quality | ❌ Missing | ✅ Comprehensive |
| Market Outlook | ❌ Missing | ✅ Comprehensive |
| Synthesis | ⚠️ Basic | ✅ Integrated |

---

## 🎯 Success Criteria

A successful multi-agent report should:

1. **Comprehensive Coverage**
   - All 6 perspectives present
   - No blind spots
   - Consistent narrative

2. **Evidence-Based**
   - Source citations throughout
   - RAG context for each perspective
   - Data-driven conclusions

3. **Actionable**
   - Clear BUY/HOLD/SELL recommendation
   - Specific triggers for action
   - Risk/reward quantified

4. **Professional Quality**
   - Investment-grade analysis
   - Comparable to manual analyst reports
   - 30-40 pages of depth

---

## 🚀 Next Steps

1. **Design Phase** (Current)
   - Define agent responsibilities ✅
   - Design communication protocol ✅
   - Plan implementation ✅

2. **Build Phase** (2-4 hours)
   - Create new agent prompts
   - Build orchestrator
   - Integrate with existing RAG

3. **Test Phase** (1-2 hours)
   - Generate multi-agent Azoty report
   - Compare quality with baseline
   - Refine and iterate

4. **Production** (Optional)
   - Add parallel execution
   - Optimize performance
   - Add agent-specific RAG filters

---

**Status:** 🚧 Ready to implement
**Estimated Time:** 6-8 hours total
**Priority:** High (completes the intelligence system vision)
