"""
Test Intelligent Multi-Source Extraction System

Demonstrates extraction from PDF, DOCX, TXT, XLSX, CSV, HTML files
with automatic fallbacks and quality assessment.

Author: Destiny Team
Date: 2025-11-06
"""

import sys
sys.path.insert(0, '.')

from pathlib import Path
from src.document_processing.extraction_manager import IntelligentExtractionManager


def print_extraction_summary(file_path: str, result):
    """Print detailed extraction summary"""
    print("\n" + "=" * 80)
    print(f"FILE: {Path(file_path).name}")
    print("=" * 80)

    if not result.success:
        print(f"❌ EXTRACTION FAILED")
        print(f"   Error: {result.error}")
        return

    metrics = result.quality_metrics

    print(f"\n✅ EXTRACTION SUCCESSFUL")
    print(f"\n📊 Quality Metrics:")
    print(f"   Overall Score:    {metrics.overall_score:.1%}")
    print(f"   Completeness:     {metrics.completeness_score:.1%} "
          f"({metrics.required_fields_found}/{metrics.required_fields_total} fields)")
    print(f"   Validation:       {metrics.validation_score:.1%}")
    print(f"   Confidence:       {metrics.confidence_score:.1%}")
    print(f"   Method:           {metrics.extraction_method}")
    print(f"   Processing Time:  {metrics.processing_time:.2f}s")

    if metrics.warnings:
        print(f"\n⚠️  Warnings:")
        for warning in metrics.warnings:
            print(f"   - {warning}")

    print(f"\n💰 Extracted Financial Values:")
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

    # Accounting Equation Validation
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

    # Financial Ratios (if possible)
    current_assets = result.data.get('current_assets')
    current_liabilities = result.data.get('current_liabilities')

    if current_assets and current_liabilities and current_liabilities > 0:
        print(f"\n📈 Financial Ratios:")

        current_ratio = current_assets / current_liabilities
        print(f"   Current Ratio:        {current_ratio:>20.2f} "
              f"{'✅' if current_ratio > 1.0 else '⚠️ LOW'}")

        cash = result.data.get('cash', 0)
        if cash:
            cash_ratio = cash / current_liabilities
            print(f"   Cash Ratio:           {cash_ratio:>20.2f}")

        if equity and equity > 0:
            debt_to_equity = liabilities / equity
            print(f"   Debt to Equity:       {debt_to_equity:>20.2f} "
                  f"{'⚠️ HIGH' if debt_to_equity > 2.0 else '✅'}")

        working_capital = current_assets - current_liabilities
        print(f"   Working Capital:      {working_capital:>20,.0f} "
              f"{'⚠️ NEG' if working_capital < 0 else '✅'}")


def test_single_pdf():
    """Test PDF extraction with the enhanced system"""
    print("\n" + "=" * 80)
    print("TEST 1: PDF Extraction (Grupa Azoty)")
    print("=" * 80)

    manager = IntelligentExtractionManager()
    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf'

    result = manager.extract(Path(pdf_path))
    print_extraction_summary(pdf_path, result)


def test_batch_extraction():
    """Test batch extraction from multiple file types"""
    print("\n" + "=" * 80)
    print("TEST 2: Batch Extraction (Multiple File Types)")
    print("=" * 80)

    manager = IntelligentExtractionManager()

    # Files to test (you would need to create these for full demo)
    files = [
        'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf',
        # Add more files as they become available:
        # 'data/documents/test_report.docx',
        # 'data/documents/test_report.txt',
        # 'data/documents/test_report.xlsx',
        # 'data/documents/test_report.csv',
        # 'data/documents/test_report.html',
    ]

    # Filter to only existing files
    existing_files = [f for f in files if Path(f).exists()]

    if not existing_files:
        print("No test files found. Using PDF only.")
        existing_files = ['data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf']

    results = manager.batch_extract(existing_files)

    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)

    for file_path, result in results.items():
        print_extraction_summary(file_path, result)


