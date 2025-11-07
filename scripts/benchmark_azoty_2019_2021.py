"""
Comprehensive Benchmark: Single-Agent vs Multi-Agent vs Claude Direct
Grupa Azoty 2019-2021 Analysis

This script runs all three analysis approaches and compares results.
"""

import sys
from pathlib import Path
import time
import json
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))

from src.intelligence.services.local_intelligence_service import LocalIntelligenceService
from src.intelligence.services.multi_agent_intelligence_service import MultiAgentIntelligenceService
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

COMPANY = "Grupa Azoty"
YEARS = [2019, 2020, 2021]
COLLECTION_NAME = "azoty_2019_2021_multi_year"


def run_single_agent_analysis():
    """Run Single-Agent RAG-based analysis"""
    print("\n" + "=" * 80)
    print("BENCHMARK 1/3: SINGLE-AGENT ANALYSIS (RAG-Enhanced)")
    print("=" * 80)
    print()

    start_time = time.time()

    service = LocalIntelligenceService(
        use_rag=True,
        qdrant_url="http://localhost:6333",
        qdrant_collection=COLLECTION_NAME
    )

    report = service.generate_multi_year_intelligence_report(
        company=COMPANY,
        years=YEARS
    )

    elapsed = time.time() - start_time

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/intelligence_reports/Azoty_SingleAgent_2019_2021_{timestamp}.md"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(report)

    # Extract metrics
    score = None
    recommendation = None
    for line in report.split('\n'):
        if 'Overall Assessment Score' in line:
            score = int(''.join(filter(str.isdigit, line.split(':')[1].split('/')[0])))
        if 'Investment Recommendation' in line and '**' in line:
            recommendation = line.split('**')[1].strip()

    print(f"✅ Single-Agent Analysis Complete")
    print(f"   Time: {elapsed:.1f}s")
    print(f"   Score: {score}/100")
    print(f"   Recommendation: {recommendation}")
    print(f"   Report Length: {len(report):,} chars")
    print(f"   Saved to: {output_file}")

    return {
        "approach": "Single-Agent (RAG)",
        "time": elapsed,
        "score": score,
        "recommendation": recommendation,
        "report_length": len(report),
        "report_file": output_file
    }


def run_multi_agent_analysis():
    """Run Multi-Agent collaborative analysis"""
    print("\n" + "=" * 80)
    print("BENCHMARK 2/3: MULTI-AGENT ANALYSIS (6 Specialized Agents)")
    print("=" * 80)
    print()

    start_time = time.time()

    service = MultiAgentIntelligenceService(
        use_rag=True,
        qdrant_url="http://localhost:6333",
        qdrant_collection=COLLECTION_NAME
    )

    report = service.generate_multi_year_intelligence_report(
        company=COMPANY,
        years=YEARS
    )

    elapsed = time.time() - start_time

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/intelligence_reports/Azoty_MultiAgent_2019_2021_{timestamp}.md"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(report)

    # Extract metrics
    score = None
    recommendation = None
    for line in report.split('\n'):
        if 'Overall Assessment Score' in line:
            score = int(''.join(filter(str.isdigit, line.split(':')[1].split('/')[0])))
        if 'Investment Recommendation' in line and '**' in line:
            recommendation = line.split('**')[1].strip()

    print(f"✅ Multi-Agent Analysis Complete")
    print(f"   Time: {elapsed:.1f}s")
    print(f"   Score: {score}/100")
    print(f"   Recommendation: {recommendation}")
    print(f"   Report Length: {len(report):,} chars")
    print(f"   Saved to: {output_file}")

    return {
        "approach": "Multi-Agent (RAG)",
        "time": elapsed,
        "score": score,
        "recommendation": recommendation,
        "report_length": len(report),
        "report_file": output_file
    }


def run_claude_direct_analysis():
    """Run Claude direct analysis (no RAG) using PDFs"""
    print("\n" + "=" * 80)
    print("BENCHMARK 3/3: CLAUDE DIRECT ANALYSIS (No RAG)")
    print("=" * 80)
    print()
    print("NOTE: This requires reading PDFs directly and sending to Claude.")
    print("      Skipping for now - would exceed context window.")
    print("      For fair comparison, use Claude with same RAG as other approaches.")
    print()

    return {
        "approach": "Claude Direct (No RAG)",
        "time": None,
        "score": None,
        "recommendation": "SKIPPED",
        "report_length": None,
        "report_file": None,
        "note": "Skipped - would require different approach than RAG systems"
    }


