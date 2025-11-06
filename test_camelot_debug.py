"""
Debug Camelot Extraction Issue

Find and fix the "cannot unpack non-iterable NoneType object" error.
"""

import camelot
import pandas as pd

def debug_camelot():
    print("=" * 80)
    print("CAMELOT DEBUG: Find the Bug")
    print("=" * 80)
    print()

    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf'

    # Test 1: Check what read_pdf returns
    print("Test 1: What does camelot.read_pdf return?")
    try:
        result = camelot.read_pdf(pdf_path, pages='38', flavor='stream')
        print(f"  Type: {type(result)}")
        print(f"  Length: {len(result)}")
        print(f"  Result: {result}")
        print()

        if len(result) > 0:
            print("Test 2: Inspect first table")
            table = result[0]
            print(f"  Type: {type(table)}")
            print(f"  Has df? {hasattr(table, 'df')}")
            print(f"  Has page? {hasattr(table, 'page')}")

            if hasattr(table, 'df'):
                df = table.df
                print(f"  DataFrame shape: {df.shape}")
                print(f"  First 5 rows:")
                print(df.head())

            if hasattr(table, 'page'):
                print(f"  Page: {table.page}")
        else:
            print("  ❌ No tables found by Camelot")

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

    print()

    # Test 3: Try both flavors
    print("Test 3: Try lattice flavor")
    try:
        lattice_result = camelot.read_pdf(pdf_path, pages='38', flavor='lattice')
        print(f"  Lattice found {len(lattice_result)} tables")
    except Exception as e:
        print(f"  Lattice error: {e}")

    print()

    # Test 4: Try pages='all' with stream
    print("Test 4: Try pages='all' with stream")
    try:
        all_result = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        print(f"  Stream (all pages) found {len(all_result)} tables")

        if len(all_result) > 0:
            for i, table in enumerate(all_result[:5]):
                print(f"  Table {i+1}: Page {table.page}, Shape {table.df.shape}")
    except Exception as e:
        print(f"  Stream (all) error: {e}")
        import traceback
        traceback.print_exc()

    print()
    print("=" * 80)

if __name__ == "__main__":
    debug_camelot()
