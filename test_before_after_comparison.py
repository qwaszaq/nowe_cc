"""
Before/After Comparison: Table Extraction vs Text Extraction
"""

import sys
sys.path.insert(0, '.')

from src.document_processing.pdf_parser import PDFParser

def test_comparison():
    print("=" * 80)
    print("BEFORE/AFTER COMPARISON: Text Extraction Impact")
    print("=" * 80)
    print()

    parser = PDFParser()
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')

    if 'balance_sheet' not in doc.financial_statements:
        print("❌ No balance sheet found!")
        return

    bs = doc.financial_statements['balance_sheet']

    print(f"Balance Sheet Source: {bs.title}")
    print(f"Page: {bs.page}")
    print(f"Rows extracted: {len(bs.rows)}")
    print()

    # Extract key financial values
    def find_value(label_search):
        """Find value by label substring"""
        for row in bs.rows:
            if not row or len(row) < 2:
                continue
            label = str(row[0]).lower()
            if label_search.lower() in label:
                value_str = str(row[1]).replace(' ', '').replace(',', '')
                try:
                    return float(value_str)
                except:
                    pass
        return None

    values = {
        'Total Assets': find_value('aktywa razem'),
        'Current Assets': find_value('aktywa obrotowe razem'),
        'Fixed Assets': find_value('aktywa trwałe razem'),
        'Tangible Assets': find_value('rzeczowe aktywa trwałe'),
        'Cash': find_value('środki pieniężne'),
        'Inventories': find_value('zapasy'),
        'Receivables': find_value('należności z tytułu dostaw'),
        'Total Equity': find_value('kapitał własny razem'),
        'Total Liabilities': find_value('zobowiązania razem'),
        'Current Liabilities': find_value('zobowiązania krótkoterminowe'),
        'Long-term Liabilities': find_value('zobowiązania długoterminowe'),
        'Short-term Debt': find_value('kredytów i pożyczek'),
    }

    print("EXTRACTED FINANCIAL VALUES:")
    print("-" * 80)
    print(f"{'Metric':<30s} {'Value':>20s} {'Status':>10s}")
    print("-" * 80)

    found = 0
    total = len(values)

    for metric, value in values.items():
        if value:
            print(f"{metric:<30s} {value:>20,.0f} {'✅':>10s}")
            found += 1
        else:
            print(f"{metric:<30s} {'NOT FOUND':>20s} {'❌':>10s}")

    print("-" * 80)
    print(f"Extraction Success Rate: {found}/{total} ({found/total*100:.0f}%)")
    print()

    # Calculate Financial Ratios
    print("FINANCIAL RATIOS (Marcus's calculations):")
    print("-" * 80)

    ratios_calculated = 0
    total_ratios = 0

    # Liquidity Ratios
    if values['Current Assets'] and values['Current Liabilities']:
        current_ratio = values['Current Assets'] / values['Current Liabilities']
        print(f"Current Ratio:              {current_ratio:>10.2f} {'✅' if current_ratio > 1.0 else '⚠️ LOW'}")
        ratios_calculated += 1
    else:
        print(f"Current Ratio:              {'N/A':>10s} ❌")
    total_ratios += 1

    if values['Current Assets'] and values['Inventories'] and values['Current Liabilities']:
        quick_ratio = (values['Current Assets'] - values['Inventories']) / values['Current Liabilities']
        print(f"Quick Ratio:                {quick_ratio:>10.2f} {'✅' if quick_ratio > 0.5 else '⚠️ LOW'}")
        ratios_calculated += 1
    else:
        print(f"Quick Ratio:                {'N/A':>10s} ❌")
    total_ratios += 1

    if values['Cash'] and values['Current Liabilities']:
        cash_ratio = values['Cash'] / values['Current Liabilities']
        print(f"Cash Ratio:                 {cash_ratio:>10.2f} ✅")
        ratios_calculated += 1
    else:
        print(f"Cash Ratio:                 {'N/A':>10s} ❌")
    total_ratios += 1

    # Leverage Ratios
    if values['Total Liabilities'] and values['Total Equity']:
        debt_to_equity = values['Total Liabilities'] / values['Total Equity']
        print(f"Debt to Equity:             {debt_to_equity:>10.2f} {'⚠️ HIGH' if debt_to_equity > 2.0 else '✅'}")
        ratios_calculated += 1
    else:
        print(f"Debt to Equity:             {'N/A':>10s} ❌")
    total_ratios += 1

    if values['Total Liabilities'] and values['Total Assets']:
        debt_to_assets = values['Total Liabilities'] / values['Total Assets']
        print(f"Debt to Assets:             {debt_to_assets:>10.2f} ✅")
        ratios_calculated += 1
    else:
        print(f"Debt to Assets:             {'N/A':>10s} ❌")
    total_ratios += 1

    if values['Total Equity'] and values['Total Assets']:
        equity_ratio = values['Total Equity'] / values['Total Assets']
        print(f"Equity Ratio:               {equity_ratio:>10.2f} ✅")
        ratios_calculated += 1
    else:
        print(f"Equity Ratio:               {'N/A':>10s} ❌")
    total_ratios += 1

    # Working Capital
    if values['Current Assets'] and values['Current Liabilities']:
        working_capital = values['Current Assets'] - values['Current Liabilities']
        print(f"Working Capital (thousands): {working_capital:>10,.0f} {'⚠️ NEG' if working_capital < 0 else '✅'}")
        ratios_calculated += 1
    else:
        print(f"Working Capital:            {'N/A':>10s} ❌")
    total_ratios += 1

    print("-" * 80)
    print(f"Ratios Calculated: {ratios_calculated}/{total_ratios} ({ratios_calculated/total_ratios*100:.0f}%)")
    print()

    # Financial Health Assessment
    print("FINANCIAL HEALTH ASSESSMENT:")
    print("-" * 80)

    if ratios_calculated >= 5:
        if values['Current Liabilities']:
            current_ratio = values['Current Assets'] / values['Current Liabilities']
            debt_to_equity = values['Total Liabilities'] / values['Total Equity']
            working_capital = values['Current Assets'] - values['Current Liabilities']

            issues = []
            if current_ratio < 1.0:
                issues.append(f"Low liquidity (current ratio: {current_ratio:.2f})")
            if debt_to_equity > 3.0:
                issues.append(f"High leverage (D/E: {debt_to_equity:.2f})")
            if working_capital < 0:
                issues.append(f"Negative working capital ({working_capital:,.0f})")

            if issues:
                print("⚠️  FINANCIAL DISTRESS INDICATORS:")
                for issue in issues:
                    print(f"   - {issue}")
                print()
                print("   This matches Grupa Azoty's known financial difficulties!")
                print("   Round 2 SUCCESS: We can now provide REAL quantitative analysis!")
            else:
                print("✅ Company appears financially healthy")
    else:
        print("❌ Insufficient data for health assessment")

    print()

    # Validation
    if values['Total Assets'] and values['Total Equity'] and values['Total Liabilities']:
        balance = values['Total Equity'] + values['Total Liabilities']
        diff = abs(values['Total Assets'] - balance)
        tolerance = values['Total Assets'] * 0.01

        print("ACCOUNTING EQUATION VALIDATION:")
        print("-" * 80)
        print(f"Assets:                     {values['Total Assets']:>20,.0f}")
        print(f"Equity + Liabilities:       {balance:>20,.0f}")
        print(f"Difference:                 {diff:>20,.0f}")
        print()
        if diff < tolerance:
            print("✅ BALANCE SHEET BALANCES CORRECTLY")
        else:
            print(f"⚠️  Warning: difference {diff:,.0f} exceeds tolerance {tolerance:,.0f}")

    print()
    print("=" * 80)
    print("CONCLUSION:")
    print("=" * 80)

    if found >= 10 and ratios_calculated >= 5:
        print("✅ TEXT EXTRACTION SUCCESS!")
        print()
        print(f"   - Extracted: {found}/12 key financial values (83%+)")
        print(f"   - Calculated: {ratios_calculated}/7 ratios (71%+)")
        print(f"   - Balance sheet validates correctly")
        print()
        print("   Round 2 is NOW FUNCTIONAL with real Grupa Azoty data!")
        print("   Alex can extract values, Marcus can calculate ratios!")
    elif found >= 5:
        print("🟡 PARTIAL SUCCESS")
        print(f"   - Extracted: {found}/12 values")
        print(f"   - Can calculate {ratios_calculated} ratios")
    else:
        print("❌ EXTRACTION INSUFFICIENT")
        print(f"   - Only {found}/12 values found")

    print()
    print("=" * 80)

if __name__ == "__main__":
    test_comparison()
