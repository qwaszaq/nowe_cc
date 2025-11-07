"""
Financial data formatters for intelligence reports
"""

from typing import Dict
import logging

logger = logging.getLogger(__name__)


def format_financial_data(data: Dict[str, Dict[int, float]]) -> str:
    """
    Format financial data as markdown table for LLM

    Input:
        {
            'Total Assets': {2020: 25000000, 2021: 26000000, 2023: 26019865},
            'Current Assets': {2020: 8000000, 2021: 7500000, 2023: 7904016}
        }

    Output:
        | Metric | 2020 | 2021 | 2023 | Trend (CAGR) |
        |--------|------|------|------|--------------|
        | Total Assets | 25,000 | 26,000 | 26,020 | +2.0% |
    """
    if not data:
        return "No data available"

    # Get years (sorted)
    all_years = set()
    for metric_data in data.values():
        all_years.update(metric_data.keys())
    years = sorted(all_years)

    if not years:
        return "No data available"

    # Build table
    rows = []
    header = f"| Metric | {' | '.join(str(y) for y in years)} | Trend (CAGR) |"
    separator = "|" + "|".join(["---"] * (len(years) + 2)) + "|"

    rows.append(header)
    rows.append(separator)

    for metric, values in data.items():
        # Format values (in thousands, with commas)
        formatted_values = []
        for year in years:
            value = values.get(year)
            if value is not None:
                # Convert to thousands and format
                formatted = f"{value/1000:,.0f}"
            else:
                formatted = "-"
            formatted_values.append(formatted)

        # Calculate trend (CAGR if we have first and last year)
        first_year = min(years)
        last_year = max(years)
        first_value = values.get(first_year)
        last_value = values.get(last_year)

        if first_value and last_value and first_value != 0:
            years_diff = last_year - first_year
            if years_diff > 0:
                cagr = ((last_value / first_value) ** (1 / years_diff) - 1) * 100
                trend = f"{cagr:+.1f}%"
            else:
                trend = "N/A"
        else:
            trend = "N/A"

        row = f"| {metric} | {' | '.join(formatted_values)} | {trend} |"
        rows.append(row)

    return "\n".join(rows)


