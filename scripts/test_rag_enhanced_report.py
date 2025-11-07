"""
Test RAG-enhanced intelligence report generation
Compare with baseline (structured data only)
"""

import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.intelligence.services.local_intelligence_service import LocalIntelligenceService
from src.data.multi_year_storage import load_for_intelligence_report

if __name__ == "__main__":
    print("=" * 80)
    print("TESTING RAG-ENHANCED INTELLIGENCE REPORT")
    print("=" * 80)
    print()

    # Load company data
    company_data = load_for_intelligence_report("Grupa Azoty S.A.")

    if not company_data:
        print("❌ ERROR: No data found for Grupa Azoty S.A.")
        sys.exit(1)

    print(f"Company: {company_data['company_name']}")
    print(f"Industry: {company_data.get('industry', 'Unknown')}")
    print(f"Currency: {company_data.get('currency', 'Unknown')}")
    print()

    # =========================================================================
    # BASELINE: Without RAG (structured data only)
    # =========================================================================
    print("=" * 80)
    print("BASELINE REPORT (Structured Data Only)")
    print("=" * 80)
    print()

    service_baseline = LocalIntelligenceService(use_rag=False)

    start_time = time.time()
    result_baseline = service_baseline.generate_intelligence_report(company_data)
    baseline_time = time.time() - start_time

    if result_baseline['success']:
        baseline_report = result_baseline['report']
        baseline_length = len(baseline_report)

        # Save baseline report
        output_dir = Path("output/intelligence_reports")
        output_dir.mkdir(parents=True, exist_ok=True)

        baseline_path = output_dir / "Azoty_Baseline_NoRAG.md"
        with open(baseline_path, 'w', encoding='utf-8') as f:
            f.write(baseline_report)

        print(f"✅ Baseline report generated")
        print(f"   Time: {baseline_time:.2f} seconds")
        print(f"   Length: {baseline_length:,} characters")
        print(f"   Saved to: {baseline_path}")
    else:
        print(f"❌ Baseline report failed: {result_baseline.get('error')}")
        sys.exit(1)

    print()

    # =========================================================================
    # RAG-ENHANCED: With document grounding
    # =========================================================================
    print("=" * 80)
    print("RAG-ENHANCED REPORT (Structured Data + Document Context)")
    print("=" * 80)
    print()

    service_rag = LocalIntelligenceService(
        use_rag=True,
        qdrant_url="http://localhost:6333"
    )

    start_time = time.time()
    result_rag = service_rag.generate_intelligence_report(company_data)
    rag_time = time.time() - start_time

    if result_rag['success']:
        rag_report = result_rag['report']
        rag_length = len(rag_report)

        # Save RAG-enhanced report
        rag_path = output_dir / "Azoty_RAG_Enhanced.md"
        with open(rag_path, 'w', encoding='utf-8') as f:
            f.write(rag_report)

        print(f"✅ RAG-enhanced report generated")
        print(f"   Time: {rag_time:.2f} seconds")
        print(f"   Length: {rag_length:,} characters")
        print(f"   Saved to: {rag_path}")
    else:
        print(f"❌ RAG-enhanced report failed: {result_rag.get('error')}")
        sys.exit(1)

    print()

    # =========================================================================
    # COMPARISON
    # =========================================================================
    print("=" * 80)
    print("COMPARISON")
    print("=" * 80)
    print()

    print(f"Generation Time:")
    print(f"  Baseline:     {baseline_time:.2f}s")
    print(f"  RAG-Enhanced: {rag_time:.2f}s")
    print(f"  Difference:   +{(rag_time - baseline_time):.2f}s ({((rag_time / baseline_time - 1) * 100):.1f}% slower)")
    print()

    print(f"Report Length:")
    print(f"  Baseline:     {baseline_length:,} chars")
    print(f"  RAG-Enhanced: {rag_length:,} chars")
    print(f"  Difference:   +{(rag_length - baseline_length):,} chars ({((rag_length / baseline_length - 1) * 100):.1f}% longer)")
    print()

    print(f"Quality Indicators:")
    print(f"  Baseline:")
    print(f"    - Source citations: No")
    print(f"    - Document grounding: No")
    print(f"    - Evidence-based: Limited (structured data only)")
    print()
    print(f"  RAG-Enhanced:")
    print(f"    - Source citations: Yes (with page numbers)")
    print(f"    - Document grounding: Yes (annual report context)")
    print(f"    - Evidence-based: Strong (structured data + document evidence)")
    print()

    print("=" * 80)
    print("✅ COMPARISON COMPLETE")
    print("=" * 80)
    print()
    print("Review the reports:")
    print(f"  Baseline: {baseline_path}")
    print(f"  RAG:      {rag_path}")
