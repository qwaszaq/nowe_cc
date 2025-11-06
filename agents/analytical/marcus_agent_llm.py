"""
Marcus Chen - Financial Analyst (LLM-Powered)
Financial Intelligence Expert with openai/gpt-oss-20b reasoning

UPGRADE: This version uses local LLM at 192.168.200.226 for real analysis
instead of template responses.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime

# Import LLM client
from src.llm import LocalLLMClient, MARCUS_SYSTEM_PROMPT, get_llm_client


class MarcusAgentLLM(BaseAgent):
    """
    Marcus Chen - Financial Analyst (LLM-Powered)

    Role: Financial Intelligence Expert
    Specialization: Financial analysis, forensic accounting, fraud detection,
                   investment analysis, money trail investigation

    Capabilities:
    - Financial statement analysis (using LLM reasoning)
    - Forensic accounting (real fraud detection)
    - Fraud detection (actual pattern recognition)
    - Investment due diligence (genuine analysis)
    - Money flow tracking (true investigation)

    UPGRADE: Uses openai/gpt-oss-20b at 192.168.200.226 for reasoning
    """

    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Marcus Chen",
            role="Financial Analyst",
            specialization="Financial intelligence, Forensic accounting, Fraud detection, Investment analysis",
            project_id=project_id
        )

        # Initialize LLM client
        self.llm = get_llm_client()

        # Initialize Financial Toolkit (keep existing tools)
        try:
            from agents.analytical.tools.financial_toolkit import FinancialToolkit
            self.toolkit = FinancialToolkit()
            self.tools = self.toolkit.get_available_tools()
        except ImportError:
            self.toolkit = None
            self.tools = []

    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute financial analysis work using LLM

        CHANGE: Instead of templates, uses real LLM reasoning
        """

        start_time = datetime.now()
        task_lower = task.description.lower()

        # Load context from previous analyses
        context = self.load_context(task.description, limit=3)

        # Route to appropriate analysis method (KEEP routing logic)
        if any(word in task_lower for word in ["fraud", "forensic", "suspicious"]):
            result = self._forensic_analysis_llm(task, context)
        elif any(word in task_lower for word in ["investment", "due diligence", "valuation"]):
            result = self._investment_analysis_llm(task, context)
        elif any(word in task_lower for word in ["financial statement", "balance sheet", "income"]):
            result = self._financial_statement_analysis_llm(task, context)
        elif any(word in task_lower for word in ["money trail", "transaction", "flow"]):
            result = self._money_trail_analysis_llm(task, context)
        else:
            result = self._general_financial_analysis_llm(task, context)

        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken

        return result

    def _forensic_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """
        Forensic accounting and fraud detection using LLM

        UPGRADE: Real AI analysis instead of template
        """

        # Prepare context for LLM
        context_text = self._format_context(context)

        # Build comprehensive prompt
        user_prompt = f"""
FORENSIC FINANCIAL ANALYSIS REQUEST:

Task: {task.title}
Description: {task.description}

Previous Context:
{context_text}

Perform comprehensive forensic analysis:

1. FRAUD INDICATORS ASSESSMENT
   - Revenue recognition issues (timing, channel stuffing, round-tripping)
   - Expense manipulation (capitalization, off-balance-sheet, related parties)
   - Cash flow discrepancies (operating cash vs earnings, working capital)
   - Balance sheet concerns (asset quality, liability completeness)

2. STATISTICAL ANALYSIS
   - Apply Benford's Law to detect number manipulation
   - Identify statistical outliers
   - Analyze digit patterns

3. FORENSIC PROCEDURES
   - Horizontal analysis (trends over time)
   - Vertical analysis (common-size statements)
   - Ratio analysis with peer comparison
   - Cash flow analysis
   - Related party transaction review

4. FINAL ASSESSMENT
   - Suspicion level (Low/Medium/High)
   - Specific red flags with evidence
   - Quantified potential impact
   - Confidence level
   - Recommendation for next steps

Be thorough, skeptical, and evidence-based. This is for criminal investigation.
"""

        # Get LLM analysis
        try:
            analysis = self.llm.chat(
                system_prompt=MARCUS_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "forensic",
                    "methodology": "ACFE compliant",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["forensic_report.md", "red_flag_summary.md"],
                next_steps="Recommend Adrian (legal) for legal assessment if fraud suspected"
            )

        except Exception as e:
            # Fallback to basic response if LLM fails
            return self._create_error_result(task, e)

    def _investment_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """Investment due diligence using LLM"""

        context_text = self._format_context(context)

        user_prompt = f"""
INVESTMENT DUE DILIGENCE REQUEST:

Investment Opportunity: {task.title}
Details: {task.description}

Context:
{context_text}

Perform comprehensive investment analysis:

1. FINANCIAL HEALTH
   - Revenue growth (CAGR calculation)
   - Profitability analysis (margins, trends)
   - Cash generation (free cash flow)
   - Capital efficiency (ROIC, ROE with numbers)

2. BUSINESS MODEL ASSESSMENT
   - Revenue stream diversification
   - Unit economics (if applicable)
   - Scalability assessment
   - Competitive moat strength

3. BALANCE SHEET ANALYSIS
   - Liquidity ratios (calculate current ratio, quick ratio)
   - Leverage analysis (D/E ratio, interest coverage)
   - Asset quality assessment
   - Working capital efficiency

4. VALUATION
   - DCF analysis approach
   - Comparable company multiples
   - Valuation range estimate

5. INVESTMENT RECOMMENDATION
   - Bull case (3 strongest points)
   - Bear case (3 key risks)
   - Base case scenario
   - Final recommendation: Buy/Hold/Pass
   - Confidence level with justification

Calculate actual numbers. Be specific and quantitative.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=MARCUS_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "investment",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["investment_memo.md", "valuation_analysis.md"],
                next_steps="Coordinate with Sofia for market validation"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _financial_statement_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """Financial statement deep-dive using LLM"""

        context_text = self._format_context(context)

        user_prompt = f"""
