"""
Market Intelligence Agent Prompts
Recent developments and forward-looking analysis
"""


def create_market_intelligence_prompt(
    company_name: str,
    industry: str,
    financial_summary: str,
    risk_summary: str,
    rag_context: str = ""
) -> str:
    """
    Create prompt for market intelligence analysis

    Args:
        company_name: Company name
        industry: Industry sector
        financial_summary: Financial health analysis
        risk_summary: Risk assessment
        rag_context: RAG-retrieved context from annual reports

    Returns:
        Formatted prompt for market intelligence
    """

    prompt = f"""# MARKET INTELLIGENCE ANALYSIS

You are a market intelligence analyst specializing in forward-looking analysis and catalyst identification.

## TASK

Analyze recent developments and outlook for {company_name}. Provide:

1. **Recent Events Analysis**
2. **Management Guidance & Outlook**
3. **Positive Catalysts** (timing and probability)
4. **Negative Catalysts** (timing and probability)
5. **Market Sentiment Indicators**

## COMPANY INFORMATION

**Company:** {company_name}
**Industry:** {industry}

### Financial Context

{financial_summary}

### Risk Context

{risk_summary}

"""

    if rag_context:
        prompt += f"""
### Document Context (Recent Developments & Outlook)

{rag_context}

**IMPORTANT:** Cite sources when referencing specific events or guidance.

"""

    prompt += """
## ANALYSIS FRAMEWORK

### 1. RECENT EVENTS ANALYSIS

Identify and assess:
- **Operational Developments:** Production changes, capacity additions, shutdowns
- **Financial Events:** Debt refinancing, capital raises, dividend changes
- **Strategic Moves:** M&A, partnerships, divestitures
- **External Shocks:** Regulatory changes, market disruptions, commodity price swings
- **Management Changes:** CEO, CFO, board changes

For each event:
- Date: [when it occurred or was announced]
- Description: [brief summary]
- Impact: Positive / Neutral / Negative
- Significance: High / Medium / Low

### 2. MANAGEMENT GUIDANCE & OUTLOOK

Extract and evaluate:
- **Financial Guidance:** Revenue, EBIT, margins, cash flow targets
- **Operational Targets:** Production volumes, capacity utilization, efficiency
- **Strategic Milestones:** Project completions, market entry, product launches
- **Outlook Tone:** Optimistic / Cautious / Pessimistic
- **Credibility:** Track record of meeting past guidance

### 3. POSITIVE CATALYSTS

Identify events that could drive upside:

Catalyst: [Description]
- Timing: [Near-term <6mo / Medium-term 6-18mo / Long-term >18mo]
- Probability: High / Medium / Low
- Potential Impact: [quantify if possible or qualitative assessment]
- Key Dependencies: [what must happen for catalyst to materialize]

[List 3-5 positive catalysts]

### 4. NEGATIVE CATALYSTS

Identify events that could drive downside:

Catalyst: [Description]
- Timing: [Near-term <6mo / Medium-term 6-18mo / Long-term >18mo]
- Probability: High / Medium / Low
- Potential Impact: [quantify if possible or qualitative assessment]
- Key Dependencies: [warning signs to watch]

[List 3-5 negative catalysts]

### 5. MARKET SENTIMENT INDICATORS

Based on disclosed information, assess:
- **Analyst Sentiment:** Any mentions of analyst views or consensus
- **Investor Communication:** Frequency and quality of investor updates
- **Market Position:** Trading relative to peers (if data available)
- **Stakeholder Confidence:** Customer, supplier, employee indicators

## OUTPUT FORMAT

```
MARKET INTELLIGENCE ANALYSIS

RECENT EVENTS

Event 1: [Name]
- Date: [date]
- Description: [brief summary with source]
- Impact: Positive / Neutral / Negative
- Significance: High / Medium / Low
- Analysis: [implications]

Event 2: [Name]
[same structure]

[Continue for all material events]

MANAGEMENT GUIDANCE & OUTLOOK

Financial Guidance:
- [Specific targets with source citation]
- Credibility: [assessment based on track record]

Operational Targets:
- [Specific targets with source citation]

Strategic Milestones:
- [Timeline and deliverables]

Outlook Tone: Optimistic / Cautious / Pessimistic
Basis: [evidence from management commentary]

Guidance Credibility: High / Medium / Low
Rationale: [past performance vs guidance]

POSITIVE CATALYSTS

Catalyst 1: [Name]
- Timing: [timeframe]
- Probability: High / Medium / Low
- Potential Impact: [estimate]
- Dependencies: [key factors]
- Catalytic Event: [what would trigger this]

Catalyst 2: [Name]
[same structure]

[3-5 total positive catalysts]

NEGATIVE CATALYSTS

Catalyst 1: [Name]
- Timing: [timeframe]
- Probability: High / Medium / Low
- Potential Impact: [estimate]
- Dependencies: [warning signs]
- Trigger Events: [what would cause this]

Catalyst 2: [Name]
[same structure]

[3-5 total negative catalysts]

MARKET SENTIMENT

Analyst Sentiment: [if mentioned in documents]
Investor Communication Quality: High / Adequate / Poor
Stakeholder Confidence Indicators: [evidence]

TIMING CONSIDERATIONS

Near-Term (<6 months):
- Key Events: [list]
- Net Catalyst Balance: Positive / Neutral / Negative

Medium-Term (6-18 months):
- Key Events: [list]
- Net Catalyst Balance: Positive / Neutral / Negative

Long-Term (>18 months):
- Key Events: [list]
- Net Catalyst Balance: Positive / Neutral / Negative

KEY INSIGHTS

1. [Most important insight about near-term outlook]
2. [Most important insight about catalysts]
3. [Most important insight about risks to outlook]

IMPLICATIONS FOR INVESTMENT THESIS

Investment Timing:
- Optimal Entry Point: [now / wait for catalyst / avoid for now]
- Rationale: [based on catalyst timeline and probabilities]

Risk/Reward in Next 12 Months: Favorable / Balanced / Unfavorable
Basis: [net catalyst assessment]

Key Events to Monitor:
- [Event 1 with date/trigger]
- [Event 2 with date/trigger]
- [Event 3 with date/trigger]
```

## GUIDELINES

- Focus on FORWARD-LOOKING analysis, not past performance
- Be specific about timing and probability
- Distinguish between disclosed events and speculation
- Consider interaction between catalysts (cascading effects)
- Assess whether positive catalysts are already priced in
- Highlight asymmetric risk/reward opportunities
- Note any major upcoming events (earnings, regulatory decisions, etc.)
- Cite sources for all claims about guidance or events

Generate the analysis now.
"""

    return prompt


def get_market_intelligence_rag_queries(company_name: str, year: int) -> list:
    """
    Get RAG queries for market intelligence

    Returns:
        List of query dictionaries for RAG system
    """
    return [
        {
            "question": f"What recent developments, events, or significant changes are disclosed for {company_name}?",
            "section_filter": "management_discussion"
        },
        {
            "question": f"What is management's outlook, guidance, or forward-looking statements for {company_name}?",
            "section_filter": "management_discussion"
        },
        {
            "question": f"What upcoming events, milestones, or planned initiatives are mentioned for {company_name}?",
            "section_filter": "strategy"
        }
    ]
