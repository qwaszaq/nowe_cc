#!/bin/bash
# Download Grupa Azoty annual reports for 2022, 2023, 2024
# Multi-year PDF analysis baseline

BASE_URL="https://tarnow.grupaazoty.com"
OUTPUT_DIR="data/documents/grupa_azoty"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "======================================================================"
echo "Downloading Grupa Azoty Annual Reports (2022-2024)"
echo "======================================================================"
echo ""

# 2024 Reports
echo "Downloading 2024 Reports..."
curl -o "$OUTPUT_DIR/Grupa_Azoty_Consolidated_Financial_Statements_2024.pdf" \
  "${BASE_URL}/upload/2/files/2025/Azoty_Group_Consolidated_Financial_Statement_2024_16052025.pdf"

curl -o "$OUTPUT_DIR/Grupa_Azoty_Directors_Report_2024.pdf" \
  "${BASE_URL}/upload/2/files/2025/rs24/en/Azoty_Group_Directors_Report_2024.pdf"

echo "✓ 2024 reports downloaded"
echo ""

# 2023 Reports
echo "Downloading 2023 Reports..."
curl -o "$OUTPUT_DIR/Grupa_Azoty_Consolidated_Financial_Statements_2023.pdf" \
  "${BASE_URL}/upload/2/files/2024/IR/r23/Consolidated financial statements 2023.pdf"

curl -o "$OUTPUT_DIR/Grupa_Azoty_Directors_Report_2023.pdf" \
  "${BASE_URL}/upload/2/files/2024/IR/r23/Directors Report on the operations 2023.pdf"

echo "✓ 2023 reports downloaded"
echo ""

# 2022 Reports
echo "Downloading 2022 Reports..."
curl -o "$OUTPUT_DIR/Grupa_Azoty_Consolidated_Financial_Statements_2022.pdf" \
  "${BASE_URL}/upload/2/files/2023/RI/R2022/eng/Consolidated_financial_statements_2022.pdf"

curl -o "$OUTPUT_DIR/Grupa_Azoty_Directors_Report_2022.pdf" \
  "${BASE_URL}/upload/2/files/2023/RI/R2022/eng/Directors report of the operations 2022.pdf"

echo "✓ 2022 reports downloaded"
echo ""

# Verify downloads
echo "======================================================================"
echo "Verification"
echo "======================================================================"
echo ""

ls -lh "$OUTPUT_DIR/"*.pdf

echo ""
echo "======================================================================"
echo "✅ Download Complete"
echo "======================================================================"
echo ""
echo "Downloaded 6 PDF files:"
echo "  - 2024: Financial Statements + Directors Report"
echo "  - 2023: Financial Statements + Directors Report"
echo "  - 2022: Financial Statements + Directors Report"
echo ""
echo "Next step: Extract financial data from PDFs"
echo "  python3 scripts/extract_azoty_multi_year.py"
