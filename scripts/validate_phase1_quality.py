#!/usr/bin/env python3
"""
Phase 1 Quality Validation: Citation Accuracy & Analysis Depth

CRITICAL: Validate that 231 citations aren't hallucinated before shipping.
"""

import sys
from pathlib import Path
import json
import re
from typing import Dict, List, Any, Tuple
from collections import Counter
import random

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_report(filename: str) -> str:
    """Load report from output directory"""
    report_path = project_root / "output/phase1_enhanced" / filename
    with open(report_path, 'r') as f:
        return f.read()


def extract_all_citations(report: str) -> List[Dict[str, Any]]:
    """Extract all citations from report with context"""
    citations = []

    # Pattern 1: (Source: Document, p. XX)
    pattern1 = r'([^.]+?)\s*\(Source:\s*([^,]+),\s*p\.\s*(\d+)\)'
    for match in re.finditer(pattern1, report):
        citations.append({
            "text": match.group(1).strip(),
            "source": match.group(2).strip(),
            "page": int(match.group(3)),
            "format": "source_with_page",
            "full_citation": match.group(0)
        })

    # Pattern 2: Annual Report YYYY
    pattern2 = r'([^.]+?)\s*(Annual Report\s+\d{4})'
    for match in re.finditer(pattern2, report):
        if "(Source:" not in match.group(0):  # Don't double-count
            citations.append({
                "text": match.group(1).strip(),
                "source": match.group(2).strip(),
                "page": None,
                "format": "annual_report_year",
                "full_citation": match.group(0)
            })

    # Pattern 3: Directors' Report
    pattern3 = r"([^.]+?)\s*(Directors['']?\s*Report)"
    for match in re.finditer(pattern3, report):
        if "(Source:" not in match.group(0):
            citations.append({
                "text": match.group(1).strip(),
                "source": match.group(2).strip(),
                "page": None,
                "format": "directors_report",
                "full_citation": match.group(0)
            })

    # Pattern 4: Financial Statement YYYY
    pattern4 = r'([^.]+?)\s*(Financial\s+Statement[s]?\s+\d{4})'
    for match in re.finditer(pattern4, report):
        if "(Source:" not in match.group(0):
            citations.append({
                "text": match.group(1).strip(),
                "source": match.group(2).strip(),
                "page": None,
                "format": "financial_statement",
                "full_citation": match.group(0)
            })

    return citations


def analyze_citation_patterns(citations: List[Dict]) -> Dict[str, Any]:
    """Analyze citation quality patterns"""

    # Format distribution
    format_dist = Counter(c["format"] for c in citations)

    # Source distribution
    source_dist = Counter(c["source"] for c in citations)

    # Unique vs duplicate citations
    unique_citations = len(set(c["full_citation"] for c in citations))

    # Citations with page numbers
    with_pages = sum(1 for c in citations if c["page"] is not None)

    # Average text length (quality indicator)
    avg_text_len = sum(len(c["text"]) for c in citations) / len(citations) if citations else 0

    return {
        "total_citations": len(citations),
        "unique_citations": unique_citations,
        "duplicate_rate": (len(citations) - unique_citations) / len(citations) if citations else 0,
        "format_distribution": dict(format_dist),
        "source_distribution": dict(source_dist),
        "with_page_numbers": with_pages,
        "page_number_rate": with_pages / len(citations) if citations else 0,
        "avg_citation_text_length": avg_text_len
    }


def extract_financial_metrics(report: str) -> Dict[str, float]:
    """Extract key financial metrics for validation"""
    metrics = {}

    # Debt-to-Equity (the problematic one)
    de_pattern = r'(?:debt[- ]to[- ]equity|D/E|D-E)(?:\s+ratio)?\s*(?:of|:|\s)\s*([\d.]+)'
    de_match = re.search(de_pattern, report, re.IGNORECASE)
    if de_match:
        metrics["debt_to_equity"] = float(de_match.group(1))

    # Current Ratio
    cr_pattern = r'current\s+ratio\s*(?:of|:|\s)\s*([\d.]+)'
    cr_match = re.search(cr_pattern, report, re.IGNORECASE)
    if cr_match:
        metrics["current_ratio"] = float(cr_match.group(1))

    # Interest Coverage
    ic_pattern = r'interest\s+coverage\s*(?:ratio)?\s*(?:of|:|\s)\s*([\d.]+)'
    ic_match = re.search(ic_pattern, report, re.IGNORECASE)
    if ic_match:
        metrics["interest_coverage"] = float(ic_match.group(1))

    # Revenue Growth
    rg_pattern = r'revenue\s+(?:growth|increased|decreased)\s*(?:of|by)?\s*(-?[\d.]+)%'
    rg_match = re.search(rg_pattern, report, re.IGNORECASE)
    if rg_match:
        metrics["revenue_growth_pct"] = float(rg_match.group(1))

    return metrics


