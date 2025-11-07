"""
Test Multi-Agent Intelligence Report Generation
Generates comprehensive 6-agent analysis for Grupa Azoty
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.intelligence.services.multi_agent_intelligence_service import MultiAgentIntelligenceService
from src.data.multi_year_storage import load_for_intelligence_report
import time
from datetime import datetime

def test_multi_agent_azoty():
    """
    Test multi-agent intelligence report generation for Grupa Azoty

    Executes 6 specialized agents:
    1. Financial Health Agent
    2. Risk Assessment Agent
    3. Industry Context Agent
    4. Strategic Evaluation Agent
    5. Market Intelligence Agent
    6. Synthesis Agent
    """

    print("=" * 80)
    print("MULTI-AGENT INTELLIGENCE REPORT TEST")
    print("=" * 80)
    print()

    # Load company data
    print("Loading company data for Grupa Azoty...")
    company_data = load_for_intelligence_report("Grupa Azoty S.A.")

    if not company_data:
        print("❌ Failed to load company data")
        return

    print(f"✓ Loaded data for: {company_data['company_name']}")
    print(f"  Industry: {company_data.get('industry', 'Unknown')}")

    balance_sheet = company_data.get('balance_sheet', {})
    if balance_sheet:
        first_metric = list(balance_sheet.keys())[0]
        years = list(balance_sheet[first_metric].keys())
        print(f"  Years available: {sorted(years)}")
    print()

    # Initialize multi-agent service with RAG
    print("Initializing Multi-Agent Intelligence Service...")
    print("  Configuration:")
    print("    - Local LLM: openai/gpt-oss-20b (LM Studio)")
    print("    - Agents: 6 specialized agents")
    print("    - RAG: Enabled (Qdrant + BGE reranker)")
    print("    - Max tokens per agent: 4000")
    print()

    service = MultiAgentIntelligenceService(
        llm_base_url="http://192.168.200.226:1234/v1",
        model="openai/gpt-oss-20b",
        max_tokens_per_pass=4000,
        use_rag=True,
        qdrant_url="http://localhost:6333"
    )

    # Generate multi-agent report
    print("Starting multi-agent report generation...")
    print("Expected time: 2-3 minutes (6 agents × ~25-30s each)")
    print()

    start_time = time.time()

    result = service.generate_intelligence_report(company_data)

    generation_time = time.time() - start_time

    # Check result
    if not result.get('success'):
        print("❌ Multi-agent report generation failed")
        print(f"Error: {result.get('error', 'Unknown error')}")
        return

    report = result['report']
    metadata = result['metadata']

    print()
    print("=" * 80)
    print("✅ MULTI-AGENT REPORT GENERATION COMPLETE")
    print("=" * 80)
    print()

    # Display metadata
    print("Report Metadata:")
    print(f"  Company: {metadata['company_name']}")
    print(f"  Report Date: {metadata['report_date']}")
    print(f"  Model: {metadata['model']}")
    print(f"  Agents: {metadata['agents']}")
    print(f"  Generation Time: {metadata['generation_time_seconds']:.2f} seconds")
    print(f"  Report Length: {metadata['report_length_chars']:,} characters")
    print(f"  RAG Enabled: {metadata['rag_enabled']}")
    print()

    # Agent breakdown
    print("Agent Contributions:")
    for agent, char_count in metadata['agent_results'].items():
        print(f"  {agent.capitalize()}: {char_count:,} chars")
    print()

    # Save report
    output_dir = Path(__file__).parent.parent / "output" / "intelligence_reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Azoty_MultiAgent_{timestamp}.md"
    output_path = output_dir / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Multi-Agent Intelligence Report: {metadata['company_name']}\n\n")
        f.write(f"**Generated:** {metadata['report_date']}\n")
        f.write(f"**Model:** {metadata['model']}\n")
        f.write(f"**Agents:** {metadata['agents']}\n")
        f.write(f"**Generation Time:** {metadata['generation_time_seconds']:.2f}s\n")
        f.write(f"**RAG:** {metadata['rag_enabled']}\n\n")
        f.write("---\n\n")
        f.write(report)

    print(f"Report saved to: {output_path}")
    print()

    # Display report preview
    print("=" * 80)
    print("REPORT PREVIEW (first 2000 characters)")
    print("=" * 80)
    print()
    print(report[:2000])
    if len(report) > 2000:
        print()
        print(f"[... {len(report) - 2000:,} more characters ...]")
    print()

    # Performance summary
    print("=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Generation Time: {generation_time:.2f} seconds")
    print(f"Average per Agent: {generation_time / metadata['agents']:.2f} seconds")
    print(f"Total Report Length: {len(report):,} characters")
    print()

    return result


if __name__ == "__main__":
    test_multi_agent_azoty()
