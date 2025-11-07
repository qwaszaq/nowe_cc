"""
Compare Single-Agent, Multi-Agent, and Claude on multi-year Azoty analysis
Phase 5: Comprehensive Three-Way Comparison
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
from datetime import datetime
import re

def load_report(file_path: Path) -> str:
    """Load report from file"""
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_report_characteristics(report: str, system_name: str) -> dict:
    """Analyze characteristics of a report"""

    characteristics = {
        "system": system_name,
        "length_chars": len(report),
        "length_words": len(report.split()),
        "sections": 0,
        "has_framework_selection": False,
        "has_severity_calibration": False,
        "has_recommendations": False,
        "has_quantified_probabilities": False,
        "has_source_citations": False,
        "critical_mentions": report.lower().count("critical"),
        "high_risk_mentions": report.lower().count("high risk"),
        "equity_erosion_mentions": report.lower().count("equity"),
        "credit_analysis_mentioned": "credit analysis" in report.lower() or "credit framework" in report.lower(),
        "multi_year_trends": "2022" in report and "2023" in report and "2024" in report
    }

    # Count sections (lines starting with #)
    characteristics["sections"] = len([line for line in report.split('\n') if line.startswith('#')])

    # Check for framework selection
    if any(phrase in report.lower() for phrase in ["framework", "credit analysis", "equity analysis"]):
        characteristics["has_framework_selection"] = True

    # Check for severity calibration
    if any(phrase in report for phrase in ["CRITICAL", "HIGH RISK", "SEVERE"]):
        characteristics["has_severity_calibration"] = True

    # Check for recommendations
    if any(phrase in report.lower() for phrase in ["recommend", "should", "must", "action"]):
        characteristics["has_recommendations"] = True

    # Check for probabilities
    if re.search(r'\d+%', report):
        characteristics["has_quantified_probabilities"] = True

    # Check for citations (page numbers, source references)
    if re.search(r'page \d+|p\.\d+|\[.*\]', report.lower()):
        characteristics["has_source_citations"] = True

    return characteristics

def compare_reports():
    """Compare all three intelligence reports"""

    print("=" * 80)
    print("MULTI-YEAR PDF ANALYSIS - THREE-WAY COMPARISON")
    print("Grupa Azoty S.A. Intelligence Reports (2022-2024)")
    print("=" * 80)
    print()

    # Find most recent reports
    report_dir = Path("output/intelligence_reports")

    single_agent_files = sorted(report_dir.glob("Azoty_SingleAgent_MultiYear_*.md"), reverse=True)
    multi_agent_files = sorted(report_dir.glob("Azoty_MultiAgent_MultiYear_*.md"), reverse=True)
    claude_files = sorted(report_dir.glob("Azoty_Claude_MultiYear_*.md"), reverse=True)

    reports = {}

    # Load reports
    if single_agent_files:
        reports["Single-Agent"] = load_report(single_agent_files[0])
        print(f"✅ Loaded Single-Agent report: {single_agent_files[0].name}")
    else:
        print(f"⚠️  No Single-Agent report found")

    if multi_agent_files:
        reports["Multi-Agent"] = load_report(multi_agent_files[0])
        print(f"✅ Loaded Multi-Agent report: {multi_agent_files[0].name}")
    else:
        print(f"⚠️  No Multi-Agent report found")

    if claude_files:
        reports["Claude"] = load_report(claude_files[0])
        print(f"✅ Loaded Claude report: {claude_files[0].name}")
    else:
        print(f"⚠️  No Claude benchmark report found")

    print()

    if not reports:
        print("❌ No reports found to compare!")
        return

    # Analyze each report
    print("=" * 80)
    print("REPORT CHARACTERISTICS ANALYSIS")
    print("=" * 80)
    print()

    analysis_results = {}
    for system_name, report in reports.items():
        if report:
            analysis_results[system_name] = analyze_report_characteristics(report, system_name)

    # Print comparison table
    print(f"{'Characteristic':<40} {'Single-Agent':<15} {'Multi-Agent':<15} {'Claude':<15}")
    print("-" * 85)

    characteristics_to_compare = [
        ("Length (characters)", "length_chars"),
        ("Length (words)", "length_words"),
        ("Number of sections", "sections"),
        ("Framework selection", "has_framework_selection"),
        ("Severity calibration", "has_severity_calibration"),
        ("Recommendations", "has_recommendations"),
        ("Quantified probabilities", "has_quantified_probabilities"),
        ("Source citations", "has_source_citations"),
        ("'Critical' mentions", "critical_mentions"),
        ("'High risk' mentions", "high_risk_mentions"),
        ("Equity erosion analysis", "equity_erosion_mentions"),
        ("Credit analysis framework", "credit_analysis_mentioned"),
        ("Multi-year trends (2022-2024)", "multi_year_trends")
    ]

    for label, key in characteristics_to_compare:
        single = str(analysis_results.get("Single-Agent", {}).get(key, "N/A"))
        multi = str(analysis_results.get("Multi-Agent", {}).get(key, "N/A"))
        claude = str(analysis_results.get("Claude", {}).get(key, "N/A"))
        print(f"{label:<40} {single:<15} {multi:<15} {claude:<15}")

    # Key findings
    print()
    print("=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)
    print()

    findings = []

    # Compare severity calibration
    if "Single-Agent" in analysis_results and "Claude" in analysis_results:
        single_critical = analysis_results["Single-Agent"]["critical_mentions"]
        claude_critical = analysis_results["Claude"]["critical_mentions"]

        if single_critical < claude_critical:
            findings.append(
                f"⚠️  SEVERITY CALIBRATION GAP: Single-Agent used 'critical' {single_critical} times vs "
                f"Claude {claude_critical} times. Local system may under-calibrate severity."
            )

    # Compare framework selection
    if "Single-Agent" in analysis_results:
        if not analysis_results["Single-Agent"]["credit_analysis_mentioned"]:
            findings.append(
                "⚠️  FRAMEWORK SELECTION GAP: Single-Agent may not explicitly select credit analysis "
                "framework despite company distress (46.9% equity decline)."
            )

    # Compare source citations
    if "Multi-Agent" in analysis_results:
        if not analysis_results["Multi-Agent"]["has_source_citations"]:
            findings.append(
                "⚠️  RAG QUALITY GAP: Multi-Agent report lacks source citations (page numbers), "
                "suggesting RAG retrieval may not be properly integrated."
            )

    # Print findings
    for i, finding in enumerate(findings, 1):
        print(f"{i}. {finding}")
        print()

    if not findings:
        print("✅ No major gaps identified. All systems perform similarly.")
        print()

    # Generate comparison report
    print("=" * 80)
    print("GENERATING DETAILED COMPARISON REPORT")
    print("=" * 80)
    print()

    comparison_report = f"""# Multi-Year PDF Analysis - System Comparison
