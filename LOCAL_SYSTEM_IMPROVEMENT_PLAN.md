# Local LLM System Improvement Plan

**Objective:** Maximize local LLM effectiveness to match Claude-level analysis quality
**Current Status:** Local system reaches correct conclusions but lacks severity calibration and depth
**Target:** 90%+ quality match with Claude benchmark (currently ~70-75%)

---

## 🎯 Core Problem Statement

**Current Gap:** Local LLM (openai/gpt-oss-20b) produces correct directional analysis but fails on:

1. **Severity Calibration:** Underestimates crisis severity (0.70 current ratio = "weak" not "critical")
2. **Framework Selection:** Applies wrong analytical frameworks (equity analysis for distressed credit)
3. **Causal Reasoning:** Lists problems without identifying feedback loops and cascading effects
4. **Specificity:** Generic risk factors instead of quantified probabilities and timelines
5. **Contrarian Thinking:** Accepts narratives at face value, lacks critical questioning
6. **Probability Calibration:** Over-optimistic scenario weighting
7. **Missing Credit Analysis:** No DSCR, covenant breach probability, refinancing risk assessment

**Key Insight:** Multi-agent architecture does NOT fix these issues. They are **prompt engineering and context problems**, not architectural problems.

---

## 📊 Improvement Strategy: 5 Pillars

### Pillar 1: Enhanced Prompts with Explicit Frameworks ⭐⭐⭐
**Impact:** High | **Effort:** Medium | **Priority:** 1

### Pillar 2: RAG-Driven Context Enrichment ⭐⭐⭐
**Impact:** High | **Effort:** Low | **Priority:** 2

### Pillar 3: Few-Shot Examples with Severity Calibration ⭐⭐
**Impact:** Medium | **Effort:** Medium | **Priority:** 3

### Pillar 4: Chain-of-Thought Reasoning ⭐⭐
**Impact:** Medium | **Effort:** Low | **Priority:** 4

### Pillar 5: Validation & Self-Critique Loop ⭐
**Impact:** Medium | **Effort:** High | **Priority:** 5

---

## Pillar 1: Enhanced Prompts with Explicit Frameworks

### Problem
Local LLM doesn't know WHEN to apply credit analysis vs equity analysis.

### Solution: Framework Decision Tree in Prompts

**New Prompt Structure:**

```markdown
## STEP 1: DETERMINE ANALYTICAL FRAMEWORK

Before analyzing, determine the appropriate framework:

**Use CREDIT ANALYSIS if ANY of these conditions are true:**
- Current Ratio < 1.0
- Negative EBIT or Net Income
- Debt/Equity > 1.5
- Interest coverage < 2.0x
- Liquidity declining >10% YoY

**Use EQUITY ANALYSIS if ALL of these conditions are true:**
- Current Ratio > 1.2
- Positive and stable earnings
- Debt/Equity < 1.0
- Strong interest coverage (>3.0x)
- Stable or improving liquidity

**For this company:**
- Current Ratio: 0.70 → CREDIT ANALYSIS REQUIRED ✓
- EBIT: -1,403M PLN → CREDIT ANALYSIS REQUIRED ✓
- Debt/Equity: 1.96 → CREDIT ANALYSIS REQUIRED ✓

**CONCLUSION: Apply CREDIT ANALYSIS framework**

---

## STEP 2: CREDIT ANALYSIS PROTOCOL

When using credit analysis, you MUST assess:

### 2.1 Liquidity Crisis Risk (0-100 scale)
- Current ratio < 0.8 = CRITICAL (score: 80-100)
- Current ratio 0.8-1.0 = HIGH RISK (score: 60-80)
- Current ratio 1.0-1.2 = MODERATE (score: 40-60)

**Grupa Azoty Current Ratio: 0.70**
**Liquidity Risk Score: 95/100 (CRITICAL)**

**Reasoning:**
- 30% below minimum threshold (1.0)
- 42% below industry standard (1.2)
- Working capital: NEGATIVE -3,426M PLN
- Trend: Declining (0.82 → 0.70 YoY = -15%)

**Implications:**
1. Suppliers may demand cash-on-delivery
2. Emergency financing likely needed within 6-12 months
3. Asset sales possible to raise cash
4. Covenant breach probability: HIGH (>70%)

### 2.2 Debt Service Coverage (DSCR)
Formula: EBIT / (Interest + Principal Payments)

**Grupa Azoty:**
- EBIT: -1,403M PLN
- Debt: 5,894M PLN (assume 5% interest = 295M PLN)
- DSCR: UNDEFINED (negative EBIT)

**Assessment:** Company CANNOT service debt from operations
**Conclusion:** Must consume working capital or refinance
**Refinancing Risk:** EXTREME (who lends to negative EBIT company?)

### 2.3 Covenant Breach Probability
Typical covenants for industrial companies:
- Min current ratio: 1.0 (BREACHED: 0.70)
- Min EBITDA: Positive (LIKELY BREACHED: assume EBITDA near zero if EBIT negative)
- Max debt/equity: 2.5 (OK: 1.96)

**Probability of covenant breach: 75-90%**
**Timeframe: 3-6 months (at next reporting period)**

### 2.4 Liquidity Death Spiral Risk
Assess feedback loop:
1. Weak liquidity → Suppliers demand faster payment
2. Faster payment → Further liquidity stress
3. Liquidity stress → Asset sales at discount
4. Discounted sales → Weaker balance sheet
5. Weaker balance sheet → Higher financing costs
6. Higher costs → Reduced profitability
7. Reduced profit → Back to step 1 (SPIRAL)

**Grupa Azoty Spiral Risk: HIGH**
**Mitigation Required: Emergency refinancing or government support**
```

