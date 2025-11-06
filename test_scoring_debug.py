"""
Debug table scoring to see which table gets selected
"""

import sys
sys.path.insert(0, '.')

from src.document_processing.pdf_parser import PDFParser
import logging

# Enable detailed logging
logging.basicConfig(level=logging.INFO)

def test_scoring():
    print("=" * 80)
    print("TABLE SCORING DEBUG")
    print("=" * 80)
    print()

    parser = PDFParser()
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')

    print(f"PDF parsed: {doc.num_pages} pages")
    print(f"Tables found: {len(doc.tables)}")
    print()

    # Find the tables we care about
    page_38_table = None
    page_40_table = None

    for table in doc.tables:
        if table.page == 38:
            page_38_table = table
        elif table.page == 40:
            page_40_table = table

    if page_38_table:
        print(f"Page 38 table: {len(page_38_table.rows)} rows × {len(page_38_table.headers)} cols")
        print(f"  Headers: {page_38_table.headers[:5]}")
        print(f"  First row: {page_38_table.rows[0][:5]}")
        print()

    if page_40_table:
        print(f"Page 40 table: {len(page_40_table.rows)} rows × {len(page_40_table.headers)} cols")
        print(f"  Headers: {page_40_table.headers[:5]}")
        print(f"  First row: {page_40_table.rows[0][:5]}")
        print()

    # Which one was selected as balance sheet?
    if 'balance_sheet' in doc.financial_statements:
        bs = doc.financial_statements['balance_sheet']
        print(f"Selected balance sheet: Page {bs.page}")
        print()

    print("=" * 80)

if __name__ == "__main__":
    test_scoring()