def calculate_financial_ratios(
    balance_sheet: Dict[str, Dict[int, float]],
    income_statement: Dict[str, Dict[int, float]],
    cash_flow: Dict[str, Dict[int, float]]
) -> Dict[str, Dict[int, float]]:
    """
    Calculate key financial ratios from statements

    Returns:
        {
            'Current Ratio': {2020: 0.7, 2021: 0.65, 2023: 0.70},
            'ROE (%)': {2020: 5.0, 2021: 3.0, 2023: 4.2},
            ...
        }
    """
    ratios = {}

    # Get years
    years = sorted(set(balance_sheet.get('Total Assets', {}).keys()))

    if not years:
        logger.warning("No years found in balance sheet data")
        return ratios

    # Current Ratio = Current Assets / Current Liabilities
    if 'Current Assets' in balance_sheet and 'Current Liabilities' in balance_sheet:
        ratios['Current Ratio'] = {}
        for year in years:
            ca = balance_sheet['Current Assets'].get(year)
            cl = balance_sheet['Current Liabilities'].get(year)
            if ca and cl and cl != 0:
                ratios['Current Ratio'][year] = ca / cl

    # Quick Ratio = (Current Assets - Inventories) / Current Liabilities
    if all(k in balance_sheet for k in ['Current Assets', 'Inventories', 'Current Liabilities']):
        ratios['Quick Ratio'] = {}
        for year in years:
            ca = balance_sheet['Current Assets'].get(year)
            inv = balance_sheet['Inventories'].get(year, 0)
            cl = balance_sheet['Current Liabilities'].get(year)
            if ca and cl and cl != 0:
                ratios['Quick Ratio'][year] = (ca - inv) / cl

    # Debt to Equity = Total Liabilities / Total Equity
    if 'Total Liabilities' in balance_sheet and 'Total Equity' in balance_sheet:
        ratios['Debt to Equity'] = {}
        for year in years:
            debt = balance_sheet['Total Liabilities'].get(year)
            equity = balance_sheet['Total Equity'].get(year)
            if debt and equity and equity != 0:
                ratios['Debt to Equity'][year] = debt / equity

    # Working Capital = Current Assets - Current Liabilities (in thousands)
    if 'Current Assets' in balance_sheet and 'Current Liabilities' in balance_sheet:
        ratios['Working Capital'] = {}
        for year in years:
            ca = balance_sheet['Current Assets'].get(year)
            cl = balance_sheet['Current Liabilities'].get(year)
            if ca and cl:
                ratios['Working Capital'][year] = ca - cl

    # Equity Ratio = Total Equity / Total Assets
    if 'Total Equity' in balance_sheet and 'Total Assets' in balance_sheet:
        ratios['Equity Ratio (%)'] = {}
        for year in years:
            equity = balance_sheet['Total Equity'].get(year)
            assets = balance_sheet['Total Assets'].get(year)
            if equity and assets and assets != 0:
                ratios['Equity Ratio (%)'][year] = (equity / assets) * 100

    # ROE = Net Income / Total Equity (only if income statement available)
    if 'Net Income' in income_statement and 'Total Equity' in balance_sheet:
        ratios['ROE (%)'] = {}
        for year in years:
            ni = income_statement['Net Income'].get(year)
            equity = balance_sheet['Total Equity'].get(year)
            if ni and equity and equity != 0:
                ratios['ROE (%)'][year] = (ni / equity) * 100

    # ROA = Net Income / Total Assets (only if income statement available)
    if 'Net Income' in income_statement and 'Total Assets' in balance_sheet:
        ratios['ROA (%)'] = {}
        for year in years:
            ni = income_statement['Net Income'].get(year)
            assets = balance_sheet['Total Assets'].get(year)
            if ni and assets and assets != 0:
                ratios['ROA (%)'][year] = (ni / assets) * 100

    # Net Margin = Net Income / Revenue (only if income statement available)
    if 'Net Income' in income_statement and 'Revenue' in income_statement:
        ratios['Net Margin (%)'] = {}
        for year in years:
            ni = income_statement['Net Income'].get(year)
            revenue = income_statement['Revenue'].get(year)
            if ni and revenue and revenue != 0:
                ratios['Net Margin (%)'][year] = (ni / revenue) * 100

    logger.info(f"Calculated {len(ratios)} financial ratios across {len(years)} years")

    return ratios


