"""
Test text-based balance sheet extraction
"""

import sys
sys.path.insert(0, '.')

from src.document_processing.pdf_parser import PDFParser

def test_text_extraction():
    print("=" * 80)
    print("TEXT-BASED BALANCE SHEET EXTRACTION TEST")
    print("=" * 80)
    print()

    parser = PDFParser()

    # Parse PDF - should now use text extraction as fallback
    print("Parsing PDF with text extraction fallback...")
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')

    print()
    print(f"PDF parsed: {doc.num_pages} pages")
    print(f"Tables found: {len(doc.tables)}")
    print(f"Financial statements: {list(doc.financial_statements.keys())}")
    print()

    if 'balance_sheet' in doc.financial_statements:
        bs = doc.financial_statements['balance_sheet']
        print(f"✅ Balance Sheet Found!")
        print(f"   Source: {bs.title}")
        print(f"   Page: {bs.page}")
        print(f"   Rows: {len(bs.rows)}")
        print(f"   Headers: {bs.headers}")
        print()

        print("Extracted Line Items:")
        print("-" * 80)
        for i, row in enumerate(bs.rows):
            if len(row) >= 3:
                label = row[0]
                val1 = row[1] if len(row) > 1 else ''
                val2 = row[2] if len(row) > 2 else ''
                print(f"  {label:50s} {val1:>15s} {val2:>15s}")
        print()

        # Check for key values
        print("KEY VALUES CHECK:")
        print("-" * 80)

        key_items = {
            'Total Assets': 'AKTYWA RAZEM',
            'Current Assets': 'Aktywa obrotowe razem',
            'Fixed Assets': 'Aktywa trwałe razem',
            'Total Equity': 'Kapitał własny razem',
            'Total Liabilities': 'Zobowiązania razem',
            'Current Liabilities': 'Zobowiązania krótkoterminowe razem',
            'Cash': 'Środki pieniężne',
            'Inventories': 'Zapasy',
        }

        found_count = 0
        for eng_name, pol_name in key_items.items():
            found = False
            for row in bs.rows:
                if row and pol_name.lower() in str(row[0]).lower():
                    value = row[1] if len(row) > 1 else 'N/A'
                    print(f"  ✅ {eng_name:30s}: {value:>15s}")
                    found = True
                    found_count += 1
                    break
            if not found:
                print(f"  ❌ {eng_name:30s}: NOT FOUND")

        print()
        print(f"Found {found_count}/{len(key_items)} key items ({found_count/len(key_items)*100:.0f}%)")
        print()

        # Validate accounting equation: Assets = Equity + Liabilities
        print("ACCOUNTING EQUATION VALIDATION:")
        print("-" * 80)

        total_assets = None
        total_equity = None
        total_liabilities = None

        for row in bs.rows:
            if not row or len(row) < 2:
                continue
            label = str(row[0]).lower()
            value_str = str(row[1]).replace(' ', '').replace(',', '')

            try:
                value = float(value_str)
                if 'aktywa razem' in label and 'obrotowe' not in label and 'trwałe' not in label:
                    total_assets = value
                elif 'kapitał własny razem' in label:
                    total_equity = value
                elif 'zobowiązania razem' in label and 'krótkoterminowe' not in label and 'długoterminowe' not in label:
                    total_liabilities = value
            except:
                pass

        if total_assets and total_equity and total_liabilities:
            balance = total_equity + total_liabilities
            diff = abs(total_assets - balance)
            tolerance = total_assets * 0.01  # 1%

            print(f"  Total Assets:      {total_assets:>15,.0f}")
            print(f"  Total Equity:      {total_equity:>15,.0f}")
            print(f"  Total Liabilities: {total_liabilities:>15,.0f}")
            print(f"  Sum (E + L):       {balance:>15,.0f}")
            print(f"  Difference:        {diff:>15,.0f}")
            print()

            if diff < tolerance:
                print(f"  ✅ BALANCE SHEET BALANCES! (diff: {diff:,.0f} < {tolerance:,.0f})")
            else:
                print(f"  ⚠️  WARNING: Balance sheet doesn't balance! (diff: {diff:,.0f})")
        else:
            print("  ⚠️  Cannot validate - missing total values")
            if not total_assets:
                print("     - Total Assets: NOT FOUND")
            if not total_equity:
                print("     - Total Equity: NOT FOUND")
            if not total_liabilities:
                print("     - Total Liabilities: NOT FOUND")

    else:
        print("❌ No balance sheet found!")

    print()
    print("=" * 80)

if __name__ == "__main__":
    test_text_extraction()
