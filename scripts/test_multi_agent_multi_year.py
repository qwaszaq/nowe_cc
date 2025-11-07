"""
Generate multi-agent intelligence report with RAG on Grupa Azoty multi-year data
Phase 4.2: Multi-Agent Analysis with RAG
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.intelligence.services.multi_agent_intelligence_service import MultiAgentIntelligenceService
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_multi_agent_report():
    """Generate 6-agent intelligence analysis with RAG on 3 years of Azoty data"""

    print("=" * 80)
    print("MULTI-AGENT INTELLIGENCE ANALYSIS (with RAG)")
    print("Grupa Azoty S.A. - Multi-Year Analysis (2022-2024)")
    print("=" * 80)
    print()

    # Load multi-year data
    data_file = Path("data/companies/grupa_azoty_multi_year.json")

    with open(data_file, 'r') as f:
        multi_year_data = json.load(f)

    # Initialize multi-agent service with RAG
    # FIXED: Now specifies correct Qdrant collection name
    service = MultiAgentIntelligenceService(
        use_rag=True,
        qdrant_collection="azoty_multi_year"
    )

    # Prepare data - service expects balance_sheet, income_statement, cash_flow at top level
    # with multi-year structure: {'metric_name': {2022: value, 2023: value, ...}}
    # Convert year keys from strings to integers (JSON stores as strings)
    def convert_year_keys(data_dict):
        """Convert year string keys to integers"""
        return {
            metric: {int(year): value for year, value in years_data.items()}
            for metric, years_data in data_dict.items()
        }

    company_data = {
        "company_name": multi_year_data["company_name"],
        "industry": multi_year_data["industry"],
        "currency": multi_year_data["currency"],
        "balance_sheet": convert_year_keys(multi_year_data["balance_sheet"]),
        "income_statement": convert_year_keys(multi_year_data["income_statement"]),
        "cash_flow": convert_year_keys(multi_year_data["cash_flow"])
    }

    print("Data loaded:")
    print(f"  Company: {company_data['company_name']}")
    print(f"  Years: {', '.join(map(str, multi_year_data['years_covered']))}")
    print(f"  Balance sheet metrics: {len(company_data['balance_sheet'])}")
    print(f"  Income statement metrics: {len(company_data['income_statement'])}")
    print(f"  Cash flow metrics: {len(company_data['cash_flow'])}")
    print(f"  RAG enabled: Yes (collection: azoty_multi_year)")
    print()

    # Generate report
    print("Generating 6-agent intelligence report with RAG...")
    print("(This may take 90-180 seconds - 6 agents working)")
    print()

    start_time = datetime.now()

    result = service.generate_intelligence_report(company_data)

    # Extract report from result dict
    report = result if isinstance(result, str) else result.get('report', str(result))

    end_time = datetime.now()
    generation_time = (end_time - start_time).total_seconds()

    # Save report
    output_dir = Path("output/intelligence_reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"Azoty_MultiAgent_MultiYear_{timestamp}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    # Print summary
    print("=" * 80)
    print("✅ MULTI-AGENT REPORT GENERATED")
    print("=" * 80)
    print()
    print(f"Output file: {output_file}")
    print(f"Generation time: {generation_time:.1f} seconds")
    print(f"Report length: {len(report):,} characters")
    print(f"Agents used: 6 (Financial, Risk, Industry, Strategy, Market, Synthesis)")
    print()

    # Show preview
    print("Report Preview (first 1000 chars):")
    print("-" * 80)
    print(report[:1000])
    print("...")
    print("-" * 80)
    print()

    return {
        "output_file": str(output_file),
        "generation_time": generation_time,
        "report_length": len(report),
        "timestamp": timestamp
    }


if __name__ == "__main__":
    try:
        result = generate_multi_agent_report()
        print("Next: Generate Claude benchmark")
        print("  python3 scripts/generate_claude_multi_year.py")
    except Exception as e:
        logger.error(f"❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