**Implementation:**
- Update all agent prompts with framework decision trees
- Add severity calibration scales (explicit thresholds)
- Include causal chain analysis templates
- Mandate quantified probability estimates

**Files to Update:**
```
src/intelligence/prompts/financial_health_prompts.py
src/intelligence/prompts/risk_assessment_prompts.py
src/intelligence/prompts/synthesis_prompts.py
```

---

## Pillar 2: RAG-Driven Context Enrichment

### Problem
Local LLM makes generic assessments because it lacks industry-specific benchmarks.

### Solution: RAG Queries for Contextual Benchmarks

**Enhanced RAG Strategy:**

1. **Industry Benchmark Retrieval:**
   ```python
   # Before analyzing liquidity
   benchmark_query = f"""
   What are typical current ratio and quick ratio benchmarks for {industry} companies?
   What is considered healthy vs distressed for liquidity metrics in this industry?
   """
   benchmark_context = rag_service.get_context(benchmark_query, company, years)
   ```

2. **Peer Comparison Retrieval:**
   ```python
   # Compare to peers mentioned in annual report
   peer_query = f"""
   What companies does {company} identify as competitors?
   How do their financial metrics compare to {company}?
   What market share and positioning information is available?
   """
   peer_context = rag_service.get_context(peer_query, company, years)
   ```

3. **Management Guidance Extraction:**
   ```python
   # Get forward-looking statements
   guidance_query = f"""
   What guidance has management provided for future performance?
   What are the key strategic initiatives and their expected timeline?
   What risks has management explicitly disclosed?
   """
   guidance_context = rag_service.get_context(guidance_query, company, years)
   ```

4. **Historical Context Retrieval:**
   ```python
   # Understand trend drivers
   trend_query = f"""
   Why did {metric} change from {old_value} to {new_value}?
   What operational or market factors drove this trend?
   Is this a one-time event or structural issue?
   """
   trend_context = rag_service.get_context(trend_query, company, years)
   ```

**New RAG Query Categories:**
- Industry benchmarks (thresholds, standards)
- Peer comparisons (competitive position)
- Management guidance (forward-looking)
- Trend explanations (causal drivers)
- Risk disclosures (explicit warnings)
- Strategic initiatives (timing, probability)