def select_analysis_framework(
    balance_sheet: Dict[str, Dict[int, float]],
    income_statement: Dict[str, Dict[int, float]]
) -> tuple[str, str]:
    """
    Select appropriate analysis framework based on company financial health

    Rules:
    - Credit Analysis: For distressed companies with any of:
        - Debt-to-Equity > 2.5
        - Current Ratio < 1.0
        - Negative equity
        - 3+ consecutive years of losses
    - Equity Analysis: Default for healthy companies

    Returns:
        tuple: (framework_name, rationale_text)
    """
    # Get latest year
    years = sorted(set(balance_sheet.get('Total Assets', {}).keys()))
    if not years:
        return ("EQUITY_ANALYSIS", "Insufficient data for framework determination")

    latest_year = max(years)

    # Calculate key distress indicators
    distress_signals = []

    # 1. Check Debt-to-Equity
    total_liabilities = balance_sheet.get('Total Liabilities', {}).get(latest_year)
    total_equity = balance_sheet.get('Total Equity', {}).get(latest_year)

    if total_liabilities and total_equity and total_equity != 0:
        debt_to_equity = total_liabilities / total_equity
        if debt_to_equity > 2.5:
            distress_signals.append(f"Debt-to-Equity ratio: {debt_to_equity:.2f} (>2.5 threshold)")

    # 2. Check Current Ratio
    current_assets = balance_sheet.get('Current Assets', {}).get(latest_year)
    current_liabilities = balance_sheet.get('Current Liabilities', {}).get(latest_year)

    if current_assets and current_liabilities and current_liabilities != 0:
        current_ratio = current_assets / current_liabilities
        if current_ratio < 1.0:
            distress_signals.append(f"Current ratio: {current_ratio:.2f} (<1.0 threshold)")

    # 3. Check for Negative Equity
    if total_equity and total_equity < 0:
        distress_signals.append(f"Negative equity: {total_equity:,.0f}")

    # 4. Check for consecutive losses (if income statement available)
    if 'Net Income' in income_statement:
        consecutive_losses = 0
        for year in sorted(years, reverse=True):
            net_income = income_statement['Net Income'].get(year)
            if net_income and net_income < 0:
                consecutive_losses += 1
            else:
                break

        if consecutive_losses >= 3:
            distress_signals.append(f"{consecutive_losses} consecutive years of losses")

    # Make framework decision
    if len(distress_signals) >= 2:
        framework = "CREDIT_ANALYSIS"
        rationale = f"""**Analysis Framework**: Credit Analysis (Distress-Focused)

**Rationale**:
{chr(10).join(f'- {signal}' for signal in distress_signals)}

This company exhibits financial distress signals. The analysis prioritizes solvency,
liquidity, and debt service capacity over growth and profitability metrics."""
    else:
        framework = "EQUITY_ANALYSIS"
        if distress_signals:
            rationale = f"""**Analysis Framework**: Equity Analysis (Growth-Focused)

**Rationale**:
While some stress indicators are present ({', '.join(distress_signals)}), the company
does not meet the distress threshold (2+ critical signals). Analysis focuses on growth
potential, profitability, and market position."""
        else:
            rationale = """**Analysis Framework**: Equity Analysis (Growth-Focused)

**Rationale**:
Company shows healthy financial metrics. Analysis focuses on growth potential,
profitability, competitive positioning, and value creation."""

    logger.info(f"Selected framework: {framework} ({len(distress_signals)} distress signals detected)")

    return (framework, rationale)


# Severity thresholds for Gap #4
SEVERITY_THRESHOLDS = {
    "CRITICAL": {
        "equity_decline_pct": 40,  # >40% = critical
        "debt_to_equity": 3.0,      # >3.0 = critical
        "current_ratio": 0.7,       # <0.7 = critical
        "consecutive_losses": 3      # 3+ years = critical
    },
    "HIGH": {
        "equity_decline_pct": 25,
        "debt_to_equity": 2.0,
        "current_ratio": 1.0,
        "consecutive_losses": 2
    },
    "MEDIUM": {
        "equity_decline_pct": 15,
        "debt_to_equity": 1.5,
        "current_ratio": 1.2,
        "consecutive_losses": 1
    }
}


