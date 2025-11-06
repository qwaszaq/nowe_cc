"""
Check what Camelot actually extracts from page 38 (balance sheet)
"""

import camelot

def test_page38():
    print("=" * 80)
    print("RAW CAMELOT EXTRACTION: Page 38 Balance Sheet")
    print("=" * 80)
    print()

    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf'

    # Extract from page 38
    tables = camelot.read_pdf(pdf_path, pages='38', flavor='stream')

    print(f"Tables found on page 38: {len(tables)}")
    print()

    if len(tables) > 0:
        for i, table in enumerate(tables):
            print(f"TABLE {i+1}")
            print("-" * 80)
            print(f"Shape: {table.df.shape}")
            print(f"Parsing quality: {table.parsing_report.get('accuracy', 'N/A')}")
            print()

            df = table.df
            print("Full DataFrame:")
            print(df)
            print()

            print("Sample cells with content check:")
            for row_idx in range(min(10, len(df))):
                row_values = []
                for col_idx in range(len(df.columns)):
                    cell_value = df.iloc[row_idx, col_idx]
                    if cell_value and str(cell_value).strip():
                        row_values.append(f"[{col_idx}]='{cell_value}'")

                if row_values:
                    print(f"  Row {row_idx}: {', '.join(row_values)}")

            print()

            # Check which cells have digits
            print("Cells with numeric content:")
            found_numeric = False
            for row_idx in range(len(df)):
                for col_idx in range(len(df.columns)):
                    cell_value = str(df.iloc[row_idx, col_idx])
                    if any(char.isdigit() for char in cell_value):
                        print(f"  Row {row_idx}, Col {col_idx}: '{cell_value}'")
                        found_numeric = True

            if not found_numeric:
                print("  ❌ NO NUMERIC CONTENT FOUND!")

            print()

    else:
        print("❌ No tables found!")

if __name__ == "__main__":
    test_page38()
