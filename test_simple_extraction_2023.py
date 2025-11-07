#!/usr/bin/env python3
"""
Simple PDF Extraction Test: Grupa Azoty 2023
Using available tools (pdfplumber + camelot)
"""

import pdfplumber
import camelot
import json
import time
from pathlib import Path
from datetime import datetime
import re

PDF_PATH = "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2023.pdf"

print("="*80)
print("LOCAL EXTRACTION TEST: Grupa Azoty 2023 (Simplified)")
print("="*80)
print(f"\nPDF: {PDF_PATH}")
print(f"Size: {Path(PDF_PATH).stat().st_size / 1024 / 1024:.1f} MB\n")

# Phase 1: Extract tables with Camelot
print("[1/3] Extracting tables with Camelot...")
start = time.time()

try:
    # Extract specific pages likely to contain balance sheet (pages 5-10 typical)
    tables = camelot.read_pdf(PDF_PATH, pages='5-10', flavor='stream')
    camelot_time = time.time() - start

    print(f"✅ Camelot extracted {len(tables)} tables in {camelot_time:.1f}s")

    # Find best table (highest numeric density)
    best_table = None
    best_score = 0

    for i, table in enumerate(tables):
        # Count numeric cells
        numeric_count = 0
        total_cells = 0

        for row in table.data:
            for cell in row:
                total_cells += 1
                # Check if cell contains numbers
                if re.search(r'\d', str(cell)):
                    numeric_count += 1

        if total_cells > 0:
            score = numeric_count / total_cells
            if score > best_score and len(table.data) > 5:  # At least 5 rows
                best_score = score
                best_table = table

    if best_table:
        print(f"\n📊 Best table found:")
        print(f"   Page: {best_table.page}")
        print(f"   Size: {len(best_table.data)} rows × {len(best_table.data[0])} cols")
        print(f"   Numeric density: {best_score:.1%}")
        print(f"   Quality: {best_table.parsing_report['accuracy']:.1%}")

        # Display first few rows
        print(f"\n   First 3 rows:")
        for i, row in enumerate(best_table.data[:3]):
            print(f"   Row {i}: {row[:3]}")  # First 3 columns

        balance_sheet_table = best_table.data
    else:
        print("⚠️ No suitable table found")
        balance_sheet_table = []

except Exception as e:
    print(f"❌ Camelot extraction failed: {e}")
    balance_sheet_table = []

# Phase 2: Extract with pdfplumber (text-based)
print(f"\n[2/3] Extracting text with pdfplumber...")
start = time.time()

financial_values = {}

try:
    with pdfplumber.open(PDF_PATH) as pdf:
        # Focus on pages 5-10 (typical balance sheet location)
        text_all = ""
        for page_num in range(4, min(10, len(pdf.pages))):  # Pages 5-10
            text_all += pdf.pages[page_num].extract_text()

        plumber_time = time.time() - start
        print(f"✅ Extracted {len(text_all)} characters in {plumber_time:.1f}s")

        # Extract key financial values using regex
        patterns = {
            'total_assets': [
                r'AKTYWA\s+RAZEM\s+(\d[\d\s]+)',
                r'Aktywa\s+razem\s+(\d[\d\s]+)',
                r'Total\s+assets\s+(\d[\d\s,]+)'
            ],
            'current_assets': [
                r'Aktywa\s+obrotowe\s+razem\s+(\d[\d\s]+)',
                r'Current\s+assets\s+total\s+(\d[\d\s,]+)'
            ],
            'fixed_assets': [
                r'Aktywa\s+trwałe\s+razem\s+(\d[\d\s]+)',
                r'Non-current\s+assets\s+total\s+(\d[\d\s,]+)'
            ],
            'total_equity': [
                r'Kapitał\s+własny\s+razem\s+(\d[\d\s]+)',
                r'Total\s+equity\s+(\d[\d\s,]+)'
            ],
            'total_liabilities': [
                r'Zobowiązania\s+razem\s+(\d[\d\s]+)',
                r'Total\s+liabilities\s+(\d[\d\s,]+)'
            ],
            'current_liabilities': [
                r'Zobowiązania\s+krótkoterminowe\s+razem\s+(\d[\d\s]+)',
                r'Current\s+liabilities\s+total\s+(\d[\d\s,]+)'
            ]
        }

        for key, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text_all, re.IGNORECASE)
                if match:
                    value_str = match.group(1).replace(' ', '').replace(',', '')
                    try:
                        financial_values[key] = float(value_str)
                        break
                    except ValueError:
                        continue

        print(f"\n💰 Extracted {len(financial_values)} financial values:")
        for key, value in financial_values.items():
            print(f"   {key.replace('_', ' ').title()}: {value:,.0f}")

except Exception as e:
    print(f"❌ pdfplumber extraction failed: {e}")

# Phase 3: Calculate quality metrics
print(f"\n[3/3] Calculating quality metrics...")

# Calculate completeness
required_fields = ['total_assets', 'current_assets', 'fixed_assets',
                   'total_equity', 'total_liabilities', 'current_liabilities']
completeness = len([f for f in required_fields if f in financial_values]) / len(required_fields)

# Validate accounting equation if we have the data
validation_score = 0.0
if all(k in financial_values for k in ['total_assets', 'total_equity', 'total_liabilities']):
    diff = abs(financial_values['total_assets'] -
               (financial_values['total_equity'] + financial_values['total_liabilities']))
    error_pct = diff / financial_values['total_assets']

    if error_pct < 0.01:  # Within 1%
        validation_score = 1.0
    elif error_pct < 0.05:  # Within 5%
        validation_score = 0.8
    else:
        validation_score = 0.0

# Overall quality score
overall_score = (completeness * 0.5) + (validation_score * 0.5)

print(f"\n📊 Quality Metrics:")
print(f"   Completeness:     {completeness:.1%} ({len([f for f in required_fields if f in financial_values])}/{len(required_fields)} fields)")
print(f"   Validation:       {validation_score:.1%}")
print(f"   Overall Score:    {overall_score:.1%}")

# Calculate financial ratios if possible
print(f"\n📈 Financial Ratios:")
if 'current_assets' in financial_values and 'current_liabilities' in financial_values:
    current_ratio = financial_values['current_assets'] / financial_values['current_liabilities']
    print(f"   Current Ratio:    {current_ratio:.2f}")

if 'total_liabilities' in financial_values and 'total_equity' in financial_values:
    debt_to_equity = financial_values['total_liabilities'] / financial_values['total_equity']
    print(f"   Debt to Equity:   {debt_to_equity:.2f}")

if 'current_assets' in financial_values and 'current_liabilities' in financial_values:
    working_capital = financial_values['current_assets'] - financial_values['current_liabilities']
    print(f"   Working Capital:  {working_capital:,.0f}")

# Save results
output = {
    'pdf_path': PDF_PATH,
    'extraction_timestamp': datetime.now().isoformat(),
    'tables_found': len(tables) if 'tables' in locals() else 0,
    'best_table_numeric_density': best_score if best_table else 0,
    'financial_values': financial_values,
    'quality_metrics': {
        'completeness': completeness,
        'validation_score': validation_score,
        'overall_score': overall_score
    },
    'processing_time': {
        'camelot': camelot_time if 'camelot_time' in locals() else 0,
        'pdfplumber': plumber_time if 'plumber_time' in locals() else 0
    }
}

output_file = "LOCAL_EXTRACTION_RESULTS_2023.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n💾 Results saved to: {output_file}")
print("\n" + "="*80)
print("✅ Local extraction complete!")
print("="*80)
