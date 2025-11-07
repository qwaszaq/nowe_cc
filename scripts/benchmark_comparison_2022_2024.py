"""
Comprehensive Benchmark: Local Single-Agent vs Multi-Agent vs Claude
Grupa Azoty 2022-2024 Analysis
"""

import sys
from pathlib import Path
import json
import time
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from src.intelligence.services.local_intelligence_service import LocalIntelligenceService
from src.intelligence.services.multi_agent_intelligence_service import MultiAgentIntelligenceService
import anthropic
import os
import re

COMPANY = "Grupa Azoty S.A."
DATA_FILE = "data/companies/grupa_azoty_multi_year.json"
YEARS = [2022, 2023, 2024]

def load_company_data():
    """Load structured company data"""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Convert year keys from strings to integers
    def convert_year_keys(data_dict):
        return {
            metric: {int(year): value for year, value in years_data.items()}
            for metric, years_data in data_dict.items()
        }

    return {
        "company_name": data["company_name"],
        "industry": data["industry"],
        "currency": data["currency"],
        "balance_sheet": convert_year_keys(data["balance_sheet"]),
        "income_statement": convert_year_keys(data["income_statement"]),
        "cash_flow": convert_year_keys(data["cash_flow"])
    }

def extract_metrics(report_text):
    """Extract score and recommendation from report"""
    score = None
    recommendation = None

    for line in report_text.split('\n'):
        # Extract score
        if 'Assessment Score' in line or 'Financial Health Score' in line:
            match = re.search(r'(\d+)(?:/100)?', line)
            if match:
                score = int(match.group(1))

        # Extract recommendation
        if 'Investment Recommendation' in line and '**' in line:
            parts = line.split('**')
            if len(parts) >= 2:
                recommendation = parts[1].strip()

    return score, recommendation

def run_single_agent():
    """Run Local Single-Agent analysis"""
    print("\n" + "=" * 80)
    print("BENCHMARK 1/3: LOCAL SINGLE-AGENT (RAG-Enhanced)")
    print("=" * 80)
    print()

    start_time = time.time()

    company_data = load_company_data()

    service = LocalIntelligenceService(
        use_rag=True,
        qdrant_url="http://localhost:6333",
        qdrant_collection="azoty_multi_year"
    )

    result = service.generate_intelligence_report(company_data)

    elapsed = time.time() - start_time

    if isinstance(result, dict):
        report = result.get('report', str(result))
    else:
        report = result

    score, recommendation = extract_metrics(report)

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/intelligence_reports/Benchmark_SingleAgent_{timestamp}.md"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(report)

    print(f"✅ Single-Agent Complete")
    print(f"   Time: {elapsed:.1f}s")
    print(f"   Score: {score}/100" if score else "   Score: N/A")
    print(f"   Recommendation: {recommendation}" if recommendation else "   Recommendation: N/A")
    print(f"   Report: {output_file}")

    return {
        "approach": "Local Single-Agent (RAG)",
        "time": elapsed,
        "score": score,
        "recommendation": recommendation,
        "report_length": len(report),
        "report_file": output_file,
        "model": "openai/gpt-oss-20b (local)"
    }

def run_multi_agent():
    """Run Local Multi-Agent analysis"""
    print("\n" + "=" * 80)
    print("BENCHMARK 2/3: LOCAL MULTI-AGENT (6 Specialized Agents)")
    print("=" * 80)
    print()

    start_time = time.time()

    company_data = load_company_data()

    service = MultiAgentIntelligenceService(
        use_rag=True,
        qdrant_url="http://localhost:6333",
        qdrant_collection="azoty_multi_year"
    )

    result = service.generate_intelligence_report(company_data)

    elapsed = time.time() - start_time

    if isinstance(result, dict):
        report = result.get('report', str(result))
    else:
        report = result

    score, recommendation = extract_metrics(report)

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/intelligence_reports/Benchmark_MultiAgent_{timestamp}.md"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    Path(output_file).write_text(report)

    print(f"✅ Multi-Agent Complete")
    print(f"   Time: {elapsed:.1f}s")
    print(f"   Score: {score}/100" if score else "   Score: N/A")
    print(f"   Recommendation: {recommendation}" if recommendation else "   Recommendation: N/A")
    print(f"   Report: {output_file}")

    return {
        "approach": "Local Multi-Agent (RAG)",
        "time": elapsed,
        "score": score,
        "recommendation": recommendation,
        "report_length": len(report),
        "report_file": output_file,
        "model": "openai/gpt-oss-20b (local) x6 agents"
    }

