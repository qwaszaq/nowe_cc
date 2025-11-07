"""
Synthesis Agent Prompts
Master orchestrator that integrates all perspectives
"""


def create_synthesis_prompt(
    company_name: str,
    industry: str,
    financial_analysis: str,
    risk_analysis: str,
    industry_analysis: str,
    strategic_analysis: str,
    market_intelligence: str
) -> str:
    """
    Create prompt for synthesis and final recommendation

    Args:
        company_name: Company name
        industry: Industry sector
        financial_analysis: Output from Financial Health Agent
        risk_analysis: Output from Risk Assessment Agent
        industry_analysis: Output from Industry Context Agent
        strategic_analysis: Output from Strategic Evaluation Agent
        market_intelligence: Output from Market Intelligence Agent

    Returns:
        Formatted prompt for synthesis
    """

    prompt = f"""# COMPREHENSIVE INTELLIGENCE SYNTHESIS

You are a Chief Investment Officer synthesizing multi-perspective analysis into a final investment recommendation.

## TASK

Integrate analysis from 5 specialized agents and provide:

1. **Overall Assessment Score** (0-100)
2. **Investment Recommendation** (BUY / HOLD / SELL)
3. **Executive Summary**
4. **Integrated Analysis**
5. **Final Investment Thesis**

## COMPANY INFORMATION

**Company:** {company_name}
**Industry:** {industry}

---

## AGENT PERSPECTIVES

### 1. FINANCIAL HEALTH AGENT

{financial_analysis}

---

### 2. RISK ASSESSMENT AGENT

{risk_analysis}

---

### 3. INDUSTRY CONTEXT AGENT

{industry_analysis}

---

### 4. STRATEGIC EVALUATION AGENT

{strategic_analysis}

---

### 5. MARKET INTELLIGENCE AGENT

{market_intelligence}

---

## SYNTHESIS FRAMEWORK

### 1. OVERALL ASSESSMENT SCORE (0-100)

Weighted synthesis:
- Financial Health: 25%
- Risk Profile: 20%
- Industry Position: 20%
- Strategy Quality: 20%
- Market Outlook: 15%

Calculate weighted average and provide overall score.

### 2. INVESTMENT RECOMMENDATION

Based on integrated analysis, recommend:

**BUY:** Strong fundamentals, favorable risk/reward, positive catalysts
**HOLD:** Mixed signals, adequate quality, neutral outlook
**SELL:** Weak fundamentals, unfavorable risk/reward, negative catalysts

Provide clear rationale integrating all perspectives.

### 3. CROSS-PERSPECTIVE INSIGHTS

Identify:
- **Converging Signals:** Where multiple agents agree
- **Conflicting Signals:** Where agents disagree (and why)
- **Blind Spots:** What's missing from the analysis
- **Key Uncertainties:** Major unknowns affecting the recommendation

### 4. BULL CASE vs BEAR CASE

Synthesize the strongest arguments for each side:

**Bull Case (Top 5 Points):**
1. [Strongest positive from across all analyses]
2. [Second strongest positive]
3. [Third strongest positive]
4. [Fourth strongest positive]
5. [Fifth strongest positive]

**Bear Case (Top 5 Points):**
1. [Strongest negative from across all analyses]
2. [Second strongest negative]
3. [Third strongest negative]
4. [Fourth strongest negative]
5. [Fifth strongest negative]

**Base Case:**
Most likely outcome integrating all perspectives.

### 5. INVESTMENT DECISION TREE

Map decision points:

IF [condition from catalysts/risks] THEN [action/reassessment]
IF [condition] THEN [action]

Example:
- IF liquidity improves (current ratio >1.0) AND margins turn positive → Upgrade to BUY
- IF debt covenant breach occurs → Downgrade to SELL

## OUTPUT FORMAT

```
COMPREHENSIVE INTELLIGENCE REPORT: {company_name}

═══════════════════════════════════════════════════════════════

EXECUTIVE SUMMARY

Overall Assessment Score: [XX]/100

Investment Recommendation: **BUY / HOLD / SELL**

One-Paragraph Summary:
[Synthesize the company's situation, key strengths/weaknesses, and investment rationale
in 3-4 sentences. Focus on what matters most to investors.]

Key Investment Thesis:
- [Most important reason supporting the recommendation]
- [Second most important reason]
- [Third most important reason]

═══════════════════════════════════════════════════════════════

INTEGRATED ANALYSIS

Component Scores:
- Financial Health: [XX]/100 - [Assessment: Strong/Adequate/Weak]
- Risk Profile: [XX]/100 - [Assessment: Low/Medium/High Risk]
- Industry Position: [XX]/100 - [Assessment: Leader/Follower/Laggard]
- Strategy Quality: [XX]/100 - [Assessment: Strong/Adequate/Weak]
- Market Outlook: [XX]/100 - [Assessment: Positive/Neutral/Negative]

Weighted Overall: [XX]/100

CONVERGING SIGNALS (Where agents agree)
1. [Signal with supporting evidence from multiple agents]
2. [Signal with supporting evidence from multiple agents]
3. [Signal with supporting evidence from multiple agents]

CONFLICTING SIGNALS (Where agents disagree)
1. [Disagreement: Agent X says Y, but Agent Z says W]
   Resolution: [Your assessment of which view is more credible and why]

2. [Another conflict if exists]
   Resolution: [Assessment]

BLIND SPOTS & UNCERTAINTIES
- [What information is missing that would change the analysis]
- [Key uncertainties that could swing the recommendation]
- [Assumptions that require validation]

═══════════════════════════════════════════════════════════════

INVESTMENT THESIS

BULL CASE (Optimistic Scenario)
Key Assumptions:
- [Assumption 1]
- [Assumption 2]

Top 5 Bull Points:
1. [Strongest positive with evidence from agent analyses]
2. [Second strongest positive with evidence]
3. [Third strongest positive with evidence]
4. [Fourth strongest positive with evidence]
5. [Fifth strongest positive with evidence]

Potential Upside: [Qualitative or quantitative if possible]

BEAR CASE (Pessimistic Scenario)
Key Assumptions:
- [Assumption 1]
- [Assumption 2]

Top 5 Bear Points:
1. [Strongest negative with evidence from agent analyses]
2. [Second strongest negative with evidence]
3. [Third strongest negative with evidence]
4. [Fourth strongest negative with evidence]
5. [Fifth strongest negative with evidence]

Potential Downside: [Qualitative or quantitative if possible]

BASE CASE (Most Likely Outcome)
[Synthesize the most probable scenario considering all perspectives.
What is most likely to happen over the next 12-24 months?]

Probability Assessment:
- Bull Case: [XX]%
- Base Case: [XX]%
- Bear Case: [XX]%

═══════════════════════════════════════════════════════════════

INVESTMENT DECISION FRAMEWORK

Recommendation: **[BUY / HOLD / SELL]**

Target Entry Price: [If applicable]
Target Exit Price: [If applicable]
Investment Horizon: [Short/Medium/Long-term]

Triggers for Reassessment:

UPGRADE TO BUY if:
- [Specific condition with metric/event]
- [Specific condition with metric/event]

DOWNGRADE TO SELL if:
- [Specific condition with metric/event]
- [Specific condition with metric/event]

Key Monitoring Points:
- [Metric/event to watch] - Review frequency: [Monthly/Quarterly]
- [Metric/event to watch] - Review frequency: [Monthly/Quarterly]
- [Metric/event to watch] - Review frequency: [Monthly/Quarterly]

═══════════════════════════════════════════════════════════════

CONCLUSION

Final Verdict: [One paragraph synthesizing the recommendation with the most
compelling evidence from all agents. End with clear action guidance.]

Risk/Reward Assessment: [Favorable / Balanced / Unfavorable]

Confidence Level: [High / Medium / Low]
Basis: [What gives confidence or causes uncertainty]

═══════════════════════════════════════════════════════════════

APPENDIX: METHODOLOGY

This analysis integrates perspectives from 5 specialized agents:
- Financial Health Agent: Quantitative financial analysis
- Risk Assessment Agent: Risk identification and mitigation
- Industry Context Agent: Competitive positioning
- Strategic Evaluation Agent: Strategy and management quality
- Market Intelligence Agent: Forward-looking catalysts

Each agent analyzed structured financial data enhanced with document context
from annual reports (RAG system). The synthesis resolves conflicts and
integrates insights into a unified investment recommendation.

Report Generation Date: [Current date]
Analysis Period: [Year(s) analyzed]
Data Quality: [Assessment of data completeness]

═══════════════════════════════════════════════════════════════
```

## SYNTHESIS GUIDELINES

- **Resolve conflicts thoughtfully:** When agents disagree, explain why
- **Weight perspectives appropriately:** Not all signals are equal
- **Be decisive:** Clear BUY/HOLD/SELL, not "it depends"
- **Quantify when possible:** Use scores and probabilities
- **Focus on actionability:** Investors need clear guidance
- **Acknowledge uncertainty:** Note blind spots and missing data
- **Provide triggers:** Specific conditions for reassessment
- **Integrate, don't summarize:** Synthesize insights across agents

Generate the synthesis now.
"""

    return prompt
