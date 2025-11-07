"""
Benchmark Test: Local System vs Claude Manual Extraction

Tests intelligent extraction system on Grupa Azoty 2023 report
and compares results with manual Claude extraction.

Author: Destiny Team
Date: 2025-11-06
"""

import sys
sys.path.insert(0, '.')

from pathlib import Path
from src.document_processing.extraction_manager import IntelligentExtractionManager


def test_local_system():
    """Test local intelligent extraction system"""
    print("=" * 80)
    print("TEST 1: LOCAL INTELLIGENT EXTRACTION SYSTEM")
    print("=" * 80)
    print()

    manager = IntelligentExtractionManager()
    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2023.pdf'

    print(f"📄 File: {Path(pdf_path).name}")
    print(f"🤖 Extractor: Intelligent Multi-Source System (Local)")
    print()

    result = manager.extract(Path(pdf_path))

    if not result.success:
        print(f"❌ EXTRACTION FAILED")
        print(f"   Error: {result.error}")
        return None

    metrics = result.quality_metrics

    print(f"✅ EXTRACTION SUCCESSFUL")
    print()
    print(f"📊 Quality Metrics:")
    print(f"   Overall Score:    {metrics.overall_score:.1%}")
    print(f"   Completeness:     {metrics.completeness_score:.1%} ({metrics.required_fields_found}/{metrics.required_fields_total} fields)")
    print(f"   Validation:       {metrics.validation_score:.1%}")
    print(f"   Confidence:       {metrics.confidence_score:.1%}")
    print(f"   Method:           {metrics.extraction_method}")
    print(f"   Processing Time:  {metrics.processing_time:.2f}s")

    if metrics.warnings:
        print(f"\n⚠️  Warnings:")
        for warning in metrics.warnings:
            print(f"   - {warning}")

    print(f"\n💰 Extracted Financial Values (2023):")
    print(f"   {'Item':<30s} {'Value':>20s}")
    print(f"   {'-'*30} {'-'*20}")

    field_labels = {
        'total_assets': 'Total Assets',
        'total_equity': 'Total Equity',
        'total_liabilities': 'Total Liabilities',
        'current_assets': 'Current Assets',
        'current_liabilities': 'Current Liabilities',
        'fixed_assets': 'Fixed Assets',
        'cash': 'Cash & Equivalents',
        'inventories': 'Inventories',
    }

    for field, label in field_labels.items():
        value = result.data.get(field)
        if value is not None:
            print(f"   {label:<30s} {value:>20,.0f}")
        else:
            print(f"   {label:<30s} {'NOT FOUND':>20s}")

    # Accounting Equation
    assets = result.data.get('total_assets', 0)
    equity = result.data.get('total_equity', 0)
    liabilities = result.data.get('total_liabilities', 0)

    if assets and equity and liabilities:
        balance = equity + liabilities
        diff = abs(assets - balance)
        diff_pct = (diff / assets * 100) if assets > 0 else 0

        print(f"\n📐 Accounting Equation:")
        print(f"   Assets:               {assets:>20,.0f}")
        print(f"   Equity + Liabilities: {balance:>20,.0f}")
        print(f"   Difference:           {diff:>20,.0f} ({diff_pct:.2f}%)")

        if diff < assets * 0.01:
            print(f"   ✅ BALANCE SHEET BALANCES")
        else:
            print(f"   ⚠️  Balance sheet doesn't balance")

    # Financial Ratios
    current_assets = result.data.get('current_assets')
    current_liabilities = result.data.get('current_liabilities')

    if current_assets and current_liabilities and current_liabilities > 0:
        print(f"\n📈 Financial Ratios (2023):")

        current_ratio = current_assets / current_liabilities
        print(f"   Current Ratio:        {current_ratio:>20.2f} {'✅' if current_ratio > 1.0 else '⚠️ LOW'}")

        cash = result.data.get('cash', 0)
        if cash:
            cash_ratio = cash / current_liabilities
            print(f"   Cash Ratio:           {cash_ratio:>20.2f}")

        if equity and equity > 0:
            debt_to_equity = liabilities / equity
            print(f"   Debt to Equity:       {debt_to_equity:>20.2f} {'⚠️ HIGH' if debt_to_equity > 2.0 else '✅'}")

        working_capital = current_assets - current_liabilities
        print(f"   Working Capital:      {working_capital:>20,.0f} {'⚠️ NEG' if working_capital < 0 else '✅'}")

    print()
    return result


