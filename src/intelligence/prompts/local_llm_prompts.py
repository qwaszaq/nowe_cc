"""
Prompts optimized for local LLM (openai/gpt-oss-20b, 44k context window)
Multi-pass analysis to stay within token limits
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
    Create prompt for financial health analysis (PASS 1)

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
{income_statement_table if income_statement_table != "No data available" else "Income statement data not yet extracted - focus on balance sheet analysis."}

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
- Evaluate ROE, ROA, net margin trends (if data available)
- Assess profit generation efficiency
- If income statement missing, note this limitation
- Identify profitability drivers or concerns based on available data

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
Key Metrics: [cite specific ratios with numbers]
Trend: [improving/stable/declining - explain based on multi-year data if available]
Analysis: [2-3 sentences explaining liquidity position with specific numbers]

**PROFITABILITY ASSESSMENT**
Status: [Strong/Adequate/Weak/Data Not Available]
Key Metrics: [cite specific ratios if available, or note missing data]
Trend: [improving/stable/declining or N/A if single year]
Analysis: [2-3 sentences on profitability drivers or note data limitations]

**LEVERAGE ASSESSMENT**
Status: [Low Risk/Medium Risk/High Risk]
Key Metrics: [cite debt ratios with specific numbers]
Analysis: [2-3 sentences on debt burden and solvency with numbers]

**TOP 3 STRENGTHS**
1. [Specific strength with supporting numbers from the data]
2. [Specific strength with supporting numbers from the data]
3. [Specific strength with supporting numbers from the data]

**TOP 3 CONCERNS**
1. [Specific concern with supporting numbers from the data]
2. [Specific concern with supporting numbers from the data]
3. [Specific concern with supporting numbers from the data]

**RED FLAGS** (if any)
- [Critical issues requiring immediate attention, with specific numbers]

Be specific, cite exact numbers from the tables, explain trends, and provide clear assessments.
""".strip()


def create_risk_assessment_prompt(
    company_name: str,
    industry: str,
    financial_summary: str,
    balance_sheet_table: str
) -> str:
    """
    Create prompt for risk assessment (PASS 2)

    Args:
        company_name: Company name
        industry: Industry sector
        financial_summary: Output from financial health analysis (PASS 1)
        balance_sheet_table: Balance sheet data for reference

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

### Balance Sheet Data (for reference)
{balance_sheet_table}

---

## RISK ASSESSMENT REQUIREMENTS

Identify and evaluate risks across four categories:

### 1. FINANCIAL RISKS
- Liquidity risk (ability to meet short-term obligations - use data from financial summary)
- Credit risk (default probability based on leverage and profitability)
- Refinancing risk (debt maturity, covenant compliance concerns)
- Currency/commodity exposure (for chemical/fertilizer companies)

### 2. OPERATIONAL RISKS
- Production disruptions (chemical industry safety, maintenance)
- Supply chain vulnerabilities (raw material dependencies)
- Key person dependencies
- Technological obsolescence

### 3. MARKET RISKS
- Industry cyclicality (chemical/fertilizer sector is highly cyclical)
- Competitive pressure (market consolidation, new entrants)
- Commodity price exposure (fertilizer prices volatile)
- Regulatory changes (EU environmental rules, emissions regulations)

### 4. STRATEGIC RISKS
- Execution risk on growth plans
- M&A integration risk
- Capital allocation effectiveness

---

## OUTPUT FORMAT

For each risk category, provide:

**FINANCIAL RISKS**

Top Risks:
1. [Risk name] - Severity: [High/Medium/Low] | Probability: [High/Medium/Low]
   Impact: [Describe potential impact with specific reference to financial data]
   Mitigation: [Existing or recommended mitigation strategies]

2. [Risk name] - Severity: [High/Medium/Low] | Probability: [High/Medium/Low]
   Impact: [Describe potential impact]
   Mitigation: [Mitigation strategies]

[Continue for all significant financial risks]

**OPERATIONAL RISKS**

Top Risks:
1. [Risk name] - Severity: [High/Medium/Low] | Probability: [High/Medium/Low]
   Impact: [Describe potential impact]
   Mitigation: [Mitigation strategies]

[Continue for operational risks]

**MARKET RISKS**

Top Risks:
1. [Risk name] - Severity: [High/Medium/Low] | Probability: [High/Medium/Low]
   Impact: [Describe potential impact]
   Mitigation: [Mitigation strategies]

[Continue for market risks]

**STRATEGIC RISKS**

Top Risks:
1. [Risk name] - Severity: [High/Medium/Low] | Probability: [High/Medium/Low]
   Impact: [Describe potential impact]
   Mitigation: [Mitigation strategies]

[Continue for strategic risks]

**OVERALL RISK PROFILE**
Summary: [2-3 sentences summarizing overall risk exposure based on the analysis above]
Risk Level: [Low/Medium/High/Critical]
Key Monitoring Points: [What metrics/events to watch going forward - be specific]

Be specific about risk triggers, quantify impact where possible using financial data, and provide actionable mitigation strategies.
""".strip()