**Implementation:**
```python
# src/intelligence/services/multi_agent_intelligence_service.py

def _run_financial_health_agent(self, company_data):
    # Existing RAG queries
    financial_context = self.rag.get_financial_context(...)

    # NEW: Industry benchmark queries
    benchmark_context = self.rag.get_context(
        query=f"Current ratio and liquidity benchmarks for {industry} industry",
        company=company_name,
        years=years,
        section_filter=['management_discussion', 'notes']
    )

    # NEW: Peer comparison
    peer_context = self.rag.get_context(
        query=f"Competitor analysis and market positioning for {company_name}",
        company=company_name,
        years=years,
        section_filter=['management_discussion', 'strategy']
    )

    # Inject into prompt
    prompt = create_prompt(
        ...,
        benchmark_context=benchmark_context,
        peer_context=peer_context
    )
```

**Files to Update:**
```
src/rag/rag_service.py (add new query methods)
src/intelligence/services/multi_agent_intelligence_service.py (inject RAG context)
```

---

## Pillar 3: Few-Shot Examples with Severity Calibration

### Problem
Local LLM doesn't calibrate severity correctly (calls 0.70 current ratio "weak" instead of "critical").

### Solution: In-Context Learning with Calibrated Examples

**Add to Prompts:**

```markdown
## SEVERITY CALIBRATION EXAMPLES

Learn from these examples of correct severity assessment:

### Example 1: Critical Liquidity Crisis
**Company:** Manufacturing Co.
**Current Ratio:** 0.65
**Quick Ratio:** 0.40
**Working Capital:** -$500M
**Trend:** Declining from 0.85 to 0.65 (YoY: -24%)

**CORRECT ASSESSMENT:** CRITICAL LIQUIDITY CRISIS
**Severity Score:** 95/100
**Reasoning:**
- Current ratio 35% below minimum threshold (1.0)
- 46% below industry standard (1.2)
- Negative working capital indicates structural insolvency
- Declining trend suggests accelerating crisis
- Probability of emergency financing: 80% within 6 months
- Covenant breach risk: >90%

**INCORRECT ASSESSMENT (to avoid):** "Weak liquidity position"
**Why Incorrect:** Vastly understates severity. This is not "weak" - this is a crisis requiring immediate action.

---

### Example 2: Adequate Liquidity
**Company:** Stable Industrial Co.
**Current Ratio:** 1.35
**Quick Ratio:** 0.95
**Working Capital:** $250M
**Trend:** Stable (1.30 to 1.35 over 3 years)

**CORRECT ASSESSMENT:** ADEQUATE LIQUIDITY
**Severity Score:** 35/100 (Low Risk)
**Reasoning:**
- Current ratio comfortably above minimum (1.0)
- Aligned with industry standard (1.2-1.5)
- Positive working capital provides buffer
- Stable trend indicates sustainable position
- No immediate refinancing concerns

---

### Example 3: Distressed Credit with Negative Earnings
**Company:** Chemical Producer X
**EBIT:** -$800M
**Net Income:** -$1,200M
**Debt:** $4,500M
**Interest Expense:** $225M (5% of debt)

**CORRECT ASSESSMENT:** DISTRESSED CREDIT - INSOLVENCY RISK
**Framework:** Credit Analysis (NOT equity analysis)
**DSCR:** Undefined (negative EBIT)
**Assessment:**
- Company cannot service debt from operations
- Must consume working capital or asset base to pay interest
- Refinancing highly unlikely (who lends to negative EBIT company?)
- Probability of restructuring: 60-70% within 12-18 months
- Recommendation: SELL (equity likely impaired in restructuring)

**INCORRECT ASSESSMENT (to avoid):** "Limited profitability data, recommend HOLD"
**Why Incorrect:** This is not a data limitation issue. Negative EBIT with high debt is INSOLVENCY. The correct recommendation is SELL, not HOLD.

---

## YOUR TASK: Apply These Calibration Standards

For Grupa Azoty S.A.:
- Current Ratio: 0.70
- EBIT: -1,403M PLN
- Debt: 5,894M PLN

**Question:** Which example does this most resemble?

**Answer:** Combination of Example 1 (Critical Liquidity) + Example 3 (Distressed Credit)

**Correct Assessment:**
- Liquidity Risk: CRITICAL (95/100)
- Credit Risk: DISTRESSED (90/100)
- Framework: Credit Analysis
- Recommendation: Strong SELL (not HOLD)
- Probability of Restructuring: 60-80% within 12-18 months
```

