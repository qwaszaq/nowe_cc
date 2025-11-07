#!/usr/bin/env python3
"""
Test Intelligent Extraction System on Grupa Azoty 2023 Report
Compare local LLM extraction vs Claude benchmark
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# PDF path
PDF_PATH = "investigations/external/grupa_azoty_reports/run_20251104_205052/pdfs/Grupa_Azoty_Skonsolidowane_Sprawozdanie_Finansowe_2023.pdf"

print("="*80)
print("INTELLIGENT EXTRACTION TEST: Grupa Azoty 2023")
print("="*80)
print(f"\nPDF: {PDF_PATH}")
print(f"Size: {Path(PDF_PATH).stat().st_size / 1024 / 1024:.1f} MB")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "="*80)

# Test 1: Check if file exists
print("\n[1/5] Verifying PDF file...")
if not Path(PDF_PATH).exists():
    print(f"❌ ERROR: PDF not found at {PDF_PATH}")
    sys.exit(1)
print("✅ PDF file found")

# Test 2: Try to import extraction modules
print("\n[2/5] Loading extraction modules...")
try:
    from src.document_processing.intelligent_extractor import (
        IntelligentExtractionManager,
        QualityMetrics,
        ExtractionResult
    )
    print("✅ Intelligent extractor loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nAttempting fallback to basic PDF extraction...")
    try:
        import pdfplumber
        import camelot
        print("✅ Basic PDF tools available (pdfplumber, camelot)")
    except ImportError as e2:
        print(f"❌ Basic tools also missing: {e2}")
        sys.exit(1)

# Test 3: Initialize extraction manager
print("\n[3/5] Initializing extraction manager...")
try:
    manager = IntelligentExtractionManager()
    print("✅ Extraction manager initialized")
except Exception as e:
    print(f"❌ Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Run extraction with local LLM
print("\n[4/5] Running intelligent extraction with local LLM...")
print("    Using: E5-large embeddings + gpt-oss-20b")
print("    Target: Balance sheet data from 2023 report")

start_time = time.time()
try:
    result = manager.extract(PDF_PATH)
    extraction_time = time.time() - start_time

    print(f"\n✅ Extraction completed in {extraction_time:.1f}s")

    # Display results
    print("\n" + "="*80)
    print("LOCAL LLM EXTRACTION RESULTS")
    print("="*80)

    if result.success:
        print(f"\n✅ SUCCESS")
        print(f"\nMethod: {result.extraction_method}")

        # Quality metrics
        metrics = result.quality_metrics
        print(f"\n📊 Quality Metrics:")
        print(f"   Overall Score:    {metrics.overall_score:.1%}")
        print(f"   Completeness:     {metrics.completeness:.1%}")
        print(f"   Validation:       {metrics.validation_score:.1%}")
        print(f"   Confidence:       {metrics.confidence_score:.1%}")
        print(f"   Processing Time:  {extraction_time:.1f}s")

        # Extracted data
        print(f"\n💰 Extracted Financial Values:")
        data = result.data
        if data:
            for key, value in data.items():
                if value:
                    print(f"   {key.replace('_', ' ').title()}: {value:,.0f}" if isinstance(value, (int, float)) else f"   {key}: {value}")

        # Calculate ratios if we have the data
        if all(k in data and data[k] for k in ['current_assets', 'current_liabilities']):
            print(f"\n📈 Financial Ratios:")
            current_ratio = data['current_assets'] / data['current_liabilities']
            print(f"   Current Ratio:    {current_ratio:.2f}")

            if 'total_equity' in data and data['total_equity']:
                debt_to_equity = data['total_liabilities'] / data['total_equity']
                print(f"   Debt to Equity:   {debt_to_equity:.2f}")

            working_capital = data['current_assets'] - data['current_liabilities']
            print(f"   Working Capital:  {working_capital:,.0f}")

    else:
        print(f"\n❌ EXTRACTION FAILED")
        print(f"Error: {result.error}")
        if result.data:
            print(f"\nPartial data extracted: {len(result.data)} fields")

    # Save results
    output_file = "test_results_local_extraction_2023.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'success': result.success,
            'extraction_method': result.extraction_method,
            'quality_metrics': {
                'overall_score': metrics.overall_score,
                'completeness': metrics.completeness,
                'validation_score': metrics.validation_score,
                'confidence_score': metrics.confidence_score,
            },
            'data': result.data,
            'processing_time': extraction_time,
            'error': result.error
        }, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")

except Exception as e:
    print(f"\n❌ Extraction failed with error:")
    print(f"   {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Prepare for Claude benchmark
print("\n[5/5] Local extraction complete!")
print("\n" + "="*80)
print("NEXT STEP: Claude Benchmark Extraction")
print("="*80)
print("\nTo compare quality, Claude will now manually extract from the same PDF")
print("and compare results against the local LLM extraction.\n")

print("✅ Local extraction test complete!")
print(f"Results available in: {output_file}")
