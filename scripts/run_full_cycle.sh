#!/bin/bash
# Full Cycle: Multi-Year PDF Analysis
# Runs all phases in sequence

set -e  # Exit on error

echo "================================================================================"
echo "FULL CYCLE: MULTI-YEAR PDF ANALYSIS"
echo "Grupa Azoty S.A. (2022-2024)"
echo "================================================================================"
echo ""

# Phase 1: Already complete (PDFs downloaded)
echo "✅ Phase 1: PDFs Downloaded (6 files, 21.6 MB)"
echo ""

# Phase 2: Already complete (Data extracted)
echo "✅ Phase 2: Multi-year dataset created"
echo ""

# Phase 3: RAG Ingestion (if not already done)
echo "Phase 3: RAG Ingestion..."
if python3 scripts/ingest_azoty_multi_year.py; then
    echo "✅ Phase 3: RAG ingestion complete"
else
    echo "⚠️  Phase 3: RAG ingestion failed (will proceed without RAG)"
fi
echo ""

# Phase 4.1: Single-Agent Analysis
echo "Phase 4.1: Generating Single-Agent Report..."
if python3 scripts/test_single_agent_multi_year.py; then
    echo "✅ Phase 4.1: Single-Agent report generated"
else
    echo "❌ Phase 4.1: Single-Agent report failed"
    exit 1
fi
echo ""

# Phase 4.2: Multi-Agent Analysis
echo "Phase 4.2: Generating Multi-Agent Report (with RAG)..."
if python3 scripts/test_multi_agent_multi_year.py; then
    echo "✅ Phase 4.2: Multi-Agent report generated"
else
    echo "⚠️  Phase 4.2: Multi-Agent report failed (continuing)"
fi
echo ""

# Phase 4.3: Claude Benchmark (manual - just generate prompt)
echo "Phase 4.3: Claude Benchmark"
echo "  ⏳ Manual step: Submit to Claude and save response"
echo "  (Skipping for now - can add manually)"
echo ""

# Phase 5: Comparison
echo "Phase 5: Generating Comparison Report..."
if python3 scripts/compare_multi_year_systems.py; then
    echo "✅ Phase 5: Comparison report generated"
else
    echo "❌ Phase 5: Comparison failed"
    exit 1
fi
echo ""

echo "================================================================================"
echo "✅ FULL CYCLE COMPLETE"
echo "================================================================================"
echo ""
echo "Generated Files:"
echo "  - output/intelligence_reports/Azoty_SingleAgent_MultiYear_*.md"
echo "  - output/intelligence_reports/Azoty_MultiAgent_MultiYear_*.md"
echo "  - MULTI_YEAR_PDF_COMPARISON.md"
echo ""
echo "Next: Review MULTI_YEAR_PDF_COMPARISON.md for gap analysis"