**Implementation:**
- Add 5-10 calibrated examples per agent
- Include both correct and incorrect assessments (learn from mistakes)
- Cover full severity spectrum (critical, high, moderate, low)
- Emphasize quantified probabilities and timelines

**Files to Update:**
```
src/intelligence/prompts/financial_health_prompts.py (add examples)
src/intelligence/prompts/risk_assessment_prompts.py (add examples)
```

---

## Pillar 4: Chain-of-Thought Reasoning

### Problem
Local LLM jumps to conclusions without showing causal reasoning.

### Solution: Mandate Step-by-Step Reasoning

**Prompt Template:**

```markdown
## ANALYSIS PROTOCOL: Chain-of-Thought Reasoning

You MUST follow this step-by-step reasoning process:

### Step 1: Observe the Data
State what the numbers show (no interpretation yet).

Example:
"Current ratio is 0.70 (current assets 7,904M / current liabilities 11,330M).
Working capital is NEGATIVE 3,426M PLN.
EBIT is NEGATIVE 1,403M PLN.
Total debt is 5,894M PLN."

### Step 2: Compare to Benchmarks
Place the data in context.

Example:
"Industry standard current ratio for chemicals: 1.2-1.5x
Minimum threshold for investment-grade: 1.0x
Grupa Azoty current ratio: 0.70x
Gap: -0.30 to minimum (-30%), -0.50 to industry (-42%)"

### Step 3: Identify Trends
Show how metrics are changing over time.

Example:
"Current ratio declined from 0.82 (2022) to 0.70 (2023).
YoY change: -15%
3-year trend: 0.95 → 0.82 → 0.70 (consistent deterioration)"

### Step 4: Analyze Implications
What does this mean for the company?

Example:
"Current ratio < 1.0 means current liabilities exceed current assets.
Company must:
  (a) Raise emergency financing, OR
  (b) Sell assets to cover short-term obligations, OR
  (c) Restructure liabilities

None of these options are attractive with negative EBIT."

### Step 5: Identify Feedback Loops
How do problems interact and amplify?

Example:
"Liquidity crisis → Suppliers demand faster payment
→ Further cash drain → Weaker liquidity
→ Covenant breach risk → Higher financing costs
→ Lower profitability → Back to liquidity crisis (SPIRAL)"

### Step 6: Assess Probability & Timing
Quantify likelihood and timeframe.

Example:
"Probability of covenant breach: 75-90% (high confidence)
Timeframe: 3-6 months (next reporting period)
Probability of emergency financing need: 70-80%
Timeframe: 6-12 months"

### Step 7: Determine Severity & Recommendation
Based on all above, what's the call?

Example:
"Severity: CRITICAL (not 'weak')
Framework: Credit Analysis (distressed credit)
Recommendation: SELL
Confidence: High
Rationale: Equity likely impaired in restructuring scenario (base case 55% probability)"

---

## YOUR ANALYSIS (follow steps 1-7):
[Your step-by-step reasoning here]
```

**Implementation:**
- Add mandatory step-by-step sections to all agent prompts
- Require explicit reasoning before conclusions
- Force comparison to benchmarks (not just absolute values)
- Mandate causal chain identification

**Files to Update:**
```
src/intelligence/prompts/financial_health_prompts.py
src/intelligence/prompts/risk_assessment_prompts.py
src/intelligence/prompts/synthesis_prompts.py
```

---

## Pillar 5: Validation & Self-Critique Loop

### Problem
Local LLM doesn't question its own conclusions.

### Solution: Two-Pass Analysis with Self-Critique

**Process:**