FINANCIAL STATEMENT ANALYSIS REQUEST:

Company: {task.title}
Task: {task.description}

Context/Data:
{context_text}

Perform detailed financial statement analysis:

1. INCOME STATEMENT ANALYSIS
   - Revenue trends (growth rates, stability)
   - Gross margin (trends, peer comparison)
   - Operating leverage
   - Net margin (quality of earnings)
   - Non-recurring items identification

2. CASH FLOW STATEMENT ANALYSIS
   - Operating cash flow quality
   - Capex requirements (maintenance vs growth)
   - Free cash flow generation
   - Cash conversion efficiency

3. BALANCE SHEET ANALYSIS
   - Asset composition and quality
   - Liability structure (maturity, cost)
   - Working capital management
   - Off-balance-sheet items review

4. KEY FINANCIAL RATIOS (CALCULATE WITH NUMBERS)
   - Liquidity: Current ratio, Quick ratio
   - Leverage: D/E ratio, Interest coverage
   - Efficiency: Asset turnover, Inventory turnover
   - Profitability: ROA, ROE, ROIC
   - Growth: Revenue CAGR, Earnings CAGR

5. TREND ANALYSIS
   - 3-5 year trends for key metrics
   - Inflection points identified
   - Peer comparison

6. FINAL ASSESSMENT
   - Financial health score (Strong/Moderate/Weak)
   - Key strengths (3-5 points)
   - Key concerns (if any)

Be quantitative. Show calculations. Compare to industry norms.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=MARCUS_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "financial_statements",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["financial_analysis.md", "ratio_analysis.md"],
                next_steps="Share with Maya for statistical validation"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _money_trail_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """Money flow and transaction analysis using LLM"""

        context_text = self._format_context(context)

        user_prompt = f"""
MONEY TRAIL ANALYSIS REQUEST:

Investigation: {task.title}
Details: {task.description}

Context:
{context_text}

Analyze money flow and transactions:

1. MONEY MOVEMENT MAPPING
   - Source of funds identification
   - Transaction path mapping
   - Intermediaries identification
   - Final destination tracking

2. ENTITY STRUCTURE ANALYSIS
   - Operating entities list
   - Holding companies
   - Offshore vehicles (if any)
   - Purpose of complex structures

3. JURISDICTIONAL ANALYSIS
   - Countries involved
   - Regulatory regime complexity
   - Tax implications
   - High-risk jurisdictions flagged

4. SUSPICIOUS PATTERN DETECTION
   - Layering detection
   - Round-tripping identification
   - Unusual timing patterns
   - Size anomalies
   - Structuring indicators

5. RELATED PARTY TRANSACTIONS
   - Connected entities
   - Transaction nature
   - Arms-length pricing check

6. ASSESSMENT
   - Complexity level (Low/Medium/High)
   - Transparency assessment
   - Concern level
   - Red flags summary

This is for criminal investigation. Be thorough and flag all suspicious patterns.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=MARCUS_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "money_trail",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["money_flow_analysis.md", "entity_structure.md"],
                next_steps="Coordinate with Adrian for legal implications"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _general_financial_analysis_llm(self, task: Task, context: list) -> TaskResult:
        """General financial intelligence using LLM"""

        context_text = self._format_context(context)

        user_prompt = f"""
