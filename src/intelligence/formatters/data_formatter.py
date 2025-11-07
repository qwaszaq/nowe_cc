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