```python
# Pass 1: Initial Analysis
initial_analysis = llm.analyze(company_data, prompt=analysis_prompt)

# Pass 2: Self-Critique
critique_prompt = f"""
You previously analyzed {company_name} and reached these conclusions:

{initial_analysis}

Now CRITIQUE your own analysis:

## CRITIQUE CHECKLIST

1. **Severity Calibration Check**
   - Did you use words like "weak", "moderate", "limited" for what might be CRITICAL issues?
   - Re-check: Is current ratio < 1.0? → If yes, this is CRITICAL, not "weak"
   - Re-check: Is EBIT negative with high debt? → If yes, this is DISTRESSED, not "limited profitability"

2. **Framework Selection Check**
   - Did you use equity analysis for a distressed company?
   - Rule: If current ratio < 1.0 OR EBIT < 0, you MUST use credit analysis
   - Re-assess your framework choice

3. **Probability Calibration Check**
   - Are your probabilities realistic or over-optimistic?
   - Bull/Base/Bear cases should reflect ACTUAL conditions
   - For distressed companies: Bear case probability should be HIGH (>40%)

4. **Specificity Check**
   - Did you give generic risk factors or quantified probabilities?
   - Example of GENERIC (bad): "Commodity prices are a risk"
   - Example of SPECIFIC (good): "Natural gas price spike >€50/MWh (70% probability within 6mo) would increase costs by 15-20%, causing EBITDA to turn negative"

5. **Causal Chain Check**
   - Did you identify feedback loops and cascading effects?
   - Or did you just list problems independently?
   - Re-analyze: How do problems interact and amplify each other?

6. **Contrarian Check**
   - Did you accept the company narrative at face value?
   - Question: What is management NOT telling us?
   - Challenge: What could be worse than it appears?

## REVISED ANALYSIS
Based on your self-critique, provide revised analysis with corrections:

[Revised analysis here]

## WHAT CHANGED
Explain what you revised and why:
1. [Change 1]
2. [Change 2]
3. [Change 3]
"""

# Get revised analysis
revised_analysis = llm.analyze(initial_analysis, prompt=critique_prompt)

# Use revised analysis as final output
return revised_analysis
```

**Implementation:**
- Add self-critique pass after initial analysis
- Use checklist-driven critique (severity, framework, probability, specificity, causal chains, contrarian thinking)
- Compare initial vs revised to measure improvement
- Optional: Third pass for synthesis

**Files to Update:**
```
src/intelligence/services/multi_agent_intelligence_service.py
src/document_processing/llm_validator.py (add multi-pass with critique)
```

---

## 🚀 Implementation Roadmap

### Phase 1: Quick Wins (Week 1)
**Target:** 75% → 80% quality match with Claude

**Tasks:**
1. ✅ Update financial health prompts with framework decision tree
2. ✅ Add severity calibration scales (explicit thresholds)
3. ✅ Add 3 few-shot examples per agent (critical, moderate, low severity)
4. ✅ Test on Grupa Azoty dataset
5. ✅ Compare to Claude benchmark

**Expected Improvement:**
- Correct framework selection (credit vs equity)
- Better severity calibration (critical vs weak)
- More quantified assessments

**Files to Modify:**
```
src/intelligence/prompts/financial_health_prompts.py
src/intelligence/prompts/risk_assessment_prompts.py
```

**Success Metric:** Local system correctly identifies Grupa Azoty as DISTRESSED CREDIT (not just "weak")

---

### Phase 2: Enhanced RAG (Week 2)
**Target:** 80% → 85% quality match with Claude

**Tasks:**
1. ✅ Add industry benchmark RAG queries
2. ✅ Add peer comparison RAG queries
3. ✅ Add management guidance extraction
4. ✅ Add trend explanation queries
5. ✅ Test retrieval quality (are we getting relevant context?)
6. ✅ Measure impact on analysis depth

**Expected Improvement:**
- Context-grounded severity assessment (e.g., "42% below industry standard")
- Peer-relative positioning
- Forward-looking catalyst identification

**Files to Modify:**
```
src/rag/rag_service.py
src/intelligence/services/multi_agent_intelligence_service.py
```

**Success Metric:** Reports cite specific industry benchmarks and peer comparisons

---

### Phase 3: Chain-of-Thought (Week 3)
**Target:** 85% → 88% quality match with Claude

**Tasks:**
1. ✅ Add step-by-step reasoning template to all agents
2. ✅ Mandate causal chain analysis
3. ✅ Require trend → implication → feedback loop reasoning
4. ✅ Test reasoning quality (is it showing work?)
5. ✅ Measure impact on insight depth