def validate_calculations(metrics: Dict[str, float]) -> Dict[str, bool]:
    """Validate financial calculations against known correct values"""

    # Known correct values from Grupa Azoty data (2024)
    expected = {
        "debt_to_equity": {"value": 3.57, "tolerance": 0.2},  # Allow some variation
        "current_ratio": {"value": 0.65, "tolerance": 0.1},
        # Interest coverage and revenue growth are harder to validate without exact data
    }

    validation = {}
    for metric, expected_data in expected.items():
        if metric in metrics:
            actual = metrics[metric]
            expected_val = expected_data["value"]
            tolerance = expected_data["tolerance"]

            is_correct = abs(actual - expected_val) <= tolerance
            validation[metric] = {
                "actual": actual,
                "expected": expected_val,
                "correct": is_correct,
                "error": abs(actual - expected_val)
            }
        else:
            validation[metric] = {
                "actual": None,
                "expected": expected_data["value"],
                "correct": False,
                "error": None,
                "note": "Metric not found in report"
            }

    return validation


def manual_citation_check(citations: List[Dict], sample_size: int = 20) -> float:
    """
    Manual validation of citation quality.
    Returns accuracy rate (0.0 - 1.0)
    """

    if len(citations) < sample_size:
        sample = citations
    else:
        sample = random.sample(citations, sample_size)

    print("\n" + "="*80)
    print("MANUAL CITATION QUALITY CHECK")
    print("="*80)
    print(f"\nValidating {len(sample)} randomly selected citations...")
    print("For each citation, assess if it appears accurate and relevant.\n")

    accurate_count = 0

    for i, citation in enumerate(sample, 1):
        print(f"\n[{i}/{len(sample)}]")
        print("-" * 80)
        print(f"Statement: {citation['text'][:200]}...")
        print(f"Source: {citation['source']}", end="")
        if citation['page']:
            print(f", p. {citation['page']}")
        else:
            print()
        print(f"Format: {citation['format']}")

        while True:
            response = input("\nIs this citation accurate & relevant? (y/n/s=skip): ").lower().strip()
            if response in ['y', 'n', 's']:
                break
            print("Please enter y, n, or s")

        if response == 'y':
            accurate_count += 1
        elif response == 's':
            continue

    accuracy = accurate_count / len(sample)

    print("\n" + "="*80)
    print(f"📊 CITATION ACCURACY: {accuracy:.1%} ({accurate_count}/{len(sample)})")
    print("="*80)

    return accuracy


def compare_reports_depth(gemma_report: str, oss_report: str) -> Dict[str, Any]:
    """Compare analysis depth between models"""

    comparison = {}

    # Length comparison
    comparison["length"] = {
        "gemma": len(gemma_report),
        "oss": len(oss_report),
        "ratio": len(gemma_report) / len(oss_report) if len(oss_report) > 0 else 0
    }

    # Word count
    comparison["word_count"] = {
        "gemma": len(gemma_report.split()),
        "oss": len(oss_report.split()),
    }

    # Risk identification (count "risk" mentions)
    comparison["risk_mentions"] = {
        "gemma": len(re.findall(r'\brisk\b', gemma_report, re.IGNORECASE)),
        "oss": len(re.findall(r'\brisk\b', oss_report, re.IGNORECASE)),
    }

    # Financial metrics mentioned
    metrics_patterns = [
        r'debt[- ]to[- ]equity',
        r'current\s+ratio',
        r'interest\s+coverage',
        r'ROE|return\s+on\s+equity',
        r'EBITDA',
        r'working\s+capital'
    ]

    comparison["metrics_coverage"] = {
        "gemma": sum(1 for p in metrics_patterns if re.search(p, gemma_report, re.IGNORECASE)),
        "oss": sum(1 for p in metrics_patterns if re.search(p, oss_report, re.IGNORECASE)),
    }

    # Tables
    comparison["tables"] = {
        "gemma": len(re.findall(r'\|[\s\-:]+\|[\s\-:]+\|', gemma_report)),
        "oss": len(re.findall(r'\|[\s\-:]+\|[\s\-:]+\|', oss_report)),
    }

    return comparison