def compare_results(single_agent, multi_agent, claude_direct):
    """Generate comprehensive comparison report"""
    print("\n" + "=" * 80)
    print("BENCHMARK COMPARISON RESULTS")
    print("=" * 80)
    print()

    print("Performance Comparison:")
    print("-" * 80)
    print(f"{'Approach':<30} {'Time':<12} {'Score':<10} {'Recommendation':<15} {'Length':<10}")
    print("-" * 80)

    for result in [single_agent, multi_agent, claude_direct]:
        time_str = f"{result['time']:.1f}s" if result['time'] else "N/A"
        score_str = f"{result['score']}/100" if result['score'] else "N/A"
        length_str = f"{result['report_length']:,}" if result['report_length'] else "N/A"

        print(f"{result['approach']:<30} {time_str:<12} {score_str:<10} {result['recommendation']:<15} {length_str:<10}")

    print("-" * 80)
    print()

    # Detailed analysis
    print("Detailed Analysis:")
    print()

    if single_agent['time'] and multi_agent['time']:
        speed_diff = ((multi_agent['time'] - single_agent['time']) / single_agent['time']) * 100
        print(f"Speed Comparison:")
        print(f"  Single-Agent: {single_agent['time']:.1f}s")
        print(f"  Multi-Agent:  {multi_agent['time']:.1f}s ({speed_diff:+.1f}%)")
        print()

    if single_agent['score'] and multi_agent['score']:
        score_diff = multi_agent['score'] - single_agent['score']
        print(f"Score Comparison:")
        print(f"  Single-Agent: {single_agent['score']}/100")
        print(f"  Multi-Agent:  {multi_agent['score']}/100 ({score_diff:+d} points)")
        print()

    if single_agent['recommendation'] and multi_agent['recommendation']:
        print(f"Recommendation Comparison:")
        print(f"  Single-Agent: {single_agent['recommendation']}")
        print(f"  Multi-Agent:  {multi_agent['recommendation']}")
        match = "✅ MATCH" if single_agent['recommendation'] == multi_agent['recommendation'] else "❌ DIFFER"
        print(f"  {match}")
        print()

    # Save comparison report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_file = f"output/benchmarks/Azoty_Benchmark_2019_2021_{timestamp}.json"
    Path(comparison_file).parent.mkdir(parents=True, exist_ok=True)

    comparison_data = {
        "timestamp": timestamp,
        "company": COMPANY,
        "years": YEARS,
        "collection": COLLECTION_NAME,
        "results": {
            "single_agent": single_agent,
            "multi_agent": multi_agent,
            "claude_direct": claude_direct
        }
    }

    with open(comparison_file, 'w') as f:
        json.dump(comparison_data, f, indent=2)

    print(f"📊 Benchmark data saved to: {comparison_file}")
    print()

    return comparison_data


def main():
    """Run complete benchmark"""
    print("=" * 80)
    print("COMPREHENSIVE BENCHMARK: GRUPA AZOTY 2019-2021")
    print("=" * 80)
    print()
    print(f"Company: {COMPANY}")
    print(f"Years: {YEARS}")
    print(f"Collection: {COLLECTION_NAME}")
    print()
    print("Running 3 analysis approaches:")
    print("  1. Single-Agent (RAG-enhanced)")
    print("  2. Multi-Agent (6 specialized agents)")
    print("  3. Claude Direct (no RAG) - SKIPPED")
    print()

    # Run all three analyses
    single_agent = run_single_agent_analysis()
    multi_agent = run_multi_agent_analysis()
    claude_direct = run_claude_direct_analysis()

    # Compare results
    comparison = compare_results(single_agent, multi_agent, claude_direct)

    print("=" * 80)
    print("BENCHMARK COMPLETE!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Review generated reports in output/intelligence_reports/")
    print("  2. Analyze comparison data in output/benchmarks/")
    print("  3. Compare with 2022-2024 results for trend analysis")
    print()


if __name__ == "__main__":
    main()