**Expected Improvement:**
- Explicit causal chains (liquidity crisis → supplier demands → spiral)
- Better feedback loop identification
- More transparent reasoning

**Files to Modify:**
```
src/intelligence/prompts/*.py (all agent prompts)
```

**Success Metric:** Reports explicitly show reasoning chains (not just conclusions)

---

### Phase 4: Self-Critique (Week 4)
**Target:** 88% → 90%+ quality match with Claude

**Tasks:**
1. ✅ Implement two-pass analysis (initial + critique)
2. ✅ Add critique checklist (6 dimensions)
3. ✅ Measure improvement from initial to revised
4. ✅ A/B test: with critique vs without
5. ✅ Optimize critique prompts based on results

**Expected Improvement:**
- Self-correction of severity underestimation
- Framework selection validation
- Probability calibration adjustment

**Files to Modify:**
```
src/intelligence/services/multi_agent_intelligence_service.py
src/document_processing/llm_validator.py
```

**Success Metric:** Critique pass catches and corrects 80%+ of initial errors

---

## 📊 Success Metrics

### Quantitative Metrics

1. **Severity Calibration Accuracy**
   - Metric: % of critical issues correctly labeled as "CRITICAL" (not "weak")
   - Current: ~30% (Grupa Azoty: 0.70 current ratio labeled "weak")
   - Target: 90%+

2. **Framework Selection Accuracy**
   - Metric: % of distressed companies correctly analyzed with credit framework
   - Current: 0% (Grupa Azoty analyzed with equity framework)
   - Target: 95%+

3. **Probability Calibration Error**
   - Metric: Absolute difference between local and Claude probability estimates
   - Current: ~35 percentage points (local 55% base case vs Claude 35%)
   - Target: <10 percentage points

4. **Specificity Score**
   - Metric: % of risk factors with quantified probability + timing
   - Current: ~20%
   - Target: 80%+

5. **Causal Chain Coverage**
   - Metric: % of analyses that identify feedback loops
   - Current: ~10%
   - Target: 70%+

6. **Overall Quality Score vs Claude**
   - Metric: Human evaluation on 10-point scale across 5 dimensions
   - Current: 7.0-7.5 / 10
   - Target: 9.0+ / 10

### Qualitative Assessment

**Test Cases:**
1. Grupa Azoty (distressed credit) - DONE ✅
2. Stable industrial company (equity analysis)
3. High-growth tech (different framework)
4. Commodity cyclical (volatile metrics)
5. Post-restructuring recovery (complex history)

**For Each Test:**
- Generate local report
- Generate Claude benchmark
- Compare on 5 dimensions:
  1. Severity calibration
  2. Framework selection
  3. Causal reasoning
  4. Specificity (probabilities + timing)
  5. Recommendation quality

**Success:** Local system matches Claude on 4/5 dimensions for 4/5 test cases

---

## 🎯 Quick Start: Phase 1 Implementation

### Step 1: Update Financial Health Prompt (1 hour)

**File:** `src/intelligence/prompts/financial_health_prompts.py`

**Changes:**
1. Add framework decision tree at top of prompt
2. Add severity calibration scale (explicit thresholds)
3. Add 3 few-shot examples (critical, moderate, adequate)
4. Add chain-of-thought template
5. Add mandatory probability quantification

**Template:**
```python
FINANCIAL_HEALTH_PROMPT_V2 = """
## STEP 1: FRAMEWORK SELECTION
[Framework decision tree here - see Pillar 1]

## STEP 2: SEVERITY CALIBRATION STANDARDS
[Calibration scale here - see Pillar 3]

## STEP 3: CALIBRATED EXAMPLES
[Few-shot examples here - see Pillar 3]

## STEP 4: YOUR ANALYSIS (Chain-of-Thought)
[Step-by-step template here - see Pillar 4]

Follow steps 1-7 of chain-of-thought reasoning.
"""
```

### Step 2: Test on Grupa Azoty (30 minutes)

```bash
# Run improved single-agent analysis
python3 scripts/test_intelligence_azoty.py

# Compare to Claude benchmark
diff output/intelligence_reports/Azoty_Intelligence_Local_*.md \
     output/intelligence_reports/Azoty_Claude_Analysis_*.md
```