def main():
    print("\n" + "="*80)
    print("PHASE 1 QUALITY VALIDATION: CITATION ACCURACY & ANALYSIS DEPTH")
    print("="*80)
    print("\nBEFORE celebrating 231 citations, we need to validate quality...")
    print()

    # Load reports
    print("📄 Loading reports...")
    gemma_report = load_report("azoty_enhanced_gemma_3_27b_it_20251108_105929.md")
    oss_report = load_report("azoty_enhanced_openai_gpt_oss_20b_20251108_110038.md")
    print("✓ Reports loaded\n")

    # =========================================================================
    # STEP 1: Citation Pattern Analysis
    # =========================================================================
    print("="*80)
    print("STEP 1: CITATION PATTERN ANALYSIS")
    print("="*80)

    gemma_citations = extract_all_citations(gemma_report)
    oss_citations = extract_all_citations(oss_report)

    print(f"\nGemma-27B: {len(gemma_citations)} citations extracted")
    print(f"OSS-20B: {len(oss_citations)} citations extracted")

    gemma_patterns = analyze_citation_patterns(gemma_citations)
    oss_patterns = analyze_citation_patterns(oss_citations)

    print(f"\n{'Metric':<40} {'Gemma-27B':>20} {'OSS-20B':>20}")
    print("-" * 80)
    print(f"{'Total Citations':<40} {gemma_patterns['total_citations']:>20} {oss_patterns['total_citations']:>20}")
    print(f"{'Unique Citations':<40} {gemma_patterns['unique_citations']:>20} {oss_patterns['unique_citations']:>20}")
    print(f"{'Duplicate Rate':<40} {gemma_patterns['duplicate_rate']:>19.1%} {oss_patterns['duplicate_rate']:>19.1%}")
    print(f"{'Citations with Page Numbers':<40} {gemma_patterns['with_page_numbers']:>20} {oss_patterns['with_page_numbers']:>20}")
    print(f"{'Page Number Rate':<40} {gemma_patterns['page_number_rate']:>19.1%} {oss_patterns['page_number_rate']:>19.1%}")
    print(f"{'Avg Citation Text Length':<40} {gemma_patterns['avg_citation_text_length']:>19.0f} {oss_patterns['avg_citation_text_length']:>19.0f}")

    # Red flags
    print("\n🚨 RED FLAGS CHECK:")
    red_flags = []

    if oss_patterns['duplicate_rate'] > 0.3:
        red_flags.append(f"❌ High duplicate rate: {oss_patterns['duplicate_rate']:.1%}")

    if oss_patterns['page_number_rate'] < 0.3:
        red_flags.append(f"⚠️  Low page number rate: {oss_patterns['page_number_rate']:.1%}")

    if oss_patterns['avg_citation_text_length'] < 20:
        red_flags.append(f"⚠️  Short citation text: {oss_patterns['avg_citation_text_length']:.0f} chars")

    if red_flags:
        for flag in red_flags:
            print(f"  {flag}")
    else:
        print("  ✅ No obvious red flags in citation patterns")

    # =========================================================================
    # STEP 2: Financial Calculations Validation
    # =========================================================================
    print("\n" + "="*80)
    print("STEP 2: FINANCIAL CALCULATIONS VALIDATION")
    print("="*80)

    gemma_metrics = extract_financial_metrics(gemma_report)
    oss_metrics = extract_financial_metrics(oss_report)

    print("\nExtracted metrics:")
    print(f"\nGemma-27B:")
    for metric, value in gemma_metrics.items():
        print(f"  {metric}: {value}")

    print(f"\nOSS-20B:")
    for metric, value in oss_metrics.items():
        print(f"  {metric}: {value}")

    print("\nValidating OSS-20B calculations...")
    validation = validate_calculations(oss_metrics)

    calculations_ok = True
    for metric, result in validation.items():
        status = "✅" if result['correct'] else "❌"
        print(f"\n{status} {metric}:")
        print(f"  Actual: {result['actual']}")
        print(f"  Expected: {result['expected']}")
        if result['error'] is not None:
            print(f"  Error: {result['error']:.2f}")
        if not result['correct']:
            calculations_ok = False
            if 'note' in result:
                print(f"  Note: {result['note']}")

    # =========================================================================
    # STEP 3: Manual Citation Quality Check
    # =========================================================================
    print("\n" + "="*80)
    print("STEP 3: MANUAL CITATION QUALITY CHECK")
    print("="*80)
    print("\nWe'll sample 20 random OSS-20B citations for manual validation.")
    print("This is the CRITICAL test - are these real or hallucinated?\n")

    proceed = input("Proceed with manual check? (y/n): ").lower().strip()

    if proceed == 'y':
        citation_accuracy = manual_citation_check(oss_citations, sample_size=20)
    else:
        print("\nSkipping manual check. Setting accuracy to 0.0 (unknown)")
        citation_accuracy = 0.0

    # =========================================================================
    # STEP 4: Analysis Depth Comparison
    # =========================================================================
    print("\n" + "="*80)
    print("STEP 4: ANALYSIS DEPTH COMPARISON")
    print("="*80)

    depth_comparison = compare_reports_depth(gemma_report, oss_report)

    print(f"\n{'Metric':<40} {'Gemma-27B':>20} {'OSS-20B':>20} {'Winner':>15}")
    print("-" * 90)

    for category, data in depth_comparison.items():
        if category in ["length", "word_count", "risk_mentions", "metrics_coverage", "tables"]:
            gemma_val = data["gemma"]
            oss_val = data["oss"]
            winner = "Gemma-27B" if gemma_val > oss_val else "OSS-20B" if oss_val > gemma_val else "Tie"

            print(f"{category.replace('_', ' ').title():<40} {gemma_val:>20} {oss_val:>20} {winner:>15}")

    # =========================================================================
    # FINAL VERDICT
    # =========================================================================
    print("\n" + "="*80)
    print("FINAL VERDICT & RECOMMENDATIONS")
    print("="*80)

    print("\n📊 QUALITY ASSESSMENT:")
    print(f"  Citation Accuracy: {citation_accuracy:.1%}")
    print(f"  Calculations Correct: {'✅ YES' if calculations_ok else '❌ NO'}")
    print(f"  Duplicate Rate: {oss_patterns['duplicate_rate']:.1%}")
    print(f"  Page Number Coverage: {oss_patterns['page_number_rate']:.1%}")

    # Decision logic
    print("\n🎯 RECOMMENDATION:")

    if citation_accuracy >= 0.8 and calculations_ok:
        print("\n✅ EXCELLENT - OSS-20B WITH ENHANCED PROMPTS IS PRODUCTION-READY!")
        print("\nNext Steps:")
        print("  1. Ship Phase 1 enhanced prompts to production")
        print("  2. Add calculation validation layer (defensive programming)")
        print("  3. Monitor citation quality in production")
        print("  4. Phase 2/3 not needed - you have a winner!")
        recommendation = "SHIP_PHASE1"

    elif citation_accuracy >= 0.6 and calculations_ok:
        print("\n⚠️  GOOD BUT NEEDS REFINEMENT")
        print("\nNext Steps:")
        print("  1. Refine citation prompts to improve quality")
        print("  2. Add examples of high-quality citations")
        print("  3. Re-test and aim for 80%+ accuracy")
        print("  4. Then ship if improved")
        recommendation = "REFINE_PROMPTS"

    elif citation_accuracy < 0.6 or not calculations_ok:
        print("\n🔄 PROCEED TO PHASE 2: AGENT SPECIALIZATION")
        print("\nIssues identified:")
        if citation_accuracy < 0.6:
            print(f"  - Citation accuracy too low: {citation_accuracy:.1%} (need 60%+)")
        if not calculations_ok:
            print("  - Financial calculations incorrect")

        print("\nNext Steps:")
        print("  1. Use Gemma-27B for financial calculations (proven accurate)")
        print("  2. Use OSS-20B for formatting/structure (proven fast)")
        print("  3. Build hybrid multi-model system (Phase 2)")
        print("  4. Specialized agents get specialized models")
        recommendation = "PROCEED_PHASE2"

    else:
        print("\n❓ UNCLEAR - MORE INVESTIGATION NEEDED")
        recommendation = "INVESTIGATE"

    # Save validation results
    output_dir = project_root / "output" / "phase1_enhanced"
    validation_file = output_dir / "quality_validation_results.json"

    with open(validation_file, 'w') as f:
        json.dump({
            "timestamp": "2025-11-08T10:02:41Z",
            "citation_patterns": {
                "gemma": gemma_patterns,
                "oss": oss_patterns
            },
            "financial_metrics": {
                "gemma": gemma_metrics,
                "oss": oss_metrics,
                "validation": validation
            },
            "citation_accuracy": citation_accuracy,
            "calculations_correct": calculations_ok,
            "depth_comparison": depth_comparison,
            "recommendation": recommendation
        }, f, indent=2)

    print(f"\n✓ Validation results saved: {validation_file}")
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