FINANCIAL ANALYSIS REQUEST:

Task: {task.title}
Description: {task.description}

Context:
{context_text}

Provide financial intelligence analysis appropriate to the task.
Use your expertise as a forensic financial analyst to:
- Analyze the financial aspects thoroughly
- Identify risks and red flags
- Provide actionable insights
- Quantify where possible
- Recommend next steps

Be specific, evidence-based, and thorough.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=MARCUS_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "general",
                    "llm_powered": True
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["financial_intelligence.md"],
                next_steps="Determined based on findings"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    # ROUND 2: Quantitative analysis with actual numeric data

    def _quantitative_financial_analysis_llm(self, task: Task, context: list,
                                            balance_sheet: dict, income_statement: dict) -> TaskResult:
        """
        ROUND 2 ENHANCEMENT: Perform quantitative analysis with actual numbers

        This method receives structured numeric data from Alex and calculates
        real financial ratios, not just methodology.
        """

        context_text = self._format_context(context)

        # Calculate actual financial ratios
        ratios = self._calculate_financial_ratios(balance_sheet, income_statement)

        # Format numeric data for LLM
        balance_sheet_str = self._format_numeric_data(balance_sheet, "Balance Sheet")
        income_statement_str = self._format_numeric_data(income_statement, "Income Statement")
        ratios_str = self._format_ratios(ratios)

        user_prompt = f"""
QUANTITATIVE FINANCIAL ANALYSIS REQUEST (ROUND 2):

Company: {task.title}
Task: {task.description}

ACTUAL NUMERIC DATA PROVIDED:

{balance_sheet_str}

{income_statement_str}

CALCULATED FINANCIAL RATIOS:

{ratios_str}

Previous Context:
{context_text}

COMPREHENSIVE ANALYSIS REQUIRED:

1. RATIO ANALYSIS INTERPRETATION
   - Liquidity Assessment: Interpret current ratio, quick ratio
   - Leverage Assessment: Interpret debt-to-equity, debt-to-assets
   - Profitability Assessment: Interpret ROA, ROE, profit margins
   - What do these numbers tell us about financial health?

2. YEAR-OVER-YEAR TREND ANALYSIS
   - Which metrics improved? By how much?
   - Which metrics deteriorated? By how much?
   - Are trends positive or concerning?
   - Identify inflection points

3. RED FLAGS & CONCERNS
   - Ratios outside acceptable ranges
   - Deteriorating trends
   - Balance sheet weaknesses
   - Income statement concerns
   - Liquidity or solvency risks

4. INDUSTRY COMPARISON (if possible)
   - Compare ratios to typical ranges for this industry
   - Are metrics better or worse than peers?
   - Competitive position assessment

5. FORENSIC OBSERVATIONS
   - Any suspicious patterns in the numbers?
   - Consistency between balance sheet and income statement?
   - Cash flow implications?
   - Areas requiring deeper investigation?

6. FINAL ASSESSMENT
   - Financial Health Score: Strong / Moderate / Weak (with justification)
   - Key Strengths: Top 3 positive findings
   - Key Concerns: Top 3 negative findings
   - Risk Level: Low / Medium / High
   - Confidence Level: % based on data completeness

7. RECOMMENDATIONS
   - Immediate actions needed (if any)
   - Areas for deeper investigation
   - Additional data required
   - Next analytical steps

Be specific, quantitative, and evidence-based. This is for criminal investigation support.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=MARCUS_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=4500
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "quantitative",
                    "llm_powered": True,
                    "ratios_calculated": len(ratios),
                    "balance_sheet_items": len(balance_sheet),
                    "income_statement_items": len(income_statement),
                    "calculated_ratios": ratios
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["quantitative_analysis.md", "financial_ratios.json", "red_flags.md"],
                next_steps="Share with team: Adrian (legal implications), Maya (statistical validation), Lucas (synthesis)"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _calculate_financial_ratios(self, balance_sheet: dict, income_statement: dict) -> dict:
        """
        Calculate actual financial ratios from numeric data - ROUND 2

        Returns dict with calculated ratios and year-over-year changes
        """
        ratios = {}

        try:
            # Extract values (current period)
            current_assets = balance_sheet.get('current_assets', {}).get('current')
            current_liabilities = balance_sheet.get('current_liabilities', {}).get('current')
            total_assets = balance_sheet.get('total_assets', {}).get('current')
            total_liabilities = balance_sheet.get('total_liabilities', {}).get('current')
            equity = balance_sheet.get('equity', {}).get('current')
            cash = balance_sheet.get('cash', {}).get('current')
            inventory = balance_sheet.get('inventory', {}).get('current')

            revenue = income_statement.get('revenue', {}).get('current')
            net_profit = income_statement.get('net_profit', {}).get('current')
            operating_profit = income_statement.get('operating_profit', {}).get('current')
            gross_profit = income_statement.get('gross_profit', {}).get('current')

            # Extract prior period values
            current_assets_prior = balance_sheet.get('current_assets', {}).get('prior')
            current_liabilities_prior = balance_sheet.get('current_liabilities', {}).get('prior')
            total_assets_prior = balance_sheet.get('total_assets', {}).get('prior')
            equity_prior = balance_sheet.get('equity', {}).get('prior')

            revenue_prior = income_statement.get('revenue', {}).get('prior')
            net_profit_prior = income_statement.get('net_profit', {}).get('prior')

            # LIQUIDITY RATIOS
            if current_assets and current_liabilities:
                current_ratio = current_assets / current_liabilities
                ratios['current_ratio'] = {
                    'value': current_ratio,
                    'interpretation': 'Strong' if current_ratio > 1.5 else 'Adequate' if current_ratio > 1.0 else 'Weak',
                    'benchmark': 1.5,
                    'formula': 'Current Assets / Current Liabilities'
                }

                # Prior period comparison
                if current_assets_prior and current_liabilities_prior:
                    current_ratio_prior = current_assets_prior / current_liabilities_prior
                    change = ((current_ratio - current_ratio_prior) / current_ratio_prior * 100)
                    ratios['current_ratio']['prior'] = current_ratio_prior
                    ratios['current_ratio']['change_pct'] = change
                    ratios['current_ratio']['trend'] = 'Improving' if change > 0 else 'Deteriorating'

            # Quick ratio (if inventory available)
            if current_assets and current_liabilities and inventory:
                quick_ratio = (current_assets - inventory) / current_liabilities
                ratios['quick_ratio'] = {
                    'value': quick_ratio,
                    'interpretation': 'Strong' if quick_ratio > 1.0 else 'Adequate' if quick_ratio > 0.7 else 'Weak',
                    'benchmark': 1.0,
                    'formula': '(Current Assets - Inventory) / Current Liabilities'
                }

            # Cash ratio
            if cash and current_liabilities:
                cash_ratio = cash / current_liabilities
                ratios['cash_ratio'] = {
                    'value': cash_ratio,
                    'interpretation': 'Strong' if cash_ratio > 0.5 else 'Adequate' if cash_ratio > 0.2 else 'Weak',
                    'benchmark': 0.5,
                    'formula': 'Cash / Current Liabilities'
                }

            # LEVERAGE RATIOS
            if total_liabilities and equity:
                debt_to_equity = total_liabilities / equity
                ratios['debt_to_equity'] = {
                    'value': debt_to_equity,
                    'interpretation': 'Conservative' if debt_to_equity < 1.0 else 'Moderate' if debt_to_equity < 2.0 else 'High',
                    'benchmark': 1.0,
                    'formula': 'Total Liabilities / Equity'
                }

            if total_liabilities and total_assets:
                debt_to_assets = total_liabilities / total_assets
                ratios['debt_to_assets'] = {
                    'value': debt_to_assets,
                    'interpretation': 'Low' if debt_to_assets < 0.5 else 'Moderate' if debt_to_assets < 0.7 else 'High',
                    'benchmark': 0.5,
                    'formula': 'Total Liabilities / Total Assets'
                }

            if equity and total_assets:
                equity_ratio = equity / total_assets
                ratios['equity_ratio'] = {
                    'value': equity_ratio,
                    'interpretation': 'Strong' if equity_ratio > 0.5 else 'Moderate' if equity_ratio > 0.3 else 'Weak',
                    'benchmark': 0.5,
                    'formula': 'Equity / Total Assets'
                }

            # PROFITABILITY RATIOS
            if net_profit and total_assets:
                roa = net_profit / total_assets
                ratios['return_on_assets'] = {
                    'value': roa,
                    'interpretation': 'Strong' if roa > 0.10 else 'Adequate' if roa > 0.05 else 'Weak',
                    'benchmark': 0.10,
                    'formula': 'Net Profit / Total Assets',
                    'percentage': roa * 100
                }

                # Prior period comparison
                if net_profit_prior and total_assets_prior:
                    roa_prior = net_profit_prior / total_assets_prior
                    change = ((roa - roa_prior) / abs(roa_prior) * 100) if roa_prior != 0 else 0
                    ratios['return_on_assets']['prior'] = roa_prior
                    ratios['return_on_assets']['change_pct'] = change
                    ratios['return_on_assets']['trend'] = 'Improving' if change > 0 else 'Deteriorating'

            if net_profit and equity:
                roe = net_profit / equity
                ratios['return_on_equity'] = {
                    'value': roe,
                    'interpretation': 'Strong' if roe > 0.15 else 'Adequate' if roe > 0.10 else 'Weak',
                    'benchmark': 0.15,
                    'formula': 'Net Profit / Equity',
                    'percentage': roe * 100
                }

                # Prior period comparison
                if net_profit_prior and equity_prior:
                    roe_prior = net_profit_prior / equity_prior
                    change = ((roe - roe_prior) / abs(roe_prior) * 100) if roe_prior != 0 else 0
                    ratios['return_on_equity']['prior'] = roe_prior
                    ratios['return_on_equity']['change_pct'] = change
                    ratios['return_on_equity']['trend'] = 'Improving' if change > 0 else 'Deteriorating'

            if net_profit and revenue:
                net_margin = net_profit / revenue
                ratios['net_profit_margin'] = {
                    'value': net_margin,
                    'interpretation': 'Strong' if net_margin > 0.10 else 'Adequate' if net_margin > 0.05 else 'Weak',
                    'benchmark': 0.10,
                    'formula': 'Net Profit / Revenue',
                    'percentage': net_margin * 100
                }

                # Prior period comparison
                if net_profit_prior and revenue_prior:
                    net_margin_prior = net_profit_prior / revenue_prior
                    change = ((net_margin - net_margin_prior) / abs(net_margin_prior) * 100) if net_margin_prior != 0 else 0
                    ratios['net_profit_margin']['prior'] = net_margin_prior
                    ratios['net_profit_margin']['change_pct'] = change
                    ratios['net_profit_margin']['trend'] = 'Improving' if change > 0 else 'Deteriorating'

            if gross_profit and revenue:
                gross_margin = gross_profit / revenue
                ratios['gross_profit_margin'] = {
                    'value': gross_margin,
                    'interpretation': 'Strong' if gross_margin > 0.40 else 'Adequate' if gross_margin > 0.25 else 'Weak',
                    'benchmark': 0.40,
                    'formula': 'Gross Profit / Revenue',
                    'percentage': gross_margin * 100
                }

            if operating_profit and revenue:
                operating_margin = operating_profit / revenue
                ratios['operating_margin'] = {
                    'value': operating_margin,
                    'interpretation': 'Strong' if operating_margin > 0.15 else 'Adequate' if operating_margin > 0.08 else 'Weak',
                    'benchmark': 0.15,
                    'formula': 'Operating Profit / Revenue',
                    'percentage': operating_margin * 100
                }

            # GROWTH METRICS
            if revenue and revenue_prior:
                revenue_growth = ((revenue - revenue_prior) / abs(revenue_prior) * 100)
                ratios['revenue_growth'] = {
                    'value': revenue_growth,
                    'interpretation': 'Strong' if revenue_growth > 10 else 'Moderate' if revenue_growth > 0 else 'Declining',
                    'benchmark': 10.0,
                    'formula': '(Revenue Current - Revenue Prior) / Revenue Prior',
                    'percentage': revenue_growth
                }

            if net_profit and net_profit_prior:
                profit_growth = ((net_profit - net_profit_prior) / abs(net_profit_prior) * 100) if net_profit_prior != 0 else 0
                ratios['profit_growth'] = {
                    'value': profit_growth,
                    'interpretation': 'Strong' if profit_growth > 15 else 'Moderate' if profit_growth > 0 else 'Declining',
                    'benchmark': 15.0,
                    'formula': '(Net Profit Current - Net Profit Prior) / Net Profit Prior',
                    'percentage': profit_growth
                }

            return ratios

        except Exception as e:
            print(f"Warning: Error calculating ratios: {e}")
            return {}

    def _format_numeric_data(self, data: dict, title: str) -> str:
        """Format numeric financial data for display - ROUND 2"""
        if not data:
            return f"{title}: No data available"

        lines = [f"{title}:"]
        for key, values in data.items():
            key_display = key.replace('_', ' ').title()
            current = values.get('current')
            prior = values.get('prior')
            current_label = values.get('current_label', 'Current')
            prior_label = values.get('prior_label', 'Prior')

            if current and prior:
                change = ((current - prior) / abs(prior) * 100) if prior != 0 else 0
                lines.append(f"  - {key_display}:")
                lines.append(f"      {current_label}: {current:,.0f}")
                lines.append(f"      {prior_label}: {prior:,.0f}")
                lines.append(f"      Change: {change:+.1f}%")
            elif current:
                lines.append(f"  - {key_display}: {current:,.0f} ({current_label})")

        return "\n".join(lines)

    def _format_ratios(self, ratios: dict) -> str:
        """Format calculated ratios for display - ROUND 2"""
        if not ratios:
            return "No ratios calculated yet (insufficient data)"

        lines = []
        for ratio_name, ratio_data in ratios.items():
            ratio_display = ratio_name.replace('_', ' ').title()
            value = ratio_data.get('value')
            interpretation = ratio_data.get('interpretation')
            formula = ratio_data.get('formula')
            percentage = ratio_data.get('percentage')

            if percentage is not None:
                value_str = f"{percentage:.2f}%"
            else:
                value_str = f"{value:.3f}"

            lines.append(f"\n{ratio_display}: {value_str}")
            lines.append(f"  Formula: {formula}")
            lines.append(f"  Assessment: {interpretation}")

            # Add trend if available
            if 'trend' in ratio_data:
                prior = ratio_data.get('prior')
                change_pct = ratio_data.get('change_pct')
                if prior and change_pct is not None:
                    if percentage is not None:
                        prior_str = f"{prior*100:.2f}%"
                    else:
                        prior_str = f"{prior:.3f}"
                    lines.append(f"  Prior Period: {prior_str}")
                    lines.append(f"  Change: {change_pct:+.1f}% ({ratio_data['trend']})")

        return "\n".join(lines)

    # Helper methods

    def _format_context(self, context: list) -> str:
        """Format context for LLM prompt"""
        if not context:
            return "No previous context available."

        formatted = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                formatted.append(f"{i}. {ctx.get('content', str(ctx))}")
            else:
                formatted.append(f"{i}. {ctx}")

        return "\n".join(formatted)

    def _create_error_result(self, task: Task, error: Exception) -> TaskResult:
        """Create error result if LLM fails"""
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.ERROR,
            output={
                "error": str(error),
                "llm_powered": False
            },
            thoughts=f"LLM analysis failed: {str(error)}\n\nFalling back to basic response.",
            time_taken=0,
            artifacts=[],
            next_steps="Retry with corrected input or check LLM connection"
        )


# Test
if __name__ == "__main__":
    print("Testing Marcus Agent (LLM-Powered)...")
    try:
        marcus = MarcusAgentLLM()
        print(f"✅ {marcus.name} initialized with LLM")
        print(f"   Role: {marcus.role}")
        print(f"   LLM: openai/gpt-oss-20b at 192.168.200.226")
        print(f"   Specialty: Real AI financial intelligence 💰")

        # Test LLM connection
        health = marcus.llm.health_check()
        print(f"\n🔗 LLM Status: {health['status']}")
        print(f"   Latency: {health.get('latency_ms', 'N/A')}ms")

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