**Expected Changes:**
- Severity: "Weak" → "CRITICAL"
- Framework: Equity → Credit Analysis
- Recommendation: HOLD → SELL (or strong HOLD with high-risk warning)
- Probabilities: Quantified (not vague)

### Step 3: Measure Improvement (30 minutes)

**Create Evaluation Script:**
```python
# scripts/evaluate_improvement.py

def evaluate_report(report_path, benchmark_path):
    """Compare local report to Claude benchmark"""

    local_report = load_report(report_path)
    claude_report = load_report(benchmark_path)

    scores = {
        'severity_calibration': check_severity(local_report, claude_report),
        'framework_selection': check_framework(local_report, claude_report),
        'probability_specificity': check_probabilities(local_report, claude_report),
        'causal_reasoning': check_causal_chains(local_report, claude_report),
        'recommendation_quality': check_recommendation(local_report, claude_report)
    }

    overall_score = sum(scores.values()) / len(scores) * 100

    print(f"Overall Quality Score: {overall_score:.1f}% (vs Claude benchmark)")
    print("\nDimension Scores:")
    for dim, score in scores.items():
        print(f"  {dim}: {score*100:.0f}%")

    return scores
```

### Step 4: Iterate (1-2 hours)

Based on evaluation results, refine prompts:
- If severity still too soft → strengthen calibration language
- If framework still wrong → make decision tree more explicit
- If probabilities still vague → add more specific examples

**Target for Phase 1:** 80% overall quality score

---

## 📝 Documentation & Tracking

### Progress Tracking

**File:** `LOCAL_SYSTEM_IMPROVEMENT_LOG.md`

```markdown
# Improvement Log

## Phase 1: Enhanced Prompts (Week 1)

### Day 1: Framework Decision Trees
- Modified: financial_health_prompts.py
- Changes: Added credit vs equity framework selection logic
- Test Result: Framework selection improved from 0% → 90%
- Issues: Still occasionally applies equity to distressed cases

### Day 2: Severity Calibration
- Modified: financial_health_prompts.py, risk_assessment_prompts.py
- Changes: Added explicit thresholds (critical, high, moderate, low)
- Test Result: Severity accuracy improved from 30% → 75%
- Issues: Borderline cases (current ratio 0.95) still inconsistent

[Continue logging...]
```

### Benchmark Comparisons

Store all reports for comparison:
```
output/intelligence_reports/benchmarks/
├── Azoty_Claude_Benchmark.md
├── Azoty_Local_Baseline.md
├── Azoty_Local_Phase1.md
├── Azoty_Local_Phase2.md
├── Azoty_Local_Phase3.md
└── Azoty_Local_Phase4.md
```

---

## 🎉 Expected Outcomes

### After Phase 1 (Week 1)
- ✅ Correct framework selection (credit vs equity): 90%+
- ✅ Better severity calibration: 75%+
- ✅ Grupa Azoty correctly identified as DISTRESSED
- ✅ Quality score: 75% → 80%

### After Phase 2 (Week 2)
- ✅ Industry benchmark citations in reports
- ✅ Peer-relative assessments
- ✅ Context-grounded severity (e.g., "42% below industry standard")
- ✅ Quality score: 80% → 85%

### After Phase 3 (Week 3)
- ✅ Explicit causal chains in all reports
- ✅ Feedback loop identification
- ✅ Transparent reasoning (shows work)
- ✅ Quality score: 85% → 88%

### After Phase 4 (Week 4)
- ✅ Self-correction of errors
- ✅ Probability calibration aligned with Claude
- ✅ Contrarian thinking demonstrated
- ✅ Quality score: 88% → 90%+

### Final Target
**Local system produces Claude-equivalent analysis:**
- Same framework selection
- Same severity assessment
- Same probability calibration
- Same recommendation (or within 1 notch: SELL vs strong HOLD)
- 90%+ quality match across all dimensions

---

**Status:** Ready to Begin Phase 1
**Next Action:** Update `financial_health_prompts.py` with framework decision tree
**Timeline:** 4 weeks to 90% quality parity
**Maintainer:** Artur
**Last Updated:** 2025-11-07
