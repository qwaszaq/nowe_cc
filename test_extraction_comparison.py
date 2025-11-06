"""
Compare what pdfplumber vs Camelot extract from page 38
"""

import pdfplumber
import camelot
import sys
sys.path.insert(0, '.')

def test_comparison():
    print("=" * 80)
    print("EXTRACTION COMPARISON: pdfplumber vs Camelot (Page 38)")
    print("=" * 80)
    print()

    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf'

    # Test pdfplumber
    print("PDFPLUMBER:")
    print("-" * 80)
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[37]  # 0-indexed
        tables = page.extract_tables()
        print(f"Tables found: {len(tables)}")
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}: {len(table)} rows")
            if table and len(table) > 3:
                print(f"  Row 0: {table[0][:3]}...")
                print(f"  Row 3: {table[3][:3]}...")
    print()

    # Test Camelot
    print("CAMELOT:")
    print("-" * 80)
    camelot_tables = camelot.read_pdf(pdf_path, pages='38', flavor='stream')
    print(f"Tables found: {len(camelot_tables)}")
    for i, table in enumerate(camelot_tables):
        df = table.df
        print(f"\nTable {i+1}: {df.shape[0]} rows × {df.shape[1]} cols")
        if len(df) > 3:
            print(f"  Row 0: {list(df.iloc[0][:3])}")
            print(f"  Row 3: {list(df.iloc[3][:3])}")
    print()

    print("=" * 80)

if __name__ == "__main__":
    test_comparison()