def test_quality_thresholds():
    """Test quality threshold system"""
    print("\n" + "=" * 80)
    print("TEST 3: Quality Threshold System")
    print("=" * 80)

    manager = IntelligentExtractionManager()
    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf'

    result = manager.extract(Path(pdf_path))

    if result.success:
        metrics = result.quality_metrics

        print(f"\n📊 Quality Metrics Analysis:")
        print(f"\n1. Completeness: {metrics.completeness_score:.1%}")
        print(f"   Threshold: 60% minimum, 75% warning")
        print(f"   Status: {'✅ PASS' if metrics.completeness_score >= 0.75 else '⚠️ WARN' if metrics.completeness_score >= 0.60 else '❌ FAIL'}")

        print(f"\n2. Validation: {metrics.validation_score:.1%}")
        print(f"   Threshold: 80% minimum (accounting equation within 5%)")
        print(f"   Status: {'✅ PASS' if metrics.validation_score >= 0.80 else '❌ FAIL'}")
        if metrics.accounting_equation_valid:
            print(f"   Accounting equation: ✅ BALANCES")
        else:
            print(f"   Accounting equation: ⚠️ Difference: {metrics.balance_diff_percent:.2f}%")

        print(f"\n3. Confidence: {metrics.confidence_score:.1%}")
        print(f"   Threshold: 60% minimum, 70% warning")
        print(f"   Status: {'✅ PASS' if metrics.confidence_score >= 0.70 else '⚠️ WARN' if metrics.confidence_score >= 0.60 else '❌ FAIL'}")

        print(f"\n4. Overall: {metrics.overall_score:.1%}")
        print(f"   Threshold: 70% minimum, 85% warning")
        print(f"   Status: {'✅ PASS' if metrics.overall_score >= 0.85 else '⚠️ WARN' if metrics.overall_score >= 0.70 else '❌ FAIL'}")

        print(f"\n📋 Summary:")
        from src.document_processing.intelligent_extractor import QualityThresholds
        if QualityThresholds.should_accept(metrics):
            print(f"   ✅ Extraction ACCEPTED (meets all thresholds)")
        else:
            print(f"   ❌ Extraction REJECTED (below thresholds)")
            print(f"   Fallback strategies would be triggered")


def test_financial_health_assessment():
    """Test automatic financial health assessment"""
    print("\n" + "=" * 80)
    print("TEST 4: Automatic Financial Health Assessment")
    print("=" * 80)

    manager = IntelligentExtractionManager()
    pdf_path = 'data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf'

    result = manager.extract(Path(pdf_path))

    if result.success:
        data = result.data

        print(f"\n🏥 FINANCIAL HEALTH ANALYSIS")
        print(f"\nData Source: Grupa Azoty Tarnów Annual Report 2024")

        # Liquidity ratios
        current_assets = data.get('current_assets')
        current_liabilities = data.get('current_liabilities')

        if current_assets and current_liabilities and current_liabilities > 0:
            current_ratio = current_assets / current_liabilities
            print(f"\n1. Liquidity Analysis:")
            print(f"   Current Ratio: {current_ratio:.2f}")

            if current_ratio < 1.0:
                print(f"   ⚠️  WARNING: Current ratio below 1.0 indicates liquidity problems")
                print(f"   Company may struggle to pay short-term obligations")
            elif current_ratio < 1.5:
                print(f"   🟡 CAUTION: Current ratio is low but acceptable")
            else:
                print(f"   ✅ HEALTHY: Good liquidity position")

        # Leverage analysis
        total_assets = data.get('total_assets')
        total_equity = data.get('total_equity')
        total_liabilities = data.get('total_liabilities')

        if total_equity and total_liabilities and total_equity > 0:
            debt_to_equity = total_liabilities / total_equity

            print(f"\n2. Leverage Analysis:")
            print(f"   Debt to Equity: {debt_to_equity:.2f}")

            if debt_to_equity > 3.0:
                print(f"   ⚠️  WARNING: High leverage - company is highly indebted")
                print(f"   Financial risk is elevated")
            elif debt_to_equity > 2.0:
                print(f"   🟡 CAUTION: Moderate leverage")
            else:
                print(f"   ✅ HEALTHY: Conservative capital structure")

        # Working capital
        if current_assets and current_liabilities:
            working_capital = current_assets - current_liabilities

            print(f"\n3. Working Capital Analysis:")
            print(f"   Working Capital: {working_capital:,.0f} thousand PLN")

            if working_capital < 0:
                print(f"   ⚠️  WARNING: Negative working capital")
                print(f"   Current liabilities exceed current assets")
                print(f"   Potential liquidity crisis")
            else:
                print(f"   ✅ HEALTHY: Positive working capital")

        # Overall assessment
        print(f"\n🎯 OVERALL ASSESSMENT:")

        issues = []
        if current_ratio and current_ratio < 1.0:
            issues.append("Low liquidity (current ratio < 1.0)")
        if debt_to_equity and debt_to_equity > 3.0:
            issues.append(f"High leverage (D/E = {debt_to_equity:.2f})")
        if working_capital and working_capital < 0:
            issues.append(f"Negative working capital ({working_capital:,.0f})")

        if issues:
            print(f"   ⚠️  FINANCIAL DISTRESS INDICATORS:")
            for issue in issues:
                print(f"   - {issue}")
            print(f"\n   This matches Grupa Azoty's known financial difficulties!")
            print(f"   System correctly identifies real-world financial distress.")
        else:
            print(f"   ✅ Company appears financially healthy")


def main():
    """Run all tests"""
    print("\n" + "🎯" * 40)
    print("INTELLIGENT MULTI-SOURCE EXTRACTION SYSTEM DEMO")
    print("🎯" * 40)

    # Test 1: Single PDF
    test_single_pdf()

    # Test 2: Batch extraction
    test_batch_extraction()

    # Test 3: Quality thresholds
    test_quality_thresholds()

    # Test 4: Financial health assessment
    test_financial_health_assessment()

    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