def assess_severity(
    balance_sheet: Dict[str, Dict[int, float]],
    income_statement: Dict[str, Dict[int, float]]
) -> tuple[str, list[str]]:
    """
    Assess financial distress severity with explicit thresholds

    Returns:
        tuple: (severity_level, list_of_critical_factors)
        severity_level: "CRITICAL", "HIGH", "MEDIUM", "LOW"
    """
    years = sorted(set(balance_sheet.get('Total Assets', {}).keys()))
    if not years or len(years) < 2:
        return ("LOW", [])

    latest_year = max(years)
    first_year = min(years)

    critical_factors = []
    high_factors = []
    medium_factors = []

    # 1. Equity decline percentage
    first_equity = balance_sheet.get('Total Equity', {}).get(first_year)
    latest_equity = balance_sheet.get('Total Equity', {}).get(latest_year)

    if first_equity and latest_equity and first_equity != 0:
        equity_decline_pct = ((first_equity - latest_equity) / first_equity) * 100

        if equity_decline_pct > SEVERITY_THRESHOLDS['CRITICAL']['equity_decline_pct']:
            critical_factors.append(f"Equity declined {equity_decline_pct:.1f}% (>{SEVERITY_THRESHOLDS['CRITICAL']['equity_decline_pct']}% threshold)")
        elif equity_decline_pct > SEVERITY_THRESHOLDS['HIGH']['equity_decline_pct']:
            high_factors.append(f"Equity declined {equity_decline_pct:.1f}%")
        elif equity_decline_pct > SEVERITY_THRESHOLDS['MEDIUM']['equity_decline_pct']:
            medium_factors.append(f"Equity declined {equity_decline_pct:.1f}%")

    # 2. Debt-to-Equity ratio
    total_liabilities = balance_sheet.get('Total Liabilities', {}).get(latest_year)
    total_equity = balance_sheet.get('Total Equity', {}).get(latest_year)

    if total_liabilities and total_equity and total_equity != 0:
        debt_to_equity = total_liabilities / total_equity

        if debt_to_equity > SEVERITY_THRESHOLDS['CRITICAL']['debt_to_equity']:
            critical_factors.append(f"Debt-to-Equity {debt_to_equity:.2f} (>{SEVERITY_THRESHOLDS['CRITICAL']['debt_to_equity']} threshold)")
        elif debt_to_equity > SEVERITY_THRESHOLDS['HIGH']['debt_to_equity']:
            high_factors.append(f"Debt-to-Equity {debt_to_equity:.2f}")
        elif debt_to_equity > SEVERITY_THRESHOLDS['MEDIUM']['debt_to_equity']:
            medium_factors.append(f"Debt-to-Equity {debt_to_equity:.2f}")

    # 3. Current ratio
    current_assets = balance_sheet.get('Current Assets', {}).get(latest_year)
    current_liabilities = balance_sheet.get('Current Liabilities', {}).get(latest_year)

    if current_assets and current_liabilities and current_liabilities != 0:
        current_ratio = current_assets / current_liabilities

        if current_ratio < SEVERITY_THRESHOLDS['CRITICAL']['current_ratio']:
            critical_factors.append(f"Current ratio {current_ratio:.2f} (<{SEVERITY_THRESHOLDS['CRITICAL']['current_ratio']} threshold)")
        elif current_ratio < SEVERITY_THRESHOLDS['HIGH']['current_ratio']:
            high_factors.append(f"Current ratio {current_ratio:.2f}")
        elif current_ratio < SEVERITY_THRESHOLDS['MEDIUM']['current_ratio']:
            medium_factors.append(f"Current ratio {current_ratio:.2f}")

    # 4. Consecutive losses
    if 'Net Income' in income_statement:
        consecutive_losses = 0
        for year in sorted(years, reverse=True):
            net_income = income_statement['Net Income'].get(year)
            if net_income and net_income < 0:
                consecutive_losses += 1
            else:
                break

        if consecutive_losses >= SEVERITY_THRESHOLDS['CRITICAL']['consecutive_losses']:
            critical_factors.append(f"{consecutive_losses} consecutive years of losses (≥{SEVERITY_THRESHOLDS['CRITICAL']['consecutive_losses']} threshold)")
        elif consecutive_losses >= SEVERITY_THRESHOLDS['HIGH']['consecutive_losses']:
            high_factors.append(f"{consecutive_losses} consecutive years of losses")
        elif consecutive_losses >= SEVERITY_THRESHOLDS['MEDIUM']['consecutive_losses']:
            medium_factors.append(f"{consecutive_losses} year of losses")

    # Determine severity level
    if len(critical_factors) >= 3:
        severity = "CRITICAL"
        all_factors = critical_factors
    elif len(critical_factors) >= 2:
        severity = "HIGH"
        all_factors = critical_factors + high_factors
    elif len(critical_factors) >= 1 or len(high_factors) >= 2:
        severity = "HIGH"
        all_factors = critical_factors + high_factors
    elif len(high_factors) >= 1 or len(medium_factors) >= 2:
        severity = "MEDIUM"
        all_factors = high_factors + medium_factors
    else:
        severity = "LOW"
        all_factors = medium_factors

    logger.info(f"Assessed severity: {severity} ({len(critical_factors)} critical, {len(high_factors)} high, {len(medium_factors)} medium)")

    return (severity, all_factors)
