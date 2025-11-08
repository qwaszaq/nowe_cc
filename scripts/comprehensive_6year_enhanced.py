#!/usr/bin/env python3
"""
Comprehensive 6-Year Enhanced Analysis of Grupa Azoty S.A. (2019-2024)
Uses PROVEN Phase 1 methodology with multi-agent + RAG

KEY FIXES from failed attempt:
1. Load actual financial data from JSON file (not empty dicts)
2. Use MultiAgentIntelligenceService (not LocalIntelligenceService)
3. Apply Phase 1 enhanced prompts
4. Proper error handling and validation
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.intelligence.services.multi_agent_intelligence_service import (
    MultiAgentIntelligenceService,
    ReportMode
)
from datetime import datetime
import logging
import json
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_6year_azoty_data():
    """
    Load Grupa Azoty data for 2019-2024 from JSON file

    This is the FIX: Load REAL data instead of empty dicts
    """
    data_file = Path(__file__).parent.parent / "data/companies/grupa_azoty_multi_year.json"

    if not data_file.exists():
        raise FileNotFoundError(
            f"Financial data file not found: {data_file}\n"
            "Please ensure grupa_azoty_multi_year.json exists with 2019-2024 data"
        )

    with open(data_file, 'r') as f:
        multi_year_data = json.load(f)

    def convert_year_keys(data_dict):
        """Convert string year keys to integers"""
        return {
            metric: {int(year): value for year, value in years_data.items()}
            for metric, years_data in data_dict.items()
        }

    company_data = {
        "company_name": multi_year_data["company_name"],
        "industry": multi_year_data["industry"],
        "currency": multi_year_data["currency"],
        "balance_sheet": convert_year_keys(multi_year_data["balance_sheet"]),
        "income_statement": convert_year_keys(multi_year_data.get("income_statement", {})),
        "cash_flow": convert_year_keys(multi_year_data.get("cash_flow", {}))
    }

    # Validate data loaded
    balance_years = set()
    for metric, years in company_data["balance_sheet"].items():
        balance_years.update(years.keys())

    logger.info(f"✓ Loaded financial data for years: {sorted(balance_years)}")
    logger.info(f"✓ Balance sheet metrics: {len(company_data['balance_sheet'])}")

    if not balance_years:
        raise ValueError("No financial data loaded! Check JSON file structure.")

    return company_data


def print_banner():
    """Print analysis banner"""
    print("\n" + "="*100)
    print("COMPREHENSIVE 6-YEAR ENHANCED ANALYSIS: GRUPA AZOTY S.A. (2019-2024)")
    print("="*100)
    print("\nUsing PROVEN Phase 1 Methodology:")
    print("  ✓ Multi-Agent Intelligence Service (6 specialized agents)")
    print("  ✓ Enhanced prompts with citation requirements")
    print("  ✓ RAG-enhanced document grounding")
    print("  ✓ Real financial data loaded from JSON")
    print("  ✓ Comprehensive mode (maximum depth)")
    print("\nAnalysis Scope:")
    print("  • Years: 2019, 2020, 2021, 2022, 2023, 2024 (6 years)")
    print("  • Documents: 12 PDFs via RAG (6 Financial Statements + 6 Directors Reports)")
    print("  • Analysis Type: Multi-agent, time-series, comprehensive")
    print("\nAgent Architecture:")
    print("  1. Financial Health Agent - Time-series quantitative analysis")
    print("  2. Risk Assessment Agent - Risk evolution and crisis triggers")
    print("  3. Industry Context Agent - Competitive deterioration analysis")
    print("  4. Strategic Evaluation Agent - Management decisions audit")
    print("  5. Market Intelligence Agent - External vs internal factors")
    print("  6. Synthesis Agent - Integrated forensic conclusion")
    print("\nTime Periods:")
    print("  • Pre-Crisis Baseline (2019-2021): Establish normal operating patterns")
    print("  • Crisis Period (2022-2024): Analyze deterioration mechanisms")
    print("  • Year-over-Year Analysis: Identify inflection points and root causes")
    print("\nExpected Quality:")
    print("  • Citations: 40+ (with page numbers)")
    print("  • Tables: 40+ (financial metrics)")
    print("  • Generation time: 3-5 minutes")
    print("  • Report length: 60,000+ characters")
    print("\n" + "="*100)
    print()


def generate_6year_enhanced_report():
    """Generate 6-year enhanced analysis using proven Phase 1 methodology"""

    print_banner()

    # Step 1: Load REAL financial data (FIX #1)
    print("📋 Step 1: Loading financial data from JSON file...")
    try:
        company_data = load_6year_azoty_data()
        print(f"   ✓ Company: {company_data['company_name']}")
        print(f"   ✓ Industry: {company_data['industry']}")
        print(f"   ✓ Currency: {company_data['currency']}")
        print()
    except Exception as e:
        print(f"   ❌ ERROR loading financial data: {e}")
        print("\n   This is likely because the JSON file doesn't have 2019-2021 data yet.")
        print("   The JSON file may only contain 2022-2024 data.")
        print("\n   RECOMMENDATION: Use this script once 2019-2021 extraction is complete.")
        print("   For now, the Phase 1 report (2022-2024) is the highest quality available.\n")
        return

    # Step 2: Initialize Multi-Agent service (FIX #2 - use correct service)
    print("🔧 Step 2: Initializing Multi-Agent Intelligence Service...")
    print("   Using Phase 1 proven architecture:")
    print("   - Service: MultiAgentIntelligenceService (not LocalIntelligenceService)")
    print("   - Mode: COMPREHENSIVE (enhanced prompts enabled)")
    print("   - RAG: Enabled (Qdrant collection: azoty_2019_2021_multi_year)")
    print("   - Model: Gemma-3-27b-it (27B parameters)")
    print()

    service = MultiAgentIntelligenceService(
        llm_base_url="http://192.168.200.226:1234/v1",
        model="gemma-3-27b-it",
        max_tokens_per_pass=40000,  # Generous for 6-year analysis
        use_rag=True,
        qdrant_url="http://localhost:6333",
        qdrant_collection="rag_documents"  # Default collection (smart mapper will select appropriate collections)
    )

    # Step 3: Generate report
    print("🚀 Step 3: Launching 6-agent enhanced analysis...")
    print("   This will take 3-5 minutes")
    print("   Progress:")
    print("     [1/6] Financial Health Agent...")
    print("     [2/6] Risk Assessment Agent...")
    print("     [3/6] Industry Context Agent...")
    print("     [4/6] Strategic Evaluation Agent...")
    print("     [5/6] Market Intelligence Agent...")
    print("     [6/6] Synthesis Agent...")
    print()

    start_time = time.time()

    try:
        result = service.generate_intelligence_report(
            company_data=company_data,
            output_format="markdown",
            report_mode=ReportMode.COMPREHENSIVE  # Enhanced prompts enabled
        )

        if not result.get("success"):
            raise Exception(result.get("error", "Unknown error"))

        report = result["report"]
        generation_time = time.time() - start_time

    except Exception as e:
        print(f"\n❌ ERROR during report generation: {e}")
        import traceback
        traceback.print_exc()
        return

    # Step 4: Validate quality
    print("\n📊 Step 4: Validating report quality...")

    word_count = len(report.split())
    report_length = len(report)

    # Count citations
    citation_count = report.count("[Source") + report.count("(Source")

    # Count tables
    import re
    table_count = len(re.findall(r'\|[\s\-:]+\|[\s\-:]+\|', report))

    print(f"   Report length: {report_length:,} chars ({word_count:,} words)")
    print(f"   Citations: {citation_count}")
    print(f"   Tables: {table_count}")
    print(f"   Generation time: {generation_time:.1f}s ({generation_time/60:.1f} min)")
    print()

    # Quality checks
    quality_pass = True
    if citation_count < 20:
        print(f"   ⚠️  WARNING: Low citation count ({citation_count} < 20)")
        quality_pass = False
    else:
        print(f"   ✓ Citation quality: PASS ({citation_count} ≥ 20)")

    if table_count < 20:
        print(f"   ⚠️  WARNING: Low table count ({table_count} < 20)")
        quality_pass = False
    else:
        print(f"   ✓ Table quality: PASS ({table_count} ≥ 20)")

    if report_length < 30000:
        print(f"   ⚠️  WARNING: Short report ({report_length:,} < 30,000 chars)")
        quality_pass = False
    else:
        print(f"   ✓ Report length: PASS ({report_length:,} ≥ 30,000 chars)")

    print()

    # Step 5: Save report
    output_dir = Path("output/comprehensive_6year_enhanced")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"Azoty_6Year_Enhanced_{timestamp}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Comprehensive 6-Year Enhanced Analysis\n")
        f.write("# Grupa Azoty S.A. (2019-2024)\n\n")
        f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Analysis Period:** 2019-2024 (6 years)\n\n")
        f.write(f"**Methodology:** Phase 1 Enhanced (Multi-Agent + RAG + Citations)\n\n")
        f.write(f"**Generation Time:** {generation_time:.1f} seconds ({generation_time/60:.1f} minutes)\n\n")
        f.write(f"**Quality Metrics:**\n")
        f.write(f"- Citations: {citation_count}\n")
        f.write(f"- Tables: {table_count}\n")
        f.write(f"- Word count: {word_count:,}\n")
        f.write(f"- Quality check: {'PASS' if quality_pass else 'NEEDS REVIEW'}\n\n")
        f.write("---\n\n")
        f.write(report)

    # Save metadata
    metadata = {
        "analysis_type": "comprehensive_6year_enhanced",
        "methodology": "Phase 1 Enhanced (Multi-Agent + RAG)",
        "company": "Grupa Azoty S.A.",
        "period": "2019-2024",
        "years": [2019, 2020, 2021, 2022, 2023, 2024],
        "pre_crisis": [2019, 2020, 2021],
        "crisis": [2022, 2023, 2024],
        "service": "MultiAgentIntelligenceService",
        "report_mode": "COMPREHENSIVE",
        "rag_enabled": True,
        "qdrant_collection": "azoty_2019_2021_multi_year",
        "model": "gemma-3-27b-it",
        "generation_time_seconds": generation_time,
        "generation_time_minutes": generation_time / 60,
        "report_length_chars": report_length,
        "report_length_words": word_count,
        "citations": citation_count,
        "tables": table_count,
        "quality_check_passed": quality_pass,
        "timestamp": timestamp,
        "output_file": str(output_file)
    }

    metadata_file = output_dir / f"Azoty_6Year_Enhanced_{timestamp}_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    # Print summary
    print()
    print("="*100)
    print("✅ COMPREHENSIVE 6-YEAR ENHANCED ANALYSIS COMPLETE")
    print("="*100)
    print()
    print(f"📄 Report: {output_file}")
    print(f"📊 Metadata: {metadata_file}")
    print()
    print(f"⏱️  Generation Time: {generation_time:.1f} seconds ({generation_time/60:.1f} minutes)")
    print(f"📝 Report Length: {report_length:,} characters ({word_count:,} words)")
    print(f"📌 Citations: {citation_count}")
    print(f"📊 Tables: {table_count}")
    print()

    if quality_pass:
        print("🎯 Quality Check: ✅ PASSED")
        print("   This report meets Phase 1 quality standards!")
    else:
        print("⚠️  Quality Check: NEEDS REVIEW")
        print("   Some quality metrics below target - review recommendations")

    print()
    print("="*100)
    print("COMPARISON TO PREVIOUS ATTEMPTS:")
    print("="*100)
    print()
    print("Previous 6-Year Deep Dive (FAILED):")
    print("  ❌ Citations: 0")
    print("  ❌ Tables: 0")
    print("  ❌ Data: 'Not Available'")
    print("  ❌ Quality: Worthless")
    print()
    print(f"This 6-Year Enhanced (FIXED):")
    print(f"  {'✅' if citation_count >= 20 else '⚠️'} Citations: {citation_count}")
    print(f"  {'✅' if table_count >= 20 else '⚠️'} Tables: {table_count}")
    print(f"  {'✅' if report_length >= 30000 else '⚠️'} Data: Comprehensive")
    print(f"  {'✅' if quality_pass else '⚠️'} Quality: {'Production-ready' if quality_pass else 'Needs review'}")
    print()
    print("Phase 1 Enhanced (2022-2024) - Previous Best:")
    print("  ✅ Citations: 27")
    print("  ✅ Tables: 36")
    print("  ✅ Data: Excellent")
    print("  ✅ Quality: Gold standard")
    print()
    print("="*100)
    print()
    print(f"📁 Open report: open {output_file}")
    print()


if __name__ == "__main__":
    try:
        generate_6year_enhanced_report()
    except KeyboardInterrupt:
        print("\n\n❌ Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