def run_claude():
    """Run Claude analysis (benchmark only)"""
    print("\n" + "=" * 80)
    print("BENCHMARK 3/3: CLAUDE (Benchmark Comparison)")
    print("=" * 80)
    print()

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not set - skipping Claude benchmark")
        return {
            "approach": "Claude (Benchmark)",
            "time": None,
            "score": None,
            "recommendation": "SKIPPED",
            "report_length": None,
            "report_file": None,
            "model": "claude-sonnet-4",
            "note": "API key not configured"
        }

    start_time = time.time()

    try:
        company_data = load_company_data()

        # Format data for Claude
        prompt = f"""Analyze {COMPANY} financial performance for {YEARS[0]}-{YEARS[-1]} and generate a comprehensive investment intelligence report.

**Financial Data**:

Balance Sheet (PLN thousands):
{json.dumps(company_data['balance_sheet'], indent=2)}

Income Statement (PLN thousands):
{json.dumps(company_data['income_statement'], indent=2)}

Cash Flow (PLN thousands):
{json.dumps(company_data['cash_flow'], indent=2)}

Generate a comprehensive report including:
1. Executive Summary with Overall Assessment Score (0-100) and Investment Recommendation
2. Financial Performance Analysis
3. Risk Assessment
4. Investment Thesis
5. Final Recommendation

Format in markdown. Must include:
- **Overall Assessment Score:** X/100
- **Investment Recommendation:** **[RECOMMENDATION]**
"""

        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        report = message.content[0].text
        elapsed = time.time() - start_time

        score, recommendation = extract_metrics(report)

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/intelligence_reports/Benchmark_Claude_{timestamp}.md"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        Path(output_file).write_text(report)

        print(f"✅ Claude Complete")
        print(f"   Time: {elapsed:.1f}s")
        print(f"   Score: {score}/100" if score else "   Score: N/A")
        print(f"   Recommendation: {recommendation}" if recommendation else "   Recommendation: N/A")
        print(f"   Report: {output_file}")

        return {
            "approach": "Claude (Benchmark)",
            "time": elapsed,
            "score": score,
            "recommendation": recommendation,
            "report_length": len(report),
            "report_file": output_file,
            "model": "claude-sonnet-4-20250514"
        }

    except Exception as e:
        print(f"❌ Claude failed: {e}")
        return {
            "approach": "Claude (Benchmark)",
            "time": None,
            "score": None,
            "recommendation": "FAILED",
            "report_length": None,
            "report_file": None,
            "model": "claude-sonnet-4",
            "error": str(e)
        }

