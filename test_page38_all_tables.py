"""
Show ALL tables from page 38
"""

import sys
sys.path.insert(0, '.')

from src.document_processing.pdf_parser import PDFParser

def test_all_page38_tables():
    print("=" * 80)
    print("ALL TABLES FROM PAGE 38")
    print("=" * 80)
    print()

    parser = PDFParser()
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')

    # Find ALL tables on page 38
    page_38_tables = [table for table in doc.tables if table.page == 38]

    print(f"Total tables on page 38: {len(page_38_tables)}")
    print()

    for i, table in enumerate(page_38_tables):
        print(f"TABLE {i+1}:")
        print(f"  Shape: {len(table.rows)} rows × {len(table.headers)} columns")
        print(f"  Headers: {table.headers[:3]}...")
        print(f"  First data row: {table.rows[0][:3]}...")
        print(f"  Row 3: {table.rows[3] if len(table.rows) > 3 else 'N/A'}")
        print()

    print("=" * 80)

if __name__ == "__main__":
    test_all_page38_tables()
