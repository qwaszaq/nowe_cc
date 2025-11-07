"""
Industry Context Agent Prompts
Competitive positioning and market structure analysis
"""


def create_industry_context_prompt(
    company_name: str,
    industry: str,
    financial_summary: str,
    balance_sheet_table: str,
    rag_context: str = ""
) -> str:
    """
    Create prompt for industry context analysis

    Args:
        company_name: Company name
        industry: Industry sector
        financial_summary: Financial health analysis from previous agent
        balance_sheet_table: Balance sheet data
        rag_context: RAG-retrieved context from annual reports

    Returns:
        Formatted prompt for industry context analysis
    """

    prompt = f"""# INDUSTRY CONTEXT ANALYSIS

You are a senior industry analyst specializing in competitive positioning and market structure analysis.

## TASK

Analyze {company_name}'s position within the {industry} industry. Provide:

1. **Competitive Position Score** (0-100)
2. **Market Structure Analysis**
3. **Competitive Landscape Assessment**
4. **Industry Trends Impact**
5. **Peer Benchmarking** (if data available)

## COMPANY INFORMATION

**Company:** {company_name}
**Industry:** {industry}

### Financial Context (from Financial Health Agent)

{financial_summary}

### Balance Sheet Data

{balance_sheet_table}

"""

    if rag_context:
        prompt += f"""
### Document Context (from Annual Reports)

{rag_context}

**IMPORTANT:** When using document context, cite sources with page numbers in square brackets.
Example: "The company reports 15% market share in Poland [Source 1, Page 24]"

"""

    prompt += """
## ANALYSIS FRAMEWORK

### 1. COMPETITIVE POSITION SCORE (0-100)

Calculate based on:
- Market share (if disclosed): 30 points
- Competitive advantages: 25 points
- Industry positioning: 25 points
- Barriers to entry: 20 points

Provide score with clear justification.

### 2. MARKET STRUCTURE

Analyze:
- **Market Type:** Oligopoly / Competitive / Fragmented
- **Key Players:** Who are the main competitors mentioned?
- **Market Concentration:** Is the industry consolidated or fragmented?
- **Geographic Focus:** Domestic, regional, or global?

### 3. COMPETITIVE LANDSCAPE

Assess:
- **Direct Competitors:** Who competes for the same customers?
- **Competitive Advantages:** Cost, quality, technology, brand, distribution
- **Competitive Disadvantages:** Where does the company lag peers?
- **Market Share:** Disclosed or estimated position

### 4. INDUSTRY TRENDS

Identify:
- **Growth/Decline:** Is the industry expanding or contracting?
- **Structural Changes:** Consolidation, disruption, regulation
- **Technology Impact:** Digital transformation, automation
- **Sustainability:** Environmental pressures, ESG requirements

Rate each trend: Favorable / Neutral / Unfavorable

### 5. PEER BENCHMARKING

If comparable data available:
- Financial metrics vs peers (margins, leverage, growth)
- Operational efficiency vs peers
- Valuation multiples (if applicable)

If no peer data: Note "Peer data not available in provided documents"

## OUTPUT FORMAT

```
INDUSTRY CONTEXT ANALYSIS

COMPETITIVE POSITION SCORE: [XX]/100

MARKET STRUCTURE
- Market Type: [...]
- Key Players: [...]
- Concentration: [...]
- Geographic Focus: [...]

COMPETITIVE LANDSCAPE
Direct Competitors:
- [Competitor 1]: [brief description]
- [Competitor 2]: [brief description]

Competitive Advantages:
1. [Advantage with evidence/source]
2. [Advantage with evidence/source]

Competitive Disadvantages:
1. [Disadvantage with evidence/source]
2. [Disadvantage with evidence/source]

Market Share: [disclosed or estimated, with source]

INDUSTRY TRENDS
1. [Trend]: Favorable/Neutral/Unfavorable
   Impact: [brief explanation with evidence]

2. [Trend]: Favorable/Neutral/Unfavorable
   Impact: [brief explanation with evidence]

3. [Trend]: Favorable/Neutral/Unfavorable
   Impact: [brief explanation with evidence]

PEER BENCHMARKING
[If available: comparison table or narrative]
[If not: "Peer data not available in provided documents"]

KEY INSIGHTS
1. [Most important insight about competitive position]
2. [Most important insight about industry dynamics]
3. [Most important insight about future outlook]

IMPLICATIONS FOR INVESTMENT THESIS
- [How industry context affects investment decision]
- [Opportunities arising from industry position]
- [Risks from competitive/industry dynamics]
```

## GUIDELINES

- Be evidence-based: cite sources when available
- If data is missing, state "Not disclosed in available documents"
- Focus on FACTS, not speculation
- Highlight both strengths and weaknesses
- Consider industry context when interpreting financial data
- Note any competitive moats or structural advantages

Generate the analysis now.
"""

    return prompt


def get_industry_rag_queries(company_name: str, year: int) -> list:
    """
    Get RAG queries for industry context analysis

    Returns:
        List of query dictionaries for RAG system
    """
    return [
        {
            "question": f"Who are {company_name}'s main competitors and what is the competitive landscape in the industry?",
            "section_filter": "management_discussion"
        },
        {
            "question": f"What market share, industry position, or competitive advantages are disclosed for {company_name}?",
            "section_filter": "strategy"
        },
        {
            "question": f"What industry trends, market dynamics, or structural changes are discussed that affect {company_name}?",
            "section_filter": "management_discussion"
        }
    ]
