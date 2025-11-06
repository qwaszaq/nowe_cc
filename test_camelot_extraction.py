"""
Test Camelot PDF Table Extraction on Grupa Azoty Report

Checks if Camelot can extract numeric values better than pdfplumber.
"""

import camelot
import pandas as pd

def test_camelot_extraction():
    print("=" * 80)
    print("CAMELOT: Grupa Azoty Balance Sheet Extraction Test")
    print("=" * 80)
    print()

    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf'
    page = '38'  # Balance sheet page

    print(f"Testing Camelot on: {pdf_path}, page {page}")
    print()

    # Try lattice method (best for tables with clear borders)
    print("-" * 80)
    print("Method 1: LATTICE (detects table borders)")
    print("-" * 80)
    try:
        tables_lattice = camelot.read_pdf(pdf_path, pages=page, flavor='lattice')
        print(f"✅ Lattice extraction successful!")
        print(f"   Tables found: {len(tables_lattice)}")
        print()

        if tables_lattice:
            for i, table in enumerate(tables_lattice):
                print(f"Table {i+1}:")
                print(f"  Shape: {table.df.shape} (rows x cols)")
                print(f"  Parsing quality: {table.parsing_report['accuracy']:.1f}%")
                print(f"  First 10 rows:")
                print(table.df.head(10))
                print()

                # Check for numeric values
                numeric_found = False
                for col in table.df.columns:
                    for val in table.df[col]:
                        val_str = str(val).strip()
                        # Check if contains digits
                        if any(char.isdigit() for char in val_str):
                            numeric_found = True
                            print(f"  ✅ Found numeric value: {val_str}")
                            break
                    if numeric_found:
                        break

                if not numeric_found:
                    print(f"  ❌ No numeric values detected in table {i+1}")
                print()
    except Exception as e:
        print(f"❌ Lattice extraction failed: {e}")
        print()

    # Try stream method (best for tables without clear borders)
    print("-" * 80)
    print("Method 2: STREAM (detects table by text alignment)")
    print("-" * 80)
    try:
        tables_stream = camelot.read_pdf(pdf_path, pages=page, flavor='stream')
        print(f"✅ Stream extraction successful!")
        print(f"   Tables found: {len(tables_stream)}")
        print()

        if tables_stream:
            for i, table in enumerate(tables_stream):
                print(f"Table {i+1}:")
                print(f"  Shape: {table.df.shape} (rows x cols)")
                print(f"  First 10 rows:")
                print(table.df.head(10))
                print()

                # Check for numeric values
                numeric_found = False
                for col in table.df.columns:
                    for val in table.df[col]:
                        val_str = str(val).strip()
                        if any(char.isdigit() for char in val_str):
                            numeric_found = True
                            print(f"  ✅ Found numeric value: {val_str}")
                            break
                    if numeric_found:
                        break

                if not numeric_found:
                    print(f"  ❌ No numeric values detected in table {i+1}")
                print()
    except Exception as e:
        print(f"❌ Stream extraction failed: {e}")
        print()

    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print()

    # Determine if Camelot is better
    lattice_success = 'tables_lattice' in locals() and tables_lattice and len(tables_lattice) > 0
    stream_success = 'tables_stream' in locals() and tables_stream and len(tables_stream) > 0

    if lattice_success or stream_success:
        print("✅ SUCCESS: Camelot can extract tables from this PDF!")
        print()
        if lattice_success:
            best_table = tables_lattice[0]
            print(f"   Best method: LATTICE")
            print(f"   Quality: {best_table.parsing_report['accuracy']:.1f}%")
        else:
            print(f"   Best method: STREAM")
        print()
        print("   Recommendation: Integrate Camelot into PDFParser")
        print("   Implementation: Add fallback chain (pdfplumber → Camelot)")
        return True
    else:
        print("❌ FAILED: Camelot cannot extract tables from this PDF")
        print()
        print("   Possible reasons:")
        print("   - PDF uses complex layout/graphics")
        print("   - Numbers embedded in images")
        print("   - Scanned document (needs OCR)")
        print()
        print("   Recommendation: Try OCR (pdf2image + pytesseract)")
        return False

if __name__ == "__main__":
    try:
        success = test_camelot_extraction()
        if success:
            print()
            print("🎉 Next step: Integrate Camelot into src/document_processing/pdf_parser.py")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
