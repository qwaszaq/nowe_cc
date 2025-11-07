#!/bin/bash

# Complete Benchmark Pipeline for Grupa Azoty 2019-2021
# This script runs the entire process from data ingestion to final comparison

set -e  # Exit on error

echo "================================================================================"
echo "COMPLETE BENCHMARK PIPELINE: GRUPA AZOTY 2019-2021"
echo "================================================================================"
echo ""
echo "This script will:"
echo "  1. Create unified Qdrant collection (azoty_2019_2021_multi_year)"
echo "  2. Run Single-Agent analysis"
echo "  3. Run Multi-Agent analysis"
echo "  4. Generate comprehensive comparison report"
echo ""
echo "Estimated time: 5-8 minutes"
echo ""

# Confirm execution
read -p "Proceed? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "================================================================================"
echo "STEP 1/2: Creating Unified Collection"
echo "================================================================================"
echo ""

python3 scripts/create_unified_azoty_2019_2021_collection.py 2>&1 | tee logs/unified_collection_2019_2021.log

if [ $? -ne 0 ]; then
    echo "❌ Collection creation failed. Check logs/unified_collection_2019_2021.log"
    exit 1
fi

echo ""
echo "✅ Collection created successfully!"
echo ""
echo "================================================================================"
echo "STEP 2/2: Running Benchmark Analysis"
echo "================================================================================"
echo ""

python3 scripts/benchmark_azoty_2019_2021.py 2>&1 | tee logs/benchmark_2019_2021.log

if [ $? -ne 0 ]; then
    echo "❌ Benchmark failed. Check logs/benchmark_2019_2021.log"
    exit 1
fi

echo ""
echo "================================================================================"
echo "BENCHMARK COMPLETE!"
echo "================================================================================"
echo ""
echo "Results available in:"
echo "  - Reports: output/intelligence_reports/"
echo "  - Comparison: output/benchmarks/"
echo "  - Logs: logs/"
echo ""