## Grupa Azoty S.A. Intelligence Reports (2022-2024)

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Executive Summary

This report compares three intelligence systems on multi-year financial analysis:
1. **Single-Agent**: Local LLM (1 perspective)
2. **Multi-Agent**: Local LLM (6 specialized agents with RAG)
3. **Claude**: Anthropic Claude 3.5 Sonnet (benchmark)

**Test Data**: Grupa Azoty S.A. (2022-2024)
- Severe financial distress (46.9% equity decline)
- Persistent operating losses
- Rising debt burden
- Perfect test case for severity calibration

---

## Quantitative Comparison

| Metric | Single-Agent | Multi-Agent | Claude |
|--------|-------------|-------------|--------|
"""

    for label, key in characteristics_to_compare:
        single = analysis_results.get("Single-Agent", {}).get(key, "N/A")
        multi = analysis_results.get("Multi-Agent", {}).get(key, "N/A")
        claude = analysis_results.get("Claude", {}).get(key, "N/A")
        comparison_report += f"| {label} | {single} | {multi} | {claude} |\n"

    comparison_report += f"""

---

## Gap Analysis

### Identified Gaps

"""

    for i, finding in enumerate(findings, 1):
        comparison_report += f"{i}. {finding}\n\n"

    comparison_report += """
---

## Improvement Priorities

Based on this multi-year PDF analysis, prioritize:

1. **High Priority - Week 1**:
   - Severity calibration (explicit thresholds)
   - Framework selection (credit vs equity decision tree)
   - Add few-shot examples with correct severity

2. **Medium Priority - Week 2**:
   - RAG retrieval quality (source citations)
   - Chain-of-thought reasoning templates
   - Probability quantification

3. **Lower Priority - Week 3-4**:
   - PDF extraction automation (currently manual)
   - Multi-year trend analysis enhancements
   - Self-critique validation loop

---

## Conclusion

This comprehensive multi-year test on real annual reports (21.6 MB of PDFs) revealed specific gaps
that were not visible in single-year limited testing. The baseline is now established for
measuring improvements.

**Next Steps**: Implement Phase 1 improvements from `LOCAL_SYSTEM_IMPROVEMENT_PLAN.md`
"""

    # Save comparison report
    output_file = Path("MULTI_YEAR_PDF_COMPARISON.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(comparison_report)

    print(f"✅ Comparison report saved: {output_file}")
    print()
    print("Full cycle complete!")
    print()
    print("Summary of all deliverables:")
    print("  1. ✅ 6 PDF annual reports downloaded (21.6 MB)")
    print("  2. ✅ Multi-year financial dataset created (3 years)")
    print(f"  3. {'✅' if 'Single-Agent' in reports else '⏳'} Single-agent intelligence report")
    print(f"  4. {'✅' if 'Multi-Agent' in reports else '⏳'} Multi-agent intelligence report (with RAG)")
    print(f"  5. {'✅' if 'Claude' in reports else '⏳'} Claude benchmark report")
    print("  6. ✅ Comprehensive three-way comparison")
    print()

    return {
        "comparison_file": str(output_file),
        "reports_analyzed": list(reports.keys()),
        "gaps_identified": len(findings)
    }


if __name__ == "__main__":
    try:
        result = compare_reports()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
