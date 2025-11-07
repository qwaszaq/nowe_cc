"""
Strategic Evaluation Agent Prompts
Strategy quality and management assessment
"""


def create_strategic_evaluation_prompt(
    company_name: str,
    industry: str,
    financial_summary: str,
    industry_context: str,
    rag_context: str = ""
) -> str:
    """
    Create prompt for strategic evaluation

    Args:
        company_name: Company name
        industry: Industry sector
        financial_summary: Financial health analysis
        industry_context: Industry context analysis
        rag_context: RAG-retrieved context from annual reports

    Returns:
        Formatted prompt for strategic evaluation
    """

    prompt = f"""# STRATEGIC EVALUATION ANALYSIS

You are a strategy consultant specializing in corporate strategy assessment and management quality evaluation.

## TASK

Evaluate {company_name}'s strategy quality and management effectiveness. Provide:

1. **Strategy Quality Score** (0-100)
2. **Growth Strategy Assessment**
3. **Capital Allocation Effectiveness**
4. **Management Quality Indicators**
5. **Strategic Initiatives Tracking**

## COMPANY INFORMATION

**Company:** {company_name}
**Industry:** {industry}

### Financial Context

{financial_summary}

### Industry Context

{industry_context}

"""

    if rag_context:
        prompt += f"""
### Document Context (Strategic Disclosures)

{rag_context}

**IMPORTANT:** Cite sources with page numbers when referencing strategic information.

"""

    prompt += """
## ANALYSIS FRAMEWORK

### 1. STRATEGY QUALITY SCORE (0-100)

Calculate based on:
- Strategic clarity and coherence: 25 points
- Execution track record: 25 points
- Resource allocation: 25 points
- Innovation and adaptability: 25 points

### 2. GROWTH STRATEGY ASSESSMENT

Analyze:
- **Stated Strategy:** What is the explicit growth strategy?
- **Growth Vectors:** Organic, M&A, geographic expansion, new products?
- **Strategic Focus:** Market share, margin expansion, diversification?
- **Credibility:** Is the strategy realistic given resources and market position?

Rate: Strong / Adequate / Weak

### 3. CAPITAL ALLOCATION EFFECTIVENESS

Evaluate:
- **CAPEX Priorities:** Where is capital being deployed?
- **R&D Investment:** Innovation spending levels and focus
- **M&A Track Record:** Past acquisitions and integration success
- **Shareholder Returns:** Dividends, buybacks, debt reduction
- **Return on Invested Capital:** Efficiency of capital deployment

Rate: Excellent / Good / Adequate / Poor

### 4. MANAGEMENT QUALITY INDICATORS

Assess based on disclosed information:
- **Strategic Communication:** Clarity of strategy articulation
- **Execution:** Track record of delivering on commitments
- **Transparency:** Quality of financial disclosure and guidance
- **Governance:** Board composition, independence, compensation alignment
- **Risk Management:** Proactive identification and mitigation

Rate: High Quality / Adequate / Concerning

### 5. STRATEGIC INITIATIVES

Identify and evaluate:
- **Current Initiatives:** What strategic projects are underway?
- **Investment Required:** Capital and resources needed
- **Expected Benefits:** Revenue growth, cost savings, market position
- **Implementation Risk:** Complexity and execution challenges
- **Timeline:** Short-term vs long-term impact

## OUTPUT FORMAT

```
STRATEGIC EVALUATION ANALYSIS

STRATEGY QUALITY SCORE: [XX]/100

GROWTH STRATEGY ASSESSMENT
Stated Strategy: [description with source citation]

Growth Vectors:
- Organic Growth: [evidence and assessment]
- M&A: [evidence and assessment]
- Geographic Expansion: [evidence and assessment]
- New Products/Services: [evidence and assessment]

Strategic Focus: [market share / margins / diversification / other]

Credibility: Strong / Adequate / Weak
Rationale: [explanation with evidence]

CAPITAL ALLOCATION EFFECTIVENESS

CAPEX Priorities:
- [Priority area]: [amount if disclosed, strategic rationale]
- [Priority area]: [amount if disclosed, strategic rationale]

R&D Investment:
- Amount: [if disclosed]
- Focus Areas: [technology, products, processes]
- Innovation Pipeline: [assessment based on disclosures]

M&A Track Record:
- Recent Transactions: [if any mentioned]
- Integration Success: [assessment if data available]
- Strategic Fit: [evaluation]

Shareholder Returns:
- Dividends: [policy and amounts]
- Buybacks: [if any]
- Debt Management: [strategy]

Overall Rating: Excellent / Good / Adequate / Poor
Rationale: [explanation with evidence]

MANAGEMENT QUALITY INDICATORS

Strategic Communication: High / Adequate / Weak
Evidence: [examples from disclosures]

Execution Track Record: Strong / Mixed / Weak
Evidence: [past performance vs commitments]

Transparency: High / Adequate / Low
Evidence: [quality of disclosures, guidance, explanations]

Governance: Strong / Adequate / Concerning
Evidence: [board structure, independence, compensation]

Risk Management: Proactive / Reactive / Inadequate
Evidence: [risk disclosure quality, mitigation strategies]

Overall Management Quality: High / Adequate / Concerning
Key Strengths: [top 2-3]
Key Concerns: [top 2-3]

STRATEGIC INITIATIVES

Initiative 1: [Name]
- Description: [brief summary]
- Investment Required: [if disclosed]
- Expected Benefits: [revenue/cost impact]
- Implementation Risk: High / Medium / Low
- Timeline: [short/medium/long-term]
- Assessment: [likely success based on evidence]

Initiative 2: [Name]
[same structure]

Initiative 3: [Name]
[same structure]

KEY INSIGHTS

1. [Most important insight about strategy quality]
2. [Most important insight about capital allocation]
3. [Most important insight about management effectiveness]

IMPLICATIONS FOR INVESTMENT THESIS

Positive Factors:
- [Strategic strength that supports investment]
- [Capital allocation advantage]
- [Management capability]

Negative Factors:
- [Strategic weakness or risk]
- [Capital allocation concern]
- [Management or execution risk]

Strategic Outlook: Favorable / Neutral / Unfavorable
Rationale: [brief explanation]
```

## GUIDELINES

- Distinguish between stated strategy and actual execution
- Evaluate credibility of strategic claims against financial reality
- Assess whether strategy addresses competitive challenges identified
- Consider whether capital allocation aligns with stated strategy
- Look for evidence of management follow-through on past commitments
- Be realistic: note where information is limited or unclear
- Cite sources for all strategic claims

Generate the analysis now.
"""

    return prompt


def get_strategic_rag_queries(company_name: str, year: int) -> list:
    """
    Get RAG queries for strategic evaluation

    Returns:
        List of query dictionaries for RAG system
    """
    return [
        {
            "question": f"What is {company_name}'s stated growth strategy, strategic objectives, and key initiatives?",
            "section_filter": "strategy"
        },
        {
            "question": f"What capital expenditures, investments, and resource allocation priorities are disclosed for {company_name}?",
            "section_filter": "strategy"
        },
        {
            "question": f"What does management say about strategic execution, achievements, and future plans for {company_name}?",
            "section_filter": "management_discussion"
        }
    ]
