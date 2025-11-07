"""
Generate Claude-powered intelligence analysis via Hercules Agent System
Compare with local LLM analysis
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.data.multi_year_storage import load_for_intelligence_report
from src.intelligence.formatters.data_formatter import format_financial_data, calculate_financial_ratios
import time
from datetime import datetime

def generate_claude_analysis():
    """
    Generate comprehensive intelligence analysis using Claude (via Hercules)
    """

    print("=" * 80)
    print("CLAUDE-POWERED INTELLIGENCE ANALYSIS (via Hercules)")
    print("=" * 80)
    print()

    # Load company data
    print("Loading company data for Grupa Azoty...")
    company_data = load_for_intelligence_report("Grupa Azoty S.A.")

    if not company_data:
        print("❌ Failed to load company data")
        return

    print(f"✓ Loaded data for: {company_data['company_name']}")
    print(f"  Industry: {company_data.get('industry', 'Unknown')}")
    print()

    # Prepare financial data for analysis
    company_name = company_data['company_name']
    industry = company_data.get('industry', 'Unknown')

    balance_sheet_table = format_financial_data(company_data['balance_sheet'])
    income_statement_table = format_financial_data(
        company_data.get('income_statement', {})
    )

    ratios = calculate_financial_ratios(
        company_data['balance_sheet'],
        company_data.get('income_statement', {}),
        company_data.get('cash_flow', {})
    )
    ratios_table = format_financial_data(ratios)

    # Create comprehensive analysis prompt for Claude
    analysis_prompt = f"""# Comprehensive Investment Intelligence Analysis: {company_name}

**Industry:** {industry}
**Analysis Type:** Multi-Agent Investment Intelligence System

## Your Task

You are a Chief Investment Officer conducting a comprehensive investment analysis. Provide a detailed intelligence report covering:

1. **Financial Health Analysis** (Score 0-100)
   - Liquidity assessment
   - Profitability assessment
   - Leverage assessment
   - Key strengths and concerns

2. **Risk Assessment** (Score 0-100)
   - Financial risks
   - Operational risks
   - Market risks
   - Strategic risks
   - Mitigation strategies

3. **Industry Context Analysis** (Score 0-100)
   - Competitive position
   - Market structure
   - Industry trends
   - Competitive advantages/disadvantages

4. **Strategic Evaluation** (Score 0-100)
   - Growth strategy quality
   - Capital allocation effectiveness
   - Management quality
   - Strategic initiatives

5. **Market Intelligence** (Score 0-100)
   - Recent events and developments
   - Management guidance and outlook
   - Positive catalysts (with timing and probability)
   - Negative catalysts (with timing and probability)

6. **Investment Synthesis**
   - Overall assessment score (weighted average)
   - Investment recommendation (BUY/HOLD/SELL)
   - Bull case vs Bear case (top 5 points each)
   - Base case scenario with probability distribution
   - Decision triggers (upgrade/downgrade conditions)
   - Key monitoring points

## Financial Data

### Balance Sheet (2023)

{balance_sheet_table}

### Income Statement (2023)

{income_statement_table}

### Financial Ratios

{ratios_table}

## Analysis Guidelines

- Be specific with metrics and scores (0-100 for each dimension)
- Provide evidence-based analysis
- Identify specific catalysts with timing (near-term <6mo, medium-term 6-18mo, long-term >18mo)
- Assign probabilities to scenarios (bull/base/bear)
- Provide quantified decision triggers
- Consider competitive context and industry dynamics
- Assess management quality and strategic execution
- Forward-looking: focus on catalysts and timing, not just current state

## Output Format

Structure your response as a comprehensive investment report with:
- Executive summary with overall score and recommendation
- Detailed analysis for each dimension (5 areas + synthesis)
- Clear investment thesis with bull/bear/base cases
- Specific decision framework with triggers and monitoring plan

Generate the comprehensive analysis now.
"""

    print("Generating Claude-powered analysis...")
    print("This will take 1-2 minutes...")
    print()

    start_time = time.time()

    # Use Claude via direct prompt (simulating Hercules agent capability)
    # In production, this would route through Hercules Agent Orchestrator

    print("⚠️  NOTE: For full Claude analysis, this would route through Hercules Agent System")
    print("    For now, generating structured analysis prompt that Claude would receive.")
    print()

    # Save the prompt for manual Claude analysis
    output_dir = Path(__file__).parent.parent / "output" / "intelligence_reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_file = output_dir / f"Claude_Analysis_Prompt_{timestamp}.md"

    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(analysis_prompt)

    print(f"✅ Analysis prompt saved to: {prompt_file}")
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("To generate Claude-powered analysis:")
    print("1. Copy the prompt from:", prompt_file)
    print("2. Submit to Claude (claude.ai or API)")
    print("3. Save Claude's response to: output/intelligence_reports/Azoty_Claude_Analysis.md")
    print()
    print("OR")
    print()
    print("I can generate the analysis directly using my capabilities as Claude Code.")
    print("Would you like me to analyze Grupa Azoty now?")
    print()

    generation_time = time.time() - start_time

    return {
        "prompt_file": str(prompt_file),
        "generation_time": generation_time,
        "company_name": company_name,
        "industry": industry
    }


if __name__ == "__main__":
    result = generate_claude_analysis()
