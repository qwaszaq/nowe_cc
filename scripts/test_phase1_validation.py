#!/usr/bin/env python3
"""
Phase 1 Validation Test: Enhanced Prompt Engineering

Tests enhanced prompts for both Gemma-27B and OSS-20B models.
Compares to baseline results from previous tests.
"""

import sys
from pathlib import Path
import time
import json
from typing import Dict, Any
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.intelligence.services.multi_agent_intelligence_service import (
    MultiAgentIntelligenceService,
    ReportMode
)


def load_azoty_data() -> Dict[str, Any]:
    """Load Grupa Azoty structured data from JSON file"""
    data_file = Path(__file__).parent.parent / "data/companies/grupa_azoty_multi_year.json"

    with open(data_file, 'r') as f:
        multi_year_data = json.load(f)

    def convert_year_keys(data_dict):
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

    return company_data


def count_rag_citations(report: str) -> int:
    """Count RAG citations in report (comprehensive citation patterns)"""
    import re

    citations = (
        report.count("(Source") +
        report.count("[Source") +
        len(re.findall(r'Annual Report \d{4}', report)) +
        len(re.findall(r'Directors.*Report', report)) +
        len(re.findall(r'Financial.*Statement', report)) +
        len(re.findall(r',\s*p\.\s*\d+', report))
    )

    return citations


def count_tables(report: str) -> int:
    """Count markdown tables in report"""
    import re

    # Count markdown table headers (lines with |---|---|)
    table_headers = len(re.findall(r'\|[\s\-:]+\|[\s\-:]+\|', report))

    return table_headers


def test_model_with_enhanced_prompts(model_name: str, max_tokens: int = 40000) -> Dict[str, Any]:
    """Test model with Phase 1 enhanced prompts"""
    print(f"\n{'='*80}")
    print(f"TESTING: {model_name} with ENHANCED PROMPTS (Phase 1)")
    print(f"{'='*80}\n")

    service = MultiAgentIntelligenceService(
        llm_base_url="http://192.168.200.226:1234/v1",
        model=model_name,
        max_tokens_per_pass=max_tokens,
        use_rag=True,
        qdrant_url="http://localhost:6333",
        qdrant_collection="rag_documents"
    )

    company_data = load_azoty_data()

    print(f"📊 Generating enhanced report for Grupa Azoty S.A. (2022, 2023, 2024)...")
    print(f"   Industry: Chemicals & Fertilizers")
    print(f"   Mode: COMPREHENSIVE (enhanced prompts enabled)")
    print(f"   Enhancements:")
    if "oss" in model_name.lower():
        print(f"     - Citation enforcement (target: 22+ citations)")
    elif "gemma" in model_name.lower():
        print(f"     - Formatting enforcement (mandatory tables)\n")

    start_time = time.time()

    try:
        result = service.generate_intelligence_report(
            company_data=company_data,
            output_format="markdown",
            report_mode=ReportMode.COMPREHENSIVE
        )

        if not result.get("success"):
            raise Exception(result.get("error", "Unknown error"))

        report = result["report"]
        generation_time = time.time() - start_time

        # Analyze report
        word_count = len(report.split())
        report_length = len(report)
        citations = count_rag_citations(report)
        tables = count_tables(report)

        print(f"✅ Enhanced report generated successfully")
        print(f"   Generation time: {generation_time:.1f}s")
        print(f"   Report length: {report_length:,} chars")
        print(f"   Word count: {word_count:,} words")
        print(f"   RAG citations: {citations}")
        print(f"   Tables: {tables}\n")

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_safe = model_name.replace("/", "_").replace("-", "_")
        output_dir = project_root / "output" / "phase1_enhanced"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"azoty_enhanced_{model_safe}_{timestamp}.md"
        with open(output_file, 'w') as f:
            f.write(report)

        return {
            "success": True,
            "model": model_name,
            "generation_time": generation_time,
            "report_length": report_length,
            "word_count": word_count,
            "rag_citations": citations,
            "tables": tables,
            "output_file": str(output_file)
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "success": False,
            "model": model_name,
            "error": str(e)
        }


