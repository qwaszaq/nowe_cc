#!/usr/bin/env python3
"""
Test intelligence report generation for Grupa Azoty 2023
Uses local LLM via LM Studio
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from src.intelligence.services.local_intelligence_service import LocalIntelligenceService


def test_azoty_intelligence_report():
    """
    Generate intelligence report for Grupa Azoty using local LLM
    """
    print("=" * 80)
    print("TESTING LOCAL INTELLIGENCE SYSTEM")
    print("=" * 80)
    print()

    # Company data (from LOCAL_EXTRACTION_RESULTS_2023.md - verified 100% accurate)
    company_data = {
        "company_name": "Grupa Azoty S.A.",
        "industry": "Chemicals & Fertilizers",
        "currency": "PLN",

        # Balance sheet (June 30, 2023) - extracted by regex system with 100% accuracy
        "balance_sheet": {
            "Total Assets": {2023: 26019865},
            "Current Assets": {2023: 7904016},
            "Fixed Assets": {2023: 18115849},  # Derived from Total - Current
            "Total Equity": {2023: 8795144},
            "Total Liabilities": {2023: 17224721},
            "Current Liabilities": {2023: 11330491},
            "Long-term Liabilities": {2023: 5894230},  # Derived from Total - Current
            "Cash & Equivalents": {2023: 1405681},
            "Inventories": {2023: 2605887}
        },

        # Income statement (would extract from PDF in full implementation)
        # For now, empty dict - system will note data limitation
        "income_statement": {},

        # Cash flow (would extract from PDF)
        "cash_flow": {}
    }

    print(f"Company: {company_data['company_name']}")
    print(f"Industry: {company_data['industry']}")
    print(f"Data points: {len(company_data['balance_sheet'])} balance sheet metrics")
    print()

    # Initialize service
    print("Initializing Local Intelligence Service...")
    print("  - LLM: openai/gpt-oss-20b (via LM Studio)")
    print("  - Endpoint: http://192.168.200.226:1234/v1")
    print("  - Context window: 44k tokens")
    print("  - Analysis method: Multi-pass (4 passes)")
    print()

    service = LocalIntelligenceService(
        llm_base_url="http://192.168.200.226:1234/v1",
        model="openai/gpt-oss-20b",
        max_tokens_per_pass=4000
    )

    # Generate report
    print("Generating intelligence report...")
    print("This will take 2-5 minutes (4 LLM passes)...")
    print()

    result = service.generate_intelligence_report(company_data)

    print()
    if result['success']:
        print("=" * 80)
        print("✅ REPORT GENERATED SUCCESSFULLY")
        print("=" * 80)
        print()
        print(f"Generation time: {result['metadata']['generation_time_seconds']:.2f} seconds")
        print(f"Report length: {result['metadata']['report_length_chars']:,} characters")
        print(f"Analysis passes: {result['metadata']['passes']}")
        print(f"Model: {result['metadata']['model']}")
        print()

        # Save report
        output_dir = Path("output/intelligence_reports")
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Azoty_Intelligence_Local_{timestamp}.md"
        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['report'])

        print(f"✅ Full report saved to: {output_path}")
        print()

        # Preview
        print("=" * 80)
        print("REPORT PREVIEW (first 3000 characters):")
        print("=" * 80)
        print()
        print(result['report'][:3000])
        print()
        print("[...report continues...]")
        print()
        print("=" * 80)
        print(f"Read full report: {output_path}")
        print("=" * 80)

    else:
        print("=" * 80)
        print("❌ REPORT GENERATION FAILED")
        print("=" * 80)
        print()
        print(f"Error: {result['error']}")
        print()
        print("Troubleshooting:")
        print("1. Check if LM Studio is running at http://192.168.200.226:1234")
        print("2. Verify openai/gpt-oss-20b model is loaded")
        print("3. Check network connectivity to LM Studio server")
        print("4. Review logs above for specific error details")


if __name__ == "__main__":
    test_azoty_intelligence_report()