def create_investment_thesis_prompt(
    company_name: str,
    industry: str,
    financial_summary: str,
    risk_summary: str,
    current_price: str = "N/A"
) -> str:
    """
    Create prompt for investment thesis and recommendation (PASS 3)

    Args:
        company_name: Company name
        industry: Industry sector
        financial_summary: Financial health analysis output (PASS 1)
        risk_summary: Risk assessment output (PASS 2)
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
- Specific financial strengths (cite from financial analysis)
- Growth opportunities (based on industry position)
- Competitive advantages
- Positive catalysts

### 2. BEAR CASE (Worst Case Scenario)
What are the 3-5 strongest arguments against investing?
- Financial weaknesses (cite from financial analysis)
- Key risks (cite from risk assessment)
- Competitive threats
- Negative catalysts

### 3. BASE CASE (Most Likely Outcome)
Given the bull and bear arguments, what's the most realistic scenario?
- Expected financial trajectory (improvement/stability/deterioration)
- Likelihood of risks materializing
- Balanced probability assessment

### 4. INVESTMENT RECOMMENDATION
Clear guidance: BUY | HOLD | SELL
- Recommendation rationale (2-3 sentences referencing specific findings)
- Key factors supporting this recommendation
- What would change your recommendation? (triggers to revisit)

### 5. KEY MONITORING POINTS
What metrics/events should be monitored going forward?
- Financial metrics to track quarterly/annually
- Industry developments to watch
- Risk triggers that would require reassessment

---

## OUTPUT FORMAT

**BULL CASE: Why This Could Be a Good Investment**
1. [Strong positive argument with supporting evidence from financial analysis]
2. [Strong positive argument with supporting evidence]
3. [Strong positive argument with supporting evidence]
4. [Additional argument if applicable]
5. [Additional argument if applicable]

**BEAR CASE: Why This Could Be a Poor Investment**
1. [Strong negative argument with supporting evidence from risk assessment]
2. [Strong negative argument with supporting evidence]
3. [Strong negative argument with supporting evidence]
4. [Additional argument if applicable]
5. [Additional argument if applicable]

**BASE CASE: Most Likely Outcome**
[3-4 sentences describing the balanced, most probable scenario based on weighing bull and bear cases]

**INVESTMENT RECOMMENDATION: [BUY/HOLD/SELL]**
Rationale: [Clear explanation of recommendation based on bull/bear/base analysis, citing specific findings]
Confidence Level: [High/Medium/Low - explain why]
Time Horizon: [Short-term (6-12 months) / Long-term (2+ years)]

**KEY MONITORING POINTS**
Financial Metrics:
1. [Specific metric to monitor with target/threshold]
2. [Specific metric to monitor]
3. [Specific metric to monitor]

Industry/Market Developments:
1. [Event or development to watch]
2. [Event or development to watch]

**TRIGGERS FOR REASSESSMENT**
- Upgrade to BUY if: [specific conditions with numbers/events]
- Downgrade to SELL if: [specific conditions with numbers/events]

Provide clear, actionable guidance backed by evidence from financial and risk analysis. Reference specific findings and numbers.
""".strip()