def main():
    print("\n" + "="*80)
    print("PHASE 1 VALIDATION: ENHANCED PROMPT ENGINEERING")
    print("="*80)
    print("\nBaseline Results (from previous test):")
    print("  Gemma-27B: 32 citations, good formatting")
    print("  OSS-20B: 8 citations, excellent formatting")
    print()
    print("Phase 1 Targets:")
    print("  Gemma-27B: Improve table consistency (mandatory tables in all sections)")
    print("  OSS-20B: Improve citations 8 → 22+ (175% improvement)")
    print()
    print("Test Configuration:")
    print("  Company: Grupa Azoty S.A.")
    print("  Years: 2022, 2023, 2024")
    print("  Industry: Chemicals & Fertilizers")
    print("  Mode: COMPREHENSIVE (with enhanced prompts)")
    print()

    # Test 1: Gemma-27B with enhanced prompts
    result_gemma = test_model_with_enhanced_prompts("gemma-3-27b-it", max_tokens=40000)

    # Test 2: OSS-20B with enhanced prompts
    result_oss = test_model_with_enhanced_prompts("openai/gpt-oss-20b", max_tokens=40000)

    # Comparison
    print("\n" + "="*80)
    print("PHASE 1 RESULTS vs BASELINE")
    print("="*80)
    print()

    if result_gemma["success"] and result_oss["success"]:
        # Baseline results (from gemma27b_vs_oss20b_40k_fair_comparison.log)
        baseline_gemma_citations = 32
        baseline_oss_citations = 8

        # Phase 1 results
        enhanced_gemma_citations = result_gemma["rag_citations"]
        enhanced_oss_citations = result_oss["rag_citations"]

        gemma_tables = result_gemma["tables"]
        oss_tables = result_oss["tables"]

        print(f"{'Metric':<40} {'Baseline':>15} {'Enhanced':>15} {'Change':>15}")
        print("-" * 90)

        # Gemma-27B
        print(f"\n{'GEMMA-27B':^90}")
        print("-" * 90)
        print(f"{'RAG Citations':<40} {baseline_gemma_citations:>15} {enhanced_gemma_citations:>15} {enhanced_gemma_citations - baseline_gemma_citations:>+15}")
        print(f"{'Tables (enforced)':<40} {'N/A':>15} {gemma_tables:>15} {'✓ ENFORCED':>15}")

        # OSS-20B
        print(f"\n{'OSS-20B':^90}")
        print("-" * 90)
        print(f"{'RAG Citations':<40} {baseline_oss_citations:>15} {enhanced_oss_citations:>15} {enhanced_oss_citations - baseline_oss_citations:>+15}")
        print(f"{'Tables':<40} {'N/A':>15} {oss_tables:>15} {'✓ CHECKED':>15}")

        # Calculate improvements
        oss_citation_improvement = ((enhanced_oss_citations - baseline_oss_citations) / baseline_oss_citations * 100) if baseline_oss_citations > 0 else 0

        print(f"\n📈 IMPROVEMENTS")
        print("-" * 80)
        print(f"OSS-20B Citation Improvement: {oss_citation_improvement:+.1f}% (target: +175% to reach 22 citations)")

        if enhanced_oss_citations >= 22:
            print(f"✅ OSS-20B TARGET MET: {enhanced_oss_citations} citations (≥22)")
        else:
            print(f"⚠️  OSS-20B TARGET PARTIAL: {enhanced_oss_citations} citations (target: 22)")
            print(f"   Gap to close: {22 - enhanced_oss_citations} more citations needed")

        if gemma_tables >= 10:  # Expect at least 10 tables in comprehensive mode
            print(f"✅ Gemma-27B TABLE ENFORCEMENT WORKING: {gemma_tables} tables detected")
        else:
            print(f"⚠️  Gemma-27B TABLE COUNT LOW: {gemma_tables} tables (expected ≥10)")

        # Save results
        output_dir = project_root / "output" / "phase1_enhanced"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        results_file = output_dir / f"phase1_validation_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "test_date": datetime.now().isoformat(),
                "baseline": {
                    "gemma_27b_citations": baseline_gemma_citations,
                    "oss_20b_citations": baseline_oss_citations
                },
                "enhanced": {
                    "gemma_27b": result_gemma,
                    "oss_20b": result_oss
                },
                "improvements": {
                    "oss_citation_improvement_pct": oss_citation_improvement,
                    "oss_target_met": enhanced_oss_citations >= 22,
                    "gemma_table_enforcement": gemma_tables >= 10
                }
            }, f, indent=2)

        print(f"\n✓ Gemma-27B enhanced report: {result_gemma['output_file']}")
        print(f"✓ OSS-20B enhanced report: {result_oss['output_file']}")
        print(f"✓ Validation results: {results_file}")

    else:
        print("❌ One or both tests failed")
        if not result_gemma["success"]:
            print(f"  Gemma-27B error: {result_gemma.get('error')}")
        if not result_oss["success"]:
            print(f"  OSS-20B error: {result_oss.get('error')}")

    print("\n" + "="*80)
    print("PHASE 1 VALIDATION COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