def print_comparison(local_result, claude_data):
    """Compare local system results with Claude manual extraction"""
    print("=" * 80)
    print("COMPARISON: LOCAL SYSTEM vs CLAUDE MANUAL EXTRACTION")
    print("=" * 80)
    print()

    print(f"{'Metric':<30s} {'Local System':>20s} {'Claude Manual':>20s} {'Match':>10s}")
    print(f"{'-'*30} {'-'*20} {'-'*20} {'-'*10}")

    field_labels = {
        'total_assets': 'Total Assets',
        'total_equity': 'Total Equity',
        'total_liabilities': 'Total Liabilities',
        'current_assets': 'Current Assets',
        'current_liabilities': 'Current Liabilities',
        'fixed_assets': 'Fixed Assets',
        'cash': 'Cash & Equivalents',
        'inventories': 'Inventories',
    }

    matches = 0
    total = 0

    for field, label in field_labels.items():
        local_val = local_result.data.get(field) if local_result else None
        claude_val = claude_data.get(field)

        local_str = f"{local_val:,.0f}" if local_val else "NOT FOUND"
        claude_str = f"{claude_val:,.0f}" if claude_val else "NOT FOUND"

        # Check if values match (within 0.1% tolerance for rounding)
        if local_val and claude_val:
            total += 1
            diff_pct = abs(local_val - claude_val) / claude_val * 100 if claude_val > 0 else 100
            if diff_pct < 0.1:
                match_str = "✅"
                matches += 1
            else:
                match_str = f"❌ {diff_pct:.1f}%"
        elif not local_val and not claude_val:
            match_str = "N/A"
        else:
            total += 1
            match_str = "❌"

        print(f"{label:<30s} {local_str:>20s} {claude_str:>20s} {match_str:>10s}")

    print(f"{'-'*30} {'-'*20} {'-'*20} {'-'*10}")

    if total > 0:
        accuracy = matches / total * 100
        print(f"\n📊 Accuracy: {matches}/{total} fields match ({accuracy:.1f}%)")

        if accuracy >= 90:
            print(f"   ✅ EXCELLENT - Local system matches Claude manual extraction")
        elif accuracy >= 75:
            print(f"   🟡 GOOD - Most values match with minor discrepancies")
        elif accuracy >= 50:
            print(f"   🟠 FAIR - Significant differences detected")
        else:
            print(f"   ❌ POOR - Major discrepancies, needs investigation")

    # Quality comparison
    if local_result:
        print(f"\n📈 Quality Analysis:")
        metrics = local_result.quality_metrics
        print(f"   Local System Quality: {metrics.overall_score:.1%}")
        print(f"   Completeness:         {metrics.completeness_score:.1%}")
        print(f"   Validation:           {metrics.validation_score:.1%}")
        print(f"   Processing Time:      {metrics.processing_time:.2f}s")
        print(f"\n   Claude Manual:")
        print(f"   Time Required:        ~5-10 minutes (manual PDF reading)")
        print(f"   Accuracy:             100% (ground truth)")

        print(f"\n🎯 Speed Advantage: {(5*60 / metrics.processing_time):.1f}x faster than manual")


def main():
    """Run benchmark test"""
    print("\n" + "🎯" * 40)
    print("BENCHMARK TEST: LOCAL SYSTEM vs CLAUDE MANUAL EXTRACTION")
    print("Document: Grupa Azoty Tarnów Annual Report 2023")
    print("🎯" * 40)
    print()

    # Test 1: Local system extraction
    local_result = test_local_system()

    # Test 2: Claude manual extraction (placeholder - will be filled in after I read the PDF)
    print("\n" + "=" * 80)
    print("TEST 2: CLAUDE MANUAL EXTRACTION")
    print("=" * 80)
    print()
    print("📄 Claude will now manually read the PDF and extract values...")
    print("⏳ Please wait while Claude analyzes the document...")
    print()
    print("(This section will be updated with manual extraction results)")
    print()

    # Placeholder for Claude manual data (will be filled after PDF reading)
    claude_data = {
        # Will be populated after manual extraction
    }

    print("=" * 80)
    print("NOTE: Manual extraction in progress...")
    print("Results will be compared once Claude completes manual analysis.")
    print("=" * 80)


if __name__ == "__main__":
    main()