def generate_comparison(results):
    """Generate comprehensive comparison report"""
    print("\n" + "=" * 80)
    print("BENCHMARK COMPARISON RESULTS")
    print("=" * 80)
    print()

    # Results table
    print("Performance Comparison:")
    print("-" * 100)
    print(f"{'Approach':<30} {'Model':<35} {'Time':<10} {'Score':<10} {'Recommendation':<15}")
    print("-" * 100)

    for result in results:
        time_str = f"{result['time']:.1f}s" if result['time'] else "N/A"
        score_str = f"{result['score']}/100" if result['score'] else "N/A"
        rec_str = result['recommendation'] if result['recommendation'] else "N/A"
        model_str = result.get('model', 'N/A')[:33]

        print(f"{result['approach']:<30} {model_str:<35} {time_str:<10} {score_str:<10} {rec_str:<15}")

    print("-" * 100)
    print()

    # Detailed analysis
    local_single = results[0]
    local_multi = results[1]
    claude = results[2]

    print("Detailed Analysis:")
    print()

    # Speed comparison
    if local_single['time'] and local_multi['time']:
        print(f"⏱️  Speed Comparison:")
        print(f"   Single-Agent: {local_single['time']:.1f}s")
        print(f"   Multi-Agent:  {local_multi['time']:.1f}s ({(local_multi['time']/local_single['time']-1)*100:+.1f}%)")
        if claude['time']:
            print(f"   Claude:       {claude['time']:.1f}s ({(claude['time']/local_single['time']-1)*100:+.1f}%)")
        print()

    # Score comparison
    scores_valid = [r for r in results if r['score'] is not None]
    if len(scores_valid) >= 2:
        print(f"📊 Score Comparison:")
        for r in scores_valid:
            print(f"   {r['approach']:<30} {r['score']}/100")
        print()

    # Recommendation comparison
    recs_valid = [r for r in results if r['recommendation'] and r['recommendation'] != 'SKIPPED' and r['recommendation'] != 'FAILED']
    if len(recs_valid) >= 2:
        print(f"💡 Recommendation Comparison:")
        for r in recs_valid:
            print(f"   {r['approach']:<30} {r['recommendation']}")

        # Check consensus
        unique_recs = set(r['recommendation'] for r in recs_valid)
        if len(unique_recs) == 1:
            print(f"\n   ✅ CONSENSUS: All approaches agree on {list(unique_recs)[0]}")
        else:
            print(f"\n   ⚠️  DIVERGENCE: Different recommendations across approaches")
        print()

    # Report length comparison
    lengths_valid = [r for r in results if r['report_length']]
    if len(lengths_valid) >= 2:
        print(f"📝 Report Length Comparison:")
        for r in lengths_valid:
            print(f"   {r['approach']:<30} {r['report_length']:,} chars")
        print()

    # Save comparison data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_file = f"output/benchmarks/Comparison_{YEARS[0]}_{YEARS[-1]}_{timestamp}.json"
    Path(comparison_file).parent.mkdir(parents=True, exist_ok=True)

    comparison_data = {
        "timestamp": timestamp,
        "company": COMPANY,
        "years": YEARS,
        "results": results
    }

    with open(comparison_file, 'w') as f:
        json.dump(comparison_data, f, indent=2)

    print(f"💾 Comparison data saved: {comparison_file}")
    print()

    return comparison_data

def main():
    """Run complete benchmark"""
    print("=" * 80)
    print(f"COMPREHENSIVE BENCHMARK: {COMPANY} ({YEARS[0]}-{YEARS[-1]})")
    print("=" * 80)
    print()
    print("Comparing 3 approaches:")
    print("  1. Local Single-Agent (RAG-enhanced)")
    print("  2. Local Multi-Agent (6 specialized agents)")
    print("  3. Claude (benchmark comparison)")
    print()

    results = []

    # Run all three
    try:
        results.append(run_single_agent())
    except Exception as e:
        print(f"❌ Single-Agent failed: {e}")
        results.append({
            "approach": "Local Single-Agent (RAG)",
            "time": None,
            "score": None,
            "recommendation": "FAILED",
            "report_length": None,
            "report_file": None,
            "error": str(e)
        })

    try:
        results.append(run_multi_agent())
    except Exception as e:
        print(f"❌ Multi-Agent failed: {e}")
        results.append({
            "approach": "Local Multi-Agent (RAG)",
            "time": None,
            "score": None,
            "recommendation": "FAILED",
            "report_length": None,
            "report_file": None,
            "error": str(e)
        })

    results.append(run_claude())

    # Generate comparison
    comparison = generate_comparison(results)

    print("=" * 80)
    print("BENCHMARK COMPLETE!")
    print("=" * 80)
    print()
    print("Reports available in: output/intelligence_reports/")
    print("Comparison data in: output/benchmarks/")
    print()

if __name__ == "__main__":
    main()
