"""
Show full content of page 38 table
"""

import sys
sys.path.insert(0, '.')

from src.document_processing.pdf_parser import PDFParser

def test_page38():
    print("=" * 80)
    print("PAGE 38 TABLE DETAIL")
    print("=" * 80)
    print()

    parser = PDFParser()
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')

    # Find page 38 table
    page_38_table = None
    for table in doc.tables:
        if table.page == 38:
            page_38_table = table
            break

    if not page_38_table:
        print("❌ No table found on page 38!")
        return

    print(f"Shape: {len(page_38_table.rows)} rows × {len(page_38_table.headers)} columns")
    print()

    print("Headers:")
    for i, header in enumerate(page_38_table.headers):
        print(f"  [{i}] {header}")
    print()

    print("ALL ROWS:")
    for i, row in enumerate(page_38_table.rows):
        print(f"Row {i:2d}: {row}")
    print()

    print("=" * 80)

if __name__ == "__main__":
    test_page38()
