"""
Test Alex's actual extraction methods directly to see where the disconnect is.
"""

import sys
sys.path.insert(0, '.')

from src.document_processing.pdf_parser import PDFParser

def test_alex_extraction():
    print("=" * 80)
    print("ALEX DIRECT EXTRACTION TEST: Debug the Pipeline")
    print("=" * 80)
    print()

    # Step 1: Parse with PDFParser
    print("STEP 1: PDFParser")
    print("-" * 80)

    parser = PDFParser()
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')

    print(f"PDF parsed: {doc.num_pages} pages")
    print(f"Tables found: {len(doc.tables)}")
    print(f"Financial statements: {list(doc.financial_statements.keys())}")
    print()

    # Step 2: Check which table was identified as balance sheet
    if 'balance_sheet' in doc.financial_statements:
        bs = doc.financial_statements['balance_sheet']
        print(f"Balance Sheet Identified:")
        print(f"  Page: {bs.page}")
        print(f"  Title: {bs.title}")
        print(f"  Rows: {len(bs.rows)}")
        print(f"  Headers: {bs.headers}")
        print()

        print("Sample rows (first 5):")
        for i, row in enumerate(bs.rows[:5]):
            print(f"  Row {i}: {row}")
        print()

        # Check for numeric content
        numeric_count = 0
        for row in bs.rows:
            for cell in row:
                if cell and any(char.isdigit() for char in str(cell)):
                    numeric_count += 1
                    break  # One per row

        print(f"Rows with numeric content: {numeric_count}/{len(bs.rows)}")
        print()

        # Show rows with numbers
        print("Rows containing numbers:")
        shown = 0
        for i, row in enumerate(bs.rows):
            row_str = str(row)
            if any(char.isdigit() for char in row_str):
                print(f"  Row {i}: {row_str[:150]}")
                shown += 1
                if shown >= 10:
                    break
    else:
        print("❌ No balance sheet found!")

    print()

    # Step 3: Check ALL tables to see which one has the numbers
    print("STEP 3: ALL TABLES SCAN")
    print("-" * 80)

    best_table = None
    best_numeric_count = 0

    for table_idx, table in enumerate(doc.tables):
        numeric_count = 0
        for row in table.rows:
            for cell in row:
                if cell and any(char.isdigit() for char in str(cell)):
                    numeric_count += 1

        if numeric_count > best_numeric_count:
            best_numeric_count = numeric_count
            best_table = (table_idx, table)

        if numeric_count > 0:
            print(f"Table {table_idx}: Page {table.page}, {len(table.rows)}×{len(table.headers)} cols, {numeric_count} numeric cells")

    print()

    if best_table:
        table_idx, table = best_table
        print(f"BEST TABLE: #{table_idx} (Page {table.page}) with {best_numeric_count} numeric cells")
        print()
        print("Sample rows:")
        for i, row in enumerate(table.rows[:10]):
            # Show cells with content
            cells_with_content = [f"[{j}]={cell}" for j, cell in enumerate(row) if cell and str(cell).strip()]
            if cells_with_content:
                print(f"  Row {i}: {', '.join(cells_with_content[:5])}")
    print()

    print("=" * 80)

if __name__ == "__main__":
    test_alex_extraction()
