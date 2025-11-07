"""
Extract financial data from 3 years of Azoty annual reports (2022, 2023, 2024)
Phase 2: Data Extraction & Preparation for multi-year analysis
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.document_processing.ai_enhanced_extractor import AIEnhancedExtractor
import json
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def extract_multi_year_data():
    """
    Extract financial data from 3 years of Azoty reports

    Returns:
        dict: Combined multi-year dataset
    """
    print("=" * 80)
    print("MULTI-YEAR FINANCIAL DATA EXTRACTION")
    print("Grupa Azoty S.A. - 2022, 2023, 2024")
    print("=" * 80)
    print()

    extractor = AIEnhancedExtractor()

    # PDF paths (Financial Statements contain the key data)
    reports = {
        2022: Path("data/documents/grupa_azoty/Grupa_Azoty_Consolidated_Financial_Statements_2022.pdf"),
        2023: Path("data/documents/grupa_azoty/Grupa_Azoty_Consolidated_Financial_Statements_2023.pdf"),
        2024: Path("data/documents/grupa_azoty/Grupa_Azoty_Consolidated_Financial_Statements_2024.pdf")
    }

    # Initialize multi-year structure
    multi_year_data = {
        "company_name": "Grupa Azoty S.A.",
        "industry": "Chemicals & Fertilizers",
        "currency": "PLN",
        "unit": "thousands",
        "extraction_date": datetime.now().isoformat(),
        "years_covered": [2022, 2023, 2024],
        "balance_sheet": {},
        "income_statement": {},
        "cash_flow": {},
        "extraction_metadata": {}
    }

    # Extract each year
    for year, pdf_path in sorted(reports.items()):
        if not pdf_path.exists():
            print(f"❌ {year}: File not found - {pdf_path}")
            continue

        print(f"\n{'=' * 80}")
        print(f"Extracting {year} data from: {pdf_path.name}")
        print(f"{'=' * 80}")

        try:
            result = extractor.extract(pdf_path)

            if result.success:
                print(f"✅ {year}: Successfully extracted {len(result.data)} metrics")
                if result.quality_metrics:
                    print(f"   Quality Score: {result.quality_metrics.overall_score:.1%}")
                    print(f"   Completeness: {result.quality_metrics.completeness_score:.1%}")
                    print(f"   Confidence: {result.quality_metrics.confidence_score:.1%}")

                # Add year dimension to all metrics
                for metric, value in result.data.items():
                    # Categorize metrics
                    if any(keyword in metric.lower() for keyword in ['asset', 'liability', 'equity', 'capital']):
                        category = 'balance_sheet'
                    elif any(keyword in metric.lower() for keyword in ['revenue', 'income', 'expense', 'profit', 'loss', 'ebit', 'ebitda']):
                        category = 'income_statement'
                    elif any(keyword in metric.lower() for keyword in ['cash flow', 'operating', 'investing', 'financing']):
                        category = 'cash_flow'
                    else:
                        # Default to balance sheet for uncategorized
                        category = 'balance_sheet'

                    # Add to multi-year structure
                    if metric not in multi_year_data[category]:
                        multi_year_data[category][metric] = {}

                    multi_year_data[category][metric][year] = value

                # Store metadata
                multi_year_data['extraction_metadata'][year] = {
                    "quality_score": result.quality_metrics.overall_score if result.quality_metrics else 0.0,
                    "completeness": result.quality_metrics.completeness_score if result.quality_metrics else 0.0,
                    "confidence": result.quality_metrics.confidence_score if result.quality_metrics else 0.0,
                    "metrics_extracted": len(result.data),
                    "source_file": pdf_path.name
                }

                # Print sample metrics
                print(f"\n   Sample Balance Sheet Metrics:")
                sample_bs = [k for k in result.data.keys() if 'asset' in k.lower() or 'liability' in k.lower()][:3]
                for metric in sample_bs:
                    print(f"     - {metric}: {result.data[metric]:,.0f}")

                print(f"\n   Sample Income Statement Metrics:")
                sample_is = [k for k in result.data.keys() if 'revenue' in k.lower() or 'ebit' in k.lower()][:3]
                for metric in sample_is:
                    if metric in result.data:
                        print(f"     - {metric}: {result.data[metric]:,.0f}")

            else:
                print(f"❌ {year}: Extraction failed - {result.error}")
                multi_year_data['extraction_metadata'][year] = {
                    "error": result.error,
                    "source_file": pdf_path.name
                }

        except Exception as e:
            print(f"❌ {year}: Exception during extraction - {str(e)}")
            multi_year_data['extraction_metadata'][year] = {
                "error": str(e),
                "source_file": pdf_path.name
            }

    # Calculate multi-year trends
    print(f"\n{'=' * 80}")
    print("MULTI-YEAR TREND ANALYSIS")
    print(f"{'=' * 80}")

    for category in ['balance_sheet', 'income_statement', 'cash_flow']:
        if multi_year_data[category]:
            print(f"\n{category.replace('_', ' ').title()}:")

            for metric, years_data in list(multi_year_data[category].items())[:5]:  # Show top 5
                if len(years_data) >= 2:
                    years_sorted = sorted(years_data.keys())
                    first_year = years_sorted[0]
                    last_year = years_sorted[-1]
                    first_val = years_data[first_year]
                    last_val = years_data[last_year]

                    if first_val != 0:
                        change_pct = ((last_val - first_val) / abs(first_val)) * 100
                        trend = "📈" if change_pct > 0 else "📉"
                        print(f"  {trend} {metric}:")
                        print(f"     {first_year}: {first_val:,.0f} → {last_year}: {last_val:,.0f} ({change_pct:+.1f}%)")

    # Validate accounting equation for each year
    print(f"\n{'=' * 80}")
    print("ACCOUNTING EQUATION VALIDATION")
    print(f"{'=' * 80}")

    for year in sorted(multi_year_data['years_covered']):
        print(f"\n{year}:")

        # Try to find total assets, liabilities, equity
        total_assets = None
        total_liabilities = None
        total_equity = None

        for metric, years_data in multi_year_data['balance_sheet'].items():
            if year in years_data:
                if 'total assets' in metric.lower() and 'non' not in metric.lower():
                    total_assets = years_data[year]
                elif 'total liabilities' in metric.lower():
                    total_liabilities = years_data[year]
                elif 'total equity' in metric.lower() or ('equity' in metric.lower() and 'total' in metric.lower()):
                    total_equity = years_data[year]

        if all(v is not None for v in [total_assets, total_liabilities, total_equity]):
            balance = total_assets - (total_liabilities + total_equity)
            balance_pct = abs(balance) / total_assets * 100 if total_assets != 0 else 0

            status = "✅ BALANCED" if abs(balance_pct) < 0.1 else "⚠️  IMBALANCED"
            print(f"  Assets = Liabilities + Equity: {status}")
            print(f"  Assets: {total_assets:,.0f}")
            print(f"  Liabilities: {total_liabilities:,.0f}")
            print(f"  Equity: {total_equity:,.0f}")
            print(f"  Balance: {balance:,.0f} ({balance_pct:.3f}%)")
        else:
            print(f"  ⚠️  Cannot validate - missing components")
            print(f"     Assets: {'✓' if total_assets else '✗'}")
            print(f"     Liabilities: {'✓' if total_liabilities else '✗'}")
            print(f"     Equity: {'✓' if total_equity else '✗'}")

    # Save to JSON
    output_dir = Path("data/companies")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "grupa_azoty_multi_year.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(multi_year_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 80}")
    print("✅ EXTRACTION COMPLETE")
    print(f"{'=' * 80}")
    print(f"\nSaved to: {output_file}")

    # Summary statistics
    total_metrics = sum(len(multi_year_data[cat]) for cat in ['balance_sheet', 'income_statement', 'cash_flow'])
    total_data_points = sum(
        len(years_data)
        for cat in ['balance_sheet', 'income_statement', 'cash_flow']
        for years_data in multi_year_data[cat].values()
    )

    print(f"\nExtraction Summary:")
    print(f"  Total unique metrics: {total_metrics}")
    print(f"  Total data points: {total_data_points}")
    print(f"  Balance Sheet metrics: {len(multi_year_data['balance_sheet'])}")
    print(f"  Income Statement metrics: {len(multi_year_data['income_statement'])}")
    print(f"  Cash Flow metrics: {len(multi_year_data['cash_flow'])}")
    print(f"  Years covered: {', '.join(map(str, multi_year_data['years_covered']))}")

    # Show extraction quality
    print(f"\nExtraction Quality by Year:")
    for year in sorted(multi_year_data['years_covered']):
        if year in multi_year_data['extraction_metadata']:
            meta = multi_year_data['extraction_metadata'][year]
            if 'quality_score' in meta:
                print(f"  {year}: Quality {meta['quality_score']:.1%}, "
                      f"Completeness {meta['completeness']:.1%}, "
                      f"Confidence {meta['confidence']:.1%}, "
                      f"{meta['metrics_extracted']} metrics")
            else:
                print(f"  {year}: ❌ {meta.get('error', 'Unknown error')}")

    print(f"\n{'=' * 80}")
    print("Next Step: Ingest PDFs into RAG system")
    print("  python3 scripts/ingest_azoty_multi_year.py")
    print(f"{'=' * 80}")

    return multi_year_data


if __name__ == "__main__":
    try:
        result = extract_multi_year_data()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
